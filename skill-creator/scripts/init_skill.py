#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--no-examples]

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py md-only-skill --path . --no-examples
"""

import argparse
import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. Common structures:
- Workflow-Based: step-by-step procedures
- Task-Based: different operations/capabilities
- Reference/Guidelines: standards or specifications
- Capabilities-Based: interrelated features]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

Replace with actual implementation or delete if not needed.
"""

def main():
    print("This is an example script for {skill_name}")

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

## When Reference Docs Are Useful

- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT loaded into context, but used within output Claude produces.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path, create_examples=True):
    """Initialize a new skill directory with template SKILL.md."""
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("Created SKILL.md")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    if create_examples:
        try:
            # Create scripts/ directory with example script
            scripts_dir = skill_dir / 'scripts'
            scripts_dir.mkdir(exist_ok=True)
            example_script = scripts_dir / 'example.py'
            example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
            example_script.chmod(0o755)
            print("Created scripts/example.py")

            # Create references/ directory with example reference doc
            references_dir = skill_dir / 'references'
            references_dir.mkdir(exist_ok=True)
            example_reference = references_dir / 'api_reference.md'
            example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
            print("Created references/api_reference.md")

            # Create assets/ directory with example asset placeholder
            assets_dir = skill_dir / 'assets'
            assets_dir.mkdir(exist_ok=True)
            example_asset = assets_dir / 'example_asset.txt'
            example_asset.write_text(EXAMPLE_ASSET)
            print("Created assets/example_asset.txt")
        except Exception as e:
            print(f"Error creating resource directories: {e}")
            return None

    print(f"\nSkill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items")
    if create_examples:
        print("2. Customize or delete example files in scripts/, references/, assets/")
        print("3. Run quick_validate.py to check the skill structure")
    else:
        print("2. Run quick_validate.py to check the skill structure")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new skill directory with a template SKILL.md.",
        epilog=(
            "Examples:\n"
            "  init_skill.py my-new-skill --path .\n"
            "  init_skill.py api-helper --path skills/\n"
            "  init_skill.py md-only-skill --path . --no-examples"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'skill_name',
        help="Skill name: hyphen-case, lowercase letters/digits/hyphens, max 40 chars"
    )
    parser.add_argument(
        '--path', required=True,
        help="Directory to create the skill folder in"
    )
    parser.add_argument(
        '--no-examples', action='store_true',
        help="Skip creating example scripts/, references/, and assets/ files"
    )
    args = parser.parse_args()

    print(f"Initializing skill: {args.skill_name}")
    print(f"Location: {args.path}\n")

    result = init_skill(args.skill_name, args.path, create_examples=not args.no_examples)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
