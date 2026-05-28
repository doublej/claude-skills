#!/usr/bin/env python3
"""Scan files for modularization candidates.

Usage:
    python3 scan_files.py /path/to/file_or_dir              # human summary
    python3 scan_files.py /path/to/file_or_dir --json        # structured JSON
    python3 scan_files.py /path/to/dir --threshold 200       # custom threshold
"""

import json
import re
import subprocess
import sys
from pathlib import Path

LANG_PATTERNS = {
    ".py": {
        "function": re.compile(r"^( *)(?:async\s+)?def\s+(\w+)\s*\(", re.MULTILINE),
        "class": re.compile(r"^( *)class\s+(\w+)[:\(]", re.MULTILINE),
        "import": re.compile(
            r"^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", re.MULTILINE
        ),
    },
    ".ts": {
        "function": re.compile(
            r"^( *)(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.MULTILINE
        ),
        "class": re.compile(
            r"^( *)(?:export\s+)?class\s+(\w+)", re.MULTILINE
        ),
        "import": re.compile(
            r"""^import\s+.*?from\s+['"]([^'"]+)['"]""", re.MULTILINE
        ),
    },
    ".tsx": None,  # shares .ts patterns
    ".js": None,   # shares .ts patterns
    ".jsx": None,  # shares .ts patterns
    ".go": {
        "function": re.compile(r"^([ \t]*)func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(", re.MULTILINE),
        "class": re.compile(r"^([ \t]*)type\s+(\w+)\s+struct\b", re.MULTILINE),
        "import": re.compile(r'"([^"]+)"', re.MULTILINE),
    },
    ".rs": {
        "function": re.compile(r"^( *)(?:pub\s+)?(?:async\s+)?fn\s+(\w+)", re.MULTILINE),
        "class": re.compile(r"^( *)(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)", re.MULTILINE),
        "import": re.compile(r"^use\s+([\w:]+)", re.MULTILINE),
    },
    ".swift": {
        "function": re.compile(r"^( *)(?:public\s+|private\s+|internal\s+)?func\s+(\w+)", re.MULTILINE),
        "class": re.compile(r"^( *)(?:public\s+|private\s+)?(?:class|struct|enum|protocol)\s+(\w+)", re.MULTILINE),
        "import": re.compile(r"^import\s+(\w+)", re.MULTILINE),
    },
}
# Aliases
for ext in (".tsx", ".jsx", ".js"):
    LANG_PATTERNS[ext] = LANG_PATTERNS[".ts"]

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "dist", "build", ".next", "target"}
DEFAULT_THRESHOLD = 150


def git_files(directory: Path) -> list[Path] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=directory, capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return None
        return [directory / f for f in result.stdout.strip().splitlines() if f]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def collect_files(target: Path, threshold: int) -> list[Path]:
    if target.is_file():
        return [target]

    tracked = git_files(target)
    if tracked is not None:
        candidates = [f for f in tracked if f.suffix in LANG_PATTERNS and f.exists()]
    else:
        candidates = [
            f for f in target.rglob("*")
            if f.is_file()
            and f.suffix in LANG_PATTERNS
            and not any(d in f.parts for d in SKIP_DIRS)
        ]

    return [f for f in candidates if count_lines(f) > threshold]


def count_lines(path: Path) -> int:
    try:
        return len(path.read_text().splitlines())
    except (OSError, UnicodeDecodeError):
        return 0


def find_symbols(text: str, pattern: re.Pattern) -> list[dict]:
    symbols = []
    lines = text.splitlines()
    for m in pattern.finditer(text):
        line_no = text[:m.start()].count("\n") + 1
        indent = len(m.group(1)) if m.group(1) else 0
        name = m.group(2)
        symbols.append({"name": name, "line": line_no, "indent": indent})
    return symbols


def measure_symbol_lengths(symbols: list[dict], total_lines: int) -> list[dict]:
    for i, sym in enumerate(symbols):
        next_line = symbols[i + 1]["line"] if i + 1 < len(symbols) else total_lines + 1
        sym["length"] = next_line - sym["line"]
    return symbols


def find_imports(text: str, pattern: re.Pattern) -> list[str]:
    return list({m.group(1) or m.group(2) for m in pattern.finditer(text) if m.group(1) or (m.lastindex and m.lastindex >= 2 and m.group(2))})


def analyze_file(path: Path) -> dict:
    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return {"path": str(path), "error": "unreadable"}

    loc = len(text.splitlines())
    suffix = path.suffix
    patterns = LANG_PATTERNS.get(suffix)
    if not patterns:
        return {"path": str(path), "loc": loc, "symbols": [], "imports": []}

    functions = find_symbols(text, patterns["function"])
    classes = find_symbols(text, patterns["class"])
    all_symbols = sorted(functions + classes, key=lambda s: s["line"])
    all_symbols = measure_symbol_lengths(all_symbols, loc)

    imports = find_imports(text, patterns["import"]) if "import" in patterns else []

    oversized = [s for s in functions if s["length"] > 20]

    return {
        "path": str(path),
        "loc": loc,
        "function_count": len(functions),
        "class_count": len(classes),
        "symbols": [
            {"name": s["name"], "line": s["line"], "length": s["length"], "indent": s["indent"]}
            for s in all_symbols
        ],
        "oversized_functions": [
            {"name": s["name"], "line": s["line"], "length": s["length"]}
            for s in oversized
        ],
        "imports": sorted(imports),
    }


def build_import_map(results: list[dict], base: Path) -> dict:
    """Map each file to the files that import from it."""
    file_stems = {}
    for r in results:
        p = Path(r["path"])
        file_stems[p.stem] = r["path"]
        file_stems[str(p.relative_to(base)).replace("/", ".")] = r["path"]

    consumer_map = {}
    for r in results:
        for imp in r.get("imports", []):
            parts = imp.split(".")
            stem = parts[-1] if parts else imp
            target = file_stems.get(stem) or file_stems.get(imp)
            if target and target != r["path"]:
                consumer_map.setdefault(target, []).append(r["path"])
    return consumer_map


def scan(target_path: str, threshold: int) -> dict:
    target = Path(target_path).resolve()
    if not target.exists():
        return {"error": f"Path not found: {target}"}

    base = target if target.is_dir() else target.parent
    files = collect_files(target, threshold)

    results = [analyze_file(f) for f in sorted(files)]
    import_map = build_import_map(results, base) if len(results) > 1 else {}

    for r in results:
        r["consumed_by"] = import_map.get(r["path"], [])

    return {
        "target": str(target),
        "threshold": threshold,
        "file_count": len(results),
        "files": results,
    }


def print_human(result: dict):
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Target:    {result['target']}")
    print(f"Threshold: {result['threshold']} lines")
    print(f"Files:     {result['file_count']} over threshold")
    print()

    if not result["files"]:
        print("No files exceed the threshold.")
        return

    for f in result["files"]:
        print(f"  {f['path']} ({f['loc']} lines, {f['function_count']} functions, {f['class_count']} classes)")
        if f.get("oversized_functions"):
            for s in f["oversized_functions"]:
                print(f"    ! {s['name']} ({s['length']} lines) at line {s['line']}")
        if f.get("consumed_by"):
            print(f"    imported by: {len(f['consumed_by'])} file(s)")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: scan_files.py <path> [--threshold N] [--json]", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    threshold = DEFAULT_THRESHOLD
    use_json = "--json" in sys.argv

    for i, arg in enumerate(sys.argv):
        if arg == "--threshold" and i + 1 < len(sys.argv):
            threshold = int(sys.argv[i + 1])

    result = scan(target, threshold)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
