# Extended prompt patterns

Optional templates for authorised workflows and project instructions. Output (internal): chosen template name and its filled task/report contract. Output (in the prompt): that contract. All paths, commands, tools, and policy slots below are illustrative; ground replacements or label them as runtime inputs.

## Independent task brief

Use only when subagents are available, authorised, and useful. Each brief carries one independent task, necessary context, and the result the parent consumes.

```xml
<task>[One scoped task and its purpose.]</task>
<context>[Verified paths, relevant facts, and the required input.]</context>
<boundaries>[Permitted actions and scope.] If required access is unavailable, report the missing input and stop.</boundaries>
<output_format>[Fields the parent needs, including evidence and unresolved cases.] Done when every item in [scope] is represented; stop after the result.</output_format>
```

## Independent acceptance trial

Give evaluator only specification and result, without author conclusions.

```xml
<task>Evaluate [result] against the specification below using [authorised checks].</task>
<specification>[Complete acceptance requirements.]</specification>
<output_format>One row per requirement: PASS / FAIL / UNVERIFIED, concrete observation, failing input if any. End with a one-line verdict. Mark checks that could not run UNVERIFIED; do not infer a pass.</output_format>
```

## Complete implementation brief

```xml
<task>[Requested change, intended result, and relevant context.]</task>
<boundaries>Edit only [scope]; [grounded reason for the boundary]. [Other authorised actions.]</boundaries>
<done_when>[Acceptance command] exits 0 and [observable behaviour]. If blocked, identify the unmet condition and evidence.</done_when>
<output_format>Files changed, acceptance result, and unresolved blockers. Stop after this report.</output_format>
```

## Claude project instructions (CLAUDE.md)

Use only the rows the project needs; do not invent stack choices or unverified policies.

```markdown
# [Project name]

[One sentence describing the project and its purpose.]

Build: `[verified command]`
Test: `[verified command]`

## Change scope
[Grounded project rules with reasons where non-obvious.]

## Completion
[Observable quality gate and authorised git actions.]

## Report
[Required result fields and meaningful length constraint.]
```

## Claude path-scoped rule file

Output: `.claude/rules/<name>.md`. Claude Code matches rules via glob frontmatter (contrast with Codex directory-cascading `AGENTS.md`).

```markdown
---
paths:
  - "[intended glob]"
---
[Rule covering every matching file, with the project's reason.]
```

## Codex project instructions (AGENTS.md)

Hierarchy: `~/.codex/AGENTS.md` (global) -> `<repo>/AGENTS.md` (root) -> `<dir>/AGENTS.md` (subsystem). `AGENTS.override.md` replaces `AGENTS.md` in that dir. Codex cascades down directory trees; do not use Claude-style glob frontmatter.

```markdown
# [Project or Directory Name]

Build: `[verified command]`
Test: `[verified command]`

## Scope & Constraints
- [Grounded rule or boundary with reason; permitted edit paths.]

## Precedence & Overrides
- Local `AGENTS.override.md` overrides this file; child directory `AGENTS.md` appends subsystem rules.
```

## Non-interactive CLI automation

```bash
# Codex: non-interactive diff review (suggest mode)
git diff origin/main...HEAD | codex -q -a suggest "Review diff for safety and regressions against [spec]" > review.md

# Codex: non-interactive auto-fix in workspace sandbox
codex -q -a auto-edit --cd [workspace] --add-dir [extra-dir] "Resolve [issue]; verify with [test command]"

# Claude Code: headless execution with bounded tools and permissions
claude -p "[task]" --permission-mode acceptEdits --allowedTools "Read,Edit,Bash([test command])"

# Claude Code: resume prior session non-interactively
claude -p "[followup task]" --resume [session-id]
```

## Claude Agent SDK patterns

```python
# Programmatic subagent registered in parent (requires "Agent" in allowed_tools)
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Agent"],
    agents={"reviewer": AgentDefinition(
        description="[Capability summary for parent routing]",
        prompt="<mission>[Scoped task]</mission><boundaries>[Allowed actions]</boundaries>",
        tools=["Read", "Glob"],
    )},
)

# PreToolUse guard (deny/allow) and PostToolUse audit hook
async def pre_tool_hook(input_data, tool_use_id, context):
    cmd = input_data.get("tool_input", {}).get("command", "")
    if "[forbidden_pattern]" in cmd:
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Blocked by policy",
        }}
    return {}

async def post_tool_hook(input_data, tool_use_id, context):
    audit_log.append({"tool_use_id": tool_use_id, "input": input_data.get("tool_input")})
    return {}
```

## Runtime variables and environment hygiene

| Variable / Setting | Source / System | Required handling |
|--------------------|-----------------|-------------------|
| `$ARGUMENTS` | Slash-command caller | Define meaning and empty-value default; treat as data |
| `{{INPUT}}` | Caller or harness | Define missing-input result; replace before dispatch |
| `@path/to/file` | Instruction-file import | Resolve from destination; verify existence before claiming it |
| `CODEX_QUIET_MODE=1` | Codex CLI | Suppress interactive spinners/banners for CI & pipe output |
| `CODEX_DISABLE_PROJECT_DOC=1` | Codex CLI | Skip automatic `AGENTS.md` loading in isolated evaluation |
| `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` | Claude Code | Unset in nested SDK subagents to prevent recursive session errors |
