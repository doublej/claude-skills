#!/usr/bin/env python3
"""Scan a codebase for naming convention inconsistencies.

Usage:
    python3 scan_naming.py /path/to/project              # human summary
    python3 scan_naming.py /path/to/project --json        # structured JSON
    python3 scan_naming.py /path/to/project --tree        # annotated tree view
    python3 scan_naming.py /path/to/project --language py  # filter language
    python3 scan_naming.py /path/to/project --allowlist "API,URL,ID"
"""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from naming_quality import (
    analyse_verb_consistency,
    build_tree,
    detect_anti_patterns,
    format_tree,
)

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "__pycache__", "dist",
    "build", ".next", "target", ".svelte-kit", "coverage",
    "vendor", ".tox", "egg-info",
}

EXT_TO_LANG = {
    ".py": "python", ".pyi": "python",
    ".ts": "typescript", ".tsx": "typescript",
    ".js": "javascript", ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".swift": "swift",
}

# Per-language symbol extraction patterns: (category, regex with group 1 = name)
SYMBOL_PATTERNS: dict[str, list[tuple[str, re.Pattern]]] = {
    "python": [
        ("function", re.compile(r"^[ \t]*(?:async\s+)?def\s+(\w+)\s*\(", re.MULTILINE)),
        ("class", re.compile(r"^[ \t]*class\s+(\w+)[:\(]", re.MULTILINE)),
        ("constant", re.compile(r"^([A-Z][A-Z0-9_]{2,})\s*=", re.MULTILINE)),
        ("variable", re.compile(r"^(?: {4}| {8}|\t|\t\t)([a-z]\w*)\s*=\s*(?!.*(?:def|class|import)\b)", re.MULTILINE)),
    ],
    "typescript": [
        ("function", re.compile(r"^[ \t]*(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.MULTILINE)),
        ("class", re.compile(r"^[ \t]*(?:export\s+)?class\s+(\w+)", re.MULTILINE)),
        ("type", re.compile(r"^[ \t]*(?:export\s+)?(?:type|interface)\s+(\w+)", re.MULTILINE)),
        ("constant", re.compile(r"^[ \t]*(?:export\s+)?const\s+([A-Z][A-Z0-9_]{2,})\s*=", re.MULTILINE)),
        ("variable", re.compile(r"^[ \t]*(?:export\s+)?(?:const|let|var)\s+([a-z]\w+)\s*=", re.MULTILINE)),
        ("enum", re.compile(r"^[ \t]*(?:export\s+)?enum\s+(\w+)", re.MULTILINE)),
    ],
    "go": [
        ("function", re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(", re.MULTILINE)),
        ("type", re.compile(r"^type\s+(\w+)\s+(?:struct|interface)\b", re.MULTILINE)),
        ("constant", re.compile(r"^\s*(\w+)\s*=.*//", re.MULTILINE)),  # rough heuristic
    ],
    "rust": [
        ("function", re.compile(r"^[ \t]*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)", re.MULTILINE)),
        ("class", re.compile(r"^[ \t]*(?:pub\s+)?(?:struct|enum)\s+(\w+)", re.MULTILINE)),
        ("type", re.compile(r"^[ \t]*(?:pub\s+)?trait\s+(\w+)", re.MULTILINE)),
        ("constant", re.compile(r"^[ \t]*(?:pub\s+)?(?:const|static)\s+(\w+)\s*:", re.MULTILINE)),
    ],
    "swift": [
        ("function", re.compile(r"^[ \t]*(?:public\s+|private\s+|internal\s+|open\s+)?(?:static\s+)?func\s+(\w+)", re.MULTILINE)),
        ("class", re.compile(r"^[ \t]*(?:public\s+|private\s+|open\s+)?(?:class|struct|enum)\s+(\w+)", re.MULTILINE)),
        ("type", re.compile(r"^[ \t]*(?:public\s+|private\s+)?protocol\s+(\w+)", re.MULTILINE)),
        ("constant", re.compile(r"^[ \t]*(?:public\s+|private\s+)?(?:static\s+)?let\s+(\w+)\s*[=:]", re.MULTILINE)),
        ("variable", re.compile(r"^[ \t]*(?:public\s+|private\s+)?var\s+([a-z]\w+)\s*[=:]", re.MULTILINE)),
    ],
}
SYMBOL_PATTERNS["javascript"] = SYMBOL_PATTERNS["typescript"]

# Expected conventions per language per category
CANONICAL_CONVENTIONS: dict[str, dict[str, str]] = {
    "python": {
        "function": "snake_case", "class": "PascalCase", "type": "PascalCase",
        "constant": "SCREAMING_SNAKE", "variable": "snake_case",
    },
    "typescript": {
        "function": "camelCase", "class": "PascalCase", "type": "PascalCase",
        "constant": "SCREAMING_SNAKE", "variable": "camelCase", "enum": "PascalCase",
    },
    "javascript": {
        "function": "camelCase", "class": "PascalCase", "type": "PascalCase",
        "constant": "SCREAMING_SNAKE", "variable": "camelCase", "enum": "PascalCase",
    },
    "go": {
        "function": "camelCase", "type": "PascalCase", "constant": "camelCase",
    },
    "rust": {
        "function": "snake_case", "class": "PascalCase", "type": "PascalCase",
        "constant": "SCREAMING_SNAKE",
    },
    "swift": {
        "function": "camelCase", "class": "PascalCase", "type": "PascalCase",
        "constant": "camelCase", "variable": "camelCase",
    },
}

# Names to skip (builtins, dunder, test fixtures, single-char)
SKIP_NAMES = frozenset({
    "main", "__init__", "__new__", "__str__", "__repr__", "__eq__",
    "__hash__", "__len__", "__getitem__", "__setitem__", "__delitem__",
    "__enter__", "__exit__", "__call__", "__iter__", "__next__",
    "setUp", "tearDown", "setUpClass", "tearDownClass",
    "self", "cls", "args", "kwargs", "_",
})


def classify_style(name: str) -> str:
    """Classify a name into its naming style."""
    if re.match(r"^[A-Z][A-Z0-9_]+$", name):
        return "SCREAMING_SNAKE"
    if re.match(r"^[A-Z][a-zA-Z0-9]*$", name):
        return "PascalCase"
    if re.match(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$", name):
        return "snake_case"
    if re.match(r"^[a-z][a-z0-9]*$", name):
        return "flat"
    if re.match(r"^_?[a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*$", name):
        return "camelCase"
    if re.match(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$", name):
        return "kebab-case"
    if re.match(r"^_+\w+$", name):
        return "private"
    return "other"


def convert_to_style(name: str, target: str) -> str:
    """Convert a name to the target naming style."""
    # Split into words
    words = _split_name(name)
    if not words:
        return name

    if target == "snake_case":
        return "_".join(w.lower() for w in words)
    if target == "camelCase":
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])
    if target == "PascalCase":
        return "".join(w.capitalize() for w in words)
    if target == "SCREAMING_SNAKE":
        return "_".join(w.upper() for w in words)
    if target == "kebab-case":
        return "-".join(w.lower() for w in words)
    return name


def _split_name(name: str) -> list[str]:
    """Split a name into its constituent words."""
    name = name.strip("_")
    if not name:
        return []
    # kebab-case
    if "-" in name:
        return [w for w in name.split("-") if w]
    # snake_case / SCREAMING_SNAKE
    if "_" in name:
        return [w for w in name.split("_") if w]
    # camelCase / PascalCase
    words = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z][a-z]|\d|\b)", name)
    return words if words else [name]


def _should_skip(name: str, allowlist: set[str]) -> bool:
    """Check if a name should be skipped from analysis."""
    if name in SKIP_NAMES:
        return True
    if name.startswith("__") and name.endswith("__"):
        return True
    if len(name) <= 1:
        return True
    if name in allowlist:
        return True
    # Skip test function names (test_xxx)
    if name.startswith("test_") or name.startswith("Test"):
        return True
    return False


def git_files(directory: Path) -> list[Path] | None:
    """Get tracked and untracked (non-ignored) files via git."""
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


def collect_files(target: Path, language_filter: str | None = None) -> list[Path]:
    """Collect source files from target, optionally filtered by language."""
    if target.is_file():
        return [target]

    tracked = git_files(target)
    if tracked is not None:
        candidates = [
            f for f in tracked
            if f.suffix in EXT_TO_LANG
            and f.exists()
            and not any(d in f.parts for d in SKIP_DIRS)
        ]
    else:
        candidates = [
            f for f in target.rglob("*")
            if f.is_file()
            and f.suffix in EXT_TO_LANG
            and not any(d in f.parts for d in SKIP_DIRS)
        ]

    if language_filter:
        candidates = [
            f for f in candidates
            if EXT_TO_LANG.get(f.suffix) == language_filter
        ]

    return candidates


def extract_symbols(text: str, lang: str) -> list[dict]:
    """Extract named symbols from source text for a given language."""
    patterns = SYMBOL_PATTERNS.get(lang, [])
    symbols = []
    for category, pattern in patterns:
        for m in pattern.finditer(text):
            name = m.group(1)
            line = text[:m.start()].count("\n") + 1
            symbols.append({
                "name": name, "line": line, "category": category,
            })
    return symbols


def classify_filename(path: Path) -> dict:
    """Classify a filename's naming style."""
    stem = path.stem
    style = classify_style(stem)
    return {"name": stem, "style": style, "path": str(path)}


def analyze_file(path: Path, base: Path, allowlist: set[str]) -> dict:
    """Analyze a single file for naming convention violations."""
    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return {"path": str(path.relative_to(base)), "error": "unreadable"}

    lang = EXT_TO_LANG.get(path.suffix)
    if not lang:
        return {"path": str(path.relative_to(base)), "symbols": []}

    raw_symbols = extract_symbols(text, lang)
    symbols = []
    seen = set()

    for sym in raw_symbols:
        name = sym["name"]
        if _should_skip(name, allowlist):
            continue
        key = (name, sym["category"])
        if key in seen:
            continue
        seen.add(key)

        style = classify_style(name)
        sym["style"] = style
        symbols.append(sym)

    return {
        "path": str(path.relative_to(base)),
        "language": lang,
        "symbols": symbols,
    }


def _merge_flat(counter: Counter, lang: str) -> Counter:
    """Merge 'flat' counts into the parent convention for the language.

    flat names (e.g. 'name', 'path') are ambiguous — they're valid in both
    snake_case and camelCase. Merge them into whichever is canonical.
    """
    flat_count = counter.pop("flat", 0)
    if not flat_count:
        return counter
    # Languages where flat is a subset of snake_case
    if lang in ("python", "rust"):
        counter["snake_case"] = counter.get("snake_case", 0) + flat_count
    # Languages where flat is a subset of camelCase
    elif lang in ("typescript", "javascript", "go", "swift"):
        counter["camelCase"] = counter.get("camelCase", 0) + flat_count
    else:
        counter["flat"] = flat_count  # restore if unknown language
    return counter


def compute_distributions(
    symbols: list[dict], lang: str = "",
) -> dict[str, dict]:
    """Compute style distributions per category."""
    by_category: dict[str, Counter] = {}
    for sym in symbols:
        cat = sym["category"]
        style = sym["style"]
        by_category.setdefault(cat, Counter())[style] += 1

    result = {}
    for cat, counter in sorted(by_category.items()):
        counter = _merge_flat(counter, lang)
        total = sum(counter.values())
        dominant = counter.most_common(1)[0][0] if counter else "unknown"
        result[cat] = {
            "dominant": dominant,
            "total": total,
            "distribution": dict(counter.most_common()),
        }
    return result


def find_violations(
    file_results: list[dict], conventions: dict[str, dict[str, str]],
) -> list[dict]:
    """Find symbols that violate the expected convention."""
    violations = []
    for fr in file_results:
        lang = fr.get("language")
        if not lang or lang not in conventions:
            continue
        lang_conventions = conventions[lang]
        for sym in fr.get("symbols", []):
            cat = sym["category"]
            expected = lang_conventions.get(cat)
            if not expected:
                continue
            if sym["style"] == expected or sym["style"] == "private":
                continue
            # flat names are ambiguous — skip for camelCase/snake_case
            if sym["style"] == "flat":
                continue
            suggested = convert_to_style(sym["name"], expected)
            if suggested == sym["name"]:
                continue
            violations.append({
                "file": fr["path"],
                "line": sym["line"],
                "symbol": sym["name"],
                "category": cat,
                "current_style": sym["style"],
                "expected_style": expected,
                "suggested": suggested,
            })
    return violations


def scan_filenames(files: list[Path], base: Path) -> dict:
    """Scan filenames for style consistency."""
    counter: Counter = Counter()
    all_files = []
    for f in files:
        info = classify_filename(f.relative_to(base))
        counter[info["style"]] += 1
        all_files.append(info)

    dominant = counter.most_common(1)[0][0] if counter else "unknown"
    return {
        "dominant": dominant,
        "total": sum(counter.values()),
        "distribution": dict(counter.most_common()),
    }


def scan(
    target_path: str,
    language_filter: str | None = None,
    allowlist: set[str] | None = None,
    include_tree: bool = False,
) -> dict:
    """Main scan entry point."""
    target = Path(target_path).resolve()
    if not target.exists():
        return {"error": f"Path not found: {target}"}

    base = target if target.is_dir() else target.parent
    allowlist = allowlist or set()
    files = collect_files(target, language_filter)
    if not files:
        return {"error": "No source files found"}

    # Analyze each file
    file_results = [analyze_file(f, base, allowlist) for f in sorted(files)]
    file_results = [r for r in file_results if "error" not in r]

    # Detect languages
    languages = sorted({r["language"] for r in file_results if "language" in r})

    # Per-language distributions
    by_language = {}
    for lang in languages:
        lang_symbols = [
            sym for fr in file_results
            if fr.get("language") == lang
            for sym in fr.get("symbols", [])
        ]
        by_language[lang] = compute_distributions(lang_symbols, lang)

    # Auto-detect conventions (majority vote per language per category)
    detected_conventions: dict[str, dict[str, str]] = {}
    for lang, cats in by_language.items():
        detected_conventions[lang] = {}
        for cat, info in cats.items():
            detected_conventions[lang][cat] = info["dominant"]

    # Find violations against detected conventions
    violations = find_violations(file_results, detected_conventions)

    # File naming
    file_naming = scan_filenames(files, base)

    # All symbols count
    symbol_count = sum(len(r.get("symbols", [])) for r in file_results)

    # Quality analysis
    verb_data = analyse_verb_consistency(file_results)
    anti_patterns = detect_anti_patterns(file_results)
    anti_pattern_counts: dict[str, int] = {}
    for ap in anti_patterns:
        anti_pattern_counts[ap["issue"]] = anti_pattern_counts.get(ap["issue"], 0) + 1

    result = {
        "target": str(target),
        "languages": languages,
        "file_count": len(file_results),
        "symbol_count": symbol_count,
        "file_naming": file_naming,
        "by_language": by_language,
        "detected_conventions": detected_conventions,
        "canonical_conventions": {
            lang: CANONICAL_CONVENTIONS.get(lang, {})
            for lang in languages
        },
        "violations": violations,
        "violation_count": len(violations),
        "quality": {
            "verb_usage": verb_data["verb_usage"],
            "verb_groups": verb_data["verb_groups"],
            "anti_patterns": anti_patterns,
            "anti_pattern_counts": anti_pattern_counts,
        },
    }

    if include_tree:
        result["tree"] = build_tree(file_results)

    return result


def print_human(result: dict, use_tree: bool = False):
    """Print a human-readable summary."""
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Target:     {result['target']}")
    print(f"Languages:  {', '.join(result['languages'])}")
    print(f"Files:      {result['file_count']}")
    print(f"Symbols:    {result['symbol_count']}")
    print(f"Violations: {result['violation_count']}")
    print()

    # Tree view
    if use_tree and "tree" in result:
        quality = result.get("quality", {})
        print(format_tree(result["tree"], quality.get("verb_groups", [])))
        print()

    # File naming
    fn = result["file_naming"]
    print(f"File naming: dominant={fn['dominant']} ({fn['total']} files)")
    for style, count in fn["distribution"].items():
        print(f"  {style:20s} {count:4d}")
    print()

    # Per-language breakdown
    for lang, cats in result["by_language"].items():
        print(f"[{lang}]")
        for cat, info in cats.items():
            dist = " ".join(f"{s}={c}" for s, c in info["distribution"].items())
            print(f"  {cat:12s} dominant={info['dominant']:16s} ({dist})")
        print()

    # Quality: verb consistency
    quality = result.get("quality", {})
    verb_groups = quality.get("verb_groups", [])
    if verb_groups:
        print("Verb consistency issues:")
        for g in verb_groups:
            verbs_str = ", ".join(f"{v}={c}" for v, c in g["verbs"].items())
            print(f"  {g['action']}: {verbs_str}  (dominant: {g['dominant']})")
        print()

    # Quality: anti-patterns
    ap_counts = quality.get("anti_pattern_counts", {})
    if ap_counts:
        print("Anti-pattern counts:")
        for issue, count in sorted(ap_counts.items()):
            print(f"  {issue:25s} {count:4d}")
        print()

    # Violations
    if result["violations"]:
        print(f"Top violations ({min(len(result['violations']), 30)} of {result['violation_count']}):")
        for v in result["violations"][:30]:
            print(
                f"  {v['file']}:{v['line']}  {v['symbol']}"
                f"  ({v['current_style']} -> {v['expected_style']}"
                f"  suggested: {v['suggested']})"
            )


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: scan_naming.py <path> [--json] [--tree] [--language LANG] [--allowlist TERMS]",
            file=sys.stderr,
        )
        sys.exit(1)

    target = sys.argv[1]
    use_json = "--json" in sys.argv
    use_tree = "--tree" in sys.argv
    language_filter = None
    allowlist: set[str] = set()

    for i, arg in enumerate(sys.argv):
        if arg == "--language" and i + 1 < len(sys.argv):
            language_filter = sys.argv[i + 1]
        if arg == "--allowlist" and i + 1 < len(sys.argv):
            allowlist = {t.strip() for t in sys.argv[i + 1].split(",")}

    result = scan(target, language_filter, allowlist, include_tree=use_tree)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result, use_tree=use_tree)


if __name__ == "__main__":
    main()
