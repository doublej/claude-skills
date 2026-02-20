#!/usr/bin/env python3
"""Scan a codebase for simplification opportunities.

Usage:
    python3 scan_codebase.py /path/to/project              # human summary
    python3 scan_codebase.py /path/to/project --json        # structured JSON
    python3 scan_codebase.py /path/to/project --threshold 50  # custom LOC threshold
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
        "export": re.compile(r"^(?!_)(?:async\s+)?def\s+(\w+)|^(?!_)class\s+(\w+)", re.MULTILINE),
        "import": re.compile(r"^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", re.MULTILINE),
    },
    ".ts": {
        "function": re.compile(r"^( *)(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.MULTILINE),
        "class": re.compile(r"^( *)(?:export\s+)?class\s+(\w+)", re.MULTILINE),
        "export": re.compile(r"^export\s+(?:async\s+)?(?:function|class|const|let|type|interface|enum)\s+(\w+)", re.MULTILINE),
        "import": re.compile(r"""^import\s+.*?from\s+['"]([^'"]+)['"]""", re.MULTILINE),
    },
    ".tsx": None,
    ".js": None,
    ".jsx": None,
    ".go": {
        "function": re.compile(r"^([ \t]*)func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(", re.MULTILINE),
        "class": re.compile(r"^([ \t]*)type\s+(\w+)\s+struct\b", re.MULTILINE),
        "export": re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?([A-Z]\w*)\s*\(|^type\s+([A-Z]\w+)", re.MULTILINE),
        "import": re.compile(r'"([^"]+)"', re.MULTILINE),
    },
    ".rs": {
        "function": re.compile(r"^( *)(?:pub\s+)?(?:async\s+)?fn\s+(\w+)", re.MULTILINE),
        "class": re.compile(r"^( *)(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)", re.MULTILINE),
        "export": re.compile(r"^pub\s+(?:async\s+)?(?:fn|struct|enum|trait|type|const)\s+(\w+)", re.MULTILINE),
        "import": re.compile(r"^use\s+([\w:]+)", re.MULTILINE),
    },
    ".swift": {
        "function": re.compile(r"^( *)(?:public\s+|private\s+|internal\s+)?func\s+(\w+)", re.MULTILINE),
        "class": re.compile(r"^( *)(?:public\s+|private\s+)?(?:class|struct|enum|protocol)\s+(\w+)", re.MULTILINE),
        "export": re.compile(r"^(?:public\s+)(?:func|class|struct|enum|protocol)\s+(\w+)", re.MULTILINE),
        "import": re.compile(r"^import\s+(\w+)", re.MULTILINE),
    },
}

for ext in (".tsx", ".jsx", ".js"):
    LANG_PATTERNS[ext] = LANG_PATTERNS[".ts"]

IMPORTED_SYMBOL_PATTERNS: dict[str, list[re.Pattern]] = {
    ".py": [re.compile(r"^from\s+[\w.]+\s+import\s+(.+)", re.MULTILINE)],
    ".ts": [
        re.compile(r"^import\s+(?:type\s+)?\{([^}]+)\}\s+from", re.MULTILINE),
        re.compile(r"^import\s+(\w+)\s+from\s+['\"]", re.MULTILINE),
    ],
    ".go": [],
    ".rs": [
        re.compile(r"^use\s+[\w:]+::(\w+)", re.MULTILINE),
        re.compile(r"^use\s+[\w:]+::\{([^}]+)\}", re.MULTILINE),
    ],
    ".swift": [],
}
for ext in (".tsx", ".jsx", ".js"):
    IMPORTED_SYMBOL_PATTERNS[ext] = IMPORTED_SYMBOL_PATTERNS[".ts"]

# Patterns for namespace-style imports where individual symbol usage can't be tracked
NAMESPACE_IMPORT_PATTERNS: dict[str, list[re.Pattern]] = {
    ".py": [re.compile(r"^import\s+(\w+)\s*$", re.MULTILINE)],
    ".ts": [re.compile(r"^import\s+\*\s+as\s+\w+\s+from\s+['\"]([^'\"]+)['\"]", re.MULTILINE)],
    ".go": [],  # Go always uses namespace access; handled by skipping Go in dead-export check
    ".rs": [re.compile(r"^use\s+([\w:]+)::\*", re.MULTILINE)],
    ".swift": [],
}
for ext in (".tsx", ".jsx", ".js"):
    NAMESPACE_IMPORT_PATTERNS[ext] = NAMESPACE_IMPORT_PATTERNS[".ts"]

COMMON_SYMBOL_NAMES = frozenset({
    "main", "__init__", "setup", "teardown", "test",
    "init", "new", "run", "start", "stop", "reset",
    "get", "set", "update", "delete", "create",
    "setUp", "tearDown", "configure", "close", "open",
    "handle", "process", "render", "build", "default",
    "toString", "toJSON", "serialize", "deserialize",
})

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "__pycache__", "dist",
    "build", ".next", "target", ".svelte-kit", "coverage",
}

DEFAULT_THRESHOLD = 0
TAB_WIDTH = 4

# Heuristics for detecting logical codebase sections
SECTION_INDICATORS = {
    "frontend": {
        "dirs": {"src/components", "src/pages", "src/views", "src/app", "app", "pages", "components", "frontend", "client", "web", "ui"},
        "files": {"next.config", "vite.config", "svelte.config", "nuxt.config", "angular.json", "tailwind.config"},
    },
    "backend": {
        "dirs": {"src/api", "src/server", "server", "backend", "api", "cmd", "internal", "pkg", "src/routes", "app/api"},
        "files": {"Dockerfile", "docker-compose", "main.go", "manage.py", "app.py"},
    },
    "shared": {
        "dirs": {"src/lib", "src/utils", "src/common", "src/shared", "lib", "utils", "common", "shared", "packages"},
        "files": {},
    },
    "tests": {
        "dirs": {"tests", "test", "__tests__", "spec", "e2e", "cypress"},
        "files": {"jest.config", "vitest.config", "pytest.ini", "conftest.py"},
    },
    "scripts": {
        "dirs": {"scripts", "tools", "bin", "tasks"},
        "files": {"Makefile", "Taskfile"},
    },
}


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
        candidates = [
            f for f in tracked
            if f.suffix in LANG_PATTERNS
            and f.exists()
            and not any(d in f.parts for d in SKIP_DIRS)
        ]
    else:
        candidates = [
            f for f in target.rglob("*")
            if f.is_file()
            and f.suffix in LANG_PATTERNS
            and not any(d in f.parts for d in SKIP_DIRS)
        ]

    if threshold > 0:
        return [f for f in candidates if count_lines(f) > threshold]
    return list(candidates)


def count_lines(path: Path) -> int:
    try:
        return len(path.read_text().splitlines())
    except (OSError, UnicodeDecodeError):
        return 0


def find_symbols(text: str, pattern: re.Pattern) -> list[dict]:
    symbols = []
    for m in pattern.finditer(text):
        line_no = text[:m.start()].count("\n") + 1
        indent = len(m.group(1).replace("\t", " " * TAB_WIDTH)) if m.group(1) else 0
        name = m.group(2)
        symbols.append({"name": name, "line": line_no, "indent": indent})
    return symbols


def measure_symbol_lengths(symbols: list[dict], total_lines: int) -> list[dict]:
    for i, sym in enumerate(symbols):
        next_line = total_lines + 1
        for j in range(i + 1, len(symbols)):
            if symbols[j]["indent"] <= sym["indent"]:
                next_line = symbols[j]["line"]
                break
        sym["length"] = next_line - sym["line"]
    return symbols


def find_imports(text: str, pattern: re.Pattern) -> list[str]:
    results = set()
    for m in pattern.finditer(text):
        for g in range(1, m.lastindex + 1 if m.lastindex else 1):
            val = m.group(g)
            if val:
                results.add(val)
    return sorted(results)


def find_exports(text: str, pattern: re.Pattern) -> list[str]:
    results = set()
    for m in pattern.finditer(text):
        for g in range(1, m.lastindex + 1 if m.lastindex else 1):
            val = m.group(g)
            if val:
                results.add(val)
    return sorted(results)


def find_imported_symbols(text: str, suffix: str) -> list[str]:
    """Extract actual symbol names from import statements."""
    patterns = IMPORTED_SYMBOL_PATTERNS.get(suffix, [])
    symbols: set[str] = set()
    for pat in patterns:
        for m in pat.finditer(text):
            for name in m.group(1).split(","):
                name = name.split(" as ")[0].strip()
                if name and name != "*":
                    symbols.add(name)
    return sorted(symbols)


def find_namespace_imports(text: str, suffix: str) -> list[str]:
    """Find module names/paths imported via namespace (import foo, import * as)."""
    patterns = NAMESPACE_IMPORT_PATTERNS.get(suffix, [])
    modules: set[str] = set()
    for pat in patterns:
        for m in pat.finditer(text):
            modules.add(m.group(1))
    return sorted(modules)


def find_go_imports(text: str) -> list[str]:
    """Extract import paths from Go import statements only."""
    results: set[str] = set()
    for m in re.finditer(r'^import\s+"([^"]+)"', text, re.MULTILINE):
        results.add(m.group(1))
    for m in re.finditer(r'^import\s*\((.*?)\)', text, re.MULTILINE | re.DOTALL):
        for path_m in re.finditer(r'"([^"]+)"', m.group(1)):
            results.add(path_m.group(1))
    return sorted(results)


def max_nesting_depth(text: str) -> int:
    """Measure max indentation depth across all lines."""
    max_depth = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        spaces = len(line) - len(line.lstrip())
        depth = spaces // TAB_WIDTH if "    " in line[:spaces + 1] else spaces // TAB_WIDTH
        # Handle tabs
        tab_count = len(line) - len(line.lstrip("\t"))
        if tab_count > 0:
            depth = tab_count
        max_depth = max(max_depth, depth)
    return max_depth


def function_nesting(text: str, func_start: int, func_length: int) -> int:
    """Measure max nesting depth within a function body."""
    lines = text.splitlines()
    end = min(func_start + func_length - 1, len(lines))
    body_lines = lines[func_start:end]  # 0-indexed, skip def line
    if not body_lines:
        return 0

    # Get base indent from first line of function
    first_line = lines[func_start - 1] if func_start > 0 else ""
    base_indent = len(first_line) - len(first_line.lstrip())

    max_depth = 0
    for line in body_lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        depth = (indent - base_indent) // TAB_WIDTH
        max_depth = max(max_depth, depth)
    return max_depth


def complexity_score(loc: int, max_nesting: int, oversized_count: int, deep_funcs: int) -> float:
    """Composite score: higher = more complex, more simplification opportunity."""
    score = 0.0
    score += min(loc / 100, 3.0)             # up to 3 for file size
    score += min(max_nesting / 2, 3.0)       # up to 3 for nesting
    score += min(oversized_count, 3.0)       # up to 3 for oversized functions
    score += min(deep_funcs, 2.0)            # up to 2 for deeply nested functions
    return round(score, 1)


def analyze_file(path: Path) -> dict:
    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return {"path": str(path), "error": "unreadable"}

    loc = len(text.splitlines())
    suffix = path.suffix
    patterns = LANG_PATTERNS.get(suffix)
    if not patterns:
        return {"path": str(path), "loc": loc, "complexity": 0}

    functions = find_symbols(text, patterns["function"])
    classes = find_symbols(text, patterns["class"])
    all_symbols = sorted(functions + classes, key=lambda s: s["line"])
    all_symbols = measure_symbol_lengths(all_symbols, loc)

    if suffix == ".go":
        imports = find_go_imports(text)
    else:
        imports = find_imports(text, patterns["import"]) if "import" in patterns else []
    exports = find_exports(text, patterns["export"]) if "export" in patterns else []
    imported_symbols = find_imported_symbols(text, suffix)
    namespace_imports = find_namespace_imports(text, suffix)

    oversized = [s for s in functions if s["length"] > 20]
    deep_funcs = []
    for s in functions:
        depth = function_nesting(text, s["line"], s["length"])
        if depth > 2:
            deep_funcs.append({"name": s["name"], "line": s["line"], "depth": depth})

    max_nest = max_nesting_depth(text)
    score = complexity_score(loc, max_nest, len(oversized), len(deep_funcs))

    return {
        "path": str(path),
        "loc": loc,
        "function_count": len(functions),
        "class_count": len(classes),
        "max_nesting": max_nest,
        "complexity": score,
        "symbols": [
            {"name": s["name"], "line": s["line"], "length": s["length"]}
            for s in all_symbols
        ],
        "oversized_functions": [
            {"name": s["name"], "line": s["line"], "length": s["length"]}
            for s in oversized
        ],
        "deep_functions": deep_funcs,
        "exports": exports,
        "imports": imports,
        "imported_symbols": imported_symbols,
        "namespace_imports": namespace_imports,
    }


def build_import_map(results: list[dict], base: Path) -> dict[str, list[str]]:
    """Map each file to the files that import from it."""
    file_stems: dict[str, str] = {}
    for r in results:
        p = Path(r["path"])
        file_stems[p.stem] = r["path"]
        rel = str(p.relative_to(base)).replace("/", ".")
        file_stems[rel] = r["path"]

    consumer_map: dict[str, list[str]] = {}
    for r in results:
        for imp in r.get("imports", []):
            stem = imp.split(".")[-1] if "." in imp else imp.split("/")[-1]
            target = file_stems.get(stem) or file_stems.get(imp)
            if target and target != r["path"]:
                consumer_map.setdefault(target, []).append(r["path"])
    return consumer_map


def find_dead_exports(results: list[dict]) -> dict[str, list[str]]:
    """Find exported symbols not imported by any other file.

    Skips files that are namespace-imported (import foo, import * as)
    since individual symbol usage can't be tracked via regex.
    Also skips Go files (always namespace-accessed via pkg.Symbol).
    """
    all_imported: set[str] = set()
    namespace_modules: set[str] = set()
    for r in results:
        all_imported.update(r.get("imported_symbols", []))
        for mod in r.get("namespace_imports", []):
            stem = mod.split("/")[-1].split(".")[-1]
            namespace_modules.add(stem)

    dead: dict[str, list[str]] = {}
    for r in results:
        p = Path(r["path"])
        if p.suffix == ".go" or p.stem in namespace_modules:
            continue
        dead_exports = [e for e in r.get("exports", []) if e not in all_imported]
        if dead_exports:
            dead[r["path"]] = dead_exports
    return dead


def find_duplicates(results: list[dict]) -> list[dict]:
    """Find functions with identical names across different files."""
    name_map: dict[str, list[dict]] = {}
    for r in results:
        for sym in r.get("symbols", []):
            name_map.setdefault(sym["name"], []).append({
                "file": r["path"], "line": sym["line"], "length": sym["length"],
            })

    dupes = []
    for name, locations in name_map.items():
        if (len(locations) > 1
                and name not in COMMON_SYMBOL_NAMES
                and any(loc["length"] >= 5 for loc in locations)):
            dupes.append({"name": name, "locations": locations})
    return dupes


def _files_in_dirs(results: list[dict], target: Path, dirs: list[str]) -> list[dict]:
    """Filter results to files under any of the given directory prefixes."""
    matched = []
    for r in results:
        rel = str(Path(r["path"]).relative_to(target))
        if any(rel.startswith(d + "/") or rel.startswith(d + "\\") for d in dirs):
            matched.append(r)
    return matched


def _section_stats(files: list[dict]) -> tuple[int, float]:
    loc = sum(r.get("loc", 0) for r in files)
    avg = round(sum(r.get("complexity", 0) for r in files) / max(len(files), 1), 1)
    return loc, avg


def detect_sections(target: Path, results: list[dict]) -> list[dict]:
    """Detect logical sections of the codebase (frontend, backend, etc.).

    Strategy:
    1. Try standard section indicators (frontend/backend/shared/tests/scripts)
    2. If few files are covered, fall back to top-level directories as sections
    """
    sections = []
    covered_files = 0

    # Strategy 1: standard section indicators
    for section_name, indicators in SECTION_INDICATORS.items():
        matched_dirs = [d for d in indicators["dirs"] if (target / d).is_dir()]

        matched_files = []
        for f in indicators["files"]:
            for ext in ("", ".js", ".ts", ".mjs", ".cjs", ".yml", ".yaml", ".toml", ".json"):
                if (target / f"{f}{ext}").exists():
                    matched_files.append(f"{f}{ext}")
                    break

        if not matched_dirs and not matched_files:
            continue

        section_files = _files_in_dirs(results, target, matched_dirs)
        loc, avg = _section_stats(section_files)
        covered_files += len(section_files)

        sections.append({
            "name": section_name,
            "dirs": matched_dirs,
            "indicator_files": matched_files,
            "file_count": len(section_files),
            "loc": loc,
            "avg_complexity": avg,
        })

    # Strategy 2: if standard sections cover <50% of files, detect top-level dirs
    if covered_files < len(results) * 0.5:
        top_dirs: dict[str, list[dict]] = {}
        for r in results:
            rel = Path(r["path"]).relative_to(target)
            top = rel.parts[0] if len(rel.parts) > 1 else None
            if top and top not in SKIP_DIRS:
                top_dirs.setdefault(top, []).append(r)

        # Only use top-level dirs if there are multiple with >2 files
        real_dirs = {d: files for d, files in top_dirs.items() if len(files) >= 2}
        if len(real_dirs) >= 2:
            sections = []  # replace standard sections with top-level dirs
            for dir_name, dir_files in sorted(real_dirs.items(), key=lambda x: -len(x[1])):
                loc, avg = _section_stats(dir_files)
                sections.append({
                    "name": dir_name,
                    "dirs": [dir_name],
                    "indicator_files": [],
                    "file_count": len(dir_files),
                    "loc": loc,
                    "avg_complexity": avg,
                })

    # Only return sections with files
    return [s for s in sorted(sections, key=lambda s: s["file_count"], reverse=True) if s["file_count"] > 0]


def scan(target_path: str, threshold: int) -> dict:
    target = Path(target_path).resolve()
    if not target.exists():
        return {"error": f"Path not found: {target}"}

    base = target if target.is_dir() else target.parent
    files = collect_files(target, threshold)
    results = [analyze_file(f) for f in sorted(files)]

    import_map = build_import_map(results, base) if len(results) > 1 else {}
    dead_exports = find_dead_exports(results) if len(results) > 1 else {}
    duplicates = find_duplicates(results)

    for r in results:
        r["consumed_by"] = len(import_map.get(r["path"], []))
        r["dead_exports"] = dead_exports.get(r["path"], [])

    total_loc = sum(r.get("loc", 0) for r in results)
    avg_complexity = round(
        sum(r.get("complexity", 0) for r in results) / max(len(results), 1), 1
    )

    sections = detect_sections(target, results) if target.is_dir() else []

    return {
        "target": str(target),
        "threshold": threshold,
        "file_count": len(results),
        "total_loc": total_loc,
        "avg_complexity": avg_complexity,
        "sections": sections,
        "duplicates": duplicates,
        "files": sorted(results, key=lambda r: r.get("complexity", 0), reverse=True),
    }


def print_human(result: dict):
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Target:     {result['target']}")
    print(f"Threshold:  {result['threshold']} lines")
    print(f"Files:      {result['file_count']}")
    print(f"Total LOC:  {result['total_loc']}")
    print(f"Avg complexity: {result['avg_complexity']}")
    print()

    if result.get("sections"):
        print("Sections:")
        for s in result["sections"]:
            dirs = ", ".join(s["dirs"])
            print(f"  {s['name']:12s} {s['file_count']:4d} files  {s['loc']:6d} LOC  avg={s['avg_complexity']}  [{dirs}]")
        print()

    if result.get("duplicates"):
        print(f"Duplicate symbols: {len(result['duplicates'])}")
        for d in result["duplicates"][:10]:
            locs = ", ".join(f"{l['file']}:{l['line']}" for l in d["locations"])
            print(f"  {d['name']} -> {locs}")
        print()

    if not result["files"]:
        print("No files found.")
        return

    for f in result["files"][:30]:
        score = f.get("complexity", 0)
        marker = " ***" if score > 7 else " **" if score > 5 else " *" if score > 3 else ""
        print(f"  [{score:4.1f}] {f['path']} ({f.get('loc', 0)} lines, {f.get('function_count', 0)} fn){marker}")
        for s in f.get("oversized_functions", []):
            print(f"         ! {s['name']} ({s['length']} lines) at L{s['line']}")
        for s in f.get("deep_functions", []):
            print(f"         ~ {s['name']} (depth {s['depth']}) at L{s['line']}")
        if f.get("dead_exports"):
            print(f"         dead exports: {', '.join(f['dead_exports'][:5])}")


def main():
    if len(sys.argv) < 2:
        print("Usage: scan_codebase.py <path> [--threshold N] [--json]", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    threshold = DEFAULT_THRESHOLD
    use_json = "--json" in sys.argv

    for i, arg in enumerate(sys.argv):
        if arg == "--threshold" and i + 1 < len(sys.argv):
            try:
                threshold = int(sys.argv[i + 1])
            except ValueError:
                print(f"Error: --threshold requires an integer, got '{sys.argv[i + 1]}'", file=sys.stderr)
                sys.exit(1)

    result = scan(target, threshold)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
