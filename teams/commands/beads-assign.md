---
description: Pull open bd tickets and print a distribution plan for a beads-pm team. Args - [team-name].
allowed-tools: Bash, SendMessage, TaskCreate, TaskUpdate
---

Fetch and distribute beads tickets.

Argument: `[team-name]` (default: `beads-pm`).

```bash
bash ~/.claude/skills/teams/scripts/beads-tickets.sh $ARGUMENTS
```

The script prints JSON:

```
{"tickets": [...], "distribution": [{"owner": "impl-1", "ticket_id": "...", "title": "..."}, ...]}
```

Then you (the lead / PM):

1. For each entry in `distribution`, call `TaskCreate` with:
   - `subject`: the ticket title.
   - `owner`: the assigned implementer name.
   - `metadata`: `{"ticket_id": <id>}`.
2. `SendMessage` each implementer a briefing: "claim bd ticket <id>, work in your worktree, signal task_done when the change is committed."
3. When an implementer signals done, `bd close <ticket-id> --commit-sha <sha>`.
4. Escalate blockers via `mcp__consult-user-mcp__ask`.
