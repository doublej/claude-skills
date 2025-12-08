---
name: opentui
description: Build terminal user interfaces (TUIs) with OpenTUI. Use when creating CLI applications with interactive components, forms, text displays, or custom graphics in TypeScript.
---

# OpenTUI Skill

Build terminal user interfaces with OpenTUI's component-based architecture.

## When to Use

- Creating interactive CLI applications
- Building terminal dashboards or forms
- Rendering styled text with colors and attributes
- Custom graphics with FrameBuffer
- Selection lists, tabs, text inputs

## Installation

```bash
bun install @opentui/core
```

**Requirement:** Zig must be installed to build native bindings.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Renderer** | Central orchestrator (`CliRenderer`) managing output, input events, and render loop |
| **Renderables** | Visual elements (text, boxes, inputs) with Yoga layout positioning |
| **Constructs** | Declarative component builders returning VNodes (like React components) |
| **FrameBuffer** | Low-level 2D cell array for custom graphics with alpha blending |

## Available Components

| Component | Purpose |
|-----------|---------|
| `TextRenderable` | Styled text with colors, bold, underline |
| `Box` | Container with borders, backgrounds, layout |
| `Input` | Text input field with cursor, placeholder |
| `Select` | Vertical list selection |
| `TabSelect` | Horizontal tab navigation |
| `ASCIIFont` | ASCII art text rendering |
| `FrameBuffer` | Custom graphics surface |
| `GroupRenderable` | Flex-based layout container |

## Quick Start

```typescript
import { createCliRenderer, TextRenderable, Box, t, bold, fg, underline } from "@opentui/core"

const renderer = await createCliRenderer()

// Simple text
const greeting = new TextRenderable(renderer, {
  id: "greeting",
  content: "Hello, OpenTUI!",
  fg: "#00FF00",
  position: "absolute",
  left: 10,
  top: 5,
})

// Styled text with template literals
const styled = new TextRenderable(renderer, {
  content: t`${bold("Important")} ${fg("#FF0000")(underline("Message"))}`,
  position: "absolute",
  left: 5,
  top: 3,
})

// Box container
const panel = new Box(renderer, {
  id: "panel",
  title: "Settings",
  border: "single",
  width: 40,
  height: 10,
  bg: "#1a1a2e",
})

renderer.root.add(greeting)
renderer.root.add(panel)
renderer.start()
```

## Keyboard Input

```typescript
renderer.keyInput.on("keypress", (key) => {
  if (key.name === "escape") renderer.stop()
  if (key.ctrl && key.name === "c") process.exit(0)
})
```

## Reference Files

See `references/` for:
- `components.md` - Detailed component API
- `patterns.md` - Common patterns and examples
