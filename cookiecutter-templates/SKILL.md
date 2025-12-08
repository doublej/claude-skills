---
name: cookiecutter-templates
description: Build rock-solid, never-failing cookiecutter templates optimized for Claude Code agents. Use this skill when creating new cookiecutter templates, debugging template generation failures, reviewing existing templates for best practices, or integrating templates with AI-assisted workflows.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  category: "development-tooling"
  version: "1.0"
---

# Cookiecutter Templates for Claude Code

Build bulletproof cookiecutter templates that work flawlessly with Claude Code agents.

## When to Use This Skill

- Creating new cookiecutter templates from scratch
- Debugging template generation failures
- Reviewing templates for robustness and best practices
- Making templates Claude Code-friendly
- Adding pre/post generation hooks
- Testing and validating templates

## Quick Start

Minimal working template structure:

```
my-template/
├── cookiecutter.json          # Variables with smart defaults
└── {{ cookiecutter.project_slug }}/
    └── README.md              # At least one generated file
```

## Core Principles

### 1. Fail Fast, Fail Loud

Templates must validate inputs BEFORE generation, not during or after.

```python
# hooks/pre_gen_project.py
import re
import sys

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"

# Validate immediately
if not re.match(r'^[a-z][a-z0-9_]*$', PROJECT_SLUG):
    print(f"ERROR: '{PROJECT_SLUG}' is not a valid Python package name")
    print("Must start with letter, contain only lowercase letters, numbers, underscores")
    sys.exit(1)
```

### 2. Smart Defaults Over Questions

Reduce cognitive load. Derive values when possible.

```json
{
    "project_name": "My Project",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
    "package_name": "{{ cookiecutter.project_slug }}",
    "author": "{{ cookiecutter._author | default('Your Name') }}",
    "year": "{% now 'utc', '%Y' %}"
}
```

### 3. Escape Everything Dangerous

Jinja2 conflicts are the #1 source of template failures.

```
# For files containing Jinja/Django syntax
{% raw %}
{{ user.name }}  {# This won't be processed by cookiecutter #}
{% endraw %}

# For GitHub Actions (uses ${{ }})
${% raw %}{{{% endraw %} secrets.GITHUB_TOKEN {% raw %}}}{% endraw %}

# Alternative: Use different delimiters in generated files
{# In cookiecutter.json #}
"_jinja2_env_vars": {
    "block_start_string": "{%=",
    "block_end_string": "=%}"
}
```

### 4. Idempotent Post-Generation

Hooks must be safe to run multiple times.

```python
# hooks/post_gen_project.py
import os
import subprocess

def run_safe(cmd, check=False):
    """Run command, don't fail if already done."""
    try:
        subprocess.run(cmd, shell=True, check=check, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # Already initialized, skip

# Safe: git init is idempotent
run_safe("git init")

# Safe: check before creating
if not os.path.exists(".venv"):
    run_safe("python -m venv .venv")
```

## Template Structure

```
cookiecutter-my-template/
├── cookiecutter.json              # REQUIRED: Variable definitions
├── hooks/
│   ├── pre_gen_project.py         # Validation before generation
│   └── post_gen_project.py        # Setup after generation
├── {{ cookiecutter.project_slug }}/   # Generated project root
│   ├── {{ cookiecutter.package_name }}/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_{{ cookiecutter.package_name }}.py
│   ├── pyproject.toml
│   ├── README.md
│   └── .claude/
│       └── CLAUDE.md              # Claude Code instructions
└── tests/                         # Template tests (not generated)
    └── test_template.py
```

## cookiecutter.json Patterns

### Basic with Derived Values

```json
{
    "project_name": "My Awesome Project",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
    "package_name": "{{ cookiecutter.project_slug.replace('-', '_') }}",
    "description": "A short description of the project",
    "author_name": "Your Name",
    "author_email": "you@example.com",
    "python_version": ["3.12", "3.11", "3.10"],
    "use_docker": ["no", "yes"],
    "license": ["MIT", "Apache-2.0", "GPL-3.0", "none"]
}
```

### With Private Variables (Underscore Prefix)

```json
{
    "project_name": "My Project",
    "_copy_without_render": [
        "*.html",
        "**/static/**"
    ],
    "_jinja2_env_vars": {
        "keep_trailing_newline": true
    },
    "_extensions": [
        "jinja2_time.TimeExtension"
    ]
}
```

### Boolean Handling

```json
{
    "use_docker": "no",
    "_use_docker": "{{ 'true' if cookiecutter.use_docker == 'yes' else 'false' }}"
}
```

In templates:
```jinja2
{% if cookiecutter._use_docker == 'true' %}
# Docker configuration
{% endif %}
```

## Pre-Generation Hook (Validation)

**File:** `hooks/pre_gen_project.py`

```python
#!/usr/bin/env python
"""Validate inputs before generating project."""
import re
import sys

# Get variables
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

def validate_slug(value, name):
    """Validate identifier format."""
    if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', value):
        print(f"ERROR: {name} '{value}' is invalid")
        print("Must: start with letter, end with letter/number, use only lowercase and hyphens")
        sys.exit(1)
    if len(value) > 50:
        print(f"ERROR: {name} too long (max 50 chars)")
        sys.exit(1)

def validate_package(value):
    """Validate Python package name."""
    if not re.match(r'^[a-z][a-z0-9_]*$', value):
        print(f"ERROR: package_name '{value}' is not valid Python identifier")
        sys.exit(1)
    # Check against reserved words
    import keyword
    if keyword.iskeyword(value):
        print(f"ERROR: '{value}' is a Python reserved keyword")
        sys.exit(1)

def validate_python_version(value):
    """Validate Python version."""
    valid = ["3.10", "3.11", "3.12", "3.13"]
    if value not in valid:
        print(f"ERROR: Python version must be one of: {valid}")
        sys.exit(1)

# Run all validations
validate_slug(PROJECT_SLUG, "project_slug")
validate_package(PACKAGE_NAME)
validate_python_version(PYTHON_VERSION)

print(f"Generating {PROJECT_SLUG}...")
```

## Post-Generation Hook (Setup)

**File:** `hooks/post_gen_project.py`

```python
#!/usr/bin/env python
"""Set up generated project."""
import os
import shutil
import subprocess
import sys

# Get variables
USE_DOCKER = "{{ cookiecutter.use_docker }}" == "yes"
LICENSE = "{{ cookiecutter.license }}"

def run(cmd, check=True):
    """Run shell command."""
    print(f"  Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  Warning: {result.stderr}")
    return result.returncode == 0

def remove_file(filepath):
    """Remove file if exists."""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"  Removed: {filepath}")

def remove_dir(dirpath):
    """Remove directory if exists."""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"  Removed: {dirpath}")

# Conditional cleanup
if not USE_DOCKER:
    remove_file("Dockerfile")
    remove_file("docker-compose.yml")
    remove_dir(".docker")

if LICENSE == "none":
    remove_file("LICENSE")

# Initialize git (idempotent)
if not os.path.exists(".git"):
    run("git init")
    run("git add .")

# Make scripts executable
for script in ["scripts/dev.sh", "scripts/test.sh"]:
    if os.path.exists(script):
        os.chmod(script, 0o755)

print("\nProject ready! Next steps:")
print("  cd {{ cookiecutter.project_slug }}")
print("  uv sync")
print("  uv run pytest")
```

## Claude Code Integration

### Include CLAUDE.md in Templates

Generate a `.claude/CLAUDE.md` file with project-specific instructions:

```markdown
# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Commands

```bash
# Development
uv sync              # Install dependencies
uv run pytest        # Run tests
uv run ruff check .  # Lint code
```

## Architecture

- `{{ cookiecutter.package_name }}/` - Main package
- `tests/` - Test files mirror package structure

## Conventions

- Use `uv` for all Python operations
- Tests in `tests/` with `test_` prefix
- Type hints required for all public functions
```

### Make Templates Agent-Friendly

1. **Clear structure** - Predictable file locations
2. **Explicit configs** - No hidden magic
3. **Standard tools** - Use `uv`, `ruff`, `pytest`
4. **Documented commands** - All commands in CLAUDE.md

### Include Claude Code Hooks

Generate pre-configured hooks for automation. Add `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/protect-files.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/auto-format.sh"
          }
        ]
      }
    ]
  }
}
```

**Common hook scripts to include:**

```
.claude/
├── CLAUDE.md
├── settings.json
└── hooks/
    ├── protect-files.sh    # Block sensitive file modifications
    ├── auto-format.sh      # Format code after writes
    └── audit-log.sh        # Log all tool executions
```

**Example: File Protection Hook**

```bash
#!/bin/bash
# .claude/hooks/protect-files.sh
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
tool_input=$(echo "$input" | jq -r '.tool_input')

if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" ]]; then
    file_path=$(echo "$tool_input" | jq -r '.file_path // .path // empty')

    case "$file_path" in
        *.env.production*|*secrets*|*.pem|*.key)
            echo "BLOCKED: Cannot modify sensitive file" >&2
            exit 2  # Blocking error
            ;;
    esac
fi

exit 0
```

**Exit codes:** `0` = continue, `2` = block with error message.

See **[claude-code-hooks.md](references/claude-code-hooks.md)** for complete hook reference.

## Testing Templates

### Manual Test

```bash
# Test generation
cookiecutter . --no-input -o /tmp/test-output

# Verify structure
ls -la /tmp/test-output/*/

# Run generated project tests
cd /tmp/test-output/*
uv sync && uv run pytest
```

### Automated Test

**File:** `tests/test_template.py`

```python
"""Test cookiecutter template generation."""
import os
import subprocess
import tempfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

TEMPLATE_DIR = Path(__file__).parent.parent


@pytest.fixture
def generated_project():
    """Generate project in temp directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = cookiecutter(
            str(TEMPLATE_DIR),
            output_dir=tmpdir,
            no_input=True,
            extra_context={
                "project_name": "Test Project",
                "author_name": "Test Author",
            },
        )
        yield Path(result)


def test_project_structure(generated_project):
    """Verify expected files exist."""
    assert (generated_project / "README.md").exists()
    assert (generated_project / "pyproject.toml").exists()
    assert (generated_project / ".claude" / "CLAUDE.md").exists()


def test_no_template_strings(generated_project):
    """Ensure no unrendered template variables."""
    for path in generated_project.rglob("*"):
        if path.is_file() and path.suffix in [".py", ".md", ".toml", ".yaml"]:
            content = path.read_text()
            assert "{{" not in content, f"Unrendered variable in {path}"
            assert "{%" not in content or "raw" in content


def test_project_runs(generated_project):
    """Verify generated project works."""
    result = subprocess.run(
        ["uv", "sync"],
        cwd=generated_project,
        capture_output=True,
    )
    assert result.returncode == 0
```

## Common Pitfalls

### 1. Jinja Conflicts

**Problem:** Template contains `{{ variable }}` meant for runtime.

**Solution:** Use `{% raw %}...{% endraw %}` blocks.

### 2. Directory Names with Variables

**Problem:** `{{cookiecutter.name}}/` fails on Windows.

**Solution:** Use allowed characters only: `{{ cookiecutter.project_slug }}/`

### 3. Hooks Fail Silently

**Problem:** Hook errors aren't visible.

**Solution:** Always use `sys.exit(1)` with clear error messages.

### 4. Non-Idempotent Hooks

**Problem:** Running template twice causes errors.

**Solution:** Check state before modifying.

### 5. Missing Defaults

**Problem:** Required value not provided, generation fails.

**Solution:** Every variable needs a sensible default.

## Checklist

Before releasing a template:

- [ ] All variables in `cookiecutter.json` have defaults
- [ ] `pre_gen_project.py` validates all inputs
- [ ] `post_gen_project.py` is idempotent
- [ ] No unescaped Jinja2 syntax in generated files
- [ ] Template generates valid, runnable project
- [ ] `.claude/CLAUDE.md` included with clear instructions
- [ ] `.claude/settings.json` with hooks (if using automation)
- [ ] Hook scripts use `set -euo pipefail` and validate input
- [ ] Hook scripts are executable (`chmod +x`)
- [ ] Tests pass: generation, structure, runtime
- [ ] Works on macOS, Linux, Windows (path separators)

## Reference Files

See `references/` for detailed guides:

- **[template-structure.md](references/template-structure.md)** - Complete file organization
- **[jinja-patterns.md](references/jinja-patterns.md)** - Advanced Jinja2 techniques
- **[hooks-guide.md](references/hooks-guide.md)** - Cookiecutter hook best practices
- **[testing-validation.md](references/testing-validation.md)** - Testing strategies
- **[claude-code-integration.md](references/claude-code-integration.md)** - Agent optimization
- **[claude-code-hooks.md](references/claude-code-hooks.md)** - Claude Code hooks for generated projects
