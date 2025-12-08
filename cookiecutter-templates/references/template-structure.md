# Template Structure Guide

Complete reference for organizing cookiecutter templates.

## Minimal Structure

```
my-template/
├── cookiecutter.json
└── {{ cookiecutter.project_slug }}/
    └── README.md
```

## Production Structure

```
cookiecutter-project-name/
├── cookiecutter.json                    # Variable definitions
├── README.md                            # Template documentation
├── LICENSE                              # Template license
├── hooks/
│   ├── pre_gen_project.py              # Input validation
│   └── post_gen_project.py             # Post-generation setup
├── tests/
│   ├── conftest.py                     # Pytest fixtures
│   └── test_template.py                # Template tests
└── {{ cookiecutter.project_slug }}/    # Generated project root
    ├── {{ cookiecutter.package_name }}/
    │   ├── __init__.py
    │   ├── main.py
    │   └── py.typed                    # PEP 561 marker
    ├── tests/
    │   ├── conftest.py
    │   └── test_main.py
    ├── scripts/
    │   ├── dev.sh
    │   └── test.sh
    ├── .claude/
    │   └── CLAUDE.md
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    ├── .gitignore
    ├── .python-version
    ├── pyproject.toml
    ├── README.md
    └── LICENSE
```

## Directory Naming Rules

### Valid Characters

Template directory names can only contain:
- Lowercase letters: `a-z`
- Numbers: `0-9`
- Underscores: `_`
- Hyphens: `-`
- Cookiecutter variables: `{{ cookiecutter.var }}`

### Windows Compatibility

Avoid these characters in any path:
- `< > : " / \ | ? *`
- Trailing spaces or dots

### Examples

```
# Good
{{ cookiecutter.project_slug }}/
{{ cookiecutter.package_name }}/
src/{{ cookiecutter.package_name }}/

# Bad - spaces
{{ cookiecutter.project name }}/

# Bad - special chars
{{ cookiecutter.project-name }}/tests/  # hyphen in package name
```

## Conditional Files

Use `_copy_without_render` in `cookiecutter.json`:

```json
{
    "_copy_without_render": [
        "*.html",
        "static/**/*",
        "*.min.js"
    ]
}
```

## Conditional Directories

Handle in `post_gen_project.py`:

```python
import shutil

USE_DOCKER = "{{ cookiecutter.use_docker }}" == "yes"
USE_CI = "{{ cookiecutter.use_ci }}" == "yes"

if not USE_DOCKER:
    shutil.rmtree("docker", ignore_errors=True)

if not USE_CI:
    shutil.rmtree(".github", ignore_errors=True)
```

## File Organization by Type

### Python Projects

```
{{ cookiecutter.project_slug }}/
├── src/
│   └── {{ cookiecutter.package_name }}/
│       ├── __init__.py
│       └── main.py
├── tests/
├── docs/
└── pyproject.toml
```

### CLI Applications

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.package_name }}/
│   ├── __init__.py
│   ├── cli.py
│   └── commands/
└── pyproject.toml (with [project.scripts])
```

### Web Applications

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.package_name }}/
│   ├── __init__.py
│   ├── app.py
│   ├── routes/
│   ├── models/
│   └── templates/
├── static/
└── pyproject.toml
```

## Multi-Package Templates

For monorepos:

```
{{ cookiecutter.project_slug }}/
├── packages/
│   ├── {{ cookiecutter.package_name }}-core/
│   └── {{ cookiecutter.package_name }}-cli/
├── shared/
└── pyproject.toml
```
