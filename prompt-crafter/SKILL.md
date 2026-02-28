---
name: prompt-crafter
description: Craft effective prompts for Claude Code — interactive sessions, CLAUDE.md files, system prompts, and CLI automation. Use when writing or improving prompts, structuring context, authoring CLAUDE.md rules, or optimising prompt performance. Covers prompt patterns, context engineering, few-shot design, chain-of-thought, reflexion, and token efficiency.
---

# Prompt Crafter

Craft high-quality prompts for Claude Code across all surfaces: interactive sessions, CLAUDE.md files, system prompts, slash commands, and CLI automation.

## Workflow

1. **Clarify intent** — What surface? (interactive, CLAUDE.md, CLI, slash command, API)
2. **Select pattern** — Match the task to a prompt pattern
3. **Structure context** — Apply the context hierarchy
4. **Draft prompt** — Write using the appropriate template
5. **Optimise** — Compress tokens, remove redundancy, add examples if needed
6. **Verify** — Self-check with the reflexion checklist

## Prompt Surfaces

| Surface | Format | Key constraint |
|---------|--------|----------------|
| Interactive session | Natural language | Conversational, builds on context |
| CLAUDE.md | Structured markdown + XML | Loaded every session, token budget matters |
| Slash command | Markdown template | Single-purpose, may accept `$ARGUMENTS` |
| CLI (`-p` flag) | Single string or piped input | No follow-up, must be self-contained |
| System prompt / API | XML-structured | Parsed programmatically, needs tags |
| Skill SKILL.md | Frontmatter + markdown | Progressive disclosure, must trigger correctly |

## Prompt Patterns

### 1. Direct Instruction (zero-shot)

Best for: simple, unambiguous tasks Claude already knows how to do.

```
Rename all snake_case variables in src/utils.ts to camelCase. Run the linter after.
```

Rules:
- Be specific about scope (which files, which variables)
- State the verification step
- No preamble needed

### 2. Few-Shot (examples)

Best for: tasks requiring a specific output format or style Claude can't infer.

```xml
<task>Convert changelog entries to release notes.</task>

<examples>
<example>
<input>fix: resolve race condition in WebSocket reconnect (#412)</input>
<output>Fixed a race condition that could cause dropped messages during WebSocket reconnection.</output>
</example>
<example>
<input>feat: add batch export for CSV and JSON (#389)</input>
<output>You can now export multiple items at once in CSV or JSON format.</output>
</example>
</examples>

<data>
{{CHANGELOG_ENTRIES}}
</data>
```

Rules:
- 2-3 diverse examples cover most cases
- Show edge cases if the format has tricky variations
- Keep examples representative, not exhaustive

### 3. Chain of Thought (CoT)

Best for: multi-step reasoning, analysis, debugging, architectural decisions.

**Basic** — just add a thinking nudge:
```
Diagnose why the login flow fails on Safari. Think step-by-step before suggesting a fix.
```

**Guided** — specify reasoning steps:
```
Before implementing the caching layer:
1. Identify which endpoints are called most frequently
2. Estimate payload sizes and TTL requirements
3. Evaluate Redis vs in-memory trade-offs for this scale
4. Propose the minimal implementation

Then implement your recommendation.
```

**Structured** — separate thinking from output:
```
Analyse the database schema for normalisation issues.
Put your reasoning in <thinking> tags.
Put your recommendations in <recommendations> tags.
```

### 4. Context Priming

Best for: starting a session with full project awareness.

```
Read README.md, then run git ls-files to understand the project structure.
Focus on: $ARGUMENTS
```

Use this as a slash command (`.claude/commands/prime.md`) to bootstrap sessions.

### 5. Reflexion (self-refinement)

Best for: improving output quality through critique loops.

```
Implement the feature, then reflect:
1. Does the implementation match the requirements?
2. Are there edge cases I missed?
3. Is there unnecessary complexity?
Fix any issues you find.
```

For deeper reflexion, use multi-perspective evaluation:
```
After implementing, evaluate from three angles:
- Correctness: Does it handle all specified inputs?
- Simplicity: Can any part be removed without losing functionality?
- Consistency: Does it follow the patterns in the existing codebase?
```

### 6. Constraint-Bounded

Best for: tasks where Claude tends to over-produce or drift.

```xml
<task>Refactor the payment module.</task>
<constraints>
- Touch only files in src/payments/
- Do not change the public API
- Maximum 3 new files
- Keep functions under 15 lines
</constraints>
```

### 7. Role + Behaviour

Best for: system prompts, CLAUDE.md, sustained behaviour across a session.

```xml
<role>You are a senior backend engineer specialising in distributed systems.</role>
<behaviour>
- Investigate before suggesting changes
- Cite line numbers when referencing code
- Prefer battle-tested patterns over novel approaches
</behaviour>
```

## Context Hierarchy for CLAUDE.md

Structure your CLAUDE.md from broadest to most specific:

```
1. Identity / role          — WHO Claude is in this project
2. Change policy            — HOW to approach modifications
3. Engineering rules        — WHAT standards to follow
4. Tooling preferences      — WHICH tools and packages to use
5. Quality gates            — WHEN and how to verify
6. Git discipline           — HOW to commit and branch
7. Output format            — SHAPE of responses
```

### CLAUDE.md Authoring Rules

- **Be specific**: "Use 2-space indentation in .ts files" beats "format code properly"
- **Use XML sections** for grouping: `<engineering_rules>`, `<change_policy>`, etc.
- **State precedence**: Define which instructions override which
- **Include commands**: Build, test, lint commands save repeated lookups
- **Budget tokens**: The file loads every session — every line costs across all conversations
- **Use @imports** for large references: `@docs/api-conventions.md`

### Path-Specific Rules

Use `.claude/rules/*.md` with YAML frontmatter for scoped instructions:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
All API endpoints must validate input with zod schemas.
Use the standard error response format from src/api/errors.ts.
```

## Token Optimisation

| Technique | Before | After |
|-----------|--------|-------|
| Remove hedging | "You should probably consider using..." | "Use..." |
| Imperative form | "It would be good if you could..." | "Do X." |
| Merge duplicates | Same rule stated in 3 sections | State once, reference |
| Use @imports | 200-line API docs inline | `@docs/api.md` |
| Cut obvious | "Write clean, readable code" | (Claude does this by default) |
| Examples over explanation | 50 words describing format | 1 concrete example |

**Challenge each line**: "Does Claude really need this, or does it already know?"

## XML Tag Quick Reference

| Tag | Use for |
|-----|---------|
| `<task>` | The specific thing to do |
| `<context>` | Background information |
| `<data>` | Input data (separate from instructions) |
| `<examples>` | Few-shot demonstrations |
| `<constraints>` | Boundaries and limits |
| `<thinking>` / `<answer>` | CoT separation |
| `<output_format>` | Desired response structure |
| `<role>` | Identity / expertise |
| `<rules>` | Hard requirements |

Always reference tags in instructions: "Using the data in `<data>` tags, ..."

## Slash Command Template

For reusable prompts, create `.claude/commands/<name>.md`:

```markdown
Analyse the test coverage for $ARGUMENTS.

1. Find all test files related to the target
2. Identify untested code paths
3. Suggest specific test cases to add

Output as a checklist of missing tests with file paths.
```

`$ARGUMENTS` gets replaced with whatever the user types after the command name.

## CLI Prompt Patterns

Self-contained prompts for `claude -p`:

```bash
# One-shot task
claude -p "find and fix all TODO comments in src/" \
  --permission-mode acceptEdits

# Scoped analysis
claude -p "review src/auth/ for security issues" \
  --allowedTools "Read,Grep"

# Chained sessions
sid=$(claude -p "analyse the API structure" --output-format json | jq -r '.session_id')
claude -r "$sid" -p "now add input validation to all POST endpoints" \
  --permission-mode acceptEdits
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Vague scope | "Improve the code" | "Refactor `parseConfig` to reduce nesting to 1 level" |
| Instructions inside data tags | Confuses data/instruction boundary | Separate `<data>` and `<task>` |
| Restating Claude's defaults | Wastes tokens | Only state what deviates from default |
| Over-nesting XML (>3 levels) | Reduces clarity | Flatten or use @imports |
| No verification step | No confidence in output | "Run tests after" / "Verify with ..." |
| Giant monolithic prompt | Hard to maintain, debug | Split into slash commands or CLAUDE.md sections |

## Verification Checklist

Before finalising any prompt, check:

- [ ] **Clear scope** — Does it say exactly what to change and where?
- [ ] **Right pattern** — Is the prompt pattern matched to the task complexity?
- [ ] **Minimal tokens** — Can any line be removed without losing meaning?
- [ ] **Examples present** — If output format matters, is there at least one example?
- [ ] **Verification included** — Does it specify how to confirm success?
- [ ] **No defaults restated** — Are you only adding what Claude doesn't already know?

## References

- For deep XML tag patterns: use the `xml-prompt` skill
- For CLAUDE.md optimisation: use the `claude-md-optimizer` skill
- For CLI automation patterns: use the `claude-skill` skill
- Extended patterns and examples: `references/patterns.md`
