# Claude Code Integration

Making cookiecutter templates work seamlessly with Claude Code agents.

## Why Claude Code Integration Matters

Claude Code agents work best with projects that:

1. Have clear, documented structure
2. Use standard, well-known tools
3. Provide explicit instructions
4. Follow predictable conventions
5. Fail loudly with clear messages

## CLAUDE.md in Templates

Every generated project should include `.claude/CLAUDE.md`:

```markdown
# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Quick Commands

```bash
uv sync              # Install dependencies
uv run pytest        # Run tests
uv run ruff check .  # Lint
uv run ruff format . # Format
uv run mypy .        # Type check
```

## Project Structure

```
{{ cookiecutter.package_name }}/     # Main package
├── __init__.py
├── main.py                          # Entry point
└── ...
tests/                               # Tests mirror package structure
scripts/                             # Utility scripts
```

## Conventions

- Use `uv` for all Python operations (never pip)
- Tests use pytest with fixtures in conftest.py
- Type hints required for all public functions
- Ruff for linting and formatting

## Architecture Decisions

<!-- Document key decisions here -->

## Common Tasks

### Adding a dependency
```bash
uv add package-name
```

### Running a specific test
```bash
uv run pytest tests/test_specific.py -v
```

### Building the package
```bash
uv build
```
```

## Tool Standardization

Use well-known, standard tools that Claude understands:

### Recommended Stack

| Category | Tool | Why |
|----------|------|-----|
| Package Manager | `uv` | Fast, reliable, well-documented |
| Testing | `pytest` | Standard, extensive ecosystem |
| Linting | `ruff` | Fast, comprehensive, good defaults |
| Type Checking | `mypy` | Standard, well-understood |
| Formatting | `ruff format` | Consistent with linting |
| Task Running | `uv run` | No extra config needed |

### Avoid

| Category | Avoid | Problem |
|----------|-------|---------|
| Package Manager | pip, poetry, pipenv | Less predictable, slower |
| Task Running | make, invoke, just | Extra config to understand |
| Testing | unittest | More verbose, less intuitive |
| Multiple tools | black + isort + flake8 | Ruff does all three |

## pyproject.toml Structure

Template for Claude-friendly configuration:

```toml
[project]
name = "{{ cookiecutter.package_name }}"
version = "0.1.0"
description = "{{ cookiecutter.description }}"
readme = "README.md"
requires-python = ">={{ cookiecutter.python_version }}"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
    "mypy>=1.13",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
target-version = "py{{ cookiecutter.python_version.replace('.', '') }}"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "{{ cookiecutter.python_version }}"
strict = true
```

## Clear Error Messages

Templates should generate projects that fail loudly:

```python
# Good: Clear error
def load_config(path: str) -> dict:
    if not Path(path).exists():
        raise FileNotFoundError(f"Config not found: {path}")
    return json.loads(Path(path).read_text())

# Bad: Silent failure
def load_config(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text())
    except:
        return {}
```

## Predictable Structure

Use feature-based organization:

```
{{ cookiecutter.package_name }}/
├── __init__.py
├── main.py           # Entry point
├── config.py         # Configuration
├── models/           # Data models
│   └── __init__.py
├── services/         # Business logic
│   └── __init__.py
└── utils/            # Utilities
    └── __init__.py
```

Not layer-based:

```
# Avoid: Harder to navigate
{{ cookiecutter.package_name }}/
├── controllers/
├── models/
├── views/
├── helpers/
└── managers/
```

## Explicit Imports

Use absolute imports:

```python
# Good: Explicit
from {{ cookiecutter.package_name }}.models.user import User
from {{ cookiecutter.package_name }}.services.auth import authenticate

# Avoid: Relative imports can confuse
from ..models.user import User
from .auth import authenticate
```

## Entry Points

Define clear entry points:

```toml
# pyproject.toml
[project.scripts]
{{ cookiecutter.package_name }} = "{{ cookiecutter.package_name }}.main:main"

[project.entry-points."{{ cookiecutter.package_name }}.plugins"]
# Plugin entry points if needed
```

## Environment Configuration

Use standard environment variable handling:

```python
# {{ cookiecutter.package_name }}/config.py
import os
from pathlib import Path

# Clear defaults, environment override
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

Document in CLAUDE.md:

```markdown
## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DEBUG | false | Enable debug mode |
| DATABASE_URL | sqlite:///db.sqlite3 | Database connection |
| LOG_LEVEL | INFO | Logging level |
```

## Test Structure

Mirror source structure for easy navigation:

```
{{ cookiecutter.package_name }}/
├── models/
│   └── user.py
└── services/
    └── auth.py

tests/
├── models/
│   └── test_user.py
└── services/
    └── test_auth.py
```

## README Template

```markdown
# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Installation

```bash
uv sync
```

## Usage

```bash
uv run {{ cookiecutter.package_name }}
```

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy .
```

## License

{{ cookiecutter.license }}
```

## Checklist for Claude Code Compatibility

- [ ] `.claude/CLAUDE.md` with clear instructions
- [ ] Standard tools: `uv`, `pytest`, `ruff`, `mypy`
- [ ] All commands documented
- [ ] Predictable project structure
- [ ] Absolute imports
- [ ] Clear error messages
- [ ] Environment variables documented
- [ ] Tests mirror source structure
- [ ] pyproject.toml with all config
- [ ] No hidden magic or implicit behavior
