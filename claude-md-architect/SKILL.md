---
name: claude-md-architect
description: Architect CLAUDE.md files across a larger codebase as context packets, not commandments. Use when asked to "explode CLAUDE.md", "complete CLAUDE.md", "add CLAUDE.md to subfolders", design nested CLAUDE.md hierarchy, set up context for a monorepo, decide where to put rules vs CLAUDE.md vs skills, audit context architecture, or apply the context-packet pattern across a tree. Verified against Claude Code docs (memory, context-window, claude-directory).
---

# CLAUDE.md Architect

## Overview

Treat CLAUDE.md as **context architecture**, not just rules. The goal is to leave Claude the minimum useful local operating manual for each part of the tree: what this folder is, what matters here, what not to break, how to verify changes, and where deeper context lives.

The best outcome is not "lots of Claude files." It is that when Claude enters a subtree, it receives the same orientation a senior engineer would give before saying: "now make the change."

## When to use this skill

Trigger on requests like:
- "Explode CLAUDE.md into subfolders"
- "Complete the CLAUDE.md hierarchy"
- "Audit our context setup"
- "Set up CLAUDE.md for this monorepo"
- "Where should this rule live — CLAUDE.md, rules, or skill?"
- "Why isn't Claude picking up our `src/billing` conventions?"

## Mental model

Five mechanisms, five jobs (verified — see `references/verified-docs.md`):

| Mechanism                        | Load behavior                                                | Use for                                                       |
| -------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| Root `CLAUDE.md`                 | Loaded in full at every session start. Survives `/compact`.  | Whole-project orientation, repo map, global invariants.       |
| Nested `CLAUDE.md` in subfolders | Loaded on demand when Claude reads files in that subfolder. **Not** re-injected after `/compact`. | Folder-local context packets: domain model, invariants, verification. |
| `.claude/rules/*.md`             | Without `paths:` frontmatter → loaded at session start. With `paths:` → loaded when matching files are read. | Cross-cutting topical rules (testing, a11y, generated files, api-contracts). |
| `.claude/skills/<name>/SKILL.md` | Listed at startup (description only). Body loads only when invoked. | Repeatable procedures ("how to do a job"). Knowledge belongs in CLAUDE.md / rules. |
| Hooks / settings                 | Enforced shell commands at lifecycle events.                 | Things that *must* run, not just "should."                    |

Folder context tells Claude **what is true**. Skills tell Claude **what to do**. Rules apply behavior **conditionally**. Hooks enforce behavior **mechanically**.

## Philosophy: context packets, not commandments

A good folder-level `CLAUDE.md` is a **context packet**, not a rule list. A bare bullet list of "always do X, never do Y" is the weakest form. The canonical shape is:

```md
# Context for this folder

## What this is
Briefly explain the purpose of this subtree.

## Mental model
Explain how the important parts fit together.

## Important invariants
List things that must stay true (with reasons where non-obvious).

## Common change patterns
Explain how changes are usually made here.

## Verification
The smallest relevant tests/checks for changes in this folder.

## Related context
Point to docs, ADRs, schemas, specs, or parent folders.
```

Rules are only one section — usually the smallest one. See `references/context-packet-template.md` for the canonical template, and `references/examples/` for filled-in cases.

## The 5-pass workflow

Run these in order. Do **not** try to add CLAUDE.md to every folder in one pass.

### Pass 1 — Inventory: find the high-value zones

A folder earns a `CLAUDE.md` when at least **two** of these are true:

- Has business logic Claude cannot infer from code alone.
- Has invariants that would cause real bugs if missed.
- Has a distinct mental model.
- Has specialized commands or tests.
- Humans often explain this folder during code review.
- Integrates with money, auth, data integrity, AI, external APIs, or permissions.

A folder does **not** get one when:

- It only repeats parent instructions.
- It only says "follow existing patterns."
- The code is already self-explanatory.
- The file would be under ~5 meaningful lines.

Use the script:

```bash
python3 scripts/audit_tree.py <repo-root>
```

It walks the tree, scores each candidate folder, marks which already have a `CLAUDE.md`, and prints a ranked proposal. Use it as a starting list — not a final answer. Human judgment overrides the score.

Typical high-value zones in a web/SaaS repo:

```
CLAUDE.md                  ← root: map + global invariants
src/db/CLAUDE.md           ← schema, migrations, data access
src/billing/CLAUDE.md      ← money, webhooks, entitlements
src/auth/CLAUDE.md         ← session, tokens, RBAC
src/api/CLAUDE.md          ← contracts, error format
src/components/CLAUDE.md   ← UI conventions
packages/ui/CLAUDE.md      ← design system
```

Resist `src/components/Button/CLAUDE.md`-style depth. Component-level is rarely worth the context cost.

### Pass 2 — Classify before placing

For every piece of knowledge, decide where it goes using `references/placement-rubric.md`:

| Knowledge                                          | Goes in                                |
| -------------------------------------------------- | -------------------------------------- |
| Whole-project purpose, stack, repo map             | root `CLAUDE.md`                       |
| Folder purpose, domain model, invariants           | nested `CLAUDE.md`                     |
| Cross-cutting rule applied to many paths           | `.claude/rules/<topic>.md` with `paths:` |
| Repeatable procedure ("how to add an X")           | `.claude/skills/<name>/SKILL.md`       |
| Long background, ADRs, specs                       | `docs/`, linked from CLAUDE.md         |
| Personal/local notes                               | `CLAUDE.local.md` (gitignored) or auto memory |
| Must-run commands (lint, format, signing)          | hooks in `.claude/settings.json`       |

Misplacement is the most common failure mode: rules that should be path-scoped get duplicated in 6 nested CLAUDE.md files; procedures that should be skills bloat the root file.

### Pass 3 — Write the root file as a map, not a manual

Root `CLAUDE.md` should give Claude orientation and **point to** deeper context, not contain it. Target under 200 lines (verified guidance: Claude Code docs recommend <200 lines per CLAUDE.md for adherence).

Required sections:
1. **What this project is** — one short paragraph.
2. **Architecture map** — top-level folders with one-line purposes.
3. **Context boundaries** — "before editing X, read `X/CLAUDE.md`".
4. **Global invariants** — only the truly global ones.
5. **Commands** — build, test, format, lint.

See `references/examples/root-claude-md.md` for a worked example.

### Pass 4 — Write context packets for the chosen zones

For each high-value folder, fill in the template from `references/context-packet-template.md`. Domain-specific examples to crib from:

- Money/billing: `references/examples/domain-billing.md`
- UI components: `references/examples/components-charts.md`
- Data layer: `references/examples/domain-db.md`

Keep each packet **under 100 lines**. If it grows past that, move long explanations into `docs/` and link from the packet.

### Pass 5 — Lift cross-cutting rules into `.claude/rules/`

Anything you'd otherwise repeat across 3+ folders belongs in a path-scoped rule. Common ones:

```text
.claude/rules/
├── accessibility.md       # paths: src/components/**, packages/ui/**
├── testing.md             # paths: **/*.test.{ts,tsx}, **/*.spec.ts
├── api-contracts.md       # paths: src/api/**
├── generated-files.md     # paths: **/*.generated.*, **/generated/**
└── migrations.md          # paths: src/db/migrations/**
```

Rule frontmatter:
```markdown
---
paths:
  - "src/api/**/*.ts"
---
```

Rules without `paths:` load every session (same priority as `.claude/CLAUDE.md`). Add `paths:` whenever the rule is truly path-local — it saves context.

## Verification

After every pass, verify in a fresh session:

1. Open Claude Code in the project root.
2. Run `/memory` — confirm the expected CLAUDE.md and rules files are listed.
3. Open a file in a subtree (e.g., `src/billing/foo.ts`). Run `/memory` again — the nested `src/billing/CLAUDE.md` should now appear.
4. Run `/context` to see what is consuming context window.
5. (Optional) Enable the `InstructionsLoaded` hook to log exactly which instruction files load and when. See `references/verified-docs.md`.

**Compaction caveat (verified):** root `CLAUDE.md` survives `/compact` and is re-injected from disk. Nested `CLAUDE.md` files are **not** auto-reinjected; they reload the next time Claude reads a file in that subtree. Plan accordingly — anything that must always be in context belongs higher up.

## Common anti-patterns

See `references/anti-patterns.md` for the full list. The biggest ones:

1. **Sprinkling `CLAUDE.md` in every folder** — context bloat, mostly no-ops. Audit removes more than it adds.
2. **Treating `CLAUDE.md` as a rule book** — pure bullet lists with no mental model give Claude nothing to reason about.
3. **Duplicating rules across nested files** — that's what `.claude/rules/*.md` with `paths:` is for.
4. **Pasting ADR-length docs inline** — link to `docs/` instead. CLAUDE.md is loaded into context; 900 lines is 900 lines of tokens.
5. **Using CLAUDE.md to specify procedures** — procedures are skills. CLAUDE.md is knowledge.
6. **Forgetting compaction behavior** — putting compaction-critical invariants only in nested files.
7. **Hand-edited generated content** — if you have generated folders, say so in the parent CLAUDE.md and link a rule.

## Quick reference: commands you will use

```bash
# Inventory candidates
python3 scripts/audit_tree.py <repo-root>

# Check what's loaded (in a Claude Code session)
/memory
/context

# Generate a starter root CLAUDE.md (Claude Code built-in)
/init
# or interactive multi-phase:
CLAUDE_CODE_NEW_INIT=1 claude   # then /init

# Install the skill after edits (this repo)
./install-skill.sh claude-md-architect
```

## What to deliver

When asked to "explode" or "complete" CLAUDE.md across a repo, deliver in this order:

1. **Inventory report** — output of `audit_tree.py` plus your human-judgment annotations.
2. **Proposed file list** — which CLAUDE.md, rules, and skills you'll add or modify.
3. **Root CLAUDE.md rewrite** — first, before the nested packets.
4. **Nested context packets** — one per chosen zone, using the template.
5. **Rules extraction** — cross-cutting rules pulled into `.claude/rules/`.
6. **Verification log** — output of `/memory` and `/context` after the changes.

Confirm the inventory + proposed file list with the user **before** writing the packets. Adding CLAUDE.md to the wrong places is the most common failure and the most expensive to undo.

## See also

- `references/context-packet-template.md` — canonical template for nested files
- `references/placement-rubric.md` — decision table for where knowledge lives
- `references/verified-docs.md` — verified Claude Code behavior with doc links
- `references/anti-patterns.md` — failure modes catalogue
- `references/examples/` — worked examples (root, billing, db, charts)
- `scripts/audit_tree.py` — inventory script
