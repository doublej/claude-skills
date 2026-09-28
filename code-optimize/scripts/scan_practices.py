#!/usr/bin/env python3
"""Scan a project for JJ's house practices: atlas wiring, dev hostname, dev-tree paths,
onenv over .env, one package manager, nothing vendored in git, daemons registered.

Usage:
    python3 scan_practices.py <root>              # human summary
    python3 scan_practices.py <root> --json       # structured JSON; `count` feeds the ratchet
    python3 scan_practices.py <root> --no-atlas   # file rules only (no atlas CLI calls)

Read-only. Every finding has a rule id, file, line and the fix; references/practices.md
says how to apply each fix.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEV = (Path.home() / "dev").resolve()
DAEMONS = DEV / "multi-stack/project-atlas/shared/daemons.json"
PORT_RANGE = range(4100, 5000)

SKIP_DIRS = {
    ".git",
    "node_modules",
    "bower_components",
    "vendor",
    "third_party",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    "out",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".output",
    "target",
    "coverage",
    "Pods",
    ".build",
    "DerivedData",
    ".gradle",
    ".dart_tool",
}
VENDORED_IN_GIT = (
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".svelte-kit",
    ".next",
    "Pods",
)
LOCKFILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lock",
    "bun.lockb",
    "uv.lock",
    "poetry.lock",
    "Pipfile.lock",
    "Cargo.lock",
    "go.sum",
}
TEXT_SUFFIXES = {
    "",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".sh",
    ".zsh",
    ".bash",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".mjs",
    ".cjs",
    ".jsx",
    ".svelte",
    ".vue",
    ".go",
    ".rs",
    ".swift",
    ".plist",
    ".html",
    ".css",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    ".rb",
    ".php",
    ".kt",
    ".java",
    ".cs",
}
ALLOWED_ENV = {
    ".env.example",
    ".env.sample",
    ".env.template",
    ".env.development",
    ".env.test",
}
DOC_NAMES = {"README.md", "CLAUDE.md", "AGENTS.md"}
AGENT_DOCS = {"CLAUDE.md", "AGENTS.md"}
# agent scratch, tool state and JJ's dead/scratch folders: absolute paths there are not project files
NOT_PROJECT = {
    ".beads",
    ".orchestrate",
    ".claude",
    ".session-search",
    ".junie",
    "_archive",
    "_sandbox",
    "sandbox",
    "_data",
}
GENERATED = {".template-meta.json"}
SERVER_SCRIPTS = {"dev", "start", "serve", "develop", "preview"}

LOCALHOST_URL = re.compile(r"https?://(?:localhost|127\.0\.0\.1):\d+")
DEV_SERVERS = {  # tool in the dev command → pattern that proves it binds all interfaces
    "vite": re.compile(r"--host\b"),
    "uvicorn": re.compile(r"--host[ =]0\.0\.0\.0"),
    "flask": re.compile(r"(?:--host|-h)[ =]0\.0\.0\.0"),
}


def finding(rule: str, file: str, line: int, message: str, fix: str) -> dict:
    return {"rule": rule, "file": file, "line": line, "message": message, "fix": fix}


def list_files(root: Path) -> tuple[list[str], bool]:
    """Repo-relative paths: git's view (tracked + untracked, ignores applied) or a walk."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout.splitlines(), True
    files = [
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(root).parts)
    ]
    return files, False


def tracked(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True
    )
    return result.stdout.splitlines() if result.returncode == 0 else []


def read_lines(path: Path) -> list[str]:
    if (
        path.suffix not in TEXT_SUFFIXES
        or not path.is_file()
        or path.stat().st_size > 1_000_000
    ):
        return []
    try:
        return path.read_text().splitlines()
    except (UnicodeDecodeError, OSError):
        return []


def grep(
    root: Path, files: list[str], pattern: re.Pattern
) -> list[tuple[str, int, str]]:
    hits = []
    for rel in files:
        for no, line in enumerate(read_lines(root / rel), 1):
            if pattern.search(line):
                hits.append((rel, no, line.strip()))
    return hits


def per_file(hits: list[tuple[str, int, str]]) -> list[tuple[str, int, str, int]]:
    """One entry per file: first hit plus the number of hits. The count tracks files to fix."""
    first: dict[str, tuple[int, str]] = {}
    counts: dict[str, int] = {}
    for rel, no, text in hits:
        first.setdefault(rel, (no, text))
        counts[rel] = counts.get(rel, 0) + 1
    return [(rel, no, text, counts[rel]) for rel, (no, text) in first.items()]


# ---- file rules (no atlas needed) -------------------------------------------------------


def check_devtree_paths(root: Path, files: list[str]) -> list[dict]:
    home = re.escape(str(Path.home()))
    pattern = re.compile(rf"{home}/dev/|Documents/development")
    scoped = [
        f
        for f in files
        if Path(f).name not in LOCKFILES | GENERATED
        and not (SKIP_DIRS | NOT_PROJECT).intersection(Path(f).parts)
    ]
    return [
        finding(
            "paths.devtree",
            rel,
            no,
            f"{n} absolute dev-tree path(s), first: {text[:100]}",
            "use a repo-relative path or $HOME/dev/...; ~/Documents/development is a dead symlink",
        )
        for rel, no, text, n in per_file(grep(root, scoped, pattern))
    ]


def check_dotenv(files: list[str], in_git: set[str]) -> list[dict]:
    out = []
    for rel in files:
        name = Path(rel).name
        if (name == ".env" or name.startswith(".env.")) and name not in ALLOWED_ENV:
            where = "tracked in git" if rel in in_git else "on disk"
            out.append(
                finding(
                    "secrets.dotenv",
                    rel,
                    1,
                    f"{name} {where}",
                    "move the values into onenv (`onenv prime`), delete the file; "
                    "a tracked one also needs `git rm --cached` and a secret rotation",
                )
            )
    return out


def check_package_managers(root: Path, files: list[str]) -> list[dict]:
    names = {Path(f).name for f in files if len(Path(f).parts) == 1}
    out = []
    js_locks = sorted(
        names
        & {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock", "bun.lockb"}
    )
    if len(js_locks) > 1:
        out.append(
            finding(
                "pm.lockfiles",
                js_locks[0],
                1,
                f"mixed JS lockfiles: {', '.join(js_locks)}",
                "keep the lockfile of the manager the repo scripts use; delete the rest",
            )
        )
    py_locks = sorted(names & {"uv.lock", "poetry.lock", "Pipfile.lock"})
    if len(py_locks) > 1:
        out.append(
            finding(
                "pm.lockfiles",
                py_locks[0],
                1,
                f"mixed Python lockfiles: {', '.join(py_locks)}",
                "keep uv.lock; migrate the rest with `uv add`",
            )
        )

    wrong = []
    if names & {"bun.lock", "bun.lockb"}:
        wrong.append(("bun", re.compile(r"\b(?:npm (?:run|install|i|ci)\b|npx )")))
    if "uv.lock" in names:
        wrong.append(
            (
                "uv",
                re.compile(r"(?<!uv )\b(?:pip3? install|poetry (?:add|install|run))\b"),
            )
        )
    command_files = [
        f
        for f in files
        if Path(f).name
        in DOC_NAMES | {"Justfile", "justfile", "package.json", "Makefile"}
        and not SKIP_DIRS.intersection(Path(f).parts)
    ]
    for manager, pattern in wrong:
        for rel, no, text in grep(root, command_files, pattern):
            out.append(
                finding(
                    "pm.commands",
                    rel,
                    no,
                    f"repo uses {manager}: {text[:120]}",
                    f"rewrite with {manager} (`bun run`/`bunx` or `uv add`/`uv run`)",
                )
            )
    return out


def check_vendored(in_git: list[str]) -> list[dict]:
    counts: dict[str, int] = {}
    for rel in in_git:
        parts = Path(rel).parts
        for i, part in enumerate(parts[:-1]):
            if part in VENDORED_IN_GIT:
                key = "/".join(parts[: i + 1])
                counts[key] = counts.get(key, 0) + 1
                break
    return [
        finding(
            "vendored.tracked",
            d,
            1,
            f"{n} files of {Path(d).name}/ are tracked in git",
            f"`git rm -r --cached {d}` and add `{Path(d).name}/` to .gitignore",
        )
        for d, n in sorted(counts.items())
    ]


def check_daemons(root: Path) -> list[dict]:
    plists = (
        sorted((root / "launchd").glob("*.plist"))
        if (root / "launchd").is_dir()
        else []
    )
    if not plists or not DAEMONS.exists():
        return []
    registry = DAEMONS.read_text()
    out = []
    for plist in plists:
        label = re.search(
            r"<key>Label</key>\s*<string>([^<]+)</string>", plist.read_text()
        )
        name = label.group(1) if label else plist.stem
        if name not in registry:
            out.append(
                finding(
                    "daemons.registry",
                    str(plist.relative_to(root)),
                    1,
                    f"launchd agent {name} missing from project-atlas daemons.json",
                    f"register it in {DAEMONS.relative_to(DEV)} after bootstrap/load",
                )
            )
    return out


# ---- atlas rules --------------------------------------------------------------------------


def atlas_info(root: Path) -> dict | None:
    result = subprocess.run(
        ["atlas", "info", "--json"], cwd=root, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def dev_command_text(root: Path, info: dict) -> str:
    texts = []
    script = (info.get("scripts") or {}).get(info.get("devCommand") or "")
    if script:
        texts.append(script)
    if "dev" in (info.get("justRecipes") or []) and shutil.which("just"):
        shown = subprocess.run(
            ["just", "--show", "dev"], cwd=root, capture_output=True, text=True
        )
        texts.append(shown.stdout)
    return "\n".join(texts)


def check_atlas(root: Path, files: list[str], info: dict) -> list[dict]:
    out = []
    if Path(info["path"]).resolve() != root:
        out.append(
            finding(
                "atlas.nested",
                ".",
                1,
                f"atlas resolves this folder to {info['relativePath']}",
                "add a `depth` entry in ~/dev/.atlas-config.json, then `atlas scan` (atlas-hostname step 1)",
            )
        )
        return out
    command = dev_command_text(root, info)
    serves = info.get("devCommand") in SERVER_SCRIPTS or any(
        re.search(rf"\b{t}\b", command) for t in DEV_SERVERS
    )
    if (
        not serves
    ):  # atlas also names `build` as devCommand for native apps; nothing to expose then
        return out

    dot_atlas = root / ".atlas"
    port = json.loads(dot_atlas.read_text()).get("port") if dot_atlas.exists() else None
    if not isinstance(port, int) or port not in PORT_RANGE:
        out.append(
            finding(
                "atlas.port",
                ".atlas",
                1,
                f"dev server port is {port or 'unset'}, not 4100-4999",
                "`curl -s localhost:47891/api/ports/allocate`, write it to .atlas `port`, pin it in the dev script",
            )
        )

    configs = [
        f for f in files if re.fullmatch(r"vite\.config\.[cm]?[jt]s", Path(f).name)
    ]
    vite_host = any(re.search(r"\bhost\s*:", (root / f).read_text()) for f in configs)
    for tool, binds_all in DEV_SERVERS.items():
        if (
            re.search(rf"\b{tool}\b", command)
            and not binds_all.search(command)
            and not (tool == "vite" and vite_host)
        ):
            out.append(
                finding(
                    "atlas.bind",
                    "package.json" if tool == "vite" else "Justfile",
                    1,
                    f"{tool} dev server binds loopback only; the hostname will 502",
                    "pin `--host 0.0.0.0 --port <.atlas port>` in the dev script (atlas-hostname step 3)",
                )
            )
    for rel, no, _ in grep(root, configs, re.compile(r"\ballowedHosts\b")):
        out.append(
            finding(
                "atlas.allowed-hosts",
                rel,
                no,
                "allowedHosts set; Caddy already rewrites Host",
                "remove allowedHosts",
            )
        )

    claude_md = root / "CLAUDE.md"
    if "atlas.local.jurrejan.com" not in (
        claude_md.read_text() if claude_md.exists() else ""
    ):
        out.append(
            finding(
                "atlas.dev-line",
                "CLAUDE.md",
                1,
                "no dev hostname line",
                "add `Dev: \\`atlas run\\` → https://<slug>.atlas.local.jurrejan.com (port <N>).` (atlas-hostname step 6)",
            )
        )
    # agent-facing docs only: a README may document localhost for other people on purpose
    docs = [
        f
        for f in files
        if Path(f).name in AGENT_DOCS and not SKIP_DIRS.intersection(Path(f).parts)
    ]
    for rel, no, text, n in per_file(grep(root, docs, LOCALHOST_URL)):
        out.append(
            finding(
                "atlas.localhost-docs",
                rel,
                no,
                f"{n} localhost URL(s) handed to agents, first: {text[:100]}",
                f"use https://{info.get('slug', '<slug>')}.atlas.local.jurrejan.com",
            )
        )
    return out


def scan(root: Path, use_atlas: bool) -> dict:
    files, is_git = list_files(root)
    in_git = tracked(root)
    findings = (
        check_devtree_paths(root, files)
        + check_dotenv(files, set(in_git))
        + check_package_managers(root, files)
        + check_vendored(in_git)
        + check_daemons(root)
    )
    skipped = []
    project = None
    if not use_atlas:
        skipped.append({"rules": "atlas.*", "reason": "--no-atlas"})
    elif not shutil.which("atlas"):
        skipped.append({"rules": "atlas.*", "reason": "atlas CLI not installed"})
    elif not root.is_relative_to(DEV):
        skipped.append({"rules": "atlas.*", "reason": f"outside {DEV}"})
    else:
        info = atlas_info(root)
        if info is None:
            findings.append(
                finding(
                    "atlas.catalog",
                    ".",
                    1,
                    "atlas has no record of this folder",
                    "`atlas scan`; still missing → `atlas init` (atlas-cli skill)",
                )
            )
        else:
            project = {
                k: info.get(k)
                for k in (
                    "slug",
                    "type",
                    "framework",
                    "runner",
                    "devCommand",
                    "git",
                    "flow",
                )
            }
            findings += check_atlas(root, files, info)
    return {
        "root": str(root),
        "git": is_git,
        "atlas": project,
        "count": len(findings),
        "rule_counts": {
            r: sum(f["rule"] == r for f in findings)
            for r in sorted({f["rule"] for f in findings})
        },
        "findings": findings,
        "skipped": skipped,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan a project for JJ's house practices."
    )
    parser.add_argument("root", help="project root")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--no-atlas", action="store_true", help="skip rules that call the atlas CLI"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    result = scan(root, use_atlas=not args.no_atlas)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"Practices: {result['count']} findings in {root}")
    for rule, n in result["rule_counts"].items():
        print(f"  {rule:<22} {n}")
    for f in result["findings"][:40]:
        print(f"  {f['file']}:{f['line']}  [{f['rule']}] {f['message']}")
    for s in result["skipped"]:
        print(f"  skipped {s['rules']}: {s['reason']}")


if __name__ == "__main__":
    main()
