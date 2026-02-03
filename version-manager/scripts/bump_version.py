#!/usr/bin/env python3
"""Bump version with validation and changelog update."""

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Tuple


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse semantic version string into (major, minor, patch)."""
    parts = version.split("-")[0].split("+")[0]  # Remove pre-release and build metadata
    major, minor, patch = parts.split(".")
    return int(major), int(minor), int(patch)


def bump_version(version: str, bump_type: str) -> str:
    """Bump version based on type (major/minor/patch)."""
    major, minor, patch = parse_version(version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def get_current_version(project_root: Path) -> str:
    """Get current version from any available file."""
    # Try VERSION file first
    version_file = project_root / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()

    # Try package.json
    package_json = project_root / "package.json"
    if package_json.exists():
        with open(package_json) as f:
            return json.load(f).get("version", "0.0.0")

    # Try pyproject.toml
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        with open(pyproject) as f:
            for line in f:
                if line.strip().startswith("version"):
                    return line.split("=")[1].strip().strip('"\'')

    # Try Cargo.toml
    cargo = project_root / "Cargo.toml"
    if cargo.exists():
        with open(cargo) as f:
            in_package = False
            for line in f:
                if line.strip() == "[package]":
                    in_package = True
                elif line.strip().startswith("[") and in_package:
                    break
                elif in_package and line.strip().startswith("version"):
                    return line.split("=")[1].strip().strip('"\'')

    # Try releases.json
    releases = project_root / "releases.json"
    if releases.exists():
        with open(releases) as f:
            data = json.load(f)
            if data.get("releases"):
                return data["releases"][0].get("version", "0.0.0")

    return "0.0.0"


def update_version_file(file_path: Path, new_version: str):
    """Update VERSION file."""
    file_path.write_text(f"{new_version}\n")
    print(f"✓ Updated {file_path.name}")


def update_package_json(file_path: Path, new_version: str):
    """Update package.json version."""
    with open(file_path) as f:
        data = json.load(f)

    data["version"] = new_version

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"✓ Updated {file_path.name}")


def update_pyproject_toml(file_path: Path, new_version: str):
    """Update pyproject.toml version."""
    content = file_path.read_text()
    lines = content.split("\n")

    for i, line in enumerate(lines):
        if line.strip().startswith("version"):
            # Preserve quote style
            if '"' in line:
                lines[i] = f'version = "{new_version}"'
            else:
                lines[i] = f"version = '{new_version}'"
            break

    file_path.write_text("\n".join(lines))
    print(f"✓ Updated {file_path.name}")


def update_cargo_toml(file_path: Path, new_version: str):
    """Update Cargo.toml version."""
    content = file_path.read_text()
    lines = content.split("\n")

    in_package = False
    for i, line in enumerate(lines):
        if line.strip() == "[package]":
            in_package = True
        elif line.strip().startswith("[") and in_package:
            break
        elif in_package and line.strip().startswith("version"):
            lines[i] = f'version = "{new_version}"'
            break

    file_path.write_text("\n".join(lines))
    print(f"✓ Updated {file_path.name}")


def update_releases_json(file_path: Path, new_version: str):
    """Update releases.json - add new version entry at the top."""
    with open(file_path) as f:
        data = json.load(f)

    # Create new release entry
    today = date.today().isoformat()
    new_release = {
        "version": new_version,
        "date": today,
        "highlight": "TODO: Add release highlight",
        "changes": [
            {
                "text": "TODO: Add changes",
                "type": "added"
            }
        ]
    }

    # Insert at beginning
    data["releases"].insert(0, new_release)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓ Updated {file_path.name} (added new release entry)")


def update_changelog(project_root: Path, new_version: str):
    """Add new version entry to CHANGELOG.md."""
    changelog_path = project_root / "CHANGELOG.md"
    if not changelog_path.exists():
        print("ℹ No CHANGELOG.md found, skipping")
        return

    today = date.today().isoformat()
    content = changelog_path.read_text()

    # Find insertion point (after header, before first version)
    lines = content.split("\n")
    insert_index = 0

    for i, line in enumerate(lines):
        if line.startswith("## [") or line.startswith("## "):
            insert_index = i
            break

    # Create new entry
    new_entry = f"""## [{new_version}] - {today}

### Added
- TODO: Add changes

"""

    lines.insert(insert_index, new_entry)
    changelog_path.write_text("\n".join(lines))
    print(f"✓ Updated CHANGELOG.md")


def create_git_tag(project_root: Path, version: str):
    """Create git tag for new version."""
    try:
        subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", f"Release v{version}"],
            cwd=project_root,
            check=True
        )
        print(f"✓ Created git tag v{version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create git tag: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("⚠ git not found, skipping tag creation")
        return False


def run_validation(project_root: Path) -> bool:
    """Run validate_version.py to check consistency."""
    script_path = Path(__file__).parent / "validate_version.py"
    if not script_path.exists():
        print("⚠ validate_version.py not found, skipping validation")
        return True

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=project_root,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Bump version with validation")
    parser.add_argument(
        "--major",
        action="store_const",
        const="major",
        dest="bump_type",
        help="Bump major version (X.0.0)"
    )
    parser.add_argument(
        "--minor",
        action="store_const",
        const="minor",
        dest="bump_type",
        help="Bump minor version (x.X.0)"
    )
    parser.add_argument(
        "--patch",
        action="store_const",
        const="patch",
        dest="bump_type",
        help="Bump patch version (x.x.X)"
    )
    parser.add_argument(
        "--no-tag",
        action="store_true",
        help="Skip git tag creation"
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

    # Pre-release validation
    print("Running pre-release validation...\n")
    if not run_validation(project_root):
        print("\n✗ Pre-release validation failed", file=sys.stderr)
        sys.exit(1)

    # Get current version
    current_version = get_current_version(project_root)
    print(f"Current version: {current_version}")

    # Determine bump type
    bump_type = args.bump_type
    if not bump_type:
        print("\nSelect version bump type:")
        print("1. major (breaking changes)")
        print("2. minor (new features)")
        print("3. patch (bug fixes)")
        choice = input("Choice [1-3]: ").strip()

        bump_map = {"1": "major", "2": "minor", "3": "patch"}
        bump_type = bump_map.get(choice)

        if not bump_type:
            print("Invalid choice", file=sys.stderr)
            sys.exit(1)

    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    print(f"New version: {new_version}\n")

    # Confirm
    confirm = input(f"Bump version from {current_version} to {new_version}? [y/N]: ").strip().lower()
    if confirm not in ["y", "yes"]:
        print("Aborted")
        sys.exit(0)

    print()

    # Update all version files
    version_files = {
        "VERSION": project_root / "VERSION",
        "package.json": project_root / "package.json",
        "pyproject.toml": project_root / "pyproject.toml",
        "Cargo.toml": project_root / "Cargo.toml",
        "releases.json": project_root / "releases.json",
    }

    update_functions = {
        "VERSION": update_version_file,
        "package.json": update_package_json,
        "pyproject.toml": update_pyproject_toml,
        "Cargo.toml": update_cargo_toml,
        "releases.json": update_releases_json,
    }

    for file_type, path in version_files.items():
        if path.exists():
            update_functions[file_type](path, new_version)

    # Update changelog
    update_changelog(project_root, new_version)

    # Create git tag
    if not args.no_tag:
        create_git_tag(project_root, new_version)

    print(f"\n✅ Version bumped to {new_version}")
    print("\nNext steps:")
    print("1. Review changes in version files and CHANGELOG.md")
    print("2. Commit: git add . && git commit -m 'chore: bump version to {}'".format(new_version))
    print("3. Push: git push origin main")
    if not args.no_tag:
        print("4. Push tag: git push origin v{}".format(new_version))


if __name__ == "__main__":
    main()
