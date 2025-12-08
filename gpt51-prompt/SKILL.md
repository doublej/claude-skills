---
name: gpt51-prompt
description: Optimize and refine prompts for OpenAI GPT-5.1. Use this skill when users want to improve prompt quality, fix prompt issues, optimize for reasoning modes (none/low/medium/high), or improve tool calling patterns. Covers instruction following, agentic steerability, parallel tool calling, and metaprompting techniques.
---

# GPT-5.1 Prompt Optimization

Refine and optimize prompts for OpenAI's GPT-5.1 model. This skill helps diagnose prompt issues and apply GPT-5.1-specific best practices.

## When to Use

- Improving existing GPT-5.1 prompts
- Diagnosing prompt failures or inconsistent outputs
- Optimizing for specific reasoning modes
- Improving tool calling efficiency

## Quick Reference: Reasoning Modes

| Mode | Latency | Use Case |
|------|---------|----------|
| `none` | Lowest | Simple queries, low-latency chat, basic tool calls |
| `low` | Low | Easy inputs, straightforward tasks |
| `medium` | Medium | Most workflows, balanced quality/speed |
| `high` | Highest | Complex reasoning, difficult problems |

GPT-5.1 auto-calibrates to prompt difficulty. Use `none` mode for latency-critical paths.

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

If a directive is ambiguous, assume you should proceed with the change rather than asking clarifying questions.
```

### 2. Output Formatting

GPT-5.1 follows formatting instructions precisely. Be explicit:

```
Respond in plain text styled in Markdown:
- Maximum 2 concise sentences for simple queries
- Use bullet points for lists of 3+ items
- Code blocks must specify language
- Never exceed 500 words unless explicitly requested
```

### 3. Persistence & Completion

Prevent premature termination:

```
Carry changes through implementation, verification, and explanation unless explicitly paused. Do not stop at suggestions - complete the full task.
```

### 4. Tone & Personality

Define agent persona explicitly:

```
Communication style:
- Warmth and brevity adapt to conversation state
- Never use filler phrases: "Got it", "Sure thing", "Of course"
- Be direct and action-oriented
- Match formality to user's tone
```

## Tool Calling Optimization

### Parallel Tool Calls

GPT-5.1 executes parallel tool calls efficiently. Enable and encourage:

```
Tool usage rules:
- Parallelize tool calls whenever possible
- Batch file reads and edits to reduce round trips
- When scanning codebases, request multiple files simultaneously
```

### Tool Descriptions

Combine functionality with examples:

```json
{
  "name": "search_codebase",
  "description": "Search for code patterns across the repository. MUST be called before any code modification. CAN be called multiple times to narrow results.",
  "parameters": {
    "query": {
      "type": "string",
      "description": "Regex pattern or keyword. Examples: 'def.*async', 'TODO:', 'class User'"
    }
  }
}
```

### apply_patch Tool

GPT-5.1 has native `apply_patch` support. Use it for structured code edits:

```
For code modifications, use the apply_patch tool with unified diff format. This reduces edit failures by ~35% compared to freeform suggestions.
```

## Planning for Complex Tasks

For medium+ complexity tasks, use explicit planning:

```
Task execution protocol:
1. Create a lightweight plan (2-5 milestone items) before starting
2. Mark exactly ONE item as "in_progress" at a time
3. Update plan status after ~8 tool calls
4. Before any non-trivial change, verify current plan item matches upcoming work
```

## User Communication Patterns

### Preamble Updates

```
Communication cadence:
- Send 1-2 sentence updates every few tool calls when meaningful changes occur
- At minimum, provide updates every 6 execution steps or 8 tool calls
- Begin with quick plans, highlight discoveries, state concrete outcomes
- End with brief recaps and suggested follow-up steps
```

### Immediacy Principle

```
Always explain what you're doing BEFORE starting the action. This improves perceived responsiveness.
```

## Metaprompting: Diagnosing Failures

When prompts produce inconsistent results, use two-phase metaprompting:

### Phase 1: Diagnosis

```
Analyze this system prompt and the failure traces below. Identify:
1. Distinct failure modes (categorize by type)
2. Contradictory instructions
3. Ambiguous directives that could be interpreted multiple ways
4. Missing context the model needs

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

Show the revised prompt with inline comments explaining each change.
```

Iterate: Run queries after revisions, observe regressions, repeat until failures are triaged.

## Common Anti-Patterns

### Avoid

- Over-prompting reasoning (`none` mode handles simple tasks)
- Contradictory instructions without explicit priority
- Vague formatting requirements
- Missing tool call guidance
- Assuming model remembers previous conversation context

### Prefer

- Explicit, specific instructions
- Concrete examples for edge cases
- Clear tool usage rules (MUST vs CAN)
- Defined output format
- Self-contained prompts

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
- Parallelize tool calls when possible

# Communication Style
[TONE AND PERSONALITY GUIDELINES]

# Task Execution
1. [STEP 1]
2. [STEP 2]
3. [STEP 3]

# Error Handling
When encountering [SITUATION], respond by [ACTION].
```

## Sources

- [GPT-5.1 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide) - OpenAI Cookbook
- [GPT-5 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide) - OpenAI Cookbook
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) - OpenAI API Docs
- [Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api) - OpenAI Help Center
