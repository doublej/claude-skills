---
name: swarm
description: >
  Orchestrate Claude Code agent teams (teammate mode). Use when user wants to spawn named agents inside the current session, coordinate parallel work, or use SendMessage between teammates. Triggers on: "create a swarm", "spawn teammates", "agent team", "teammate mode", "run agents in parallel inside session".
---

# Swarm — Claude Code Agent Teams

Spawns named teammate agents inside the current Claude Code session. Teammates run concurrently with independent context windows and communicate via SendMessage.

## Activation requirement

Agent teams require the experimental flag:
```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```

Without this flag, Agent() calls create disposable subagents, not persistent teammates.

## Spawn language (exact phrasing matters)

To trigger teammate mode (not subagent mode), use:
```
Create an agent team to [goal]. Spawn teammates:
- one named [name-a] to [role]
- one named [name-b] to [role]
```

Or concise:
```
Spawn a teammate named [name] using the [subagent_type] agent type to [task].
```

The word **teammate** and a **name** are the two signals that distinguish teammate from subagent.

## Agent tool parameters for teammates

```
Agent({
  name: "worker-a",              // address via SendMessage
  team_name: "my-team",         // groups teammates together
  subagent_type: "general-purpose",  // or any registered subagent type
  prompt: "...",                 // spawn-time briefing
  mode: "acceptEdits",          // permission mode (see below)
  isolation: "worktree",        // optional: isolated git branch
  run_in_background: true       // non-blocking spawn
})
```

## Communication: SendMessage

Teammates cannot hear each other through terminal output. Only SendMessage works.

```
SendMessage({
  to: "worker-a",       // teammate name, or "broadcast" for all
  message: "..."
})
```

Message types: `message` · `broadcast` · `shutdown_request` · `shutdown_response` · `plan_approval_response`

Continue a previously spawned agent (same session):
```
SendMessage({ to: "worker-a", message: "continue with phase 2" })
```

Or by agent ID returned in the Agent tool result.

## Permission modes

| Mode | Auto-approves |
|------|--------------|
| `default` | reads only |
| `acceptEdits` | reads + file edits + fs ops |
| `plan` | reads only (planning/research) |
| `auto` | everything (Team plan + Sonnet/Opus 4.6+ required) |
| `dontAsk` | pre-approved tools only |
| `bypassPermissions` | everything (VMs/containers only) |

## Worktree isolation

```
Agent({
  ...
  isolation: "worktree",  // teammate gets isolated git branch
})
```

Worktree is cleaned up automatically if teammate makes no changes.

## Swarm workflow template

```
Goal: [describe parallel task]

1. Spawn teammates (run_in_background: true for all):
   - researcher: explores codebase, gathers facts
   - implementer: writes code based on researcher findings
   - reviewer: audits implementer output

2. Researcher → SendMessage to implementer when done
3. Implementer → SendMessage to reviewer when done
4. Reviewer → SendMessage to lead with final verdict

Lead collects results and synthesizes.
```

## Teammates vs subagents

| Use teammates when... | Use subagents when... |
|----------------------|----------------------|
| Tasks run truly in parallel | Tasks are sequential |
| Agents need to talk to each other | Only lead needs results |
| Work benefits from isolated context | Single context is fine |
| Long-running independent roles | Short delegated queries |

## Common mistakes

- Missing `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` → falls back to subagent
- No `name` on Agent call → teammate unreachable via SendMessage
- Using terminal output to coordinate → teammates can't see it; use SendMessage
- Spawning without `run_in_background: true` → blocks lead until teammate finishes
