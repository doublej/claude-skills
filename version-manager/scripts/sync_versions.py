#!/usr/bin/env python3
"""Sync version across multiple files based on configuration."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


def load_sync_config(project_root: Path) -> Dict:
    """Load version sync configuration."""
    config_path = project_root / ".version-sync.json"

    if not config_path.exists():
        # Return default config
        return {
            "source": "VERSION",
            "targets": []
        }

    with open(config_path) as f:
        return json.load(f)


def get_source_version(project_root: Path, source: str) -> str:
    """Get version from source file."""
    if source == "VERSION":
        path = project_root / "VERSION"
        if path.exists():
            return path.read_text().strip()

    elif source == "package.json":
        path = project_root / "package.json"
        if path.exists():
            with open(path) as f:
                return json.load(f).get("version", "")

    elif source == "pyproject.toml":
        path = project_root / "pyproject.toml"
        if path.exists():
            with open(path) as f:
                for line in f:
                    if line.strip().startswith("version"):
                        return line.split("=")[1].strip().strip('"\'')

    elif source == "Cargo.toml":
        path = project_root / "Cargo.toml"
        if path.exists():
            with open(path) as f:
                in_package = False
                for line in f:
                    if line.strip() == "[package]":
                        in_package = True
                    elif line.strip().startswith("[") and in_package:
                        break
                    elif in_package and line.strip().startswith("version"):
                        return line.split("=")[1].strip().strip('"\'')

    elif source == "releases.json":
        path = project_root / "releases.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                if data.get("releases"):
                    return data["releases"][0].get("version", "")

    return ""


def sync_target(project_root: Path, target: Dict, version: str, dry_run: bool = False) -> bool:
    """Sync version to a target file."""
    file_path = project_root / target["file"]

    if not file_path.exists():
        print(f"⚠ Target file does not exist: {target['file']}")
        return False

    # Replace {{VERSION}} in pattern
    pattern = target["pattern"]
    new_content = pattern.replace("{{VERSION}}", version)

    # Read current content
    current_content = file_path.read_text()

    # Try to find and replace existing version line
    # Match the pattern structure (everything except version number)
    pattern_regex = re.escape(pattern).replace(r"\{\{VERSION\}\}", r"[\d.]+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?")

    if re.search(pattern_regex, current_content):
        # Replace existing line
        new_file_content = re.sub(pattern_regex, new_content, current_content)
    else:
        # Pattern not found - cannot sync
        print(f"⚠ Pattern not found in {target['file']}: {pattern}")
        return False

    if current_content == new_file_content:
        print(f"✓ {target['file']} already up to date")
        return True

    if dry_run:
        print(f"Would update {target['file']}:")
        print(f"  Pattern: {pattern}")
        print(f"  New content: {new_content}")
        return True
    else:
        file_path.write_text(new_file_content)
        print(f"✓ Updated {target['file']}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Sync version across multiple files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files"
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

    # Load config
    config = load_sync_config(project_root)

    if not config.get("targets"):
        print("No sync targets configured")
        print("Create .version-sync.json to configure version synchronization")
        print("")
        print("Example:")
        print(json.dumps({
            "source": "VERSION",
            "targets": [
                {
                    "file": "src/mypackage/__init__.py",
                    "pattern": "__version__ = \"{{VERSION}}\""
                }
            ]
        }, indent=2))
        sys.exit(0)

    # Get source version
    source = config.get("source", "VERSION")
    version = get_source_version(project_root, source)

    if not version:
        print(f"Error: Could not read version from {source}", file=sys.stderr)
        sys.exit(1)

    print(f"Source version ({source}): {version}\n")

    if args.dry_run:
        print("DRY RUN - No files will be modified\n")

    # Sync to all targets
    success_count = 0
    for target in config["targets"]:
        if sync_target(project_root, target, version, args.dry_run):
            success_count += 1

    print(f"\n✅ Synced {success_count}/{len(config['targets'])} target(s)")

    if success_count < len(config["targets"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
