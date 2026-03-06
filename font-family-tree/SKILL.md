---
name: font-family-tree
description: Scan a project's style files for font-family declarations and generate a Mermaid LR flowchart showing the typography hierarchy. Use when analyzing font usage, auditing font stacks, or visualizing font-family overrides in CSS/SCSS/Svelte/Tailwind projects.
---

# Font Family Tree

Scan project styles and output a deterministic Mermaid flowchart of all font-family declarations, rooted at body/html/:root.

## Usage

Run the bundled script and save the output as a markdown file in the project root:

```bash
bash {{SKILL_DIR}}/scripts/scan-fonts.sh <project-dir> > <project-dir>/font-family-tree.md
```

Always save to `font-family-tree.md` — never just print to stdout.

## What it scans

- `.css` files
- `.scss` / `.sass` files
- `.svelte` files (`<style>` blocks)
- `tailwind.config.{js,ts,mjs,cjs}` (`theme.fontFamily` / `theme.extend.fontFamily`)

Excludes: `node_modules`, `.svelte-kit`, `dist`, `build`, `vendor`, `.git`, `.claude`

## Graph structure

- **Root node**: `body`, `html`, or `:root` font-family declaration
- **Child nodes**: all other selectors with `font-family` overrides
- **Node label**: `selector → font1, font2, ... | file:line`
- **Deterministic**: sorted by selector then location, deduped

## When to use

- "What fonts does this project use?"
- "Show me the font-family hierarchy"
- "Audit typography / font stacks"
- "Map font overrides"
