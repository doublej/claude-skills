#!/usr/bin/env python3
"""Scan SKILL.md files and display a compact table overview."""

import sys
import re
from pathlib import Path


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            frontmatter[key.strip()] = value.strip().strip('"\'')
    return frontmatter


def truncate(text: str, max_len: int) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 1] + '…'


def main():
    search_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    skills = []

    for skill_file in sorted(search_path.glob('*/SKILL.md')):
        # Skip nested/cache directories
        if '.cache' in str(skill_file) or 'node_modules' in str(skill_file):
            continue

        content = skill_file.read_text()
        fm = extract_frontmatter(content)

        if fm.get('name'):
            skills.append({
                'name': fm['name'],
                'desc': fm.get('description', ''),
                'path': str(skill_file.parent.relative_to(search_path))
            })

    if not skills:
        print("No skills found.")
        return

    # Calculate column widths
    name_w = min(20, max(len(s['name']) for s in skills))
    desc_w = 60

    # Header
    print(f"{'Skill':<{name_w}}  Description")
    print(f"{'-' * name_w}  {'-' * desc_w}")

    # Rows
    for s in skills:
        name = truncate(s['name'], name_w)
        desc = truncate(s['desc'], desc_w)
        print(f"{name:<{name_w}}  {desc}")

    print(f"\n{len(skills)} skills found")


if __name__ == '__main__':
    main()
