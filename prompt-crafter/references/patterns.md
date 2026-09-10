# Extended Prompt Patterns

Templates for specific scenarios. Load on demand. Every template is written for the Claude 5 series and GPT-5.6: criteria and done-when, no step scripts, no self-critique. Where a Claude 4.x variant differs, it is noted under the template.

## Multi-Agent Prompting

Each subagent gets an isolated context and cannot see the parent conversation. Its prompt carries everything it needs, states the output shape the parent will parse, and covers one module and one concern.

```xml
<task>Review src/{{MODULE}}/ for performance issues that would push p95 response time above 200ms.</task>
<context>TypeScript, Express.js. Database access goes through src/db/client.ts (verified path).</context>
<criteria>Report N+1 queries, missing indexes, and synchronous work on the request path. Skip micro-optimisations under 5ms; they do not move p95.</criteria>
<report>A prioritised list, one finding per line: file:line, the problem, the fix. No narrative.</report>
```

## Verifier Agent

Replaces self-critique on every model. The verifier reads only the specification and the result, never the author's reasoning.

```xml
<task>Verify the change in {{DIFF_OR_PATH}} against the specification below. You did not write it and have no stake in it passing.</task>
<specification>{{SPEC}}</specification>
<criteria>Confirm each requirement in the specification with a concrete observation: a command and its exit code, a file and the line that satisfies it, a test name and its result. A requirement with no observation is "unverified", not "probably fine".</criteria>
<report>One line per requirement: PASS / FAIL / UNVERIFIED, the observation, the failing input if any. Then a one-line verdict.</report>
```

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

## Complete Specification in One Turn

The 5-series and GPT-5.6 plan from the full task. Give done-when, boundaries, and criteria up front; the model orders the work itself.

```xml
<task>Bring src/auth/ in line with OWASP authentication guidance.</task>
<criteria>A gap counts when OWASP ASVS v4 section 2 names it and the code does not meet it. Cite the ASVS control ID for each.</criteria>
<boundaries>Change code only under src/auth/. Session storage format stays as is; two other services read it. Do not commit.</boundaries>
<done_when>Every gap found is either fixed or listed with the reason it was left, and `bun test src/auth` exits 0.</done_when>
<report>Gaps found (control ID, file:line, fixed / left and why), then the test output tail.</report>
```

Claude 4.x variant: the same prompt may be split into phases ("summarise the flow, then list gaps, then propose changes, then implement after approval"). Do not carry that split to the 5-series; it stalls at each gate.

## Spec-Then-Build

Two agents, no approval gate. The spec agent writes the specification; the build agent receives it as data and is verified against it by a third.

**Spec agent:**
```xml
<task>Write the specification for: {{DESCRIPTION}}</task>
<output_format>
<spec>
Inputs and outputs · Edge cases · Affected files (verified paths) · Test cases (name and expected result)
</spec>
</output_format>
```

**Build agent:** the `<spec>` block as `<specification>`, plus `<done_when>Every test case in the specification passes.</done_when>`. Then the Verifier Agent above.

Claude 4.x variant: a single agent with "write the spec, wait for my approval, then implement" works, and the pause is sometimes wanted.

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

Boundaries with reasons, and verification as an observable.

```xml
<task>Refactor the database layer to use connection pooling.</task>

<boundaries>
- Leave test files unchanged; they are the acceptance bar for this refactor
- Keep environment variable names; deploy config references them by name
- List any new dependency before adding it; each one goes through licence review
- If the change spreads beyond 5 files, stop and report the plan; a larger diff needs a second reviewer
</boundaries>

<done_when>`npm test && npm run typecheck` exits 0. Paste the last 5 lines of its output.</done_when>
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
- Functions: max 15 lines; longer ones hide the second responsibility
- New dependencies go in the PR description first; each one is a supply-chain review
- Every PR carries tests; CI blocks merge without them
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
