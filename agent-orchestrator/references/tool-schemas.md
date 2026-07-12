# Tool Schemas — Full Parameter Reference

Exact parameter schemas for all orchestration tools. Grep for tool name to find its schema.

Note: team-scoped entries (`TeamCreate`, `TeamDelete`, the `team_name` param, `TeammateIdle`) require teammate mode — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` plus `TeamCreate` before spawning. That workflow belongs to the **teams** skill; they are listed here only for schema completeness.

## Agent

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | yes | Complete task description with all needed context |
| `description` | string | yes | 3-5 word summary |
| `subagent_type` | string | no | Agent definition name (e.g., `"Explore"`, `"code-reviewer"`) |
| `name` | string | no | Makes agent addressable via SendMessage |
| `model` | enum | no | `"sonnet"` \| `"opus"` \| `"haiku"` |
| `mode` | enum | no | `"default"` \| `"plan"` \| `"acceptEdits"` \| `"dontAsk"` \| `"bypassPermissions"` \| `"auto"` |
| `run_in_background` | bool | no | `true` = returns immediately, notifies on completion |
| `isolation` | enum | no | `"worktree"` = isolated git worktree copy |
| `team_name` | string | no | Team name for spawning (uses current if omitted) |

**Returns:** Agent's final response text (foreground) or completion notification (background).

## SendMessage

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | string | yes | Agent name, agent ID, or `"broadcast"` |
| `message` | string | yes | Message text |

**Returns:** Delivery confirmation.

## TaskCreate

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `subject` | string | yes | Task title |
| `description` | string | no | Detailed description |
| `depends_on` | string[] | no | Task IDs that must complete first |
| `assigned_to` | string | no | Teammate name |

**Returns:** `task_id` (string).

## TaskUpdate

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | yes | Task to update |
| `status` | enum | no | `"pending"` \| `"in-progress"` \| `"completed"` |
| `subject` | string | no | New title |
| `description` | string | no | New description |
| `assigned_to` | string | no | Teammate name |
| `depends_on` | string[] | no | Replace dependency list |
| `delete` | bool | no | `true` = delete the task |

## TaskList

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `filter` | enum | no | `"pending"` \| `"in-progress"` \| `"completed"` (omit = all) |

**Returns:** Array of task objects (`task_id`, `subject`, `status`, `assigned_to`, `depends_on`, timestamps).

## TaskGet

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | yes | Task to retrieve |

**Returns:** Full task object.

## TaskOutput

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | yes | Background task ID |
| `lines` | number | no | Number of output lines (default: all) |

**Returns:** Buffered stdout/stderr from background bash command.

## TaskStop

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | yes | Background task ID to kill |

## TeamCreate

Creates an agent team for multi-agent collaboration.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Team identifier |

## TeamDelete

Removes an agent team.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Team to delete |

## EnterWorktree

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | no | Worktree name (auto-generated if omitted) |

**Returns:** Worktree path and branch name.

## ExitWorktree

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `should_keep` | bool | no | Keep worktree on exit (prompts user if omitted) |

## Hook Event Schemas

### TeammateIdle

Input to hook command (JSON on stdin):
```json
{
  "session_id": "abc123",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-team",
  "cwd": "/path/to/project",
  "transcript_path": "..."
}
```
- Exit 0 = allow idle
- Exit 2 = send stderr as feedback, agent continues

### TaskCompleted

```json
{
  "task_id": "task-001",
  "task_subject": "Implement authentication",
  "task_description": "Add JWT...",
  "teammate_name": "implementer",
  "team_name": "my-team"
}
```
- Exit 0 = allow completion
- Exit 2 = reject completion, stderr → agent feedback

### WorktreeCreate

```json
{"name": "feature-auth"}
```
Must print absolute worktree path to stdout.

### WorktreeRemove

```json
{"worktree_path": "/path/to/worktree"}
```
No decision control (cannot block removal).

### SubagentStart

```json
{
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```
Can inject context via `hookSpecificOutput.additionalContext`.

### SubagentStop

```json
{
  "agent_id": "agent-abc123",
  "agent_type": "Explore",
  "agent_transcript_path": "...",
  "last_assistant_message": "..."
}
```
Can block with `{"decision": "block", "reason": "..."}`.
