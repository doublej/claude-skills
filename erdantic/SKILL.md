---
name: erdantic
description: "Generate ERD diagrams from Python data models (Pydantic, dataclasses, attrs)"
---

# Erdantic

Generate entity relationship diagrams from Python data model classes using Graphviz.

<supported_frameworks>

- Pydantic V2 / V1
- Python dataclasses
- attrs
- msgspec

</supported_frameworks>

<quick_start>

### CLI

```bash
erdantic path.to.module.ModelClass -o diagram.png
```

### Python

```python
import erdantic as erd

# One-liner
erd.draw(MyModel, out="diagram.png")

# Or inspect first
diagram = erd.create(MyModel)
diagram.draw("diagram.png")
```

<output_formats>

## Output Formats

Extension determines format: `.png`, `.svg`, `.pdf`, `.dot`

</output_formats>

<customization>

Pass Graphviz attributes to customize appearance:

```python
diagram.draw(
    "diagram.png",
    graph_attr={"nodesep": "0.5", "ranksep": "1.0", "fontsize": "12"},
    node_attr={"fontname": "Arial"},
    edge_attr={"color": "gray"}
)
```

</customization>

<api_reference>

### Main Functions

- `erd.create(model, ...)` - Create diagram object
- `erd.draw(model, out, ...)` - Render directly to file

### EntityRelationshipDiagram

```python
diagram = erd.create(MyModel)
diagram.models       # Dict of ModelInfo objects
diagram.edges        # Dict of Edge objects
diagram.to_dot()     # Get DOT source
diagram.draw(path)   # Render to file
```

### Edge Relationships

</api_reference>

<edge_relationships>

Uses crow's foot notation:
- **Cardinality**: ONE or MANY (max associations)
- **Modality**: ZERO or ONE (min associations / optional)

</edge_relationships>

<installation>

Requires Graphviz system library.

```bash
# Conda (recommended)
conda install erdantic -c conda-forge

# Pip (install Graphviz first)
pip install erdantic
```

**macOS Homebrew troubleshooting** — if `pip install erdantic` fails with a missing `graphviz/cgraph.h` header, set the Homebrew include/lib paths first:

```bash
CFLAGS="-I$(brew --prefix graphviz)/include" \
LDFLAGS="-L$(brew --prefix graphviz)/lib" \
pip install erdantic
```

</installation>

<project_usage>

### Ephemeral install (no pyproject.toml change)

Run erdantic without adding it as a permanent dependency:

```bash
PYTHONPATH="$PWD" uv run --with erdantic python scripts/generate_erd.py my.module.Model -o out.png
```

`PYTHONPATH=$PWD` is required when running generator scripts from a subdirectory so the project's own packages stay importable (otherwise `sys.path[0]` points at the script directory, not the project root).

</project_usage>

<script>

Use `scripts/generate_erd.py` for common diagram generation tasks.

```bash
# Basic usage
PYTHONPATH="$PWD" uv run --with erdantic python scripts/generate_erd.py \
    myapp.models.User -o diagram.png

# With layout tuning
PYTHONPATH="$PWD" uv run --with erdantic python scripts/generate_erd.py \
    myapp.models.User -o diagram.svg \
    --nodesep 0.5 --ranksep 1.2 --fontsize 11
```

Arguments:
- `model` — dotted path to model class (e.g. `myapp.models.User`)
- `-o / --output` — output file; extension sets format (`.png`, `.svg`, `.pdf`, `.dot`)
- `--nodesep` — vertical node spacing (float)
- `--ranksep` — horizontal rank spacing (float)
- `--fontsize` — label font size (int)

</script>
