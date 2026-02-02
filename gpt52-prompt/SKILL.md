---
name: gpt52-prompt
description: Optimize and refine prompts for OpenAI GPT-5.2. Use this skill when users want to improve prompt quality, fix prompt issues, optimize for reasoning modes (none/minimal/low/medium/high/xhigh), leverage compaction for long workflows, or improve tool calling with preambles. Covers enterprise agentic workflows, parallel tool calling, context management, and metaprompting techniques.
---

# GPT-5.2 Prompt Optimization

Refine and optimize prompts for OpenAI's GPT-5.2 model—the flagship for professional knowledge work and long-running agents.

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
| `minimal` | Very low | Fast responses where slight reasoning helps |
| `low` | Low | Easy inputs, straightforward tasks |
| `medium` | Medium | Most workflows, balanced quality/speed |
| `high` | High | Complex reasoning, difficult problems |
| `xhigh` | Highest | **NEW** - Maximum reasoning depth, research tasks |

GPT-5.2 auto-calibrates to prompt difficulty. Default is `none`—explicitly set higher for complex tasks.

## Compaction for Long Workflows

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

GPT-5.2 follows formatting with less verbosity than predecessors:

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

GPT-5.2 excels at parallel execution:

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

GPT-5.2 has native `apply_patch` support with improved accuracy:

```
For code modifications, use the apply_patch tool with unified diff format. This reduces edit failures compared to freeform suggestions.
```

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

## Metaprompting: Diagnosing Failures

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

## Migration from GPT-5.1

1. **Keep prompt identical** - Test model change first
2. **Pin reasoning_effort** - Match prior latency profile (both default to `none`)
3. **Run evals** - If results good, ship
4. **If regressions** - Use Prompt Optimizer + targeted constraints
5. **Consider compaction** - For workflows that hit context limits

## Common Anti-Patterns

### Avoid

- Over-prompting reasoning when `none`/`minimal` suffices
- Contradictory instructions without priority
- Missing tool preamble guidance
- Assuming context survives compaction verbatim
- Setting `xhigh` for simple tasks (wasteful)

### Prefer

- Explicit, specific instructions
- Concrete examples for edge cases
- Clear tool usage rules (MUST vs CAN)
- Persistence reminders for low reasoning modes
- Preamble guidance for agentic flows

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
- Before each tool call, explain your intent briefly
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

## Sources

- [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide) - OpenAI Cookbook
- [GPT-5.2 Model Docs](https://platform.openai.com/docs/models/gpt-5.2) - OpenAI Platform
- [GPT-5.1 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide) - OpenAI Cookbook
- [Simon Willison's GPT-5.2 Overview](https://simonwillison.net/2025/Dec/11/gpt-52/) - Technical Summary
