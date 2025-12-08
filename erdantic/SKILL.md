---
name: erdantic
description: Generate entity relationship diagrams (ERDs) from Python data model classes. Use when visualizing data models (Pydantic, dataclasses, attrs, msgspec), creating documentation diagrams, or understanding relationships between model classes. Triggers on requests like "create ERD", "visualize models", "diagram for dataclass", or "show relationships between classes".
---

# Erdantic

Generate entity relationship diagrams from Python data model classes using Graphviz.

## Supported Frameworks

- Pydantic V2 / V1
- Python dataclasses
- attrs
- msgspec

## Quick Start

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

## Customization

Pass Graphviz attributes to customize appearance:

```python
diagram.draw(
    "diagram.png",
    graph_attr={"nodesep": "0.5", "ranksep": "1.0", "fontsize": "12"},
    node_attr={"fontname": "Arial"},
    edge_attr={"color": "gray"}
)
```

## API Reference

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

Uses crow's foot notation:
- **Cardinality**: ONE or MANY (max associations)
- **Modality**: ZERO or ONE (min associations / optional)

## Installation

Requires Graphviz system library.

```bash
# Conda (recommended)
conda install erdantic -c conda-forge

# Pip (install Graphviz first)
pip install erdantic
```

## Script

Use `scripts/generate_erd.py` for common diagram generation tasks.
