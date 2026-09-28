#!/usr/bin/env python3
"""Ratchet: one deterministic count per dimension, with a ceiling that only goes down.

Usage:
    python3 ratchet.py <root> lower [--dimensions smells logging] [--json]
    python3 ratchet.py <root> check [--json]        # exit 1 if any count exceeds its ceiling

Ceilings live in <root>/.optimize/baseline.json. `lower` creates missing entries at the
current count and lowers existing ones; it never raises a ceiling. Raising one is a manual
edit the user approves.

Custom counts (perf benchmarks) are entries with a `cmd` whose stdout ends in one number:
    {"perf:send-message": {"cmd": "node bench/send.js --count", "ceiling": 48213}}
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILLS = Path(__file__).parent.parent.parent
BASELINE = Path(".optimize") / "baseline.json"


def _scan(cmd: list[str], root: Path, ok: tuple[int, ...] = (0,)) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root)
    if result.returncode not in ok:
        sys.exit(
            f"scan failed (exit {result.returncode}): {' '.join(cmd)}\n{result.stderr}"
        )
    return json.loads(result.stdout)


def _arch(root: Path) -> int | None:
    # archcheck exits 1 on violations and 2 when the repo has no blueprint; both still print JSON.
    data = _scan(
        [
            "python3",
            str(SKILLS / "code-arch-drift/scripts/archcheck.py"),
            "--root",
            str(root),
            "--json",
        ],
        root,
        ok=(0, 1, 2),
    )
    return None if data.get("status") == "no_blueprint" else data["count"]


def _logging(root: Path) -> int:
    summary = _scan(
        [
            "python3",
            str(SKILLS / "code-logging/scripts/scan_logging.py"),
            str(root),
            "--json",
        ],
        root,
    )["summary"]
    return sum(summary["issue_counts"].values()) + sum(summary["gap_counts"].values())


def _smells(root: Path) -> int:
    return _scan(
        ["python3", str(SKILLS / "code-audit/analyze.py"), str(root), "--json"], root
    )["count"]


def _modularize(root: Path) -> int:
    return _scan(
        [
            "python3",
            str(SKILLS / "code-modularize/scripts/scan_files.py"),
            str(root),
            "--json",
        ],
        root,
    )["file_count"]


def simplify_count(files: list[dict]) -> int:
    """Oversized plus deeply nested functions. Function-level on purpose: splitting a file
    (modularize) leaves it unchanged, where a summed per-file score would rise."""
    return sum(
        len(f.get("oversized_functions", [])) + len(f.get("deep_functions", []))
        for f in files
    )


def _simplify(root: Path) -> int:
    files = _scan(
        [
            "python3",
            str(SKILLS / "code-optimize/scripts/scan_codebase.py"),
            str(root),
            "--json",
        ],
        root,
    )["files"]
    return simplify_count(files)


def _practices(root: Path) -> int:
    return _scan(
        [
            "python3",
            str(SKILLS / "code-optimize/scripts/scan_practices.py"),
            str(root),
            "--json",
        ],
        root,
    )["count"]


# structure, claude-md, glossary, docs have no deterministic count; they are not ratcheted.
MEASURES = {
    "arch": _arch,
    "logging": _logging,
    "smells": _smells,
    "modularize": _modularize,
    "simplify": _simplify,
    "practices": _practices,
}


def measure_custom(cmd: str, root: Path) -> int:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=root)
    if result.returncode != 0:
        sys.exit(
            f"custom count failed (exit {result.returncode}): {cmd}\n{result.stderr}"
        )
    return round(float(result.stdout.split()[-1]))


def lower(baseline: dict, measured: dict) -> dict:
    """New baseline: missing entries start at the measured count; existing ceilings only drop."""
    updated = {name: dict(entry) for name, entry in baseline.items()}
    for name, count in measured.items():
        if count is None:
            continue
        entry = updated.setdefault(name, {})
        entry["ceiling"] = min(entry.get("ceiling", count), count)
    return updated


def violations(baseline: dict, measured: dict) -> dict:
    return {
        name: {"count": count, "ceiling": baseline[name]["ceiling"]}
        for name, count in measured.items()
        if count is not None
        and "ceiling" in baseline.get(name, {})
        and count > baseline[name]["ceiling"]
    }


def measure_all(root: Path, baseline: dict, dimensions: list[str] | None) -> dict:
    names = dimensions or (list(baseline) if baseline else list(MEASURES))
    measured = {}
    for name in names:
        if name in MEASURES:
            measured[name] = MEASURES[name](root)
        elif "cmd" in baseline.get(name, {}):
            measured[name] = measure_custom(baseline[name]["cmd"], root)
        else:
            sys.exit(
                f"unknown count '{name}': not a dimension ({', '.join(MEASURES)}) and no `cmd` in baseline"
            )
    return measured


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count ratchet for code-optimize dimensions."
    )
    parser.add_argument("root", help="project root")
    parser.add_argument("mode", choices=["lower", "check"])
    parser.add_argument(
        "--dimensions",
        nargs="*",
        help="counts to measure (default: every baseline entry, or all dimensions)",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    path = root / BASELINE
    baseline = json.loads(path.read_text()) if path.exists() else {}
    measured = measure_all(root, baseline, args.dimensions)

    if args.mode == "lower":
        updated = lower(baseline, measured)
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n")
        rows = {
            n: {
                "count": measured.get(n),
                "ceiling": e["ceiling"],
                "was": baseline.get(n, {}).get("ceiling"),
            }
            for n, e in updated.items()
        }
        failed = {}
    else:
        failed = violations(baseline, measured)
        rows = {
            n: {"count": c, "ceiling": baseline.get(n, {}).get("ceiling")}
            for n, c in measured.items()
        }

    if args.json:
        print(
            json.dumps(
                {"mode": args.mode, "counts": rows, "violations": failed}, indent=2
            )
        )
    else:
        for name, row in rows.items():
            flag = "  RAISED" if name in failed else ""
            print(f"{name:<24} count={row['count']}  ceiling={row['ceiling']}{flag}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
