# Token efficiency — tactics and measured deltas

Teams are token-expensive by default. A five-member team triples+ the cost of a single-agent session because each teammate pays to load CLAUDE.md, skills, and MCP lists. This document collects what actually works.

## Ranked tactics

| Tactic | Effectiveness | Verified? | Risk |
|---|---|---|---|
| Tight `tools` allowlist on subagent type | High | Yes (docs) | None |
| Smaller model per role (haiku > sonnet > opus) | High | Yes (billing) | Downgrade blindness |
| Compact spawn prompt + "ignore memory, no skills unless asked" | Medium | Prompt-level | Teammate may ignore |
| Read-only mode for review/critique roles | Medium | Indirect (fewer actions) | None |
| Per-worktree `.claude/settings.local.json` stripping MCPs | Unknown | **Not verified** | Docs silent |

## Per-role model defaults

Bundled presets make role→model choices intentional:

| Role pattern | Model | Why |
|---|---|---|
| scribe / doc writer / simple test runner / coverage reporter | claude-haiku-4-5 | High-volume, low-judgment work |
| implementer / reviewer / synthesizer | claude-sonnet-4-6 | Primary working-memory tier |
| architect / adversarial critic / final gatekeeper | claude-opus-4-7 | Where the judgment lives |

Overriding per-role in user presets is fine; the `_schema.yaml` documents the field.

## Subagent type `tools` allowlists

Shipped types lock tools to the minimum:

- `minimal-worker.md` → `[Read, Grep, Glob]` + no Bash.
- `read-only-reviewer.md` → `[Read, Grep, Glob, Bash(git:*,rg:*,jq:*)]`.
- `write-implementer.md` → `[Read, Edit, Write, Bash(git:*,npm:*,pnpm:*,pytest:*,uv:*,cargo:*)]`.
- `adversarial-critic.md` → `[Read, Grep, Glob]` + no Bash (critics don't run things).

Additive fields in presets (`tools: [...]`) merge with these. If a preset adds `WebFetch`, the resulting effective allowlist is the union. `spawn.py` emits the union; the lead passes it through as-is.

## Spawn prompt template

≤10 lines, no fluff. Every shipped preset uses this frame:

```
You are {role} for {team_name}.
Goal: {one-line deliverable}.
Stop condition: {when you're done}.
Do NOT invoke skills unless the lead asks.
Do NOT consult memory unless the lead asks.
{role-specific instruction — 1–3 lines max}
```

Why this specific phrasing: memory and skill load are the two largest context costs on spawn. The prompt can't prevent the harness from loading them initially, but it reduces *invocations* in-session, which is where cost escalates.

## Mode choice

| Mode | When to use |
|---|---|
| `plan` | Every read-only preset and every Opus critic. Cheapest: no edit operations billed. |
| `acceptEdits` | Writer roles that don't need destructive-cmd approval. |
| `dontAsk` | Only if you've pre-approved a tight tool allowlist that can't hurt anything. |
| `auto` | Avoid — gives teammates unchecked reign. |
| `bypassPermissions` | Never, outside of sandboxes. |

## Experimental: per-worktree MCP stripping

**Unverified.** Hypothesis: dropping `~/.claude/settings.local.json` inside `.claude/worktrees/<name>/` with an empty `mcpServers: {}` prevents the teammate from loading user-level MCPs on startup, saving ~2–8k input tokens.

Template: `templates/lean.claude-settings.json`.

Docs are silent on whether worktree-scoped settings are honored by teammates. Until verified:

- Do NOT depend on this for any load-bearing behavior.
- Do NOT apply it when the user has MCP servers the team actually needs.
- If you test this, record the result in this file.

### Log

| Date | Claude Code version | Preset tested | Result |
|---|---|---|---|
| (none yet) | — | — | — |

## Measurable deltas (informal)

First-turn tokens observed on a trivial "read one file and summarize" task:

- `minimal-worker` (haiku, 3 tools) — ~4k input.
- `read-only-reviewer` (sonnet, 6 tools + git/jq) — ~6k input.
- `write-implementer` (sonnet, 12 tools + bash families) — ~8k input.
- No scoping, default `general-purpose` — ~12k input.

Numbers will drift across versions; re-measure before citing. The ordering is the stable claim.

## Anti-patterns

- Using `opus` for a scribe role — 5× the cost for identical output.
- Leaving `tools: []` (no allowlist) — teammate gets everything, including MCPs they'll never use.
- Including the full plan/PR text in every round of a broadcast — hash or link instead.
- Respawning teammates when a `SendMessage` would do — Agent cost ≈ 10× SendMessage cost.
- Running a 4-member team when a subagent would suffice.
