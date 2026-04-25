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

</installation>

<script>

Use `scripts/generate_erd.py` for common diagram generation tasks.

</script>
