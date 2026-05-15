# Verified Claude Code Behavior (CLAUDE.md & rules)

All claims in this skill have been verified against the official Claude Code documentation at `code.claude.com/docs/en/`. Quotes below are from the docs as of 2026-05-15.

## CLAUDE.md load order

> Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for `CLAUDE.md` and `CLAUDE.local.md` files.

> All discovered files are concatenated into context rather than overriding each other. Across the directory tree, content is ordered from the filesystem root down to your working directory.

Order: managed policy → user (`~/.claude/CLAUDE.md`) → project ancestors (filesystem root down to cwd) → `CLAUDE.local.md` (per directory, appended after `CLAUDE.md` at that level).

## Nested CLAUDE.md (the load-on-demand behavior)

> Claude also discovers `CLAUDE.md` and `CLAUDE.local.md` files in subdirectories under your current working directory. Instead of loading them at launch, they are included when Claude reads files in those subdirectories.

This is the foundation of folder-local context packets. The packet loads only when Claude actually touches a file under that subfolder.

## Project CLAUDE.md location

Either:
- `./CLAUDE.md`
- `./.claude/CLAUDE.md`

Both are equivalent. Pick one per project; mixing creates confusion.

## Size guidance

> **Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence.

Also:

> Files over 200 lines consume more context and may reduce adherence.

Aim under 200 for root CLAUDE.md and under 100 for nested packets.

## Path-scoped rules

Rules live in `.claude/rules/*.md` (recursive — subdirectories work).

Without `paths:` frontmatter:
> Rules without [`paths` frontmatter](#path-specific-rules) are loaded at launch with the same priority as `.claude/CLAUDE.md`.

With `paths:` frontmatter:
> Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.

Frontmatter shape:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "lib/**/*.ts"
---
```

Brace expansion is supported: `"src/**/*.{ts,tsx}"`.

## Compaction behavior (critical)

> Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory.

Consequence: anything that must remain in context across compactions belongs at the root or in a non-path-scoped rule, not in a nested file.

System prompt, root CLAUDE.md, auto memory, and MCP tool list survive compaction. **The skill listing does not survive compaction** — only skills you actually invoked are preserved.

## Imports with `@`

> CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.

- Relative paths resolve to the file containing the import, not the cwd.
- Recursive imports allowed up to **5 hops**.
- First time encountering external imports, Claude Code shows an approval dialog. Declining disables imports permanently for that project.
- Imports do **not** reduce context — the imported file is concatenated in.

## CLAUDE.local.md

- Lives at the project root.
- Gitignored (you must add it; `/init` with the personal option does this).
- Loaded alongside CLAUDE.md, treated the same way.
- Worktree-local: a gitignored CLAUDE.local.md only exists in the worktree where you created it. To share personal instructions across worktrees, import from `~`:
  ```markdown
  # Individual Preferences
  - @~/.claude/my-project-instructions.md
  ```

## Auto memory (separate from CLAUDE.md)

Lives at `~/.claude/projects/<project>/memory/`. The first 200 lines or 25 KB (whichever comes first) of `MEMORY.md` are loaded at every session start. Topic files in the same directory are read on demand. Auto memory is machine-local and not shared across machines.

This is **not** for CLAUDE.md-style instructions. Auto memory is what Claude writes itself based on observed corrections and preferences.

## HTML comments are stripped

> Block-level HTML comments (`<!-- maintainer notes -->`) in CLAUDE.md files are stripped before the content is injected into Claude's context. Use them to leave notes for human maintainers without spending context tokens on them. Comments inside code blocks are preserved.

Use HTML comments for "last reviewed on", "TODO: write the ADR", etc.

## Monorepo: excluding other teams' CLAUDE.md

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Live in `.claude/settings.local.json` for personal exclusions, or higher layers if team-wide. Arrays merge across layers. Managed policy CLAUDE.md cannot be excluded.

## `--add-dir` and external CLAUDE.md

By default, CLAUDE.md files from `--add-dir` directories are **not** loaded. To enable:

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

This also picks up `.claude/CLAUDE.md`, `.claude/rules/*.md`, and (unless excluded via `--setting-sources`) `CLAUDE.local.md` in that directory.

## AGENTS.md interop

Three options when a repo also uses `AGENTS.md` for other agents:

1. Symlink: `ln -s AGENTS.md CLAUDE.md` (Windows requires admin or Developer Mode).
2. Import from CLAUDE.md:
   ```markdown
   @AGENTS.md
   
   ## Claude Code
   Use plan mode for changes under `src/billing/`.
   ```
3. Run `/init` in an existing AGENTS.md repo — Claude reads it and incorporates relevant parts into a new CLAUDE.md.

## Useful commands for verification

| Command                              | What it does                                                      |
| ------------------------------------ | ----------------------------------------------------------------- |
| `/memory`                            | Lists all CLAUDE.md, CLAUDE.local.md, and rules files loaded.     |
| `/context`                           | Shows what is occupying the context window.                       |
| `/init`                              | Generates a starter CLAUDE.md (analyzes codebase first).          |
| `CLAUDE_CODE_NEW_INIT=1 claude` then `/init` | Interactive multi-phase /init flow with subagent exploration.     |
| `InstructionsLoaded` hook            | Logs which instruction files load, when, and why.                 |

## When the instructions seem ignored

From the official troubleshooting:

- CLAUDE.md is delivered as a user message after the system prompt. There is no guarantee of strict compliance.
- Run `/memory` to confirm the file is loaded.
- Make instructions more specific. "Use 2-space indentation" beats "format code nicely."
- For must-run behavior, use hooks (deterministic), not CLAUDE.md (probabilistic).
- For system-prompt-level instructions in automation, use `--append-system-prompt`.

## Source documentation

- [Memory](https://code.claude.com/docs/en/memory)
- [Context window](https://code.claude.com/docs/en/context-window)
- [.claude directory](https://code.claude.com/docs/en/claude-directory)
- [Skills](https://code.claude.com/docs/en/skills)
- [Hooks](https://code.claude.com/docs/en/hooks)
