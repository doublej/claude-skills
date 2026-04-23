#!/usr/bin/env python3
"""Lint aggregate token budget for skill descriptions loaded into Claude context.

Each skill contributes one "- name: description" line to the Skills section.
Totals them with tiktoken cl100k_base. Fails if over budget.

Usage:
    ./validate-context-budget.py            # 5000 token budget, this repo
    ./validate-context-budget.py -b 4000
    ./validate-context-budget.py --scope installed   # scan ~/.claude/skills + plugins
"""
import argparse
import os
import re
import sys
from pathlib import Path

import tiktoken

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
DESC_RE = re.compile(r"^description:\s*(.+?)(?=\n[a-z_-]+:|\Z)", re.MULTILINE | re.DOTALL)


def parse_skill(path):
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return None
    fm = FRONTMATTER_RE.search(text)
    if not fm:
        return None
    name = NAME_RE.search(fm.group(1))
    desc = DESC_RE.search(fm.group(1))
    if not (name and desc):
        return None
    return name.group(1).strip().strip("\"'"), desc.group(1).strip().strip("\"'")


def scan(base):
    for dirpath, _, files in os.walk(base, followlinks=True):
        if "SKILL.md" in files:
            yield Path(dirpath) / "SKILL.md"


def collect(roots, enc):
    seen = set()
    entries = []
    for root in roots:
        if not root.exists():
            continue
        for skill_md in scan(root):
            resolved = skill_md.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            parsed = parse_skill(skill_md)
            if not parsed:
                continue
            name, desc = parsed
            line = f"- {name}: {desc}"
            entries.append((name, len(enc.encode(line)), len(desc), skill_md))
    entries.sort(key=lambda e: -e[1])
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--budget", type=int, default=5000)
    ap.add_argument(
        "--scope",
        choices=["repo", "installed"],
        default="repo",
        help="repo = this directory (default). installed = ~/.claude/skills + plugins.",
    )
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent
    if args.scope == "repo":
        roots = [repo_root]
    else:
        home = Path.home()
        roots = [home / ".claude/skills", home / ".claude/plugins"]

    enc = tiktoken.get_encoding("cl100k_base")
    entries = collect(roots, enc)
    total = sum(e[1] for e in entries)

    if args.json:
        import json
        out = {
            "budget": args.budget,
            "total": total,
            "count": len(entries),
            "over_budget": total > args.budget,
            "skills": [
                {"name": n, "tokens": t, "desc_chars": c, "path": str(p)}
                for n, t, c, p in entries
            ],
        }
        print(json.dumps(out, indent=2))
        return 0 if total <= args.budget else 1

    pct = (total / args.budget) * 100 if args.budget else 0
    status = "OVER" if total > args.budget else "OK"
    color_red = "\033[0;31m"
    color_green = "\033[0;32m"
    color_yellow = "\033[1;33m"
    color_reset = "\033[0m"
    color = color_red if status == "OVER" else (color_yellow if pct > 80 else color_green)

    print(f"{color}[{status}]{color_reset} {total}/{args.budget} tokens "
          f"({pct:.0f}%) across {len(entries)} skills")
    print(f"Top {args.top} by size:")
    for name, toks, chars, path in entries[: args.top]:
        rel = path.relative_to(repo_root) if args.scope == "repo" else path
        print(f"  {toks:5d}  {name:40s}  ({chars} chars)  {rel}")

    if total > args.budget:
        over = total - args.budget
        print()
        print(f"{color_red}Budget exceeded by {over} tokens.{color_reset} "
              "Trim descriptions on top offenders or remove unused skills.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
