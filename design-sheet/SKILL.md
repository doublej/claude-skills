---
name: design-sheet
description: >
  Generates a compact, one-page "Design Sheet" that defines a system's colors,
  typography, spacing, borders, backgrounds, and containers. Use when you need
  to extract a design system from code, summarize a visual direction, or
  prepare a handoff for Claude Code. Triggers on "make a design sheet",
  "summarize design system", "extract tokens", "handoff bundle".
---

# Design Sheet

High-density, one-page summary of a design system, made to be ingested by
agents (like Claude Code) or used as the source of truth for frontend work.

<workflow>
1. Extract from the input (code or description): color tokens, font families
   and roles, spacing scale + base unit, container/border logic, effects.
2. Fill every section of `assets/template.md`, keeping its table formats.
3. Distill one **Signature Motif** sentence — the visual hook that governs
   all other decisions.
4. Build the Midjourney baseprompt as
   `[subject], [details], [environment], [mood], [technical] --ar --v`.
</workflow>

<rules>
- Deliver the sheet as a single Markdown block.
- Multiple themes (light/dark) → one color table per theme.
- Value missing from the source → infer from context and mark `(inferred)`;
  never leave template placeholders in the output.
- Specifics over prose: exact hex, px, weights — no "roughly" or ranges
  unless the source itself is a range.
</rules>

<example>
```markdown
# Design Sheet: Project Obsidian

## 1. Typography (The Monarchy)
| Role | Family | Weights | Scale (px) | Tracking |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | Geist Sans | 700, 900 | 48, 64, 96 | -0.03em |
| **Body** | Geist Sans | 400, 500 | 16, 18 | 0 |
| **Mono** | Geist Mono | 400 | 14, 15 | 0 |

## 2. Color (Dark Theme)
| Token | Hex/Value | Intent |
| :--- | :--- | :--- |
| `bg-primary` | #000000 | Base background |
| `bg-surface` | #111111 | Card/Container background |
| `text-base` | #EDEDED | Primary readability |
| `text-muted` | #A0A0A0 | Supporting info |
| `accent` | #FFFFFF | The hook |
| `border` | #333333 | Separation |

## 3. Spacing & Rhythm
- **Base Unit:** 4px
- **Scale:** 4, 8, 16, 24, 40, 64, 96
- **Gutter:** 24px (Desktop) / 16px (Mobile)

## 4. Containers & Borders
- **Radius:** None
- **Border Width:** 1px (Standard)
- **Container Max-Width:** 1100px

## 5. Atmosphere & Effects
- **Shadows:** None (inferred)
- **Texture:** Grain, 3% opacity
- **Backdrop:** Solid

## 6. Signature Motif
- Pure-black void where white is spent only on the one thing that matters;
  hierarchy is done with weight and space, never with color.

## 7. Midjourney Baseprompt
`minimal dashboard interface, stark white text on pure black, thin 1px hairline
borders, monospaced data readouts, brutalist restraint, studio product shot,
high contrast --ar 16:9 --v 8.2`
```
</example>
