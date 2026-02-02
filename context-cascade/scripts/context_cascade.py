#!/usr/bin/env python3
"""
Context Cascade - Find and analyze CLAUDE.md files in the current project hierarchy.

Walks from CWD up to home directory, collecting CLAUDE.md files.
Outputs JSON with file paths, token counts, line counts, and hierarchy info.

Usage:
    python3 context_cascade.py [--cwd /path/to/project]
"""

import json
import sys
from pathlib import Path


def estimate_tokens(text: str) -> int:
    """Estimate token count using ~4 chars per token heuristic."""
    return len(text) // 4


def find_claude_md_files(cwd: str | None = None) -> dict:
    """Find all CLAUDE.md files from CWD up to home, plus global."""
    home = Path.home()
    start = Path(cwd).resolve() if cwd else Path.cwd()

    found = []
    seen = set()

    # Walk up from CWD to home, collecting CLAUDE.md files
    current = start
    while True:
        claude_md = current / "CLAUDE.md"
        if claude_md.is_file() and claude_md not in seen:
            seen.add(claude_md)
            found.append(claude_md)
        if current == home or current == current.parent:
            break
        current = current.parent

    # Check global ~/.claude/CLAUDE.md
    global_md = home / ".claude" / "CLAUDE.md"
    if global_md.is_file() and global_md not in seen:
        seen.add(global_md)
        found.append(global_md)

    # Reverse so global is first, then parent dirs, then CWD
    found.reverse()

    results = []
    for i, path in enumerate(found):
        text = path.read_text(encoding="utf-8", errors="replace")
        tokens = estimate_tokens(text)
        lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)

        # Determine scope label
        if path == global_md:
            scope = "global"
        elif path.parent == start:
            scope = "project"
        else:
            scope = "parent"

        results.append({
            "path": str(path),
            "scope": scope,
            "tokens": tokens,
            "lines": lines,
            "chars": len(text),
            "depth": i,
        })

    # Add totals
    total_tokens = sum(r["tokens"] for r in results)
    total_lines = sum(r["lines"] for r in results)
    total_chars = sum(r["chars"] for r in results)

    return {
        "files": results,
        "total": {
            "count": len(results),
            "tokens": total_tokens,
            "lines": total_lines,
            "chars": total_chars,
        },
        "cwd": str(start),
    }


def main():
    cwd = None
    if "--cwd" in sys.argv:
        idx = sys.argv.index("--cwd")
        if idx + 1 < len(sys.argv):
            cwd = sys.argv[idx + 1]

    result = find_claude_md_files(cwd)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
