#!/usr/bin/env python3
"""
Sync Claude Code skills to Codex CLI.

Lists all skills, shows sync status, and enables selective or bulk syncing
with validation and safety features.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# Color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


@dataclass
class Skill:
    """Represents a skill with its installation status."""
    name: str
    source_path: Path
    description: str
    description_length: int
    in_claude: bool
    in_codex: bool
    claude_valid: bool
    codex_valid: bool


@dataclass
class SyncStatus:
    """Summary statistics for skill sync status."""
    total_skills: int
    in_claude: int
    in_codex: int
    synced: int
    invalid_links: int
    description_warnings: int


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{color}{text}{Colors.RESET}"


def parse_skill_yaml(skill_path: Path) -> tuple[str, str]:
    """
    Extract name and description from SKILL.md frontmatter.
    Falls back to regex parsing if PyYAML not available.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return skill_path.name, ""

    content = skill_md.read_text()

    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return skill_path.name, ""

    frontmatter = match.group(1)

    # Parse name and description using regex
    name = skill_path.name
    description = ""

    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip()

    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    if desc_match:
        description = desc_match.group(1).strip()

    return name, description


def is_valid_symlink(link_path: Path, expected_target: Path) -> bool:
    """Check if symlink exists and points to correct target."""
    if not link_path.exists():
        return False
    if not link_path.is_symlink():
        return False
    return link_path.resolve() == expected_target.resolve()


def scan_source_skills(source_dir: Path) -> list[Path]:
    """Find all skill directories in source."""
    skills = []
    for item in source_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                skills.append(item)
    return sorted(skills, key=lambda p: p.name)


def check_installation_status(skill_path: Path, claude_dir: Path, codex_dir: Path) -> tuple[bool, bool, bool, bool]:
    """
    Check if skill is installed in Claude and Codex.
    Returns: (in_claude, in_codex, claude_valid, codex_valid)
    """
    skill_name = skill_path.name

    claude_link = claude_dir / skill_name
    codex_link = codex_dir / skill_name

    in_claude = claude_link.exists()
    in_codex = codex_link.exists()

    claude_valid = is_valid_symlink(claude_link, skill_path) if in_claude else False
    codex_valid = is_valid_symlink(codex_link, skill_path) if in_codex else False

    return in_claude, in_codex, claude_valid, codex_valid


def validate_skill(skill: Skill) -> list[str]:
    """Validate skill and return list of warnings."""
    warnings = []

    if skill.description_length > 500:
        warnings.append(f"Description too long ({skill.description_length} chars > 500)")

    if not skill.description:
        warnings.append("No description found")

    if skill.in_claude and not skill.claude_valid:
        warnings.append("Invalid Claude symlink")

    if skill.in_codex and not skill.codex_valid:
        warnings.append("Invalid Codex symlink")

    return warnings


def collect_skills(source_dir: Path, claude_dir: Path, codex_dir: Path) -> list[Skill]:
    """Scan all skills and collect their status."""
    skills = []

    for skill_path in scan_source_skills(source_dir):
        name, description = parse_skill_yaml(skill_path)
        in_claude, in_codex, claude_valid, codex_valid = check_installation_status(
            skill_path, claude_dir, codex_dir
        )

        skill = Skill(
            name=name,
            source_path=skill_path,
            description=description,
            description_length=len(description),
            in_claude=in_claude,
            in_codex=in_codex,
            claude_valid=claude_valid,
            codex_valid=codex_valid
        )
        skills.append(skill)

    return skills


def get_sync_status(skills: list[Skill], codex_dir: Path) -> SyncStatus:
    """Calculate sync status statistics."""
    total = len(skills)
    in_claude = sum(1 for s in skills if s.in_claude)
    in_codex = sum(1 for s in skills if s.in_codex)
    synced = sum(1 for s in skills if s.in_claude and s.in_codex)

    # Count invalid symlinks in Codex
    invalid_links = 0
    for link in codex_dir.iterdir():
        if link.is_symlink() and not link.exists():
            invalid_links += 1

    description_warnings = sum(1 for s in skills if s.description_length > 500)

    return SyncStatus(
        total_skills=total,
        in_claude=in_claude,
        in_codex=in_codex,
        synced=synced,
        invalid_links=invalid_links,
        description_warnings=description_warnings
    )


def print_status_table(skills: list[Skill], filter_mode: Optional[str] = None):
    """Print formatted table of skills with sync status."""
    # Filter skills
    filtered = skills
    if filter_mode == "claude-only":
        filtered = [s for s in skills if s.in_claude and not s.in_codex]
    elif filter_mode == "codex-only":
        filtered = [s for s in skills if s.in_codex and not s.in_claude]
    elif filter_mode == "synced":
        filtered = [s for s in skills if s.in_claude and s.in_codex]
    elif filter_mode == "issues":
        filtered = [s for s in skills if not s.claude_valid or not s.codex_valid or s.description_length > 500]

    # Print header
    print(f"\n{Colors.BOLD}{'Skill Name':<35} {'Claude':<8} {'Codex':<8} {'Status':<20}{Colors.RESET}")
    print("=" * 75)

    # Print skills
    for skill in filtered:
        # Claude status
        if skill.in_claude and skill.claude_valid:
            claude_status = colorize("✓", Colors.GREEN)
        elif skill.in_claude:
            claude_status = colorize("⚠", Colors.YELLOW)
        else:
            claude_status = colorize("✗", Colors.RED)

        # Codex status
        if skill.in_codex and skill.codex_valid:
            codex_status = colorize("✓", Colors.GREEN)
        elif skill.in_codex:
            codex_status = colorize("⚠", Colors.YELLOW)
        else:
            codex_status = colorize("✗", Colors.RED)

        # Overall status
        warnings = validate_skill(skill)
        if warnings:
            status = colorize(warnings[0][:18], Colors.YELLOW)
        elif skill.in_claude and skill.in_codex:
            status = colorize("Synced", Colors.GREEN)
        elif skill.in_claude:
            status = "Claude only"
        elif skill.in_codex:
            status = "Codex only"
        else:
            status = colorize("Not installed", Colors.RED)

        print(f"{skill.name:<35} {claude_status:<15} {codex_status:<15} {status}")

    print()


def print_summary(status: SyncStatus):
    """Print summary statistics."""
    print(f"\n{Colors.BOLD}Sync Status Summary{Colors.RESET}")
    print("=" * 40)
    print(f"Total skills:          {status.total_skills}")
    print(f"In Claude:             {colorize(str(status.in_claude), Colors.GREEN)}")
    print(f"In Codex:              {colorize(str(status.in_codex), Colors.BLUE)}")
    print(f"Synced:                {colorize(str(status.synced), Colors.GREEN)}")

    if status.invalid_links > 0:
        print(f"Invalid symlinks:      {colorize(str(status.invalid_links), Colors.RED)}")

    if status.description_warnings > 0:
        print(f"Description warnings:  {colorize(str(status.description_warnings), Colors.YELLOW)}")

    print()


def create_symlink(target: Path, link: Path, dry_run: bool = False) -> bool:
    """Create symlink, removing stale one if exists."""
    if link.exists() or link.is_symlink():
        if dry_run:
            print(f"  [DRY RUN] Would remove existing: {link}")
        else:
            link.unlink()

    if dry_run:
        print(f"  [DRY RUN] Would create: {link} -> {target}")
        return True

    try:
        link.symlink_to(target)
        return True
    except OSError as e:
        print(f"  {colorize('Error', Colors.RED)}: {e}")
        return False


def confirm_action(prompt: str) -> bool:
    """Ask user for confirmation."""
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ('y', 'yes')


def cmd_list(args, skills: list[Skill]):
    """List all skills with their sync status."""
    print_status_table(skills, args.filter if hasattr(args, 'filter') else None)


def cmd_status(_args, skills: list[Skill], codex_dir: Path):
    """Show summary statistics."""
    status = get_sync_status(skills, codex_dir)
    print_summary(status)


def cmd_sync(args, skills: list[Skill], codex_dir: Path):
    """Sync skills to Codex."""
    # Filter skills to sync
    if args.skill:
        to_sync = [s for s in skills if s.source_path.name == args.skill]
        if not to_sync:
            print(f"{colorize('Error', Colors.RED)}: Skill '{args.skill}' not found")
            return 1
    elif args.all:
        to_sync = [s for s in skills if s.in_claude]
        if args.validated_only:
            to_sync = [s for s in to_sync if s.description_length <= 500]
    else:
        print(f"{colorize('Error', Colors.RED)}: Specify --all or <skill>")
        return 1

    # Confirm bulk sync
    if args.all and not args.dry_run:
        print(f"\nWill sync {len(to_sync)} skills to Codex")
        if not confirm_action("Continue?"):
            print("Cancelled")
            return 0

    # Sync skills
    success_count = 0
    for skill in to_sync:
        link_path = codex_dir / skill.source_path.name

        if skill.in_codex and skill.codex_valid and not args.dry_run:
            print(f"✓ {skill.name} (already synced)")
            success_count += 1
            continue

        print(f"Syncing {skill.name}...")
        if create_symlink(skill.source_path, link_path, args.dry_run):
            success_count += 1

    print(f"\n{colorize('✓', Colors.GREEN)} Synced {success_count}/{len(to_sync)} skills")

    if not args.dry_run:
        print(f"{colorize('Note', Colors.BLUE)}: Restart Codex CLI to load new skills")

    return 0


def cmd_fix(args, codex_dir: Path):
    """Fix broken symlinks in Codex."""
    broken = []
    for link in codex_dir.iterdir():
        if link.is_symlink() and not link.exists():
            broken.append(link)

    if not broken:
        print(f"{colorize('✓', Colors.GREEN)} No broken symlinks found")
        return 0

    print(f"\nFound {len(broken)} broken symlinks:")
    for link in broken:
        print(f"  - {link.name}")

    if not args.dry_run:
        if not confirm_action("\nRemove broken symlinks?"):
            print("Cancelled")
            return 0

    for link in broken:
        if args.dry_run:
            print(f"  [DRY RUN] Would remove: {link}")
        else:
            link.unlink()
            print(f"  Removed: {link.name}")

    print(f"\n{colorize('✓', Colors.GREEN)} Fixed {len(broken)} symlinks")
    return 0


def cmd_validate(_args, skills: list[Skill]):
    """Validate all skills for Codex compatibility."""
    issues = []

    for skill in skills:
        warnings = validate_skill(skill)
        if warnings:
            issues.append((skill, warnings))

    if not issues:
        print(f"{colorize('✓', Colors.GREEN)} All skills validated successfully")
        return 0

    print(f"\n{colorize('⚠', Colors.YELLOW)} Found {len(issues)} skills with issues:\n")

    for skill, warnings in issues:
        print(f"{colorize(skill.name, Colors.BOLD)}")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Sync Claude Code skills to Codex CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List all skills with sync status")
    list_parser.add_argument(
        "--filter",
        choices=["all", "claude-only", "codex-only", "synced", "issues"],
        default="all",
        help="Filter skills"
    )

    # Status command
    subparsers.add_parser("status", help="Show summary statistics")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync skills to Codex")
    sync_parser.add_argument("skill", nargs="?", help="Skill name to sync")
    sync_parser.add_argument("--all", action="store_true", help="Sync all skills")
    sync_parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    sync_parser.add_argument("--validated-only", action="store_true", help="Only sync validated skills")

    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Fix broken symlinks")
    fix_parser.add_argument("--dry-run", action="store_true", help="Show what would be done")

    # Validate command
    subparsers.add_parser("validate", help="Validate all skills")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Setup paths
    source_dir = Path(__file__).parent
    claude_dir = Path.home() / ".claude" / "skills"
    codex_dir = Path.home() / ".codex" / "skills"

    # Ensure directories exist
    claude_dir.mkdir(parents=True, exist_ok=True)
    codex_dir.mkdir(parents=True, exist_ok=True)

    # Execute command
    if args.command == "fix":
        return cmd_fix(args, codex_dir)

    # Collect skills for other commands
    skills = collect_skills(source_dir, claude_dir, codex_dir)

    if args.command == "list":
        cmd_list(args, skills)
    elif args.command == "status":
        cmd_status(args, skills, codex_dir)
    elif args.command == "sync":
        return cmd_sync(args, skills, codex_dir)
    elif args.command == "validate":
        return cmd_validate(args, skills)

    return 0


if __name__ == "__main__":
    sys.exit(main())
