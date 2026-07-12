#!/usr/bin/env python3
"""Inject Umami analytics tracking into HTML files.

Supports two modes:
1. Placeholder: replaces <!-- TRACKING_PLACEHOLDER --> with the script tag
2. Auto-inject: inserts the script tag before </head> in all HTML files

Usage:
    python inject_tracking.py <project_dir> [<website_id>] [<umami_url>] [--auto]
"""
import re
import sys
from pathlib import Path

DEFAULT_UMAMI_URL = "https://umami-inky-two.vercel.app"
DEFAULT_WEBSITE_ID = "YOUR_WEBSITE_ID"
PLACEHOLDER_RE = re.compile(r"\s*<!--\s*TRACKING_PLACEHOLDER\s*-->\s*\n?")
HEAD_CLOSE_RE = re.compile(r"([ \t]*)</head>", re.IGNORECASE)


def make_snippet(umami_url: str, website_id: str) -> str:
    return f'<script defer src="{umami_url}/script.js" data-website-id="{website_id}"></script>'


def inject_placeholder(project_dir: Path, snippet: str) -> int:
    count = 0
    for html_file in project_dir.rglob("*.html"):
        content = html_file.read_text()
        if "TRACKING_PLACEHOLDER" not in content:
            continue
        updated = PLACEHOLDER_RE.sub(f"\n    {snippet}\n", content)
        html_file.write_text(updated)
        print(f"  [placeholder] {html_file.relative_to(project_dir)}")
        count += 1
    return count


def inject_auto(project_dir: Path, snippet: str) -> int:
    count = 0
    for html_file in project_dir.rglob("*.html"):
        content = html_file.read_text()
        if snippet in content:
            continue
        if not HEAD_CLOSE_RE.search(content):
            continue
        updated = HEAD_CLOSE_RE.sub(rf"\1    {snippet}\n\1</head>", content, count=1)
        html_file.write_text(updated)
        print(f"  [auto] {html_file.relative_to(project_dir)}")
        count += 1
    return count


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--auto"]
    auto_mode = "--auto" in sys.argv

    if len(args) < 1:
        print(f"Usage: {sys.argv[0]} <project_dir> [<website_id>] [<umami_url>] [--auto]")
        sys.exit(1)

    project_dir = Path(args[0])
    website_id = args[1] if len(args) > 1 else DEFAULT_WEBSITE_ID
    umami_url = (args[2] if len(args) > 2 else DEFAULT_UMAMI_URL).rstrip("/")

    if not project_dir.is_dir():
        print(f"ERROR: {project_dir} is not a directory")
        sys.exit(1)

    snippet = make_snippet(umami_url, website_id)

    # Try placeholder mode first
    count = inject_placeholder(project_dir, snippet)

    # Fall back to auto-inject if no placeholders found, or if --auto flag
    if count == 0 or auto_mode:
        auto_count = inject_auto(project_dir, snippet)
        count += auto_count

    if count == 0:
        print("  No HTML files found to inject tracking into")
    else:
        print(f"  Injected tracking into {count} file(s)")


if __name__ == "__main__":
    main()
