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
