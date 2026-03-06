"""Naming quality analysis — verb consistency, anti-patterns, tree builder.

The scanner does mechanical extraction. Claude does semantic judgment.
"""

import re
from pathlib import PurePosixPath

# Synonym groups for verb consistency detection
VERB_GROUPS: dict[str, list[str]] = {
    "read": ["get", "fetch", "retrieve", "load", "find", "query"],
    "create": ["create", "make", "build", "add", "insert", "generate"],
    "delete": ["delete", "remove", "destroy", "drop", "clear"],
    "update": ["update", "modify", "set", "change", "edit", "patch"],
    "check": ["check", "validate", "verify", "ensure"],
    "transform": ["convert", "parse", "format", "serialize", "encode", "decode"],
    "send": ["send", "emit", "dispatch", "publish", "notify", "push"],
    "handle": ["handle", "process", "on", "manage"],
}

# Vague names to flag
GENERIC_NAMES: frozenset[str] = frozenset({
    "data", "result", "temp", "val", "item", "thing", "obj", "info",
    "stuff", "output", "input", "ret", "buf", "manager", "handler",
    "helper", "utils", "misc",
})

# Common abbreviations that are OK
KNOWN_ABBREVIATIONS: frozenset[str] = frozenset({
    "id", "url", "api", "http", "json", "db", "ui", "fn", "ctx",
    "str", "int", "max", "min", "err", "msg", "auth", "env", "req",
    "res", "src", "dst", "cmd", "arg", "cfg", "pkg", "lib", "fmt",
    "buf", "len", "idx", "num", "pos", "ptr", "ref", "tmp", "var",
    "opt", "io", "fs", "os", "ws", "tx", "rx", "cb", "ok", "ip",
})

# Build reverse lookup: verb → action group
_VERB_TO_GROUP: dict[str, str] = {}
for _action, _verbs in VERB_GROUPS.items():
    for _v in _verbs:
        _VERB_TO_GROUP[_v] = _action


def split_name(name: str) -> list[str]:
    """Split a name into constituent words (reusable version)."""
    name = name.strip("_")
    if not name:
        return []
    if "-" in name:
        return [w for w in name.split("-") if w]
    if "_" in name:
        return [w for w in name.split("_") if w]
    words = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z][a-z]|\d|\b)", name)
    return words if words else [name]


def decompose_verb_noun(name: str, category: str) -> tuple[str, str]:
    """For functions, extract verb (first word) and noun (rest)."""
    if category not in ("function",):
        return "", ""
    words = split_name(name)
    if not words:
        return "", ""
    return words[0].lower(), "_".join(w.lower() for w in words[1:])


def analyse_verb_consistency(file_results: list[dict]) -> dict:
    """Analyse verb usage across all functions for consistency."""
    verb_usage: dict[str, int] = {}

    for fr in file_results:
        for sym in fr.get("symbols", []):
            if sym["category"] != "function":
                continue
            verb, _ = decompose_verb_noun(sym["name"], sym["category"])
            if verb:
                verb_usage[verb] = verb_usage.get(verb, 0) + 1

    # Group verbs by action
    group_data: dict[str, dict[str, int]] = {}
    for verb, count in verb_usage.items():
        action = _VERB_TO_GROUP.get(verb)
        if action:
            group_data.setdefault(action, {})[verb] = count

    verb_groups = []
    for action, verbs in sorted(group_data.items()):
        if len(verbs) < 2:
            continue
        dominant = max(verbs, key=lambda v: verbs[v])
        inconsistent = [v for v in verbs if v != dominant]
        verb_groups.append({
            "action": action,
            "verbs": verbs,
            "dominant": dominant,
            "inconsistent": inconsistent,
        })

    return {"verb_usage": verb_usage, "verb_groups": verb_groups}


def detect_anti_patterns(file_results: list[dict]) -> list[dict]:
    """Detect naming anti-patterns across all symbols."""
    issues = []

    for fr in file_results:
        path = fr.get("path", "")
        for sym in fr.get("symbols", []):
            name = sym["name"]
            cat = sym["category"]
            line = sym.get("line", 0)
            words = split_name(name)
            lower_words = [w.lower() for w in words]

            # Generic name
            if name.lower() in GENERIC_NAMES:
                issues.append(_issue(path, line, name, cat, "generic_name"))

            # Missing bool prefix
            if cat == "variable" and lower_words:
                bool_words = {"valid", "active", "enabled", "disabled", "visible",
                              "ready", "done", "open", "closed", "empty", "loaded"}
                if lower_words[0] in bool_words and lower_words[0] not in ("is", "has"):
                    issues.append(_issue(path, line, name, cat, "missing_bool_prefix"))

            # Overly long
            if len(name) > 35:
                issues.append(_issue(path, line, name, cat, "overly_long"))

            # Unknown abbreviation
            for w in lower_words:
                if len(w) <= 3 and w not in KNOWN_ABBREVIATIONS and not w.isdigit():
                    issues.append(_issue(path, line, name, cat, "unknown_abbreviation",
                                         detail=w))
                    break  # one per symbol

    return issues


def _issue(path, line, symbol, category, issue_type, detail=""):
    entry = {
        "file": path, "line": line, "symbol": symbol,
        "category": category, "issue": issue_type,
    }
    if detail:
        entry["detail"] = detail
    return entry


def build_tree(file_results: list[dict]) -> list[dict]:
    """Group files by directory, nest functions under classes."""
    dirs: dict[str, list[dict]] = {}

    for fr in file_results:
        path = fr.get("path", "")
        dir_path = str(PurePosixPath(path).parent) if "/" in path else "."
        symbols = _nest_symbols(fr.get("symbols", []))
        dirs.setdefault(dir_path, []).append({
            "path": path,
            "symbols": symbols,
        })

    return [
        {"path": d, "files": sorted(files, key=lambda f: f["path"])}
        for d, files in sorted(dirs.items())
    ]


def _nest_symbols(symbols: list[dict]) -> list[dict]:
    """Nest function symbols under preceding class symbols."""
    if not symbols:
        return []

    sorted_syms = sorted(symbols, key=lambda s: s.get("line", 0))
    result = []
    current_class = None

    for sym in sorted_syms:
        enriched = _enrich_symbol(sym)

        if sym["category"] == "class":
            enriched["children"] = []
            result.append(enriched)
            current_class = enriched
        elif current_class and sym["category"] == "function":
            current_class["children"].append(enriched)
        else:
            current_class = None
            result.append(enriched)

    return result


def _enrich_symbol(sym: dict) -> dict:
    """Add verb/noun decomposition and style_ok flag."""
    entry = {
        "name": sym["name"],
        "category": sym["category"],
        "line": sym.get("line", 0),
        "style": sym.get("style", ""),
    }
    verb, noun = decompose_verb_noun(sym["name"], sym["category"])
    if verb:
        entry["verb"] = verb
        entry["noun"] = noun
    return entry


def format_tree(tree: list[dict], verb_groups: list[dict]) -> str:
    """Render annotated tree for human-readable CLI output."""
    inconsistent_verbs = {}
    for g in verb_groups:
        for v in g["inconsistent"]:
            inconsistent_verbs[v] = g["dominant"]

    lines = []
    for dir_entry in tree:
        lines.append(f"{dir_entry['path']}/")
        for file_entry in dir_entry["files"]:
            fname = PurePosixPath(file_entry["path"]).name
            lines.append(f"  {fname}")
            for sym in file_entry["symbols"]:
                _format_symbol(lines, sym, inconsistent_verbs, indent=4)
    return "\n".join(lines)


def _format_symbol(lines, sym, inconsistent_verbs, indent):
    pad = " " * indent
    parts = [f"{pad}{sym['name']}"]

    if sym.get("style"):
        parts.append(f"({sym['style']})")

    verb = sym.get("verb")
    noun = sym.get("noun")
    if verb:
        parts.append(f"verb:{verb}")
        if noun:
            parts.append(f"noun:{noun}")
        if verb in inconsistent_verbs:
            parts.append(f"[inconsistent: dominant is \"{inconsistent_verbs[verb]}\"]")

    lines.append(" ".join(parts))

    for child in sym.get("children", []):
        _format_symbol(lines, child, inconsistent_verbs, indent + 2)
