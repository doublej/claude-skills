---
name: prompt-gpt
description: "Optimize prompts for OpenAI GPT-5.x models (GPT-5.1 and GPT-5.2): reasoning modes, tool calling, preambles, compaction, metaprompting, and 5.1→5.2 migration. Use when writing, improving, or debugging prompts targeting GPT-5.1 or GPT-5.2, tuning reasoning_effort, or diagnosing inconsistent outputs. For Claude-targeted prompts use prompt-crafter instead. Triggers: 'gpt-5', 'gpt-5.1', 'gpt-5.2', 'optimize my gpt prompt', 'openai prompt', 'gpt system prompt'."
---

# GPT-5.x Prompt Optimization (GPT-5.1 / GPT-5.2)

Refine and optimize prompts for OpenAI's GPT-5.x models. GPT-5.2 is the flagship for professional knowledge work and long-running agents; GPT-5.1 remains in use for existing deployments. Guidance below targets GPT-5.2 by default — GPT-5.1 deviations are collected in the `<gpt51_differences>` section.

<key_differences>
## Key Differences from GPT-5.1

| Feature | GPT-5.1 | GPT-5.2 |
|---------|---------|---------|
| Context window | 200K | **400K** |
| Max output | 64K | **128K** |
| Reasoning levels | none/low/medium/high | **none/minimal/low/medium/high/xhigh** |
| Default reasoning | none | **none** |
| Compaction API | No | **Yes** |
| Reasoning summaries | No | **Concise summaries** |
| Knowledge cutoff | May 2025 | **August 31, 2025** |

## Quick Reference: Reasoning Modes

| Mode | Latency | Use Case |
|------|---------|----------|
| `none` | Lowest | Simple queries, low-latency chat, basic tool calls |
| `minimal` | Very low | Fast responses where slight reasoning helps (5.2 only) |
| `low` | Low | Easy inputs, straightforward tasks |
| `medium` | Medium | Most workflows, balanced quality/speed |
| `high` | High | Complex reasoning, difficult problems |
| `xhigh` | Highest | Maximum reasoning depth, research tasks (5.2 only) |

GPT-5.x auto-calibrates to prompt difficulty. Default is `none`—explicitly set higher for complex tasks.
</key_differences>

<compaction>
## Compaction for Long Workflows (GPT-5.2 only)

GPT-5.2 introduces server-side compaction for extended agent sessions:

```python
# After reaching context limits, call:
response = client.responses.compact(
    response_id=current_response_id
)
# Returns encrypted, compressed context to continue workflow
```

**When to use:**
- Multi-hour agent sessions
- Workflows exceeding 200K tokens
- Tasks requiring many tool calls

**In prompts, add:**
```
For long-running tasks, the system will automatically compact context when approaching limits. Continue working seamlessly after compaction.
```
</compaction>

<prompt_optimization>
## Prompt Optimization Checklist

### 1. Clarity & Specificity

**Before:**
```
Help the user with their code.
```

**After:**
```
You are an autonomous senior pair-programmer. When the user describes a code problem:
1. Analyze the issue thoroughly
2. Propose a solution with rationale
3. Implement the fix completely
4. Verify the change works
5. Explain what you changed and why

If a directive is ambiguous, proceed with the change rather than asking clarifying questions.
```

### 2. Output Formatting

GPT-5.2 follows formatting with less verbosity than predecessors (GPT-5.1 also follows formatting instructions precisely — be explicit either way):

```
Respond in plain text styled in Markdown:
- Maximum 2 concise sentences for simple queries
- Use bullet points for lists of 3+ items
- Code blocks must specify language
- Never exceed 500 words unless explicitly requested
```

### 3. Persistence & Completion

Prevent premature termination (critical at low reasoning):

```
Carry changes through implementation, verification, and explanation unless explicitly paused. Do not stop at suggestions - complete the full task. Never terminate early due to perceived complexity.
```

### 4. Agentic Persistence (Important for minimal/low reasoning)

```
IMPORTANT: Do not stop working until the task is fully complete. If you encounter obstacles:
1. Try alternative approaches
2. Use available tools to gather more context
3. Only ask for clarification if genuinely blocked
4. Never assume the task is "too complex" - break it down and continue
```

### 5. Tone & Personality

Define agent persona explicitly:

```
Communication style:
- Warmth and brevity adapt to conversation state
- Never use filler phrases: "Got it", "Sure thing", "Of course"
- Be direct and action-oriented
- Match formality to user's tone
```
</prompt_optimization>

<tool_calling>
## Tool Calling Optimization

### Preambles (NEW in GPT-5.2)

Preambles are brief explanations before tool calls. Enable them for transparency:

```
Before calling any tool, briefly explain why you are calling it and what you expect to learn. This helps with debugging and user confidence.
```

**Example output:**
```
I'll search the codebase for authentication handlers to understand the current implementation.
[tool_call: search_codebase(query="auth handler")]
```

### Parallel Tool Calls

Both models execute parallel tool calls efficiently; GPT-5.2 excels at it:

```
Tool usage rules:
- Parallelize tool calls whenever possible
- Batch file reads and edits to reduce round trips
- When scanning codebases, request multiple files simultaneously
- Example: Reading 5 related files? Call read_file 5 times in parallel
```

### Tool Descriptions

Combine functionality with behavioral hints:

```json
{
  "name": "search_codebase",
  "description": "Search for code patterns across the repository. MUST be called before any code modification. CAN be called multiple times in parallel to gather comprehensive context.",
  "parameters": {
    "query": {
      "type": "string",
      "description": "Regex pattern or keyword. Examples: 'def.*async', 'TODO:', 'class User'"
    }
  }
}
```

### apply_patch Tool

GPT-5.x has native `apply_patch` support (accuracy improved in 5.2):

```
For code modifications, use the apply_patch tool with unified diff format. This reduces edit failures compared to freeform suggestions.
```
</tool_calling>

<planning_complex_tasks>
## Planning for Complex Tasks

Explicit planning is more important at lower reasoning levels:

```
Task execution protocol:
1. Create a lightweight plan (2-5 milestone items) before starting
2. Mark exactly ONE item as "in_progress" at a time
3. Update plan status after completing each milestone
4. Before any non-trivial change, verify current plan item matches upcoming work
5. After compaction events, re-establish current position in plan
```
</planning_complex_tasks>

<user_communication>
## User Communication Patterns

### Preamble Updates

```
Communication cadence:
- Explain your intent BEFORE each significant action
- Send 1-2 sentence updates when meaningful changes occur
- At minimum, provide updates every 6 execution steps
- End tasks with brief recaps and suggested follow-up steps
```

### Progress Transparency

```
When calling tools, always prefix with a brief explanation of:
1. What you're about to do
2. Why it's necessary
3. What you expect to find
```

### Immediacy Principle

```
Always explain what you're doing BEFORE starting the action. This improves perceived responsiveness.
```
</user_communication>

<metaprompting>
## Metaprompting: Diagnosing Failures

When prompts produce inconsistent results, use two-phase metaprompting:

### Phase 1: Diagnosis

```
Analyze this system prompt and the failure traces below. Identify:
1. Distinct failure modes (categorize by type)
2. Contradictory instructions
3. Ambiguous directives that could be interpreted multiple ways
4. Missing context the model needs
5. Reasoning effort mismatches (too low for task complexity)

System prompt: [PASTE PROMPT]
Failure examples: [PASTE FAILURES]
```

### Phase 2: Surgical Revision

```
Based on the diagnosis, propose surgical revisions that:
1. Clarify conflicting rules (make tradeoffs explicit)
2. Remove redundant instructions
3. Add missing context
4. Resolve ambiguities with concrete examples
5. Adjust reasoning_effort recommendation if needed

Show the revised prompt with inline comments explaining each change.
```

Iterate: Run queries after revisions, observe regressions, repeat until failures are triaged.
</metaprompting>

<gpt51_differences>
## Targeting GPT-5.1: What Changes

When the prompt targets GPT-5.1 instead of 5.2, apply these deltas:

- **No preambles feature, no compaction API, no reasoning summaries** — skip the `<compaction>` section and the "Preambles" guidance; instead rely on the Immediacy Principle and explicit cadence rules.
- **Reasoning modes**: only `none`/`low`/`medium`/`high` (`minimal` and `xhigh` do not exist). GPT-5.1 auto-calibrates to prompt difficulty; use `none` for latency-critical paths.
- **Context limits**: 200K context / 64K output — budget prompts and expected outputs accordingly.
- **apply_patch**: native support; reduces edit failures by ~35% compared to freeform suggestions.
- **Plan cadence**: update plan status after ~8 tool calls (5.2 guidance: after each completed milestone).
- **Communication cadence**: send 1-2 sentence updates every few tool calls when meaningful changes occur; at minimum every 6 execution steps or 8 tool calls. Begin with quick plans, highlight discoveries, state concrete outcomes.
- **Tool description hint**: phrase repeat-call permission as "CAN be called multiple times to narrow results" (5.2 phrasing emphasizes parallel calls instead).
- **Anti-patterns specific to 5.1**: vague formatting requirements, missing tool call guidance, and assuming the model remembers previous conversation context — keep prompts self-contained with a defined output format.
</gpt51_differences>

<migration>
## Migration from GPT-5.1 to GPT-5.2

1. **Keep prompt identical** - Test model change first
2. **Pin reasoning_effort** - Match prior latency profile (both default to `none`)
3. **Run evals** - If results good, ship
4. **If regressions** - Use Prompt Optimizer + targeted constraints
5. **Consider compaction** - For workflows that hit context limits
</migration>

<anti_patterns>
## Common Anti-Patterns

### Avoid

- Over-prompting reasoning when `none`/`minimal` suffices
- Contradictory instructions without priority
- Missing tool preamble guidance (5.2)
- Assuming context survives compaction verbatim (5.2)
- Setting `xhigh` for simple tasks (wasteful)
- Vague formatting requirements
- Assuming the model remembers previous conversation context

### Prefer

- Explicit, specific instructions
- Concrete examples for edge cases
- Clear tool usage rules (MUST vs CAN)
- Persistence reminders for low reasoning modes
- Preamble guidance for agentic flows (5.2)
- Defined output format; self-contained prompts
</anti_patterns>

<template>
## Example: Full System Prompt Template

```markdown
# Role
You are [ROLE]. Your purpose is [PURPOSE].

# Capabilities
- [CAPABILITY 1]
- [CAPABILITY 2]

# Constraints
- [CONSTRAINT 1]
- [CONSTRAINT 2]

# Output Format
[SPECIFIC FORMAT REQUIREMENTS]

# Tool Usage
- MUST call [TOOL] before [ACTION]
- CAN use [TOOL] for [USE CASE]
- Before each tool call, explain your intent briefly (5.2)
- Parallelize tool calls when possible

# Communication Style
[TONE AND PERSONALITY GUIDELINES]

# Task Execution
1. [STEP 1]
2. [STEP 2]
3. [STEP 3]

# Persistence
Complete all tasks fully. Do not terminate early. If blocked, try alternatives before asking for help.

# Error Handling
When encountering [SITUATION], respond by [ACTION].
```
</template>

<sources>
- [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide) - OpenAI Cookbook
- [GPT-5.2 Model Docs](https://platform.openai.com/docs/models/gpt-5.2) - OpenAI Platform
- [GPT-5.1 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide) - OpenAI Cookbook
- [GPT-5 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide) - OpenAI Cookbook
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) - OpenAI API Docs
- [Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api) - OpenAI Help Center
- [Simon Willison's GPT-5.2 Overview](https://simonwillison.net/2025/Dec/11/gpt-52/) - Technical Summary
</sources>
