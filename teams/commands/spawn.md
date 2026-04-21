---
description: Spawn a Claude Code agent team from a preset. Args - <preset> [team-name].
allowed-tools: Bash, Agent, SendMessage, TeamCreate
---

Spawn a team using the teams skill.

Arguments: `<preset-name> [team-name]`. If `$ARGUMENTS` is empty, first run `/teams:list` to show the catalog, then ask the user which preset to use via consult-user-mcp.

Execute:

```bash
python3 ~/.claude/skills/teams/scripts/spawn.py $ARGUMENTS
```

The script prints a JSON spec. You (the lead) must then:

1. Parse the JSON.
2. Call `TeamCreate(...)` with `team_create_args` exactly as given.
3. For each member in `members`, call `Agent(...)` with `agent_args` verbatim. Do **not** substitute `subagent_type`, `model`, `mode`, or `isolation`.
4. If a member has non-empty `initial_messages`, send them via `SendMessage` after the Agent call succeeds.
5. Implement the `lead_behavior` string's intent (broadcast, synthesize, merge, etc.).
6. Honor `escalation` — all user-facing questions go through `mcp__consult-user-mcp__ask` (not `AskUserQuestion`).

Report the team name + snapshot tag back to the user.
