# Testing and Validation

Comprehensive testing strategies for cookiecutter templates.

## Test Levels

1. **Template Tests** - Does the template generate correctly?
2. **Output Tests** - Is the generated output valid?
3. **Runtime Tests** - Does the generated project work?

## Directory Structure

```
cookiecutter-my-template/
├── cookiecutter.json
├── hooks/
├── {{ cookiecutter.project_slug }}/
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── test_generation.py   # Template generation tests
│   ├── test_output.py       # Output validation tests
│   └── test_runtime.py      # Runtime tests
├── pyproject.toml
└── tox.ini                   # Multi-environment testing
```

## Fixtures

```python
# tests/conftest.py
import tempfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

TEMPLATE_DIR = Path(__file__).parent.parent


@pytest.fixture
def default_context():
    """Default context for template generation."""
    return {
        "project_name": "Test Project",
        "project_slug": "test-project",
        "package_name": "test_project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.12",
        "use_docker": "no",
        "license": "MIT",
    }


@pytest.fixture
def generated_project(default_context):
    """Generate project with default settings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = cookiecutter(
            str(TEMPLATE_DIR),
            output_dir=tmpdir,
            no_input=True,
            extra_context=default_context,
        )
        yield Path(result)


@pytest.fixture
def generated_project_docker(default_context):
    """Generate project with Docker enabled."""
    default_context["use_docker"] = "yes"
    with tempfile.TemporaryDirectory() as tmpdir:
        result = cookiecutter(
            str(TEMPLATE_DIR),
            output_dir=tmpdir,
            no_input=True,
            extra_context=default_context,
        )
        yield Path(result)
```

## Generation Tests

```python
# tests/test_generation.py
import pytest
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import FailedHookException


def test_default_generation(generated_project):
    """Template generates with default values."""
    assert generated_project.exists()
    assert generated_project.is_dir()


def test_all_options():
    """Template generates with all option combinations."""
    options = {
        "use_docker": ["yes", "no"],
        "license": ["MIT", "Apache-2.0", "none"],
        "python_version": ["3.10", "3.11", "3.12"],
    }

    for docker in options["use_docker"]:
        for license_ in options["license"]:
            for python in options["python_version"]:
                with tempfile.TemporaryDirectory() as tmpdir:
                    result = cookiecutter(
                        str(TEMPLATE_DIR),
                        output_dir=tmpdir,
                        no_input=True,
                        extra_context={
                            "project_name": "Test",
                            "use_docker": docker,
                            "license": license_,
                            "python_version": python,
                        },
                    )
                    assert Path(result).exists()


def test_invalid_slug_fails(default_context):
    """Invalid project_slug fails validation."""
    default_context["project_slug"] = "INVALID-SLUG!"

    with pytest.raises(FailedHookException):
        with tempfile.TemporaryDirectory() as tmpdir:
            cookiecutter(
                str(TEMPLATE_DIR),
                output_dir=tmpdir,
                no_input=True,
                extra_context=default_context,
            )


def test_reserved_keyword_fails(default_context):
    """Python keyword as package name fails."""
    default_context["package_name"] = "class"

    with pytest.raises(FailedHookException):
        with tempfile.TemporaryDirectory() as tmpdir:
            cookiecutter(
                str(TEMPLATE_DIR),
                output_dir=tmpdir,
                no_input=True,
                extra_context=default_context,
            )
```

## Output Validation Tests

```python
# tests/test_output.py
import tomllib
from pathlib import Path


def test_required_files(generated_project):
    """All required files are generated."""
    required = [
        "README.md",
        "pyproject.toml",
        ".gitignore",
        ".claude/CLAUDE.md",
    ]

    for file in required:
        assert (generated_project / file).exists(), f"Missing: {file}"


def test_package_structure(generated_project):
    """Package has correct structure."""
    pkg = generated_project / "test_project"

    assert pkg.is_dir()
    assert (pkg / "__init__.py").exists()
    assert (pkg / "main.py").exists()


def test_no_template_variables(generated_project):
    """No unrendered template variables in output."""
    patterns = ["{{", "}}", "{%", "%}"]

    for path in generated_project.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".md", ".toml", ".yaml", ".yml"}:
            content = path.read_text()

            for pattern in patterns:
                # Allow raw blocks in templates that need Jinja at runtime
                if pattern in content and "{% raw %}" not in content:
                    assert False, f"Unrendered '{pattern}' in {path}"


def test_pyproject_valid(generated_project):
    """pyproject.toml is valid TOML."""
    pyproject = generated_project / "pyproject.toml"
    content = pyproject.read_text()

    # Should parse without error
    data = tomllib.loads(content)

    # Required sections
    assert "project" in data
    assert "name" in data["project"]
    assert "version" in data["project"]


def test_docker_conditional(generated_project, generated_project_docker):
    """Docker files only present when enabled."""
    # Without Docker
    assert not (generated_project / "Dockerfile").exists()
    assert not (generated_project / "docker-compose.yml").exists()

    # With Docker
    assert (generated_project_docker / "Dockerfile").exists()
    assert (generated_project_docker / "docker-compose.yml").exists()


def test_license_conditional(generated_project):
    """LICENSE file present unless 'none' selected."""
    assert (generated_project / "LICENSE").exists()


def test_no_license(default_context):
    """No LICENSE file when license is 'none'."""
    default_context["license"] = "none"

    with tempfile.TemporaryDirectory() as tmpdir:
        result = cookiecutter(
            str(TEMPLATE_DIR),
            output_dir=tmpdir,
            no_input=True,
            extra_context=default_context,
        )

        assert not (Path(result) / "LICENSE").exists()
```

## Runtime Tests

```python
# tests/test_runtime.py
import subprocess
from pathlib import Path


def test_uv_sync(generated_project):
    """Generated project installs with uv."""
    result = subprocess.run(
        ["uv", "sync"],
        cwd=generated_project,
        capture_output=True,
        timeout=120,
    )

    assert result.returncode == 0, f"uv sync failed: {result.stderr.decode()}"


def test_pytest_passes(generated_project):
    """Generated project tests pass."""
    # First install
    subprocess.run(["uv", "sync"], cwd=generated_project, capture_output=True)

    # Then test
    result = subprocess.run(
        ["uv", "run", "pytest"],
        cwd=generated_project,
        capture_output=True,
        timeout=60,
    )

    assert result.returncode == 0, f"pytest failed: {result.stderr.decode()}"


def test_ruff_passes(generated_project):
    """Generated project passes linting."""
    subprocess.run(["uv", "sync"], cwd=generated_project, capture_output=True)

    result = subprocess.run(
        ["uv", "run", "ruff", "check", "."],
        cwd=generated_project,
        capture_output=True,
    )

    assert result.returncode == 0, f"ruff check failed: {result.stdout.decode()}"


def test_type_check_passes(generated_project):
    """Generated project passes type checking."""
    subprocess.run(["uv", "sync"], cwd=generated_project, capture_output=True)

    result = subprocess.run(
        ["uv", "run", "mypy", "."],
        cwd=generated_project,
        capture_output=True,
    )

    assert result.returncode == 0, f"mypy failed: {result.stdout.decode()}"


def test_docker_builds(generated_project_docker):
    """Dockerfile builds successfully."""
    result = subprocess.run(
        ["docker", "build", "-t", "test-image", "."],
        cwd=generated_project_docker,
        capture_output=True,
        timeout=300,
    )

    assert result.returncode == 0, f"Docker build failed: {result.stderr.decode()}"

    # Cleanup
    subprocess.run(["docker", "rmi", "test-image"], capture_output=True)
```

## CI Configuration

```yaml
# .github/workflows/test.yml
name: Test Template

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests
        run: uv run pytest tests/ -v

      - name: Test generation
        run: |
          uv run cookiecutter . --no-input -o /tmp/test
          cd /tmp/test/*
          uv sync
          uv run pytest
```

## Manual Testing Checklist

```bash
# 1. Clean test
rm -rf /tmp/test-output
cookiecutter . --no-input -o /tmp/test-output
cd /tmp/test-output/*

# 2. Verify structure
tree -a

# 3. Check for template artifacts
grep -r "{{" . --include="*.py" --include="*.md" --include="*.toml"
grep -r "{%" . --include="*.py" --include="*.md" --include="*.toml"

# 4. Install and test
uv sync
uv run pytest
uv run ruff check .
uv run mypy .

# 5. Build (if applicable)
uv build

# 6. Docker (if enabled)
docker build -t test .
docker run --rm test

# 7. Verify CLAUDE.md
cat .claude/CLAUDE.md
```
