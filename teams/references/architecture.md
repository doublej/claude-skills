# Architecture — how agent teams work under the hood

## Teammate vs subagent

Both are spawned via the `Agent` tool. The distinction:

| Property | Subagent (default) | Teammate |
|---|---|---|
| Trigger | `Agent(...)` without `team_name` | `Agent(..., team_name: "t")` inside an existing team |
| Lifetime | Single task, returns a summary string | Persistent across messages within the session |
| Addressable | No | Yes, via `SendMessage({to: name})` |
| Context inheritance | Gets parent CLAUDE.md + skills; no session history | Same, plus shared task list |
| Concurrency | Sequential unless multiple in one message block | Truly parallel (run_in_background: true) |
| Config file | None | `~/.claude/teams/<team>/config.json` auto-created at `TeamCreate` |

Teammate mode requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Missing that env → silently falls back to subagent. The preflight script checks explicitly.

## Spawn lifecycle

```
lead → TeamCreate(name: "t", ...)        # creates ~/.claude/teams/t/config.json
lead → Agent(team_name: "t",
             name: "worker-a",
             subagent_type: "read-only-reviewer",
             model: "claude-sonnet-4-6",
             mode: "plan",
             isolation: "worktree",      # optional — creates .claude/worktrees/worker-a/
             run_in_background: true,
             prompt: "<spawn briefing>")
lead → SendMessage(to: "worker-a", message: "...")
...
lead → SendMessage(to: "worker-a", message_type: "shutdown_request")
worker-a → SendMessage(to: "lead", message_type: "shutdown_response")
lead → TeamDelete(team_name: "t")        # removes config.json
```

Key timing note: `TeamCreate` must precede every `Agent` call that passes `team_name`. The harness won't create the team on first `Agent`; it errors out.

## What a teammate inherits

Verified (per Claude Code agent-teams docs):

- Project and user `CLAUDE.md` — loaded automatically on spawn.
- All skills installed at `~/.claude/skills/` and `<repo>/.claude/skills/`.
- User-level MCP servers configured in `~/.claude/settings.json`.
- Environment variables from parent shell (including `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`).

NOT inherited:

- Lead's conversation history — a teammate starts fresh, it only knows what you put in `prompt` and later `SendMessage` calls.
- Lead's task list entries — but both sides see the shared team task list after creation.

Subagent definition fields honored for teammates: **`tools`** and **`model`** only. The `skills` and `mcpServers` frontmatter fields from a subagent definition are **ignored** for teammate spawns. This shapes our `subagents/*.md` design — we scope purely via `tools` allowlists.

## Worktree isolation details

`Agent({isolation: "worktree"})` causes the harness to:

1. `git worktree add -b worktree-<name> <repo>/.claude/worktrees/<name> HEAD`
2. Pass that path as the teammate's cwd.
3. If the teammate makes zero commits / edits, the worktree is cleaned up on shutdown.

There is **no** `branch` or `cwd` parameter on the `Agent` call. You cannot pre-seed the worktree's first turn with a different branch or working tree state. If you need a custom starting branch, create it on the main tree first and make sure HEAD points there before spawning.

## config.json (observed schema)

```json
{
  "team_name": "plan-committee-2026-04-21",
  "created_at": "2026-04-21T12:00:00Z",
  "members": [
    {"name": "risk-auditor", "agent_id": "<uuid>", "status": "running"},
    ...
  ],
  "lead_agent_id": "<uuid>"
}
```

Auto-written by the harness; do not hand-edit. `status.sh` reads these to list active teams and members.

## SendMessage message types

From agent-teams docs:

- `message` — normal inter-teammate message (default).
- `broadcast` — sends to every member of the current team; `to: "broadcast"`.
- `shutdown_request` — graceful stop; teammate should ACK with `shutdown_response`.
- `shutdown_response` — ACK for the above.
- `plan_approval_response` — reply to a plan-mode teammate waiting for approval; payload includes approved / rejected / revise.

## Plan approval protocol

A teammate spawned with `mode: "plan"` can propose a plan via a special tool. The lead receives a message and must reply with `plan_approval_response`. This is how `refactor-crew`'s architect gates downstream work: its plan approval blocks the implementer's first task.

## Shared task list

Once `TeamCreate` runs, `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet`, `TaskOutput`, `TaskStop` all operate on a **team-shared** list. Any member can see any task. Presets with dependency chains (fullstack-feature, refactor-crew) exploit this: the lead creates tasks with `addBlockedBy` edges upfront, implementers claim them via `owner`, and the hook system enforces metadata like `owner` presence at creation.

## Where `~/.claude/teams/` lives

```
~/.claude/teams/
├── <team-name-1>/
│   ├── config.json
│   └── (possibly logs)
└── <team-name-2>/
    └── config.json
```

After `TeamDelete`, the directory is removed. If the process crashes mid-run, entries may linger — preflight detects this and offers cleanup via consult.
