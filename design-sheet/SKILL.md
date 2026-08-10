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

Creates a high-density summary of a design system. This format is designed to be
ingested by agents (like Claude Code) or used as a source of truth for frontend
implementation.

## Workflow

1. **Analyze Input:** Identify existing color tokens, font families, spacing
   scales, and container logic from the provided code or description.
2. **Apply Template:** Use `assets/template.md` as the structure.
3. **Populate Tokens:**
   - **Typography:** Map specific roles (Display, Body, Mono) to font families
     and define the px scale.
   - **Color:** List the primary functional tokens (bg, surface, text, accent,
     border).
   - **Spacing:** Identify the base unit (usually 4px or 8px) and the scale.
   - **Containers:** Define max-widths, border radius, and border weights.
   - **Atmosphere:** Describe shadows, textures, and backdrop effects.
4. **Define Motif:** Distill the visual identity into one "Signature Motif"
   sentence that governs all other decisions.

## Output Format

Always deliver the Design Sheet as a single Markdown block. If the system
has multiple themes (e.g., Light/Dark), provide two color tables.

## Example

```markdown
# Design Sheet: Project Obsidian

## 1. Typography
- **Display:** "Geist Sans", 700/900, [48, 64, 96]px
- **Body:** "Geist Sans", 400/500, [16, 18]px
- **Mono:** "Geist Mono", 400, [14, 15]px

## 2. Color (Dark Theme)
- `bg-primary`: #000000
- `bg-surface`: #111111
- `text-base`: #EDEDED
- `text-muted`: #A0A0A0
- `accent`: #FFFFFF
- `border`: #333333

... [rest of sections] ...
```
