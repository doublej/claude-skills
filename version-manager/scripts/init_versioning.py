#!/usr/bin/env python3
"""Initialize versioning in a project."""

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


def detect_project_type(project_root: Path) -> str:
    """Detect project type based on manifest files."""
    if (project_root / "package.json").exists():
        return "node"
    elif (project_root / "pyproject.toml").exists():
        return "python"
    elif (project_root / "Cargo.toml").exists():
        return "rust"
    elif (project_root / "go.mod").exists():
        return "go"
    elif (project_root / "VERSION").exists():
        return "simple"
    else:
        return "unknown"


def get_current_version(project_root: Path, project_type: str) -> str:
    """Extract current version from project files or default to 1.0.0."""
    if project_type == "node":
        try:
            with open(project_root / "package.json") as f:
                return json.load(f).get("version", "1.0.0")
        except:
            return "1.0.0"
    elif project_type == "python":
        try:
            with open(project_root / "pyproject.toml") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        return line.split("=")[1].strip().strip('"\'')
        except:
            pass
        return "1.0.0"
    elif project_type == "rust":
        try:
            with open(project_root / "Cargo.toml") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        return line.split("=")[1].strip().strip('"\'')
        except:
            pass
        return "1.0.0"
    elif project_type == "simple":
        try:
            return (project_root / "VERSION").read_text().strip()
        except:
            return "1.0.0"
    else:
        return "1.0.0"


def create_version_file(project_root: Path, version: str):
    """Create VERSION file."""
    (project_root / "VERSION").write_text(f"{version}\n")
    print(f"✓ Created VERSION file with version {version}")


def create_changelog(project_root: Path, version: str):
    """Create CHANGELOG.md if it doesn't exist."""
    changelog_path = project_root / "CHANGELOG.md"
    if changelog_path.exists():
        print("✓ CHANGELOG.md already exists")
        return

    today = date.today().isoformat()
    content = f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [{version}] - {today}

### Added
- Initial release
"""
    changelog_path.write_text(content)
    print(f"✓ Created CHANGELOG.md")


def create_releases_json(project_root: Path, version: str):
    """Create releases.json for advanced pattern."""
    releases_path = project_root / "releases.json"
    if releases_path.exists():
        print("✓ releases.json already exists")
        return

    today = date.today().isoformat()
    content = {
        "$schema": "./assets/schema/releases.schema.json",
        "releases": [
            {
                "version": version,
                "date": today,
                "highlight": "Initial release",
                "changes": [
                    {
                        "text": "First stable release",
                        "type": "added"
                    }
                ]
            }
        ]
    }

    with open(releases_path, "w") as f:
        json.dump(content, f, indent=2)

    print(f"✓ Created releases.json")


def add_claude_md_section(project_root: Path, pattern: str, version: str, project_type: str):
    """Add versioning section to CLAUDE.md."""
    claude_md = project_root / "CLAUDE.md"

    version_files = []
    if project_type == "simple":
        version_files.append("Primary: VERSION")
    elif project_type == "node":
        version_files.append("Primary: package.json")
    elif project_type == "python":
        version_files.append("Primary: pyproject.toml")
    elif project_type == "rust":
        version_files.append("Primary: Cargo.toml")

    if pattern == "advanced":
        version_files.append("Source of truth: releases.json")

    section = f"""
## Versioning

Current version: {version}

### Release Process
1. {'Update releases.json with changes' if pattern == 'advanced' else 'Update CHANGELOG.md with changes'}
2. Run: python3 scripts/bump_version.py
3. Select version bump type (major/minor/patch)
4. Review and confirm changes
5. Push: git push && git push --tags

### Version Files
{chr(10).join(f'- {vf}' for vf in version_files)}

### Git Tags
Format: vX.Y.Z (e.g., v{version})
"""

    if pattern in ["standard", "advanced"]:
        section += """
### Commit Conventions
Use conventional commit format:
- feat: new feature
- fix: bug fix
- docs: documentation
- chore: maintenance
"""

    if claude_md.exists():
        content = claude_md.read_text()
        if "## Versioning" not in content:
            claude_md.write_text(content + section)
            print("✓ Added versioning section to CLAUDE.md")
        else:
            print("✓ CLAUDE.md already has versioning section")
    else:
        claude_md.write_text(f"# Project Documentation{section}")
        print("✓ Created CLAUDE.md with versioning section")


def install_git_hooks(project_root: Path):
    """Install git hooks."""
    hooks_dir = project_root / ".git" / "hooks"
    if not hooks_dir.exists():
        print("⚠ Not a git repository, skipping hooks installation")
        return

    # Get the skill directory (2 levels up from scripts/)
    skill_dir = Path(__file__).parent.parent
    source_hooks_dir = skill_dir / "hooks"

    if not source_hooks_dir.exists():
        print("⚠ Hooks directory not found in skill, skipping")
        return

    for hook_file in source_hooks_dir.glob("*"):
        if hook_file.is_file():
            dest = hooks_dir / hook_file.name
            dest.write_text(hook_file.read_text())
            dest.chmod(0o755)
            print(f"✓ Installed {hook_file.name} hook")


def create_git_tag(project_root: Path, version: str):
    """Create initial git tag."""
    try:
        # Check if tag already exists
        result = subprocess.run(
            ["git", "tag", "-l", f"v{version}"],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            print(f"✓ Tag v{version} already exists")
            return

        # Create tag
        subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", f"Release v{version}"],
            cwd=project_root,
            check=True
        )
        print(f"✓ Created git tag v{version}")
    except subprocess.CalledProcessError:
        print("⚠ Failed to create git tag (not a git repo?)")
    except FileNotFoundError:
        print("⚠ git not found, skipping tag creation")


def main():
    parser = argparse.ArgumentParser(description="Initialize versioning in a project")
    parser.add_argument(
        "--pattern",
        choices=["simple", "standard", "advanced", "automated"],
        help="Force specific versioning pattern"
    )
    parser.add_argument(
        "--no-hooks",
        action="store_true",
        help="Skip git hooks installation"
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

    print(f"Initializing versioning in: {project_root}\n")

    # Detect project type
    project_type = detect_project_type(project_root)
    print(f"Detected project type: {project_type}")

    # Determine pattern
    if args.pattern:
        pattern = args.pattern
        print(f"Using pattern: {pattern} (forced)")
    else:
        if project_type == "simple" or project_type == "unknown":
            pattern = "simple"
        else:
            pattern = "standard"
        print(f"Using pattern: {pattern} (auto-detected)")

    # Get current version
    version = get_current_version(project_root, project_type)
    print(f"Version: {version}\n")

    # Create files based on pattern
    if pattern == "simple" or project_type == "simple" or project_type == "unknown":
        create_version_file(project_root, version)

    create_changelog(project_root, version)

    if pattern == "advanced":
        create_releases_json(project_root, version)

    # Add CLAUDE.md section
    add_claude_md_section(project_root, pattern, version, project_type)

    # Install git hooks
    if not args.no_hooks:
        install_git_hooks(project_root)

    # Create initial tag
    create_git_tag(project_root, version)

    print(f"\n✅ Versioning initialized successfully!")
    print(f"\nNext steps:")
    print(f"1. Review created files")
    print(f"2. Commit changes: git add . && git commit -m 'chore: initialize versioning'")
    print(f"3. Push tag: git push --tags")


if __name__ == "__main__":
    main()
