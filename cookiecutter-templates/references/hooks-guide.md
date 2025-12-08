# Hooks Guide

Pre and post generation hooks for bulletproof templates.

## Hook Basics

Hooks are Python scripts that run during template generation:

- `pre_gen_project.py` - Runs BEFORE files are generated
- `post_gen_project.py` - Runs AFTER files are generated

## Pre-Generation Hook

### Purpose

1. Validate all input values
2. Fail fast with clear error messages
3. Prevent invalid project generation

### Template

```python
#!/usr/bin/env python
"""Validate inputs before generating project.

Exit with code 1 to abort generation.
All print() output is visible to users.
"""
import keyword
import re
import sys

# Template variables are rendered at hook execution time
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_project_slug(value: str) -> None:
    """Validate project slug format."""
    if not value:
        raise ValidationError("project_slug cannot be empty")

    if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', value):
        raise ValidationError(
            f"project_slug '{value}' is invalid.\n"
            "Must: start with letter, end with alphanumeric, "
            "contain only lowercase letters, numbers, and hyphens"
        )

    if len(value) > 50:
        raise ValidationError(
            f"project_slug '{value}' is too long (max 50 characters)"
        )

    if "--" in value:
        raise ValidationError("project_slug cannot contain consecutive hyphens")


def validate_package_name(value: str) -> None:
    """Validate Python package name."""
    if not value:
        raise ValidationError("package_name cannot be empty")

    if not re.match(r'^[a-z][a-z0-9_]*$', value):
        raise ValidationError(
            f"package_name '{value}' is not a valid Python identifier.\n"
            "Must: start with letter, contain only lowercase letters, "
            "numbers, and underscores"
        )

    if keyword.iskeyword(value):
        raise ValidationError(
            f"package_name '{value}' is a Python reserved keyword"
        )

    # Check against common conflicts
    forbidden = {'test', 'tests', 'setup', 'pip', 'site'}
    if value in forbidden:
        raise ValidationError(
            f"package_name '{value}' conflicts with common Python conventions"
        )


def validate_python_version(value: str) -> None:
    """Validate Python version."""
    valid_versions = {"3.10", "3.11", "3.12", "3.13"}
    if value not in valid_versions:
        raise ValidationError(
            f"python_version '{value}' is not supported.\n"
            f"Choose from: {', '.join(sorted(valid_versions))}"
        )


def main() -> None:
    """Run all validations."""
    try:
        validate_project_slug(PROJECT_SLUG)
        validate_package_name(PACKAGE_NAME)
        validate_python_version(PYTHON_VERSION)

        print(f"Generating '{PROJECT_NAME}'...")

    except ValidationError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Post-Generation Hook

### Purpose

1. Clean up conditional files/directories
2. Initialize git repository
3. Set file permissions
4. Install dependencies (optional)
5. Print next steps

### Template

```python
#!/usr/bin/env python
"""Set up generated project.

This hook runs AFTER all files are generated.
Current working directory is the generated project root.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Template variables
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
USE_DOCKER = "{{ cookiecutter.use_docker }}" == "yes"
USE_CI = "{{ cookiecutter.use_ci }}" == "yes"
LICENSE = "{{ cookiecutter.license }}"


def remove_path(path: str) -> None:
    """Remove file or directory if it exists."""
    p = Path(path)
    if p.is_file():
        p.unlink()
        print(f"  Removed: {path}")
    elif p.is_dir():
        shutil.rmtree(p)
        print(f"  Removed: {path}/")


def run_command(cmd: str, check: bool = False) -> bool:
    """Run shell command, return success status."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and check:
        print(f"  Warning: {cmd} failed")
        print(f"    {result.stderr.strip()}")
    return result.returncode == 0


def make_executable(path: str) -> None:
    """Make file executable."""
    if os.path.exists(path):
        os.chmod(path, 0o755)


def main() -> None:
    """Set up the generated project."""
    print("Setting up project...")

    # Conditional cleanup
    if not USE_DOCKER:
        remove_path("Dockerfile")
        remove_path("docker-compose.yml")
        remove_path(".docker")

    if not USE_CI:
        remove_path(".github")
        remove_path(".gitlab-ci.yml")

    if LICENSE == "none":
        remove_path("LICENSE")

    # Make scripts executable
    for script in Path("scripts").glob("*.sh"):
        make_executable(str(script))

    # Initialize git (idempotent)
    if not Path(".git").exists():
        print("Initializing git repository...")
        run_command("git init")
        run_command("git add .")

    # Print success message
    print(f"""
Project '{PROJECT_NAME}' created successfully!

Next steps:
  cd {PROJECT_SLUG}
  uv sync
  uv run pytest
""")


if __name__ == "__main__":
    main()
```

## Idempotency

Hooks MUST be safe to run multiple times.

### Bad (Not Idempotent)

```python
# WRONG: Will fail if .git exists
subprocess.run(["git", "init"], check=True)

# WRONG: Will fail on second run
os.mkdir("build")
```

### Good (Idempotent)

```python
# RIGHT: Check before acting
if not Path(".git").exists():
    subprocess.run(["git", "init"])

# RIGHT: Use exist_ok
Path("build").mkdir(exist_ok=True)

# RIGHT: Use ignore_errors
shutil.rmtree("temp", ignore_errors=True)
```

## Error Handling

### Pre-Gen: Always Exit on Error

```python
# ALWAYS use sys.exit(1) to abort generation
if not valid:
    print("ERROR: Invalid input", file=sys.stderr)
    sys.exit(1)  # This aborts the entire generation
```

### Post-Gen: Warn but Continue

```python
# Soft failures - warn but don't abort
def run_optional(cmd: str) -> None:
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode != 0:
        print(f"Warning: {cmd} failed (non-critical)")
```

## Environment Access

Hooks have access to environment variables:

```python
import os

# User's environment
home = os.environ.get("HOME")
user = os.environ.get("USER")

# Cookiecutter sets these
# COOKIECUTTER_REPO_DIR - template directory
# COOKIECUTTER_OUTPUT_DIR - output directory
```

## Cross-Platform Considerations

```python
import platform
import subprocess

# Check platform
IS_WINDOWS = platform.system() == "Windows"

# Use platform-appropriate commands
if IS_WINDOWS:
    subprocess.run(["cmd", "/c", "script.bat"])
else:
    subprocess.run(["bash", "script.sh"])

# Use pathlib for cross-platform paths
from pathlib import Path
config = Path.home() / ".config" / "myapp"
```

## Hook Dependencies

Hooks can import standard library modules. For external dependencies:

```python
try:
    import requests
except ImportError:
    print("Warning: 'requests' not installed, skipping API check")
    requests = None

if requests:
    # Use requests
    pass
```

Better approach: Keep hooks dependency-free, use subprocess for external tools.

## Testing Hooks

```python
# tests/test_hooks.py
import subprocess
import tempfile
from pathlib import Path

def test_pre_gen_validation():
    """Test pre-generation hook catches invalid input."""
    hook = Path("hooks/pre_gen_project.py").read_text()

    # Simulate invalid input
    test_hook = hook.replace(
        '{{ cookiecutter.project_slug }}',
        'INVALID-slug!'
    )

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(test_hook.encode())
        f.flush()

        result = subprocess.run(
            ["python", f.name],
            capture_output=True,
        )

        assert result.returncode == 1
        assert b"ERROR" in result.stderr
```
