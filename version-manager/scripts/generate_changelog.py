#!/usr/bin/env python3
"""Generate CHANGELOG.md from releases.json or conventional commits."""

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List
import re


def generate_from_releases_json(project_root: Path) -> str:
    """Generate changelog from releases.json."""
    releases_path = project_root / "releases.json"

    if not releases_path.exists():
        print("Error: releases.json not found", file=sys.stderr)
        sys.exit(1)

    with open(releases_path) as f:
        data = json.load(f)

    releases = data.get("releases", [])
    if not releases:
        print("Error: No releases found in releases.json", file=sys.stderr)
        sys.exit(1)

    # Generate changelog in Keep a Changelog format
    lines = [
        "# Changelog",
        "",
        "All notable changes to this project will be documented in this file.",
        "",
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),",
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).",
        "",
    ]

    for release in releases:
        version = release["version"]
        release_date = release["date"]
        highlight = release.get("highlight", "")

        # Version header
        lines.append(f"## [{version}] - {release_date}")
        if highlight:
            lines.append(f"\n{highlight}")
        lines.append("")

        # Group changes by type
        changes_by_type = {}
        for change in release.get("changes", []):
            change_type = change["type"]
            if change_type not in changes_by_type:
                changes_by_type[change_type] = []
            changes_by_type[change_type].append(change["text"])

        # Output in standard order
        type_order = ["added", "changed", "deprecated", "removed", "fixed", "security"]
        type_headers = {
            "added": "### Added",
            "changed": "### Changed",
            "deprecated": "### Deprecated",
            "removed": "### Removed",
            "fixed": "### Fixed",
            "security": "### Security"
        }

        for change_type in type_order:
            if change_type in changes_by_type:
                lines.append(type_headers[change_type])
                for text in changes_by_type[change_type]:
                    lines.append(f"- {text}")
                lines.append("")

    return "\n".join(lines)


def parse_conventional_commit(message: str) -> Dict:
    """Parse conventional commit message."""
    # Pattern: type(scope): description
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore|build|ci|revert)(\(([^)]+)\))?: (.+)$'
    match = re.match(pattern, message)

    if not match:
        return None

    commit_type = match.group(1)
    scope = match.group(3) if match.group(3) else None
    description = match.group(4)

    # Check for breaking change
    breaking = "!" in message or "BREAKING CHANGE" in message

    return {
        "type": commit_type,
        "scope": scope,
        "description": description,
        "breaking": breaking
    }


def generate_from_commits(project_root: Path, since: str = None) -> str:
    """Generate changelog from conventional commits."""
    # Get git log
    cmd = ["git", "log", "--pretty=format:%s"]
    if since:
        cmd.append(f"{since}..HEAD")

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}", file=sys.stderr)
        sys.exit(1)

    commit_messages = result.stdout.strip().split("\n")

    # Parse commits
    changes_by_type = {
        "breaking": [],
        "feat": [],
        "fix": [],
        "perf": [],
        "revert": [],
        "docs": [],
        "style": [],
        "refactor": [],
        "test": [],
        "build": [],
        "ci": [],
        "chore": []
    }

    for message in commit_messages:
        parsed = parse_conventional_commit(message)
        if parsed:
            if parsed["breaking"]:
                changes_by_type["breaking"].append(parsed["description"])
            else:
                changes_by_type[parsed["type"]].append(parsed["description"])

    # Generate changelog
    today = date.today().isoformat()
    lines = [
        "# Changelog",
        "",
        "All notable changes to this project will be documented in this file.",
        "",
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),",
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).",
        "",
        f"## [Unreleased] - {today}",
        ""
    ]

    # Map conventional types to Keep a Changelog categories
    type_mapping = {
        "breaking": "### Breaking Changes",
        "feat": "### Added",
        "fix": "### Fixed",
        "perf": "### Changed",
        "revert": "### Removed",
        "docs": "### Documentation",
        "style": "### Changed",
        "refactor": "### Changed",
    }

    display_order = ["breaking", "feat", "fix", "perf", "docs", "style", "refactor", "revert"]

    for commit_type in display_order:
        if changes_by_type[commit_type]:
            header = type_mapping.get(commit_type, f"### {commit_type.title()}")
            lines.append(header)
            for change in changes_by_type[commit_type]:
                lines.append(f"- {change}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate CHANGELOG.md")
    parser.add_argument(
        "--from-releases",
        action="store_true",
        help="Generate from releases.json (Pattern 3: Advanced)"
    )
    parser.add_argument(
        "--from-commits",
        action="store_true",
        help="Generate from conventional commits (Pattern 2: Standard)"
    )
    parser.add_argument(
        "--since",
        help="Git tag/commit to start from (for --from-commits)"
    )
    parser.add_argument(
        "--output",
        help="Output file (default: CHANGELOG.md)"
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=".",
        help="Project directory (default: current directory)"
    )

    args = parser.parse_args()
    project_root = Path(args.project_dir).resolve()

    if not project_root.exists():
        print(f"Error: Directory {project_root} does not exist", file=sys.stderr)
        sys.exit(1)

    # Determine source
    if args.from_releases:
        content = generate_from_releases_json(project_root)
    elif args.from_commits:
        content = generate_from_commits(project_root, args.since)
    else:
        # Auto-detect
        if (project_root / "releases.json").exists():
            print("Auto-detected: Using releases.json")
            content = generate_from_releases_json(project_root)
        else:
            print("Auto-detected: Using conventional commits")
            content = generate_from_commits(project_root)

    # Write output
    output_path = project_root / (args.output or "CHANGELOG.md")
    output_path.write_text(content)

    print(f"✅ Generated {output_path}")


if __name__ == "__main__":
    main()
