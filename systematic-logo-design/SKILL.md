---
name: systematic-logo-design
description: Design logos using a constrained grid system. Instead of free-form SVG, define logos as JSON grid maps (3x3 to 9x9) that force geometric alignment. Use when user needs a logo, icon, wordmark, monogram, or brand mark. Triggers on "create logo", "design logo", "make icon", "brand identity", "logomark", "grid logo".
---

# Systematic Logo Design

Constraint liberates. Think in cells, not coordinates.

Free-form SVG produces random, misaligned results. This skill forces every mark onto a discrete grid — 3x3 to 9x9 cells — so every shape is intentional, every alignment is structural, every logo is geometric by default.

## Pre-Flight: Logo Brief

Before ANY design work, produce this brief:

```
LOGO BRIEF
Brand: [name]
Essence: [one word — what feeling does this brand evoke?]
Grid: [3-9, default 5]
Type: [logomark | lettermark | combination | abstract]
Signature Element: [the ONE thing that makes this memorable]
Palette: [max 3 colours as hex]
Aesthetic Thesis: [one sentence — the WHY behind your visual direction]
```

The aesthetic thesis is your conviction. It drives every cell placement. "Modern and clean" is not a thesis. "Brutalist geometry that refuses decoration" is.

## The Grid System

### Grid Sizes

| Grid | Character | Best For |
|------|-----------|----------|
| 3x3 | Ultra-bold, iconic | Favicons, app icons, marks that must read at 16px |
| 4x4 | Bold, structural | Strong geometric marks, letterforms |
| 5x5 | Balanced (default) | Most logos — enough detail, still simple |
| 6x6 | Detailed | Complex lettermarks, multi-element marks |
| 7x7 | Fine | Intricate geometric patterns, detailed icons |
| 8x8–9x9 | Precise | Pixel-art-adjacent marks, detailed emblems |

### JSON Schema

```json
{
  "brand": "Acme",
  "grid": 5,
  "palette": { "a": "#1a1a1a", "b": "#0066ff" },
  "cells": [
    { "r": 0, "c": 1, "w": 3, "h": 1, "color": "a" },
    { "r": 2, "c": 2, "shape": "circle", "color": "b" }
  ],
  "text": { "content": "ACME", "position": "right", "color": "a" }
}
```

Fields:
- `brand` — brand name (used in SVG `<title>`)
- `grid` — grid size, 3–9 (default 5)
- `palette` — colour map, max 3 entries + transparent. Single-letter keys.
- `cells` — array of cell definitions
- `text` — optional, text element positioned outside the grid

### Cell Properties

| Property | Required | Default | Description |
|----------|----------|---------|-------------|
| `r` | yes | — | Row (0-indexed from top) |
| `c` | yes | — | Column (0-indexed from left) |
| `w` | no | 1 | Column span |
| `h` | no | 1 | Row span |
| `shape` | no | rect | Shape type |
| `color` | yes | — | Palette key |

### Shapes (7 total)

| Shape | Description |
|-------|-------------|
| `rect` | Rectangle filling the cell (default) |
| `circle` | Circle inscribed in the cell |
| `triangle-up` | Triangle pointing up |
| `triangle-down` | Triangle pointing down |
| `triangle-left` | Triangle pointing left |
| `triangle-right` | Triangle pointing right |
| `diamond` | Diamond (rotated square) inscribed in cell |

### Palette Rules

- Maximum 3 colours + transparent
- Use single-letter keys: `a`, `b`, `c`
- Hex values only, no named colours
- One colour should dominate (60%+), one accent (10-30%), one optional detail

## Design Rules

### Banned Elements

These signal lazy design — never place them on the grid:
- Swooshes, swoops, curves that "suggest motion"
- Generic globes, puzzle pieces, light bulbs
- Handshake icons, generic people silhouettes
- Laurel wreaths (unless actually classical)
- Arrows pointing up/right (for "growth")
- Infinity symbols, generic gears

### Simplicity Test

Every logo must pass: **would it still read if reduced to 3x3?** If not, simplify. A 5x5 logo that needs all 25 cells is probably overdesigned.

### Banned Words

Never use these in briefs or descriptions — they signal slop:
- "Sleek", "synergy", "innovative", "cutting-edge"
- "Elevate", "leverage", "holistic", "dynamic"
- "Premium feel", "modern aesthetic", "clean lines"

Say what you actually mean instead.

### Colour Strategy

| Approach | When | Palette |
|----------|------|---------|
| Monochrome | Maximum impact, serious brands | 1 colour + background |
| Duotone | Most logos, balanced presence | 2 colours |
| Triadic | Bold, playful, high energy | 3 colours (use sparingly) |

## Text Handling

Text is NOT grid-constrained. Forcing text into cells produces pixel art, not typography.

### Text Properties

| Property | Required | Default | Description |
|----------|----------|---------|-------------|
| `content` | yes | — | The text string |
| `position` | no | right | `right`, `below`, `above`, `center` |
| `color` | yes | — | Palette key |
| `size` | no | 0.6 | Size ratio relative to grid |
| `font` | no | sans-serif | Font family |
| `weight` | no | bold | Font weight |

### Restricted Fonts

Only use these — they render reliably across systems:
- `sans-serif` (system default)
- `serif` (system default)
- `monospace` (system default)
- `Arial, Helvetica, sans-serif`
- `Georgia, serif`

Do not specify custom web fonts. Logos must render without external dependencies.

## Workflow

### 1. Brief
Establish brand essence, grid size, type, palette, and aesthetic thesis.

### 2. ASCII Preview
Sketch the grid using palette letters before writing JSON. This forces spatial thinking.

```
ASCII PREVIEW (5x5, palette: a=#1a1a1a, b=#0066ff)
. a a a .
. . a . .
b . a . b
b b a b b
. b b b .
```

- Use `.` for empty cells
- Use palette letters for filled cells
- Think about negative space — the dots matter as much as the letters

### 3. JSON Grid
Convert the ASCII preview to the JSON grid format. Every filled cell becomes an entry.

### 4. Convert
Run the converter:
```bash
python3 systematic-logo-design/scripts/grid_to_svg.py input.json output.svg
```

### 5. Variants
Generate minimum two variants:
- **Primary** — full logo (mark + text if combination)
- **Icon** — mark only, square format

Optional:
- **Monochrome** — single colour version
- **Reversed** — for dark backgrounds

### 6. Verify
Run the quality checklist before delivery.

## Quality Checklist

Before delivery:
- [ ] Works at 16px (favicon) — test 3x3 reduction
- [ ] Works at 512px (hero)
- [ ] Readable in monochrome (swap all colours to single)
- [ ] Grid cells are within bounds
- [ ] Palette has max 3 colours
- [ ] viewBox is correct
- [ ] `<title>` element present
- [ ] Colours are hex, not named
- [ ] No external font dependencies
- [ ] ASCII preview matches final JSON

## Output

Deliver:
1. Logo brief (the thinking)
2. ASCII preview (the spatial reasoning)
3. JSON grid definition
4. SVG code (primary version)
5. Icon variant SVG
6. Usage notes (2-3 lines max)
