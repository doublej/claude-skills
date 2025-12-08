# Jinja2 Patterns for Cookiecutter

Advanced Jinja2 techniques for robust templates.

## String Transformations

### Slugification

```jinja2
{# Input: "My Awesome Project" #}

{# To slug: my-awesome-project #}
{{ cookiecutter.project_name.lower().replace(' ', '-') }}

{# To Python identifier: my_awesome_project #}
{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}

{# To PascalCase: MyAwesomeProject #}
{{ cookiecutter.project_name.title().replace(' ', '').replace('-', '') }}

{# To CONSTANT_CASE: MY_AWESOME_PROJECT #}
{{ cookiecutter.project_name.upper().replace(' ', '_').replace('-', '_') }}
```

### Safe Identifier

```jinja2
{# Remove non-alphanumeric, ensure starts with letter #}
{% set safe = cookiecutter.name | regex_replace('[^a-zA-Z0-9_]', '') %}
{% if safe[0].isdigit() %}pkg_{{ safe }}{% else %}{{ safe }}{% endif %}
```

## Conditional Content

### If/Else in cookiecutter.json

```json
{
    "use_docker": ["no", "yes"],
    "_docker_image": "{% if cookiecutter.use_docker == 'yes' %}python:{{ cookiecutter.python_version }}-slim{% else %}{% endif %}"
}
```

### Inline Conditionals in Templates

```jinja2
# Short form
{{ "include Docker" if cookiecutter.use_docker == "yes" else "skip Docker" }}

# Multi-line
{% if cookiecutter.license != "none" %}
This project is licensed under {{ cookiecutter.license }}.
{% endif %}
```

### Boolean Patterns

Cookiecutter doesn't have native booleans. Use string comparison:

```json
{
    "use_feature": "no",
    "_use_feature_bool": "{{ 'true' if cookiecutter.use_feature == 'yes' else 'false' }}"
}
```

```jinja2
{% if cookiecutter._use_feature_bool == 'true' %}
feature_enabled = True
{% endif %}
```

## Escaping Jinja2 Syntax

### Raw Blocks

For files that use Jinja2/Django syntax at runtime:

```jinja2
{% raw %}
<!DOCTYPE html>
<html>
<body>
  {{ user.name }}
  {% for item in items %}
    <li>{{ item }}</li>
  {% endfor %}
</body>
</html>
{% endraw %}
```

### GitHub Actions

GitHub Actions use `${{ }}` syntax:

```yaml
# Option 1: Raw blocks
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        env:
          TOKEN: {% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}
```

```yaml
# Option 2: Escape braces
        env:
          TOKEN: ${% raw %}{{{% endraw %} secrets.GITHUB_TOKEN {% raw %}}}{% endraw %}
```

### Terraform

Terraform uses `${}` which doesn't conflict, but `%{ }` does:

```hcl
# No escaping needed for ${}
output = "${var.name}"

# Escape %{ } if needed
{% raw %}
%{ for item in items }
  ${item}
%{ endfor }
{% endraw %}
```

## Loops

### List Generation

```jinja2
{# In pyproject.toml #}
classifiers = [
{% for version in cookiecutter.python_versions.split(',') %}
    "Programming Language :: Python :: {{ version.strip() }}",
{% endfor %}
]
```

### Conditional Iteration

```jinja2
dependencies = [
    "click>=8.0",
{% if cookiecutter.use_async == "yes" %}
    "httpx>=0.24",
    "anyio>=3.0",
{% endif %}
]
```

## Extensions

### Time Extension

```json
{
    "_extensions": ["jinja2_time.TimeExtension"],
    "year": "{% now 'utc', '%Y' %}"
}
```

Usage:
```jinja2
Copyright {% now 'utc', '%Y' %} {{ cookiecutter.author_name }}
```

### UUID Extension

```json
{
    "_extensions": ["cookiecutter.extensions.RandomStringExtension"],
    "secret_key": "{{ random_ascii_string(64) }}"
}
```

## Private Variables

Variables starting with `_` are not prompted:

```json
{
    "project_name": "My Project",
    "_project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
    "_package_name": "{{ cookiecutter._project_slug.replace('-', '_') }}",
    "_copy_without_render": ["*.min.js", "static/**"],
    "_extensions": ["jinja2_time.TimeExtension"]
}
```

## Filters

### Built-in Filters

```jinja2
{{ cookiecutter.name | lower }}
{{ cookiecutter.name | upper }}
{{ cookiecutter.name | title }}
{{ cookiecutter.name | capitalize }}
{{ cookiecutter.name | trim }}
{{ cookiecutter.description | truncate(100) }}
{{ cookiecutter.items | join(', ') }}
{{ cookiecutter.value | default('fallback') }}
```

### Custom Filters

In `hooks/pre_gen_project.py`, you can't add filters. Instead, compute values in `cookiecutter.json`:

```json
{
    "name": "my-project",
    "_name_upper": "{{ cookiecutter.name.upper() }}"
}
```

## Common Patterns

### Version Pinning

```json
{
    "python_version": ["3.12", "3.11", "3.10"],
    "_python_version_tuple": "{{ cookiecutter.python_version.replace('.', ', ') }}"
}
```

```python
# pyproject.toml
requires-python = ">={{ cookiecutter.python_version }}"
```

### Optional Dependencies

```jinja2
dependencies = [
    "click>=8.0",
{% if cookiecutter.use_database == "postgres" %}
    "psycopg[binary]>=3.0",
{% elif cookiecutter.use_database == "sqlite" %}
    # sqlite3 is built-in
{% endif %}
]
```

### Multi-Choice Handling

```json
{
    "database": ["none", "sqlite", "postgres", "mysql"]
}
```

```jinja2
{% if cookiecutter.database != "none" %}
DATABASE_URL = "{{ cookiecutter.database }}://..."
{% endif %}
```
