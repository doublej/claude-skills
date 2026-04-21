---
name: teams
description: >
  Orchestrate Claude Code agent teams (teammate mode) via named presets with strict safety gates. Use when the user wants parallel multi-agent work, competing perspectives, distributed writers across worktrees, plan review by multiple critics, PR review squad, debugging panel, refactor crew, research pod, beads ticket distribution, or a security audit team. Triggers on: "agent team", "teammate mode", "spawn a team", "plan committee", "think tank", "pr review team", "debug panel", "refactor crew", "research pod", "beads team", "security audit team", "fullstack feature team", preset names.
---

# Teams — Claude Code Agent Team Orchestrator

Spawns named **teammate** agents (not disposable subagents) from preset blueprints. Safety-first: dirty working directories block, snapshots tag HEAD before spawn, worktrees isolate writers, every decision routes through `consult-user-mcp`.

For raw primitives (SendMessage, plan approval, modes) see `../swarm/SKILL.md`. This skill sits on top: it adds presets, safety gates, merge orchestration, and a bundle of opinionated role definitions.

## Decision flow

1. Is work parallelizable? If no → don't use this skill.
2. Does work benefit from competing perspectives OR independent writers OR distributed tickets? If no → one subagent is usually enough.
3. Pick a preset below. If none fit, adapt the closest or author a new preset (see `references/preset-authoring.md`).

## Command cheat sheet

The lead should call the **bash** column (terser, token-cheaper). The **slash** column is user-typable.

| Intent | Bash | Slash |
|---|---|---|
| Verify repo + env ready | `bash ~/.claude/skills/teams/scripts/preflight.sh` | `/teams:preflight` |
| Browse presets | `bash ~/.claude/skills/teams/scripts/list-presets.sh` | `/teams:list` |
| Spawn a team | `python3 ~/.claude/skills/teams/scripts/spawn.py <preset> [team-name]` | `/teams:spawn <preset>` |
| Active teams + members | `bash ~/.claude/skills/teams/scripts/status.sh` | `/teams:status` |
| Graceful shutdown | `bash ~/.claude/skills/teams/scripts/shutdown.sh <team>` | `/teams:shutdown <team>` |
| Worktree + team delete | `bash ~/.claude/skills/teams/scripts/cleanup.sh <team>` | `/teams:cleanup <team>` |
| Distribute beads tickets | `bash ~/.claude/skills/teams/scripts/beads-tickets.sh <team>` | `/teams:beads-assign` |
| Pre-spawn snapshot tag | `bash ~/.claude/skills/teams/scripts/snapshot.sh <team>` | — (internal) |

## Lead contract

`spawn.py <preset> [team-name]` emits a JSON spec. The lead must:

1. Parse the JSON.
2. Call `TeamCreate` with `team_create_args`.
3. Call `Agent(...)` once per member using `agent_args` **verbatim** — do not substitute `subagent_type`, `model`, `mode`, or `isolation` unless the spec marks that field mutable.
4. Send each member's `initial_messages` (if present) via `SendMessage`.
5. Implement `lead_behavior` (synthesize, merge worktrees in order, etc.).
6. Escalate per `escalation` rules to `consult-user-mcp` (never `AskUserQuestion`).

The spec is portable; the lead is a thin executor.

## Preset catalog

Full YAML in `presets/`. One-liners:

- **plan-committee** — 3 critics (risk / completeness / simplicity) review a plan doc in plan mode. Deliverable: synthesized findings + verdict.
- **creative-think-tank** — 4 brainstormers (dreamer / pragmatist / devil / synthesizer) run 3-round debate. Deliverable: ranked ideas doc.
- **fullstack-feature** — 4 writers (db → be → fe → qa) across worktrees with strict dependency chain. Lead merges in reverse order.
- **pr-review-squad** — 3 read-only reviewers (security / performance / coverage) aggregate into a single PR review.
- **bug-debug-panel** — 5 hypothesis-testers debate theories, attack each other's, converge on survivor + repro.
- **refactor-crew** — 4 writers (architect → implementer → test-writer → docs). Architect's plan approval gates the rest.
- **research-pod** — 3 read-only (researcher + fact-checker + synthesizer) with WebFetch/WebSearch.
- **beads-pm** — PM lead pulls `bd list --json`, distributes tickets to N implementers who `bd claim`, work in worktrees named `teams/beads/<id>`.
- **security-audit** — 4 auditors (appsec / infrasec / depsec / compliance) produce severity-scored findings.

## Safety contract (strict mode, non-negotiable)

Every spawn passes through 5 gates:

1. **Env gate** (`preflight.sh`) — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` must be set and we must be inside a git repo.
2. **Repo gate** (`preflight.sh`) — dirty working directory forces a `consult-user-mcp` pick (commit / stash / abort). Current branch in `{main, master, production, release/*}` forces a `confirm` with default=no.
3. **Snapshot gate** (`snapshot.sh`) — tag `teams/<team-name>-snapshot` on HEAD so `git reset --hard` can roll back.
4. **Worktree gate** — write-capable presets require `isolation: "worktree"` on every member. Read-only presets run in `mode: "plan"` so they cannot write.
5. **Hook gate** — `PreToolUse: Agent`, `TaskCreated`, `TaskCompleted`, `TeammateIdle` hooks enforce safety per preset. Exit 2 blocks the action and returns feedback to the lead.

Details in `references/safety.md`.

## Token-efficiency contract

Every preset specifies model + tools per role so the lead doesn't pay Opus prices for Haiku work:

- **Haiku** — scribe / test runner / coverage reporter / doc writer.
- **Sonnet** — implementer / reviewer / synthesizer.
- **Opus** — architect / adversarial critic / final-verdict gatekeeper.

Bundled `subagents/` types ship tight `tools` allowlists. Spawn prompts are ≤10 lines and include "ignore memory, do not invoke skills unless asked." Per-worktree MCP stripping is documented in `references/token-efficiency.md` as experimental / future work.

## Consult-user-mcp protocol

All user-facing decisions during a team's lifetime flow through `mcp__consult-user-mcp__ask` or `__notify`. `scripts/_consult.sh` wraps the four call shapes (confirm / pick / text / notify). Never use `AskUserQuestion`.

## Presets live outside ~/.claude/teams/

`~/.claude/teams/<team>/config.json` is auto-generated by the harness at TeamCreate time — not pre-authorable. This skill keeps presets in:

- **Bundled**: `~/.claude/skills/teams/presets/<name>.yaml`
- **User overrides**: `~/.claude/team-presets/<name>.yaml` (created by `scripts/install.sh`)

On name collision, user override wins. Users can ship their own presets without forking this skill.

## Cross-references

- `references/architecture.md` — teammate vs subagent lifecycle, what's actually inherited, config.json schema observed in the wild.
- `references/safety.md` — dirty-WD rationale, snapshot rollback recipe, worktree merge escalation flow.
- `references/token-efficiency.md` — model/tools/prompt tactics, measured deltas, worktree-override experiment log.
- `references/hooks.md` — hook payloads (TeammateIdle, TaskCreated, TaskCompleted, PreToolUse:Agent), exit-code contract.
- `references/preset-authoring.md` — YAML schema and how to add your own preset.
- `../swarm/SKILL.md` — underlying primitives (SendMessage, modes, plan-approval, isolation).

## Install

```bash
# From repo root
./install-skill.sh teams

# Then the skill's post-install (idempotent)
~/.claude/skills/teams/scripts/install.sh
```

The post-install step copies commands into `~/.claude/commands/teams/`, hooks into `~/.claude/hooks/teams/`, jq-merges hook entries into `~/.claude/settings.json` (full backup taken first), and creates `~/.claude/team-presets/`. Restart Claude Code to activate hooks.

## Common failure modes

- **Preset not found** → `scripts/spawn.py` calls `_consult.sh pick` with the union of bundled + user presets.
- **Dirty WD blocks spawn** → lead asks via consult (commit / stash / abort). Don't auto-stash silently.
- **Worktree conflict on merge** → lead asks via consult (resolve-here / leave-for-user / abort). Never force-merge.
- **Teammate goes idle without deliverable** → `teammate-idle.sh` hook nudges via SendMessage; after `escalation.on_idle_stall_turns`, lead escalates to user.
- **Orphaned `~/.claude/teams/` entries** → detected by preflight, offered cleanup via consult.
