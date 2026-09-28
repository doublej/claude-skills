#!/usr/bin/env python3
"""Scan files for modularization candidates.

Usage:
    python3 scan_files.py /path/to/file_or_dir              # human summary
    python3 scan_files.py /path/to/file_or_dir --json        # structured JSON
    python3 scan_files.py /path/to/dir --threshold 200       # custom threshold
"""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
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
            r"^([ \t]*)(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.MULTILINE
        ),
        "class": re.compile(
            r"^([ \t]*)(?:export\s+)?class\s+(\w+)", re.MULTILINE
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
    ".kt": {
        "function": re.compile(
            r"^([ \t]*)(?:(?:public|private|protected|internal|override|open|abstract|final|suspend|inline"
            r"|operator|infix|tailrec|external|actual|expect)[ \t]+)*fun[ \t]+(?:<[^>\n]*>[ \t]*)?"
            r"(?:[\w.<>?]+\.)?(\w+)[ \t]*\(",
            re.MULTILINE,
        ),
        "class": re.compile(
            r"^([ \t]*)(?:(?:public|private|protected|internal|open|abstract|sealed|data|enum|annotation"
            r"|inner|value|final|companion)[ \t]+)*(?:class|interface|object)[ \t]+(\w+)",
            re.MULTILINE,
        ),
        "import": re.compile(r"^import\s+([\w.]+)", re.MULTILINE),
    },
    # Java/C# methods need a leading modifier: package-private methods and constructors
    # are missed on purpose, so a statement like `if (` or `foo(` is never counted.
    ".java": {
        "function": re.compile(
            r"^([ \t]*)(?:@\w+(?:\([^)\n]*\))?[ \t]+)*(?:(?:public|protected|private|static|final|abstract"
            r"|synchronized|native|default|strictfp)[ \t]+)+(?:<[^>\n]+>[ \t]+)?[\w.<>\[\]?, ]+?[ \t]+(\w+)[ \t]*\(",
            re.MULTILINE,
        ),
        "class": re.compile(
            r"^([ \t]*)(?:(?:public|protected|private|static|final|abstract|sealed|non-sealed|strictfp)[ \t]+)*"
            r"(?:class|interface|record|enum|@interface)[ \t]+(\w+)",
            re.MULTILINE,
        ),
        "import": re.compile(r"^import\s+(?:static\s+)?([\w.]+)", re.MULTILINE),
    },
    ".cs": {
        "function": re.compile(
            r"^([ \t]*)(?:(?:public|private|protected|internal|static|async|virtual|override|abstract|sealed"
            r"|extern|unsafe|new|partial|readonly)[ \t]+)+[\w.<>\[\]?, ]+?[ \t]+(\w+)[ \t]*(?:<[^>\n]*>)?[ \t]*\(",
            re.MULTILINE,
        ),
        "class": re.compile(
            r"^([ \t]*)(?:(?:public|private|protected|internal|static|abstract|sealed|partial|readonly|unsafe"
            r"|new|file|ref)[ \t]+)*(?:record(?:[ \t]+(?:struct|class))?|class|interface|enum|struct)[ \t]+(\w+)",
            re.MULTILINE,
        ),
        "import": re.compile(r"^(?:global\s+)?using\s+(?:static\s+)?([\w.]+)\s*;", re.MULTILINE),
    },
    ".rb": {
        "function": re.compile(r"^([ \t]*)def[ \t]+(?:self\.)?(\w+[?!]?)", re.MULTILINE),
        "class": re.compile(r"^([ \t]*)(?:class|module)[ \t]+([A-Z]\w*)", re.MULTILINE),
        "import": re.compile(r"""^[ \t]*require(?:_relative)?[ \t(]+['"]([^'"]+)['"]""", re.MULTILINE),
    },
    ".php": {
        "function": re.compile(
            r"^([ \t]*)(?:(?:public|private|protected|static|abstract|final)[ \t]+)*function[ \t]+&?(\w+)[ \t]*\(",
            re.MULTILINE,
        ),
        "class": re.compile(
            r"^([ \t]*)(?:(?:abstract|final|readonly)[ \t]+)*(?:class|trait|interface|enum)[ \t]+(\w+)",
            re.MULTILINE,
        ),
        "import": re.compile(
            r"""^[ \t]*(?:use[ \t]+([\w\\]+)|(?:require|include)(?:_once)?[ \t(]+['"]([^'"]+)['"])""",
            re.MULTILINE,
        ),
    },
    # Dart functions have no keyword: best-effort, only a capitalised or primitive return type
    # followed by `name(` counts, so `if (`, `return foo(` and constructor calls never match.
    ".dart": {
        "function": re.compile(
            r"^([ \t]*)(?:(?:static|external|abstract)[ \t]+)*(?:[A-Z][\w.]*(?:<[^\n]*?>)?\??|void|int|double"
            r"|bool|num|dynamic)[ \t]+(\w+)[ \t]*(?:<[^>\n]*>)?\(",
            re.MULTILINE,
        ),
        "class": re.compile(
            r"^([ \t]*)(?:(?:abstract|base|final|sealed|interface|mixin)[ \t]+)*"
            r"(?:class|mixin|enum|extension(?![ \t]+on\b))[ \t]+(\w+)",
            re.MULTILINE,
        ),
        "import": re.compile(r"""^import\s+['"]([^'"]+)['"]""", re.MULTILINE),
    },
    # C/C++: column-0 definitions only (indented lines are statements far too often),
    # never a line starting with a control keyword, never a `;`-terminated prototype.
    ".c": {
        "function": re.compile(
            r"^()(?!(?:if|else|while|for|switch|return|do|case|goto|sizeof|typedef|throw|delete|new|using"
            r"|namespace)\b)[A-Za-z_][\w \t*:<>,&]*?[ \t*&]+(?:\w+::)*(\w+)[ \t]*\([^;\n]*$",
            re.MULTILINE,
        ),
        "class": re.compile(r"^([ \t]*)(?:class|struct)[ \t]+(\w+)[^;\n]*$", re.MULTILINE),
        "import": re.compile(r"""^#include\s+[<"]([^>"]+)[>"]""", re.MULTILINE),
    },
}
# Aliases
for ext in (".tsx", ".jsx", ".js", ".mjs", ".cjs", ".svelte", ".vue"):
    LANG_PATTERNS[ext] = LANG_PATTERNS[".ts"]
LANG_PATTERNS[".kts"] = LANG_PATTERNS[".kt"]
for ext in (".h", ".cc", ".cpp", ".hpp", ".cxx", ".hh"):
    LANG_PATTERNS[ext] = LANG_PATTERNS[".c"]

# Only the <script> blocks of these files are code; the markup around them is not.
MARKUP_SUFFIXES = {".svelte", ".vue"}
SCRIPT_BLOCK = re.compile(r"<script\b[^>]*>(.*?)</script>", re.DOTALL)

SKIP_DIRS = {
    ".git", "node_modules", "bower_components", "vendor", "third_party",
    ".venv", "venv", "__pycache__", "dist", "build", "out", ".next", ".nuxt",
    ".svelte-kit", ".output", "target", "coverage", "Pods", ".build",
    "DerivedData", ".gradle", ".dart_tool", ".terraform",
    "generated", "__generated__",
}
GENERATED_SUFFIXES = (".min.js", ".bundle.js", ".d.ts")
# Source languages this scanner has no patterns for; reported so an empty result is not read as clean.
UNSCANNED_SOURCE = {
    ".scala", ".ex", ".exs", ".erl", ".hs", ".ml", ".clj", ".lua", ".r", ".jl",
    ".zig", ".nim", ".m", ".mm", ".fs", ".elm", ".sol", ".gd",
}
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


def is_skipped(rel: Path) -> bool:
    return bool(SKIP_DIRS.intersection(rel.parts)) or rel.name.endswith(GENERATED_SUFFIXES)


def list_files(target: Path) -> list[Path]:
    """All tracked (or walked) files under target, minus vendored and generated ones."""
    tracked = git_files(target)
    files = tracked if tracked is not None else target.rglob("*")
    return [f for f in files if not is_skipped(f.relative_to(target)) and f.is_file()]


def build_coverage(files: list[Path]) -> dict:
    scanned = Counter(f.suffix for f in files if f.suffix in LANG_PATTERNS)
    unscanned = Counter(f.suffix.lower() for f in files if f.suffix.lower() in UNSCANNED_SOURCE)
    return {"scanned": dict(sorted(scanned.items())), "unscanned": dict(sorted(unscanned.items()))}


def collect_files(target: Path, threshold: int) -> tuple[list[Path], dict]:
    if target.is_file():
        return [target], build_coverage([target])

    files = list_files(target)
    candidates = [f for f in files if f.suffix in LANG_PATTERNS]
    return [f for f in candidates if count_lines(f) > threshold], build_coverage(files)


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


def script_only(text: str) -> str:
    """Blank everything outside <script> blocks, keeping line numbers."""
    parts, pos = [], 0
    for m in SCRIPT_BLOCK.finditer(text):
        parts.append("\n" * text.count("\n", pos, m.start(1)))
        parts.append(m.group(1))
        pos = m.end(1)
    parts.append("\n" * text.count("\n", pos))
    return "".join(parts)


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

    code_end = loc
    if suffix in MARKUP_SUFFIXES:
        text = script_only(text)
        code_end = len(text.rstrip().splitlines())

    functions = find_symbols(text, patterns["function"])
    classes = find_symbols(text, patterns["class"])
    all_symbols = sorted(functions + classes, key=lambda s: s["line"])
    all_symbols = measure_symbol_lengths(all_symbols, code_end)

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
    files, coverage = collect_files(target, threshold)

    results = [analyze_file(f) for f in sorted(files)]
    import_map = build_import_map(results, base) if len(results) > 1 else {}

    for r in results:
        r["consumed_by"] = import_map.get(r["path"], [])

    return {
        "target": str(target),
        "threshold": threshold,
        "file_count": len(results),
        "coverage": coverage,
        "files": results,
    }


def print_unscanned(coverage: dict) -> None:
    if coverage["unscanned"]:
        print("Unscanned: " + ", ".join(f"{ext} ({n})" for ext, n in coverage["unscanned"].items()))


def print_human(result: dict) -> None:
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Target:    {result['target']}")
    print(f"Threshold: {result['threshold']} lines")
    print(f"Files:     {result['file_count']} over threshold")
    print_unscanned(result["coverage"])
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan files for modularization candidates."
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=f"Only include files over N lines (default: {DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit structured JSON output"
    )
    args = parser.parse_args()

    result = scan(args.path, args.threshold)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
