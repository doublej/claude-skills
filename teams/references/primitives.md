# Primitives — raw teammate-mode building blocks

The low-level primitives the teams skill builds on: activation, spawn mechanics,
SendMessage, permission modes, worktree isolation. Merged in from a formerly
standalone skill. For lifecycle internals (inheritance, config.json, plan
approval) see `architecture.md`.

<activation_requirement>

Agent teams require the experimental flag:

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```

Without this flag, `Agent(...)` calls create disposable subagents, not
persistent teammates — silently. `scripts/preflight.sh` checks it explicitly.

</activation_requirement>

<spawn_mechanics>

Two things are required to get teammates instead of subagents:

1. The env flag above.
2. `TeamCreate` **before** any `Agent` call that passes `team_name`. The
   harness does not auto-create the team on first `Agent` — it errors out.

```
TeamCreate({ name: "my-team" })   # creates ~/.claude/teams/my-team/config.json

Agent({
  name: "worker-a",              # address via SendMessage
  team_name: "my-team",          # groups teammates together
  subagent_type: "general-purpose",  # or any registered subagent type
  prompt: "...",                 # spawn-time briefing (teammate sees no history)
  mode: "acceptEdits",           # permission mode (see below)
  isolation: "worktree",         # optional: isolated git worktree
  run_in_background: true        # non-blocking spawn
})
```

When done: `SendMessage(to, message_type: "shutdown_request")` per member,
then `TeamDelete({ name: "my-team" })`.

The lead_contract in `SKILL.md` is authoritative on spawn order when using
presets: parse spawn.py's JSON spec → `TeamCreate` → `Agent(...)` per member
verbatim → initial `SendMessage`s.

</spawn_mechanics>

<spawn_language>

When asking a lead in prose (no preset spec), use language that signals
teammate mode:

```
Create an agent team to [goal]. Spawn teammates:
- one named [name-a] to [role]
- one named [name-b] to [role]
```

Or concise:

```
Spawn a teammate named [name] using the [subagent_type] agent type to [task].
```

The word **teammate** and a **name** are the two signals that distinguish
teammate from subagent — but prose alone is not enough: the env flag and
`TeamCreate` (above) are what actually switch modes.

</spawn_language>

<communication>

Teammates cannot hear each other through terminal output. Only SendMessage works.

```
SendMessage({
  to: "worker-a",       # teammate name, or "broadcast" for all
  message: "..."
})
```

Message types: `message` · `broadcast` · `shutdown_request` ·
`shutdown_response` · `plan_approval_response`

Continue a previously spawned agent (same session):

```
SendMessage({ to: "worker-a", message: "continue with phase 2" })
```

Or by agent ID returned in the Agent tool result.

</communication>

<permission_modes>

| Mode | Auto-approves |
|------|--------------|
| `default` | reads only |
| `acceptEdits` | reads + file edits + fs ops |
| `plan` | reads only (planning/research) |
| `auto` | everything (Team plan + Sonnet/Opus 4.6+ required) |
| `dontAsk` | pre-approved tools only |
| `bypassPermissions` | everything (VMs/containers only) |

</permission_modes>

<worktree_isolation>

```
Agent({
  ...
  isolation: "worktree",  # teammate gets isolated git branch
})
```

Worktree is cleaned up automatically if the teammate makes no changes.
Mechanics (branch naming, no `cwd`/`branch` param, pre-seeding caveats) in
`architecture.md`.

</worktree_isolation>

<workflow_template>

```
Goal: [describe parallel task]

1. TeamCreate, then spawn teammates (run_in_background: true for all):
   - researcher: explores codebase, gathers facts
   - implementer: writes code based on researcher findings
   - reviewer: audits implementer output

2. Researcher → SendMessage to implementer when done
3. Implementer → SendMessage to reviewer when done
4. Reviewer → SendMessage to lead with final verdict

Lead collects results and synthesizes.
```

</workflow_template>

<comparison>

| Use teammates when... | Use subagents when... |
|----------------------|----------------------|
| Tasks run truly in parallel | Tasks are sequential |
| Agents need to talk to each other | Only lead needs results |
| Work benefits from isolated context | Single context is fine |
| Long-running independent roles | Short delegated queries |

For subagent + Task-DAG patterns (fan-out, pipeline, supervisor, debate) see
the `agent-orchestrator` skill.

</comparison>

<mistakes>

- Missing `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` → falls back to subagent
- No `TeamCreate` before `Agent(team_name: ...)` → harness errors out
- No `name` on Agent call → teammate unreachable via SendMessage
- Using terminal output to coordinate → teammates can't see it; use SendMessage
- Spawning without `run_in_background: true` → blocks lead until teammate finishes

</mistakes>
