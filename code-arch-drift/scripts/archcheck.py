#!/usr/bin/env python3
"""Deterministic architecture-drift checker. Stdlib only, no LLM.

Reads layer/dependency rules from an `arch` fenced block in a blueprint file
(CLAUDE.md / ARCHITECTURE.md / SPEC.md), resolves intra-repo imports to layers,
and reports edges that violate the rules. Exit code 1 when violations exist.
"""
import argparse
import fnmatch
import json
import os
import re
import sys

BLUEPRINTS = ("CLAUDE.md", "ARCHITECTURE.md", "SPEC.md")
SRC_EXT = (".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".rs", ".swift")
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", "target", ".next"}

ARCH_BLOCK = re.compile(r"```arch\s*\n(.*?)```", re.DOTALL)


def find_blueprint(root, explicit):
    """Return the blueprint file path, or None."""
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    for name in BLUEPRINTS:
        path = os.path.join(root, name)
        if os.path.isfile(path):
            return path
    return None


def parse_rules(text):
    """Parse an arch block into (layers, allows, forbids)."""
    m = ARCH_BLOCK.search(text)
    if not m:
        return None
    layers, allows, forbids = {}, [], []
    for raw in m.group(1).splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("layer "):
            name, globs = line[6:].split("=", 1)
            layers[name.strip()] = [g.strip() for g in globs.split(",") if g.strip()]
        elif "->" in line:
            forbid = line.startswith("forbid ")
            body = line[7:] if forbid else line
            left, right = (s.strip() for s in body.split("->", 1))
            (forbids if forbid else allows).append((left, right))
    return layers, allows, forbids


def collect_files(root):
    """Yield source file paths relative to root."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(SRC_EXT):
                yield os.path.relpath(os.path.join(dirpath, f), root)


def layer_of(relpath, layers):
    """First layer whose globs match relpath, else None."""
    norm = relpath.replace(os.sep, "/")
    for name, globs in layers.items():
        if any(fnmatch.fnmatch(norm, g) for g in globs):
            return name
    return None


# --- import extraction -------------------------------------------------------

PY_IMPORT = re.compile(r"^\s*(?:from\s+(\.*[\w.]+)\s+import|import\s+([\w.]+))", re.M)
JS_IMPORT = re.compile(r"""(?:import[^'"]*?from\s*|require\s*\(\s*|import\s*\(\s*)['"]([^'"]+)['"]""")
GO_IMPORT = re.compile(r"""["`]([^"`\s]+)["`]""")
RS_USE = re.compile(r"^\s*use\s+(crate|super|self)((?:::\w+)+)", re.M)


def extract_imports(relpath, text):
    """Return raw import specifiers found in the file."""
    if relpath.endswith(".py"):
        return [a or b for a, b in PY_IMPORT.findall(text)]
    if relpath.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")):
        return JS_IMPORT.findall(text)
    if relpath.endswith(".go"):
        return _go_imports(text)
    if relpath.endswith(".rs"):
        return ["::".join([h, *t.split("::")[1:]]) for h, t in RS_USE.findall(text)]
    return []


def _go_imports(text):
    block = re.search(r"import\s*\((.*?)\)", text, re.DOTALL)
    body = block.group(1) if block else text
    return GO_IMPORT.findall(body)


# --- import resolution to repo files ----------------------------------------

def resolve(spec, relpath, fileset, root):
    """Resolve an import spec to a repo-relative file path, or None (external)."""
    if spec.startswith((".", "crate", "super", "self")) or "/" in spec or "\\" in spec:
        return _resolve_path_like(spec, relpath, fileset)
    return _resolve_dotted(spec, fileset)


def _candidates(base):
    yield base + ".py"
    for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".swift"):
        yield base + ext
    yield base + "/__init__.py"
    for ext in (".ts", ".tsx", ".js", ".jsx"):
        yield base + "/index" + ext
    yield base + "/mod.rs"


def _match(base, fileset):
    norm = base.replace(os.sep, "/").lstrip("/")
    for cand in _candidates(norm):
        if cand in fileset:
            return cand
    return None


def _resolve_path_like(spec, relpath, fileset):
    srcdir = os.path.dirname(relpath)
    if spec.startswith(("crate", "super", "self")):  # Rust
        parts = spec.split("::")[1:]
        base = ("src/" + "/".join(parts)) if spec.startswith("crate") else \
               os.path.normpath(os.path.join(srcdir, *parts))
        return _match(base, fileset)
    if spec.startswith("."):  # JS/TS relative
        return _match(os.path.normpath(os.path.join(srcdir, spec)), fileset)
    return _match(spec, fileset)  # Go-style module/path or explicit path


def _resolve_dotted(spec, fileset):
    """Python dotted module: a.b.c -> a/b/c.{py,/__init__.py}, by longest suffix."""
    parts = spec.split(".")
    while parts:
        hit = _match("/".join(parts), fileset)
        if hit:
            return hit
        parts = parts[:-1]
    return None


# --- rule evaluation ---------------------------------------------------------

def edge_violation(src_layer, tgt_rel, tgt_layer, layers, allows, forbids):
    """Return (severity, rule) if the edge violates rules, else None."""
    tgt_norm = tgt_rel.replace(os.sep, "/")
    for left, right in forbids:
        if _side_matches(left, src_layer, None, layers) and \
           _side_matches(right, tgt_layer, tgt_norm, layers):
            return "forbidden", f"forbid {left} -> {right}"
    src_allows = [(l, r) for l, r in allows if l == src_layer]
    if src_layer and src_allows and tgt_layer and tgt_layer != src_layer:
        if not any(_side_matches(r, tgt_layer, tgt_norm, layers) for _, r in src_allows):
            return "layer", f"no allow: {src_layer} -> {tgt_layer}"
    return None


def _side_matches(token, layer, path, layers):
    if token == "*":
        return True
    if token == layer:
        return True
    if path is not None and token not in layers:
        return fnmatch.fnmatch(path, token)
    return False


def check(root, rules):
    layers, allows, forbids = rules
    files = list(collect_files(root))
    fileset = set(f.replace(os.sep, "/") for f in files)
    violations = []
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        src_layer = layer_of(rel, layers)
        for spec in extract_imports(rel, text):
            tgt = resolve(spec, rel, fileset, root)
            if not tgt:
                continue
            tgt_layer = layer_of(tgt, layers)
            v = edge_violation(src_layer, tgt, tgt_layer, layers, allows, forbids)
            if v:
                violations.append({
                    "severity": v[0], "src": rel, "src_layer": src_layer,
                    "target": tgt, "target_layer": tgt_layer, "rule": v[1],
                })
    return violations


def report(violations, as_json):
    if as_json:
        print(json.dumps({"violations": violations, "count": len(violations)}, indent=2))
        return
    if not violations:
        print("✓ no architectural drift detected")
        return
    print(f"✗ {len(violations)} violation(s):\n")
    for v in sorted(violations, key=lambda x: x["severity"]):
        sl, tl = v["src_layer"] or "?", v["target_layer"] or "?"
        print(f"  {v['severity']:<9} {v['src']} [{sl}] -> {v['target']} [{tl}]  ({v['rule']})")


def main():
    ap = argparse.ArgumentParser(description="Architecture-drift checker (deterministic).")
    ap.add_argument("--root", default=".", help="repo root to scan")
    ap.add_argument("--rules", help="blueprint file (default: auto-detect CLAUDE.md/ARCHITECTURE.md/SPEC.md)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    blueprint = find_blueprint(args.root, args.rules)
    if not blueprint:
        print("no blueprint found (need an `arch` block in CLAUDE.md/ARCHITECTURE.md/SPEC.md)", file=sys.stderr)
        sys.exit(2)
    with open(blueprint, encoding="utf-8") as fh:
        rules = parse_rules(fh.read())
    if not rules or not rules[0]:
        print(f"no `arch` block with layers found in {blueprint}", file=sys.stderr)
        sys.exit(2)

    violations = check(args.root, rules)
    report(violations, args.json)
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
