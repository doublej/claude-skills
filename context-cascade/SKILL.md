---
name: context-cascade
description: "Visualize the CLAUDE.md file hierarchy with token counts and inheritance. Use when user asks about their context, CLAUDE.md files, context cascade, or wants to understand what instructions are loaded."
---

# Context Cascade

Visualize the CLAUDE.md context hierarchy for the current project.

## Run

Execute the scanner from the current working directory:

```bash
python3 {SKILL_DIR}/scripts/context_cascade.py --cwd "$(pwd)"
```

## Display

Parse the JSON output and render a cascade tree. Format:

```
CONTEXT CASCADE
===============

~/.claude/CLAUDE.md                          [global]
│  ~1,012 tokens · 98 lines
│  Engineering rules, git discipline, code caps, tooling prefs
│
└─ ~/Documents/development/CLAUDE.md         [parent]
   │  ~591 tokens · 46 lines
   │  Development directory overview, folder structure
   │
   └─ .../claude-skills/CLAUDE.md            [project]
        ~74 tokens · 4 lines
        Skill creation instructions

───────────────────────────────────────────────
Total: 3 files · ~1,677 tokens · 148 lines
```

Rules for the cascade:
- Shorten paths using `~` for home dir
- Right-align scope labels `[global]`, `[parent]`, `[project]`
- Include a 1-line summary of each file's content (read the file to determine this)
- Show totals at the bottom

## Full Content

After the cascade tree, show the full content of each CLAUDE.md file with clear visual separation and cascading structure that mirrors the tree hierarchy. Format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1 · ~/.claude/CLAUDE.md                  [global]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<full file contents rendered as-is>

  ┌─────────────────────────────────────────────────
  │ 2 · ~/Documents/development/CLAUDE.md  [parent]
  └─────────────────────────────────────────────────

  <full file contents rendered as-is, indented 2 spaces>

    ┌───────────────────────────────────────────────────
    │ 3 · .../claude-skills/CLAUDE.md        [project]
    └───────────────────────────────────────────────────

    <full file contents rendered as-is, indented 4 spaces>
```

Rules:
- Number each file (1, 2, 3...) matching cascade depth order
- Use box-drawing characters for headers: `━` for top-level, `┌─┘` for nested levels
- Indent nested file headers AND their content by 2 spaces per depth level
- Use the same shortened paths and scope labels as the cascade tree
- Render each file's content verbatim (markdown will be rendered naturally)
- Leave a blank line between the header box and the content, and between sections

## Post-display

After showing the full content, ask the user via `consult-user-mcp` `ask_confirmation`:

> "Would you like an inferred analysis of how these context files interact and what they prioritize?"

If confirmed, provide a brief analysis covering:
1. **Override chain** — which rules override which (project > parent > global)
2. **Key policies** — the most impactful rules active in this context
3. **Gaps or conflicts** — any contradictions or missing coverage between levels
