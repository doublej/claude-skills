# Extended Prompt Patterns

Advanced patterns for specific scenarios. Load on demand.

## Multi-Agent Prompting

When spawning subagents via Task tool, each agent gets an isolated context. Structure their prompts for independence:

```
You are reviewing {{MODULE}} for performance issues.

Context:
- Language: TypeScript
- Framework: Express.js
- Target: Response times under 200ms at p95

Steps:
1. Read all files in src/{{MODULE}}/
2. Profile any database queries (look for N+1, missing indexes)
3. Check for synchronous operations that could be async
4. Report findings as a prioritised list with file:line references
```

Key principles:
- Include all context the agent needs (it cannot see the parent conversation)
- Be explicit about output format (the parent needs to parse/use it)
- Scope narrowly (one module, one concern per agent)

## Debate Pattern (multi-perspective evaluation)

Spawn parallel agents with opposing viewpoints, then synthesise:

**Advocate prompt:**
```
Argue FOR adopting {{APPROACH}} in this codebase.
Consider: developer experience, performance, maintainability, ecosystem support.
Be enthusiastic but cite specific evidence from the code.
```

**Critic prompt:**
```
Argue AGAINST adopting {{APPROACH}} in this codebase.
Consider: migration cost, learning curve, lock-in risk, alternatives.
Be sceptical but fair.
```

**Synthesiser prompt:**
```
Given the advocate and critic perspectives below, make a recommendation.
Weight: 40% technical fit, 30% team impact, 30% maintenance burden.

<advocate>{{ADVOCATE_OUTPUT}}</advocate>
<critic>{{CRITIC_OUTPUT}}</critic>
```

## Progressive Disclosure Prompt

For complex tasks, break the prompt into phases:

```
Phase 1: Read src/auth/ and summarise the current authentication flow.
Phase 2: Identify gaps against OWASP authentication guidelines.
Phase 3: Propose changes (do not implement yet).
Phase 4: After I approve, implement the changes.

Start with Phase 1.
```

## Spec-Driven Development Prompt

From task description to working code via structured specification:

```
Task: {{DESCRIPTION}}

Before implementing:
1. Write a specification in <spec> tags covering:
   - Inputs and outputs
   - Edge cases
   - Affected files
   - Test cases
2. Wait for my approval of the spec
3. Implement following the approved spec
4. Run all tests in the spec
```

## Context Compression Prompt

When working with large codebases, compress context before the main task:

```
Read the following files and create a concise summary (max 200 words)
focusing only on the public API and data flow:
- src/services/payment.ts
- src/services/order.ts
- src/services/inventory.ts

Then, using your summary as context, design a new refund service
that integrates with all three.
```

## Guard Rail Prompt

Prevent common Claude Code mistakes with explicit boundaries:

```xml
<task>Refactor the database layer to use connection pooling.</task>

<guardrails>
- Do NOT modify any test files
- Do NOT change environment variable names
- Do NOT add new dependencies without listing them first
- If a change affects more than 5 files, stop and report your plan
</guardrails>

<verification>
Run: npm test && npm run typecheck
All must pass before reporting completion.
</verification>
```

## Iterative Refinement Prompt

For tasks where first-pass quality matters:

```
Write the migration script for the schema change described in MIGRATION.md.

After writing it:
1. Re-read your script and check for:
   - Missing rollback logic
   - Data loss scenarios
   - Transactions around multi-step operations
2. Fix any issues found
3. Dry-run with: npm run migrate:dry
4. Report the result
```

## Template Variables

Common variables for reusable prompts:

| Variable | Source | Use in |
|----------|--------|--------|
| `$ARGUMENTS` | User input after command name | Slash commands |
| `{{FILE_PATH}}` | Specified by caller | Subagent prompts |
| `{{MODULE}}` | Extracted from task context | Scoped analysis |
| `@path/to/file` | CLAUDE.md imports | Reference loading |

## CLAUDE.md Section Templates

### Minimal Project CLAUDE.md

```markdown
# Project: {{NAME}}

Stack: {{LANGUAGE}} / {{FRAMEWORK}}
Build: `{{BUILD_CMD}}`
Test: `{{TEST_CMD}}`
Lint: `{{LINT_CMD}}`

<change_policy>
Follow existing patterns. Keep changes minimal and focused.
</change_policy>

<rules>
- Functions: max 15 lines
- No new dependencies without discussion
- All PRs need tests
</rules>
```

### Personal CLAUDE.md (~/.claude/CLAUDE.md)

```markdown
<defaults>
Prefer: uv, bun, Svelte, FastAPI.
Use imperative commit messages: "verb: description".
Run the smallest set of checks that gives confidence.
</defaults>

<output_format>
What I changed (max 4 bullets)
Where (file paths)
Commands run (or "not run" + why)
Risks/notes (max 2 bullets)
</output_format>
```

### Rule File (.claude/rules/testing.md)

```markdown
---
paths:
  - "src/**/*.ts"
  - "tests/**/*.ts"
---
Run affected tests after any code change.
Use vitest. Prefer integration tests over unit tests for API endpoints.
Mock only external services, never internal modules.
```
