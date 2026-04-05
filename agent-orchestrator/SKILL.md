---
name: agent-orchestrator
description: "Multi-agent workflows: subagents, worktrees, fan-out, pipelines"
---

Orchestrate multi-agent work using the tools below. Pick the simplest pattern that fits.

## Decision: Subagents vs Agent Teams

| Need | Use |
|------|-----|
| Parallel research / analysis (no shared files) | Subagents with `run_in_background: true` |
| Parallel implementation (shared repo) | Agent Teams with worktree isolation |
| Sequential pipeline (stage → stage) | Tasks with `depends_on` |
| Single focused task delegation | One subagent (foreground) |

## Core Tools

### Agent — Spawn a subagent

```
Agent(
  prompt: "...",              # required — complete task description
  description: "3-5 words",  # required — short label
  subagent_type: "...",       # optional — agent definition name
  name: "researcher",         # optional — addressable via SendMessage
  model: "sonnet",            # optional — sonnet | opus | haiku
  mode: "plan",               # optional — plan | acceptEdits | bypassPermissions | default
  run_in_background: true,    # optional — returns immediately, notifies on completion
  isolation: "worktree",      # optional — isolated git worktree copy
)
```

**Key rules:**
- Subagents do NOT inherit conversation history — include all context in `prompt`
- Launch independent agents in a **single message** with multiple Agent calls
- Background agents cannot ask questions — they fail silently on AskUserQuestion
- `name` makes the agent addressable via `SendMessage(to: "researcher")`
- `isolation: "worktree"` gives each agent its own repo copy (auto-cleaned if no changes)

### SendMessage — Talk to a running agent

```
SendMessage(
  to: "researcher",    # agent name or agent ID
  message: "..."       # the message
)
```

- Resume a stopped agent by sending to its ID
- Teammates can message each other directly

### TaskCreate — Create a tracked task

```
TaskCreate(
  subject: "Implement auth",           # required
  description: "Add JWT login...",     # optional
  depends_on: ["task-001"],            # optional — blocked until these complete
  assigned_to: "backend-dev"           # optional — teammate name
)
# Returns: task_id
```

### TaskUpdate — Update task state

```
TaskUpdate(
  task_id: "task-001",                 # required
  status: "in-progress",              # pending | in-progress | completed
  assigned_to: "researcher",           # optional
  description: "Updated scope...",     # optional
  depends_on: ["task-003"],            # optional — replaces deps
  delete: true                         # optional — removes task
)
```

### TaskList / TaskGet

```
TaskList(filter: "pending")   # pending | in-progress | completed | omit for all
TaskGet(task_id: "task-001")  # full details for one task
```

### TaskOutput / TaskStop — Background task control

```
TaskOutput(task_id: "task-001", lines: 50)  # read output from background bash
TaskStop(task_id: "task-001")               # kill background task
```

## Orchestration Patterns

### Pattern 1: Fan-Out (parallel research)

Spawn N agents in ONE message. Each investigates independently. Merge results.

```
# Single message with 3 parallel Agent calls:
Agent(name: "db-analyst", prompt: "Analyze database schema for...", run_in_background: true)
Agent(name: "code-reviewer", prompt: "Review recent changes to...", run_in_background: true)
Agent(name: "api-tester", prompt: "Test the /users endpoint...", run_in_background: true)
# Wait for all 3 to complete, then synthesize
```

**When:** Multiple independent angles on the same problem.
**Model tip:** Use `sonnet` for research agents to save tokens.

### Pattern 2: Pipeline (sequential stages)

Use task dependencies to enforce ordering. Agents self-claim next unblocked task.

```
t1 = TaskCreate(subject: "Design API schema")
t2 = TaskCreate(subject: "Implement endpoints", depends_on: [t1])
t3 = TaskCreate(subject: "Write integration tests", depends_on: [t2])
```

**When:** Each stage depends on the previous stage's output.

### Pattern 3: Supervisor (hierarchical delegation)

Main agent stays in control, spawns focused subagents for specific work.

```
# Foreground — blocks until done, result comes back to you
Agent(prompt: "Review auth module for security issues", description: "Security review")

# Use the result to decide next step
Agent(prompt: "Fix the XSS vulnerability in login.ts:42", description: "Fix XSS bug")
```

**When:** You need results before deciding next steps.

### Pattern 4: Parallel Implementation (worktree-isolated)

Each agent edits code in its own repo copy. No file conflicts.

```
Agent(
  name: "auth-feature",
  prompt: "Implement JWT authentication in src/auth/",
  isolation: "worktree",
  run_in_background: true
)
Agent(
  name: "api-feature",
  prompt: "Add REST endpoints in src/api/",
  isolation: "worktree",
  run_in_background: true
)
```

**When:** Multiple agents need to edit files simultaneously.
**Note:** Worktrees with changes are kept; without changes are auto-cleaned.

### Pattern 5: Debate (adversarial evaluation)

Multiple agents argue for/against, a synthesizer resolves.

```
Agent(name: "advocate", prompt: "Argue FOR adopting Redis. Cite evidence.", run_in_background: true)
Agent(name: "critic", prompt: "Argue AGAINST adopting Redis. Be skeptical.", run_in_background: true)
# Wait for both, then:
Agent(prompt: "Given advocate's arguments: {adv} and critic's arguments: {crit}, synthesize a recommendation.")
```

**When:** Evaluating options where bias is a risk.

### Pattern 6: Swarm (batch distribution)

Split N tasks across M agents. Each gets a batch.

```
# Create task list
for item in items:
    TaskCreate(subject: f"Process {item}", assigned_to: f"worker-{i % num_agents}")

# Spawn workers
for i in range(num_agents):
    Agent(
      name: f"worker-{i}",
      prompt: "Work through your assigned tasks: {batch}. Mark each completed.",
      model: "sonnet",
      run_in_background: true
    )
```

**When:** Many similar, independent work items.

## Agent Definitions

Define reusable agent types in `.claude/agents/<name>.md`:

```markdown
---
name: code-reviewer
description: Reviews code for bugs, security, and quality issues
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 15
permissionMode: plan
---

You are a senior code reviewer. Analyze code changes and report issues by severity.
```

### Frontmatter reference

| Field | Values | Default |
|-------|--------|---------|
| `tools` | Comma-separated tool names | All (inherited) |
| `disallowedTools` | Tools to remove | None |
| `model` | sonnet, opus, haiku | inherit |
| `permissionMode` | default, plan, acceptEdits, dontAsk, bypassPermissions | default |
| `maxTurns` | Positive integer | Unlimited |
| `isolation` | worktree | None |
| `background` | true/false | false |
| `effort` | low, medium, high | inherit |
| `memory` | user, project, local | None |
| `mcpServers` | Server names or inline configs | None |
| `skills` | Skill names to preload | None |

**Locations** (highest priority first):
1. `.claude/agents/` (project, checked in)
2. `~/.claude/agents/` (user-level)
3. Plugin `agents/` directory

## Lifecycle Hooks

Configure in `settings.json` under `hooks`:

### TeammateIdle — Quality gate before agent stops

```json
{"event": "TeammateIdle", "command": "npm test || exit 2"}
```
Exit 2 = send stderr as feedback, agent continues working.

### TaskCompleted — Gate before task closes

```json
{"event": "TaskCompleted", "command": "./check-task.sh"}
```
Exit 2 = task NOT marked complete, agent gets feedback.

### WorktreeCreate / WorktreeRemove — Custom VCS

Override git worktree behavior for SVN/Perforce/Mercurial.

## Best Practices

1. **Include full context in prompts** — subagents don't see your conversation
2. **One message, multiple agents** — always launch independent agents in parallel
3. **Use `sonnet` for workers** — save tokens, reserve `opus` for synthesis/decisions
4. **Grant minimal tools** — restrict via `tools` in agent definitions
5. **Avoid file conflicts** — use worktree isolation when agents edit the same repo
6. **3-5 teammates max** — token cost scales linearly per agent
7. **5-6 tasks per agent** — keeps workload balanced
8. **Don't broadcast often** — sends to ALL teammates, scales cost
9. **Background for independence** — foreground when you need the result next
10. **Tasks persist across compaction** — use them as coordination memory

## Limitations

- No session resume with in-process teammates
- No nested teams (teammates can't spawn teams)
- Lead is fixed — can't transfer leadership
- One team per session
- Background agents can't ask questions
- Worktree changes only tracked via git
