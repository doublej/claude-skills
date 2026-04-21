# Hooks — payloads, exit codes, and how the skill uses them

## Events we hook

| Event | Script | Purpose |
|---|---|---|
| `PreToolUse` matcher `Agent` | `preflight-agent.sh` | Re-check dirty WD & rate-limit spawns right before each `Agent()` call |
| `TaskCreated` | `task-created.sh` | Enforce owner + dependency or deadline on every team task |
| `TaskCompleted` | `task-completed.sh` | Block completion if the member's worktree is dirty without `leave_dirty: true` |
| `TeammateIdle` | `teammate-idle.sh` | Preset-specific gates (enforce_verdict, enforce_severity) |

All registered under `hooks.<Event>` in `~/.claude/settings.json`, installed by `scripts/install.sh`.

## Exit code contract

| Code | Meaning |
|---|---|
| 0 | Allow the action. |
| 1 | Allow but print script's stderr to the lead as a warning. |
| 2 | **Block** the action. Script's stderr is forwarded to the lead as structured feedback. |
| other | Treated as 0 with a logged warning. |

Scripts must be deterministic and fast (<500ms). They run on every fire; slow scripts degrade the whole session.

## Payloads (observed shapes)

### PreToolUse matcher=`Agent`

```json
{
  "tool_name": "Agent",
  "tool_input": {
    "team_name": "plan-committee-...",
    "name": "risk-auditor",
    "subagent_type": "adversarial-critic",
    "model": "claude-opus-4-7",
    "mode": "plan",
    "isolation": "worktree",
    "run_in_background": true,
    "prompt": "..."
  },
  "cwd": "/path/to/repo"
}
```

`preflight-agent.sh` reads `tool_input.team_name` — if it starts with a known team prefix, re-runs dirty-WD check.

### TaskCreated

```json
{
  "task": {
    "id": "42",
    "subject": "...",
    "description": "...",
    "owner": "implementer-1",
    "metadata": {"deadline": "2026-04-21T18:00:00Z"},
    "blockedBy": ["41"]
  },
  "team_name": "refactor-crew-..."
}
```

`task-created.sh` rejects if `owner` is empty AND `blockedBy` is empty AND `metadata.deadline` is absent. Prevents orphan tasks.

### TaskCompleted

```json
{
  "task": {
    "id": "42",
    "owner": "implementer-1",
    "metadata": {"worktree": ".claude/worktrees/implementer-1"}
  },
  "team_name": "..."
}
```

`task-completed.sh` reads `task.metadata.worktree`, runs `git -C <path> status --porcelain`, exits 2 if non-empty and `task.metadata.leave_dirty` is not `true`.

### TeammateIdle

```json
{
  "teammate": {"name": "risk-auditor", "agent_id": "...", "last_message": {...}},
  "team_name": "plan-committee-..."
}
```

`teammate-idle.sh` reads the last message body and the team's preset name (from `~/.claude/teams/<team>/config.json` — optional; we store preset in team name prefix by convention). Enforces:

- `enforce_verdict` — last message must contain `verdict:` (approve/reject/revise). Block otherwise.
- `enforce_severity` — last message must include `severity:` (critical/high/medium/low/info). Block otherwise.
- `none` — no-op.

## Writing a custom hook for your preset

1. Add a script under `~/.claude/hooks/teams/<name>.sh` (mkdir the dir if needed).
2. Set it executable: `chmod +x <name>.sh`.
3. Register in `~/.claude/settings.json` under `hooks.<Event>`. Pattern:

```json
{
  "hooks": {
    "TeammateIdle": [
      {"command": "~/.claude/hooks/teams/<name>.sh"}
    ]
  }
}
```

4. Script reads JSON from stdin, writes feedback to stderr, exits 0/1/2.

Minimal skeleton:

```bash
#!/usr/bin/env bash
set -euo pipefail
payload="$(cat)"
# inspect with jq
if echo "$payload" | jq -e '.teammate.last_message.text | test("verdict:")' >/dev/null; then
  exit 0
fi
echo "teammate did not include verdict — ask for one" >&2
exit 2
```

## Debugging

- Hook output appears in Claude Code's transcript as tool feedback when exit 2.
- To test a hook standalone: `echo '<payload>' | ~/.claude/hooks/teams/foo.sh; echo $?`
- `scripts/install.sh` backs up the settings file before touching it; to roll back a bad hook install: `cp ~/.claude/settings.json.pre-teams-<timestamp> ~/.claude/settings.json`.
