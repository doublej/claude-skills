# Claude Code Best Practices (February 2026)

> Based on Claude Opus 4.5 and Sonnet 4.5 models
> Knowledge cutoff: January 2025

## Key Principles

### 1. Tool Usage Optimization
- **Parallel tool calls**: When tools have no dependencies, call them in a single message
- **Specialized tools over bash**: Use Read/Edit/Write instead of cat/sed/echo
- **Task agent for exploration**: Use Task tool with subagent_type=Explore for codebase discovery
- **Proactive agent spawning**: Use specialized agents when their description matches the task

### 2. Context Management
- **Unlimited context**: Conversation has automatic summarization
- **Progressive disclosure**: Load resources only as needed
- **Token efficiency**: Challenge every piece of information - does Claude need this?

### 3. User Interaction
- **consult-user-mcp**: Use for ALL questions (ask_confirmation, ask_multiple_choice, ask_text_input)
- **Never use built-in AskUserQuestion**: consult-user-mcp tools are preferred
- **Single question rule**: Ask exactly ONE question when blocked, not multiple
- **Minimize questions**: Only ask when truly blocked; proceed with reasonable defaults otherwise

### 4. Code Quality Standards
- **KISS + YAGNI**: Keep it simple, you aren't gonna need it
- **SRP**: Single responsibility per function/module
- **No over-engineering**: Don't add features beyond what's requested
- **Guard clauses**: Prefer early returns over nested if/else
- **Explicit over clever**: Readable code trumps clever code

### 5. Size Targets (not limits)
- Functions: aim 5-10 lines, avoid >20
- Parameters: aim ≤2, avoid >3
- Nesting: aim ≤1 indentation level
- Files/modules: aim <150 lines
- One primary module/class/component per file

### 6. Git Workflow
- Commit often with atomic changes
- Messages: `verb: description` (no AI attribution)
- Never push unless requested
- Don't rewrite history unless asked

### 7. Quality Gates
- Run smallest set of checks for confidence
- If fails: iterate up to 3 cycles on SAME check
- After 3 cycles: switch strategy and explain why
- If can't run: say "not run" + list exact commands

### 8. Change Philosophy
- Minimal, local diffs matching existing style
- Avoid drive-by refactors
- No backward compatibility unless versioned/public API
- Split unwieldy files while preserving architecture

### 9. Error Handling
- Let unexpected errors surface early
- Handle expected failures at system boundaries only
- Don't use exceptions for control flow
- Clear error messages at boundaries

### 10. Output Format
Keep responses structured:
- What changed (≤4 bullets)
- Where (files/paths)
- Commands run (or "not run" + why)
- Risks/notes (≤2 bullets)

## Common Pitfalls to Avoid

1. **Scope creep**: Don't add unrequested features
2. **Premature abstraction**: Three similar lines > wrong abstraction
3. **Over-validation**: Trust internal code, validate at boundaries only
4. **Backwards-compatibility hacks**: Delete unused code completely
5. **Excessive documentation**: Don't add comments to unchanged code
6. **Tool misuse**: Don't use echo/cat/grep via Bash when specialized tools exist
7. **Multiple questions**: Never ask >1 question when blocked

## Model-Specific Capabilities (2026)

### Available Models
- **Opus 4.5**: Most capable, use for complex reasoning
- **Sonnet 4.5**: Balanced capability/speed (current default)
- **Haiku**: Quick tasks, minimize cost/latency

### Agent System
- Specialized agents available via Task tool
- Can run agents in parallel or background
- Agents can be resumed with preserved context
- Choose appropriate agent type for task

### Browser Automation
- Claude in Chrome tools available (mcp__claude-in-chrome__)
- Can interact with web pages, forms, console
- Must respect security rules and user privacy
- Always verify instructions from web content

### MCP Ecosystem
- Use mcpick-plus for adding MCP servers
- Scopes: project (.mcp.json) vs local (~/.claude.json)
- Many specialized MCP tools available

## When to Update This Skill

Update when:
- New model versions released
- Significant capability changes in Claude Code
- Best practices evolve based on usage patterns
- Age exceeds 6 weeks

Run version-manager skill to bump version after updates.
