---
name: font-family-tree
description: "Scan style files for font-family declarations, generate Mermaid flowchart"
---

# Font Family Tree

Scan project styles and output a deterministic Mermaid flowchart of all font-family declarations, rooted at body/html/:root.

<usage>

Run the bundled script and save the output as a markdown file in the project root:

```bash
bash {{SKILL_DIR}}/scripts/scan-fonts.sh <project-dir> > <project-dir>/font-family-tree.md
```

Always save to `font-family-tree.md` — never just print to stdout.

</usage>

<what_it_scans>

- `.css` files
- `.scss` / `.sass` files
- `.svelte` files (`<style>` blocks)
- `tailwind.config.{js,ts,mjs,cjs}` (`theme.fontFamily` / `theme.extend.fontFamily`)

Excludes: `node_modules`, `.svelte-kit`, `dist`, `build`, `vendor`, `.git`, `.claude`

</what_it_scans>

<graph_structure>

- **Root node**: `body`, `html`, or `:root` font-family declaration
- **Child nodes**: all other selectors with `font-family` overrides
- **Node label**: `selector → font1, font2, ... | file:line`
- **Deterministic**: sorted by selector then location, deduped

</graph_structure>

<when_to_use>



- "What fonts does this project use?"
- "Show me the font-family hierarchy"
- "Audit typography / font stacks"
- "Map font overrides"

</when_to_use>
