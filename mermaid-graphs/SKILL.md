---
name: mermaid-graphs
description: Create Mermaid diagrams (flowcharts, sequence, class, state, ER, gantt, pie, mindmap, etc.) and render visually. Use when creating diagrams, visualizing workflows, or documenting architecture. Triggers on "diagram", "flowchart", "visualize", "chart", "graph".
---

# Mermaid Graphs

Create diagrams from text using Mermaid syntax and present them visually.

## Quick Presentation Methods

### 1. Browser Preview (Fastest)
```bash
python3 scripts/preview.py diagram.mmd           # Opens mermaid.live
python3 scripts/preview.py diagram.mmd -m local  # Local HTML file
python3 scripts/preview.py diagram.mmd -m kroki  # Via kroki.io
```

### 2. Render to File
```bash
python3 scripts/render.py diagram.mmd -o output.png
python3 scripts/render.py diagram.mmd -o output.svg -t dark
python3 scripts/render.py diagram.mmd -o output.pdf
```
Requires: `npm install -g @mermaid-js/mermaid-cli`

### 3. Inline URL (No File Needed)
Generate and open URL directly:
```python
import base64, zlib, json, webbrowser
code = "graph TD\n  A-->B"
state = {"code": code, "mermaid": {"theme": "default"}, "autoSync": True}
encoded = base64.urlsafe_b64encode(zlib.compress(json.dumps(state).encode(), 9)).decode()
webbrowser.open(f"https://mermaid.live/edit#pako:{encoded}")
```

## Diagram Types & Syntax

### Flowchart
```mermaid
graph TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```
Directions: `TD` (top-down), `LR` (left-right), `BT`, `RL`
Shapes: `[rect]`, `(rounded)`, `{diamond}`, `([stadium])`, `[[subroutine]]`, `[(cylinder)]`, `((circle))`

### Sequence Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant D as Database
    U->>S: Request
    activate S
    S->>D: Query
    D-->>S: Result
    S-->>U: Response
    deactivate S
```
Arrows: `->>` (solid), `-->>` (dashed), `-x` (cross), `-)` (async)

### Class Diagram
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +fetch() void
    }
    Animal <|-- Dog
```
Relations: `<|--` (inheritance), `*--` (composition), `o--` (aggregation), `-->` (association), `..>` (dependency)

### State Diagram
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start
    Processing --> Done: complete
    Processing --> Error: fail
    Done --> [*]
    Error --> Idle: retry
```

### Entity Relationship
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
    USER {
        int id PK
        string email
        string name
    }
```
Cardinality: `||` (one), `o{` (zero+), `|{` (one+), `o|` (zero/one)

### Gantt Chart
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Task A :a1, 2024-01-01, 30d
    Task B :after a1, 20d
    section Phase 2
    Task C :2024-02-01, 15d
```

### Pie Chart
```mermaid
pie title Distribution
    "Category A" : 45
    "Category B" : 30
    "Category C" : 25
```

### Mindmap
```mermaid
mindmap
  root((Topic))
    Branch 1
      Leaf 1a
      Leaf 1b
    Branch 2
      Leaf 2a
```

### Timeline
```mermaid
timeline
    title Project History
    2020 : Founded
    2021 : Series A
    2022 : Launch v1.0
    2023 : 1M users
```

### Quadrant Chart
```mermaid
quadrantChart
    title Prioritization Matrix
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Do First
    quadrant-2 Schedule
    quadrant-3 Delegate
    quadrant-4 Eliminate
    Feature A: [0.8, 0.9]
    Feature B: [0.3, 0.7]
```

### Git Graph
```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
```

## Styling

### Inline Styles
```mermaid
graph LR
    A:::highlight --> B
    classDef highlight fill:#f9f,stroke:#333,stroke-width:2px
```

### Theme Options
- `default` - Standard colors
- `forest` - Green tones
- `dark` - Dark background
- `neutral` - Grayscale

## Workflow

1. Write diagram in `.mmd` file or inline
2. Preview quickly: `python3 scripts/preview.py file.mmd`
3. If needed, render to file: `python3 scripts/render.py file.mmd -o output.png`
