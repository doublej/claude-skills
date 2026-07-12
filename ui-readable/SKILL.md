---
name: ui-readable
description: "Typography, spacing, contrast, and type tokens for readable interfaces — ships assets/tokens.css, a contrast-safe type/spacing scale with semantic role classes. Use when setting or reviewing text size, hierarchy, line height, measure, density, or spacing rhythm; for heuristic/form/flow review use ui-usability. Triggers on 'readable', 'typography', 'line height', 'text too small', 'spacing scale', 'type tokens', 'contrast'."
---

# Readable UI

## Overview

Use this skill when interface clarity depends on typography, spacing, contrast, or hierarchy. It turns layout and text decisions into practical defaults for product UI, dashboards, and reading-heavy surfaces.

## What To Optimize First

1. Legibility: size, weight, contrast, and line height.
2. Structure: headings, labels, grouping, and spacing.
3. Scannability: front-loaded words, short blocks, and obvious actions.
4. Density: keep information compact without making it ambiguous.

## Core Rules

- Use text roles, not arbitrary font sizes.
- Keep body text readable by default, usually 16px or larger on web.
- Aim for body line height around 1.45 to 1.65.
- Keep long-form text to roughly 60 to 75 characters per line.
- Use strong contrast for text and meaningful UI boundaries.

Form, label, and validation guidance (persistent labels, inline validation, primary actions, error placement) lives in the **ui-usability** skill.

## How To Apply It

- For pages with long reading, use larger body text, generous line height, and constrained measure.
- For SaaS dashboards and dense views, preserve clarity with alignment, hierarchy, and readable metadata.
- For empty states, buttons, and alerts, say what happened and what the user should do next.
- For review work, check whether the interface can be understood by scanning headings, labels, values, and actions in a few seconds.

## Resources

- [assets/tokens.css](assets/tokens.css) — copy-pasteable, contrast-safe type/spacing/color scale and semantic role classes. Start here when generating UI.
- [references/readability-guidelines.md](references/readability-guidelines.md) — detailed principles, good/bad examples, and a review checklist.
