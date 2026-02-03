#!/usr/bin/env python3
"""Validate version consistency across project files."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


SEMVER_PATTERN = re.compile(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$')


def is_valid_semver(version: str) -> bool:
    """Check if version string is valid semantic version."""
    return bool(SEMVER_PATTERN.match(version))


def get_version_from_file(file_path: Path, file_type: str) -> Optional[str]:
    """Extract version from a specific file."""
    if not file_path.exists():
        return None

    try:
        if file_type == "VERSION":
            return file_path.read_text().strip()

        elif file_type == "package.json":
            with open(file_path) as f:
                data = json.load(f)
                return data.get("version")

        elif file_type == "pyproject.toml":
            with open(file_path) as f:
                for line in f:
                    if line.strip().startswith("version"):
                        return line.split("=")[1].strip().strip('"\'')

        elif file_type == "Cargo.toml":
            with open(file_path) as f:
                in_package = False
                for line in f:
                    if line.strip() == "[package]":
                        in_package = True
                    elif line.strip().startswith("[") and in_package:
                        break
                    elif in_package and line.strip().startswith("version"):
                        return line.split("=")[1].strip().strip('"\'')

        elif file_type == "releases.json":
            with open(file_path) as f:
                data = json.load(f)
                releases = data.get("releases", [])
                if releases:
                    return releases[0].get("version")

    except Exception as e:
        print(f"⚠ Error reading {file_path}: {e}", file=sys.stderr)
        return None

    return None


def find_version_files(project_root: Path, staged_only: bool = False) -> Dict[str, Path]:
    """Find all version-containing files in the project."""
    version_files = {}

    candidates = {
        "VERSION": project_root / "VERSION",
        "package.json": project_root / "package.json",
        "pyproject.toml": project_root / "pyproject.toml",
        "Cargo.toml": project_root / "Cargo.toml",
        "releases.json": project_root / "releases.json",
    }

    if staged_only:
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=True
            )
            staged_files = set(result.stdout.strip().split("\n"))

            for file_type, path in candidates.items():
                if path.exists() and path.name in staged_files:
                    version_files[file_type] = path
        except subprocess.CalledProcessError:
            pass
    else:
        for file_type, path in candidates.items():
            if path.exists():
                version_files[file_type] = path

    return version_files


def check_changelog_entry(project_root: Path, version: str) -> bool:
    """Check if CHANGELOG.md has an entry for the current version."""
    changelog_path = project_root / "CHANGELOG.md"
    if not changelog_path.exists():
        return True  # No changelog required

    content = changelog_path.read_text()
    # Look for version in square brackets or as heading
    patterns = [
        f"[{version}]",
        f"## {version}",
        f"## [{version}]",
    ]

    return any(pattern in content for pattern in patterns)


def check_git_tag(project_root: Path, version: str) -> Optional[bool]:
    """Check if git tag exists for version. Returns None if not a git repo."""
    try:
        result = subprocess.run(
            ["git", "tag", "-l", f"v{version}"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        return bool(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def check_working_directory_clean(project_root: Path) -> Optional[bool]:
    """Check if git working directory is clean. Returns None if not a git repo."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        return not bool(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def main():
    parser = argparse.ArgumentParser(description="Validate version consistency")
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Validate only staged changes (for pre-commit hook)"
    )
    parser.add_argument(
        "--version",
        help="Validate specific version instead of auto-detecting"
    )
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Require clean working directory"
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

    errors = []
    warnings = []

    # Find version files
    version_files = find_version_files(project_root, args.staged)

    if not version_files:
        print("⚠ No version files found", file=sys.stderr)
        sys.exit(1)

    # Extract versions from all files
    versions = {}
    for file_type, path in version_files.items():
        version = get_version_from_file(path, file_type)
        if version:
            versions[file_type] = version

    if not versions:
        errors.append("No version information found in any file")
    else:
        # Check if all versions match
        unique_versions = set(versions.values())
        if len(unique_versions) > 1:
            errors.append("Version mismatch across files:")
            for file_type, version in versions.items():
                errors.append(f"  {file_type}: {version}")
        else:
            current_version = list(unique_versions)[0]
            print(f"✓ Version consistent across {len(versions)} file(s): {current_version}")

            # Use provided version or detected version
            version_to_check = args.version or current_version

            # Validate semver format
            if not is_valid_semver(version_to_check):
                errors.append(f"Invalid semantic version format: {version_to_check}")
            else:
                print(f"✓ Valid semantic version format: {version_to_check}")

            # Check changelog entry
            if not args.staged:  # Skip for staged-only validation
                if check_changelog_entry(project_root, version_to_check):
                    print(f"✓ CHANGELOG.md has entry for {version_to_check}")
                else:
                    warnings.append(f"CHANGELOG.md missing entry for {version_to_check}")

            # Check git tag (only if not staged and not requiring specific version)
            if not args.staged and not args.version:
                tag_exists = check_git_tag(project_root, version_to_check)
                if tag_exists is None:
                    print("ℹ Not a git repository, skipping tag check")
                elif tag_exists:
                    warnings.append(f"Git tag v{version_to_check} already exists")
                else:
                    print(f"✓ No existing tag for v{version_to_check}")

            # Check working directory
            if args.require_clean:
                is_clean = check_working_directory_clean(project_root)
                if is_clean is None:
                    print("ℹ Not a git repository, skipping clean check")
                elif is_clean:
                    print("✓ Working directory is clean")
                else:
                    errors.append("Working directory has uncommitted changes")

    # Print warnings
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"⚠ {warning}", file=sys.stderr)

    # Print errors and exit
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"✗ {error}", file=sys.stderr)
        sys.exit(1)

    print("\n✅ All validation checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
