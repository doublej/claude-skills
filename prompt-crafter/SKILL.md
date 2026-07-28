---
name: prompt-crafter
description: "Write/improve prompts, CLAUDE.md rules, system prompts, few-shot, CoT design, XML-structured prompts, with model-specific guidance for Claude 5 (Fable/Opus/Sonnet), Claude 4.x, and GPT-5.6. Use when the deliverable is a prompt, CLAUDE.md, system prompt, slash command, or skill instruction. Triggers on 'write a prompt', 'improve this prompt', 'lint my prompt', 'XML prompt', 'system prompt', 'CLAUDE.md rules', 'prompt for opus 5', 'prompt for sonnet 5', 'fable prompt', 'gpt-5.6 prompt'."
---

# Prompt Crafter

Craft high-quality prompts across all surfaces: interactive sessions, CLAUDE.md files, system prompts, slash commands, and CLI automation.

Optional argument (`$ARGUMENTS`): target model. See `<model_routing>` for accepted values. Default: `generic`.

<scope>
## Step 0 — Scope check (do this first, before anything else)

Before applying any prompt pattern, confirm the **deliverable is a prompt or instruction** — writing, reviewing, or improving a prompt, CLAUDE.md, system prompt, slash command, skill description, or agent prompt.

**If it is not** (the skill co-loaded incidentally alongside a broader task — an HTML artifact, codebase audit, research, app design, a feature build):

1. State the mismatch in one line: "This loaded, but the real deliverable is X, not a prompt."
2. **Exit skill mode.** Stop applying prompt patterns and handle the task with the right tool as a normal engineering task. Do not produce a prompt-shaped artifact (design brief, instruction doc) as a consolation deliverable just because the skill is open.

Only exception: if the user *intentionally* invoked `/prompt-crafter` for a fuzzy/large task and an implementation brief is genuinely what they want, you may produce it — but say so explicitly and confirm that's the intent rather than defaulting to it.
</scope>

<model_routing>
## Step 1 — Resolve the target model

Do this for **both** paths — writing a new prompt and linting an existing one. Model-specific guidance is conditional: it only applies once a target is resolved.

Resolution order:
1. `$ARGUMENTS` if provided (e.g. `/prompt-crafter opus-5`)
2. Stated in conversation, or named inside the draft prompt / surrounding code (a model ID string, an SDK call, a `model=` field)
3. Default: `generic`

| Accepted value | Route | Reference |
|----------------|-------|-----------|
| `fable-5`, `fable`, `mythos-5`, `claude-fable-5` | Claude Fable 5 / Mythos 5 | `references/lint-fable-5.md` |
| `opus-5`, `opus`, `claude-opus-5` | Claude Opus 5 | `references/lint-opus-5.md` |
| `sonnet-5`, `sonnet`, `claude-sonnet-5` | Claude Sonnet 5 | `references/lint-sonnet-5.md` |
| `gpt-5.6`, `gpt-5.6-sol`, `sol`, `terra`, `luna` | GPT-5.6 | `references/lint-gpt-5-6.md` |
| `opus-4-8` | Claude Opus 4.8 | `references/lint-opus-4-8.md` |
| `opus-4-7` | Claude Opus 4.7 | `references/lint-opus-4-7.md` |
| `sonnet-4-6` | Claude Sonnet 4.6 | `references/lint-sonnet-4-6.md` |
| `generic` / unspecified | Model-agnostic | `references/lint-generic.md` |

Bare `opus` / `sonnet` resolve to the **5-series**. Older models need the explicit version suffix.
For GPT-5.1 / 5.2 targets, hand off to the `prompt-gpt` skill instead.

### Lint + Rewrite

When the user asks to **improve, review, or lint a prompt**: read the routed reference, substitute `<<PLACEHOLDERS>>` with user-provided values (ask if critical ones are missing), then apply the lint + rewrite workflow inline. The templates are self-contained instructions — follow them exactly.

### New prompt authoring

When **writing** a prompt, do not load the full lint template. Apply the `<model_profiles>` deltas below on top of the base patterns, and load the routed reference only if the prompt is agentic, long-horizon, or the user asks for a full review.
</model_routing>

<model_profiles>
## Step 2 — Apply the model profile (conditional)

Base patterns below are model-agnostic. These deltas override them for the resolved target. If the target is `generic`, skip this section entirely.

| Target | Apply | Delete |
|--------|-------|--------|
| **Claude Opus 5** | Explicit conciseness instruction (effort does **not** shorten visible output); deliverable-length calibration; scope-discipline clause; subagent cap; correction-narration limit | Verification instructions ("double-check", "verify before responding", "use a subagent to verify"); forced-progress scaffolding; any "delegate more" guidance |
| **Claude Sonnet 5** | Explicit scope on instructions meant to generalise (it will not infer); tool-triggering nudge when thinking is off; concrete design specs or propose-4-directions; coverage-first code review | Forced-progress scaffolding; `temperature`/`top_p`/`top_k` (400); `budget_tokens` (400); holdover 4.6 style directives |
| **Claude Fable 5** | Anti-gold-plating clause; anti-overplanning clause; progress-claim grounding; explicit boundaries; checkpoint rule; memory surface; async subagent delegation | Step-by-step scaffolding written for older models; any "show your reasoning" instruction (triggers `reasoning_extraction` refusal); all `thinking` config; assistant prefill |
| **GPT-5.6** | Autonomy boundaries naming safe local actions; concrete tone choices; what a short answer must still contain; task-specific PTC routing | Duplicated instructions and redundant examples (10–15% eval gain, 41–66% fewer tokens); broad brevity instructions carried from 5.5; "ask first" on already-safe actions; irrelevant tools |

**Shared across the Claude 5 series:** adaptive thinking (no `budget_tokens`), no sampling parameters, no last-assistant-turn prefill, `thinking.display` defaults to `"omitted"`, effort ladder `low`→`max`. Sweep low/medium before assuming high — all three punch above their tier at reduced effort.

**Cross-cutting inversion:** on the 5-series, "tell the model to self-check" and "enumerate every step" are anti-patterns, not best practices. Cutting instructions is usually the higher-yield edit.
</model_profiles>

<workflow>
---

## Workflow (new prompt creation)

1. **Clarify intent** — What surface? (interactive, CLAUDE.md, CLI, slash command, API)
2. **Resolve the target model** — see `<model_routing>`
3. **Select pattern** — Match the task to a prompt pattern
4. **Structure context** — Apply the context hierarchy
5. **Draft prompt** — Write using the appropriate template
6. **Apply the model profile** — layer the `<model_profiles>` deltas on top; skip if target is `generic`
7. **Optimise** — Compress tokens, remove redundancy, add examples if needed
8. **Verify** — Self-check with the reflexion checklist
</workflow>

<surfaces>
## Prompt Surfaces

| Surface | Format | Key constraint |
|---------|--------|----------------|
| Interactive session | Natural language | Conversational, builds on context |
| CLAUDE.md | Structured markdown + XML | Loaded every session, token budget matters |
| Slash command | Markdown template | Single-purpose, may accept `$ARGUMENTS` |
| CLI (`-p` flag) | Single string or piped input | No follow-up, must be self-contained |
| System prompt / API | XML-structured | Parsed programmatically, needs tags |
| Skill SKILL.md | Frontmatter + markdown | Progressive disclosure, must trigger correctly |
| Workflow agent (script) | XML role + CoT + constraint-bounded | Inject a shared context BRIEF into all downstream agents; set label/phase/effort opts; return raw data not prose; use a schema for structured output |
</surfaces>

<patterns>
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
</patterns>

<constraint_patterns>
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
</constraint_patterns>

<role_patterns>
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
</role_patterns>

<context_hierarchy>
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
</context_hierarchy>

<authoring>
### CLAUDE.md Authoring Rules

- **Be specific**: "Use 2-space indentation in .ts files" beats "format code properly"
- **Use XML sections** for grouping: `<engineering_rules>`, `<change_policy>`, etc.
- **State precedence**: Define which instructions override which
- **Include commands**: Build, test, lint commands save repeated lookups
- **Budget tokens**: The file loads every session — every line costs across all conversations
- **Use @imports** for large references: `@docs/api-conventions.md`
- **Mind the formatting**: flat sections, one instruction per line, sparing emphasis — see worked
  good/bad examples in `../claude-md-optimizer/references/formatting-examples.md`
</authoring>

<path_rules>
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
</path_rules>

<token_optimization>
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
</token_optimization>

<xml_reference>
## XML Tag Quick Reference

| Tag | Use for |
|-----|---------|
| `<task>` | The specific thing to do |
| `<instructions>` | Task steps Claude must follow |
| `<context>` | Background information |
| `<data>` | Input data (separate from instructions) |
| `<document>` | Long content (PDFs, reports, code) |
| `<examples>` | Few-shot demonstrations |
| `<constraints>` | Boundaries and limits |
| `<thinking>` / `<answer>` | CoT separation |
| `<output_format>` | Desired response structure |
| `<formatting_example>` | Output template / desired structure |
| `<role>` | Identity / expertise |
| `<rules>` | Hard requirements |

Always reference tags in instructions: "Using the data in `<data>` tags, ..."
Deep dive (10-component framework, long-context structure, chaining, validation checklist): `references/xml-patterns.md`
</xml_reference>

<slash_command>
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
</slash_command>

<cli_patterns>
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
</cli_patterns>

<anti_patterns>
| Avoid | Why | Instead |
|-------|-----|---------|
| Vague scope | "Improve the code" | "Refactor `parseConfig` to reduce nesting to 1 level" |
| Instructions inside data tags | Confuses data/instruction boundary | Separate `<data>` and `<task>` |
| Restating Claude's defaults | Wastes tokens | Only state what deviates from default |
| Over-nesting XML (>3 levels) | Reduces clarity | Flatten or use @imports |
| No verification step | No confidence in output | "Run tests after" / "Verify with ..." |
| Giant monolithic prompt | Hard to maintain, debug | Split into slash commands or CLAUDE.md sections |
</anti_patterns>

<verification>
## Verification Checklist

Before finalising any prompt, check:

- [ ] **Clear scope** — Does it say exactly what to change and where?
- [ ] **Right pattern** — Is the prompt pattern matched to the task complexity?
- [ ] **Minimal tokens** — Can any line be removed without losing meaning?
- [ ] **Examples present** — If output format matters, is there at least one example?
- [ ] **Verification included** — Does it specify how to confirm success?
- [ ] **No defaults restated** — Are you only adding what Claude doesn't already know?
- [ ] **Model profile applied** — If a target model was resolved, are its deltas layered on (including the deletions)?
</verification>

## References

- Model-specific lint templates: `references/lint-<target>.md` — see `<model_routing>` for the map
- For deep XML tag patterns: `references/xml-patterns.md`
- For GPT-5.1 / 5.2 targets: use the `prompt-gpt` skill
- For CLAUDE.md optimisation: use the `claude-md-optimizer` skill
- For CLAUDE.md/AGENT.md formatting (good vs bad examples): `../claude-md-optimizer/references/formatting-examples.md`
- For CLI automation patterns: use the `claude-headless` skill
- Extended patterns and examples: `references/patterns.md`
