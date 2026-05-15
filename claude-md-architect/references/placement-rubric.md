# Placement Rubric: Where Does This Knowledge Live?

Before adding any line to a CLAUDE.md, classify it. Most "what's wrong with my CLAUDE.md setup" pain is misplacement, not missing content.

## Decision table

| What you have                                              | Where it goes                                          | Why                                                                |
| ---------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ |
| Project mission, stack, repo map                           | root `CLAUDE.md`                                       | Needed every session, top-level orientation.                       |
| Global invariants ("never push to main")                   | root `CLAUDE.md`                                       | Apply everywhere.                                                  |
| Folder-local domain model, invariants, verification        | nested `CLAUDE.md`                                     | Only relevant when working in that subtree.                        |
| Same rule that applies to many paths matching a glob       | `.claude/rules/<topic>.md` with `paths:` frontmatter   | One source of truth. Loads only when matching files are read.      |
| Same rule everywhere, no path scope                        | `.claude/rules/<topic>.md` without `paths:`            | Loads at session start; same priority as `.claude/CLAUDE.md`.      |
| Repeatable procedure ("how to add an API endpoint")        | `.claude/skills/<name>/SKILL.md`                       | Skills are workflows. CLAUDE.md is knowledge.                      |
| Long historical context, ADR, spec                         | `docs/`, **linked** from CLAUDE.md                     | CLAUDE.md is loaded into context; long files cost tokens.          |
| Personal preferences (your sandbox URLs, test data)        | `CLAUDE.local.md` at project root                      | Gitignored; not shared with team.                                  |
| Things Claude should learn from you over time              | auto memory (`~/.claude/projects/<project>/memory/`)   | Claude writes these itself based on corrections.                   |
| Cross-project personal preferences                         | `~/.claude/CLAUDE.md`                                  | Applies everywhere you work.                                       |
| Cross-project personal rules with file scope               | `~/.claude/rules/<topic>.md`                           | Same as project rules, scoped to your user.                        |
| Must-run commands (format-on-save, pre-commit checks)      | hooks in `.claude/settings.json`                       | Enforced regardless of what Claude does. Not guidance.             |
| Tool/path permissions                                      | `permissions` in settings                              | Hard enforcement, not behavioral guidance.                         |
| Org-wide policy that individuals cannot override           | managed `CLAUDE.md` (`/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS, `/etc/claude-code/CLAUDE.md` on Linux/WSL, `C:\Program Files\ClaudeCode\CLAUDE.md` on Windows) or `claudeMd` key in managed settings | Cannot be excluded by individual settings.                         |
| Instructions written for another AI tool (AGENTS.md)       | `@AGENTS.md` import from CLAUDE.md, or symlink         | Both tools read the same file. Symlink needs admin on Windows.     |

## When two locations seem valid

Use these tiebreakers, in order:

1. **Scope**: prefer the narrowest location that still gets the rule loaded when needed. Path-scoped rules beat nested CLAUDE.md beat root CLAUDE.md beat user-level CLAUDE.md.
2. **Reuse count**: if the same content would otherwise appear in 3+ files, lift it into a rule or shared doc and link from each.
3. **Procedural vs. factual**: procedures are skills, facts are CLAUDE.md / rules. Test: does the content describe *steps to take* or *what is true*?
4. **Survives compaction?**: root CLAUDE.md does; nested doesn't. If a rule is critical mid-conversation regardless of which files Claude is reading, keep it at the root.

## When NOT to write anything

Skip the entry entirely when:

- Claude could infer it by reading the code (file names, types, exports).
- It only restates the parent CLAUDE.md.
- It says "follow existing patterns" — that's not actionable.
- It is a one-off that won't repeat.
- The fix should be a hook (deterministic) instead of guidance (probabilistic).

## A worked classification

User says: "Always run `pnpm test billing` after changing anything in `src/billing/`. Also, webhook handlers must be idempotent. Also, our payment provider is Stripe but we'll switch to Adyen next year."

Classification:

| Sentence                                              | Destination                                                              |
| ----------------------------------------------------- | ------------------------------------------------------------------------ |
| Always run `pnpm test billing` after `src/billing/`   | `src/billing/CLAUDE.md` "Verification" section. Or a hook if must-run.   |
| Webhook handlers must be idempotent                   | `src/billing/CLAUDE.md` "Important invariants" (with the *why*).         |
| Payment provider is Stripe                            | `src/billing/CLAUDE.md` "Mental model" (one line).                       |
| Switching to Adyen next year                          | `docs/adr/NNN-payment-provider-migration.md`, linked from billing packet. The CLAUDE.md should not carry the future plan; ADRs do. |

That's four destinations for four sentences. That is the level of separation worth aiming for.
