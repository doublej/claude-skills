---
name: prompt-crafter
description: "Write, improve, or review prompts, CLAUDE.md rules, system prompts, slash commands, skill instructions, and agent briefs. Routes Claude 5, Claude 4.x, GPT-5.6, and generic targets to model-specific lint and pasteable clauses. Use when the deliverable is a prompt or instruction file, not the implementation it describes."
---

# Prompt Crafter

Produce prompts that a model follows on the first run: interactive asks, CLAUDE.md files, AGENTS.md files, system prompts, slash commands, skill instructions, agent briefs, workflow agents, and headless CLI strings (`claude -p`, `codex -q`).

Optional argument (`$ARGUMENTS`): target model. Default: `generic`. In `/prompt-crafter sonnet-5: <request>`, strip the separator colon from the model token; the remaining text is the request. The target is the model that will run the finished prompt, not the model crafting it.

The test for every deliverable: a fresh model, given only the prompt, produces the wanted output without a correction turn. Every step below names its output. Outputs marked *reply* appear in the selected path's output format; the rest are internal artifacts, not narrated reasoning. The authoring reply always includes the Target header, Assumptions, Facts, fenced prompt, Cuts, and Test it line. Writing a command means delivering its template, not executing its task or installing it unless requested.

<scope>
## Step 0 — Scope gate

Output (internal): the deliverable kind, one of prompt, CLAUDE.md, AGENTS.md, system prompt, slash command, skill instruction, agent brief. Only a failed gate reaches the reply, as the one line: `Deliverable: not a prompt (<what it is>), exiting skill`.

The skill applies only when the deliverable is a prompt or instruction file: writing, reviewing, or improving one. If it is not (the skill co-loaded next to a build, audit, research, or artifact task):

1. Say so in one line: "This loaded, but the real deliverable is X, not a prompt."
2. Exit skill mode for the rest of the session and handle the task normally. Do not produce a prompt-shaped consolation artifact.

Multi-phase tasks: the skill governs only the phase that produces a prompt or instruction. Research, git, builds, and orchestration in the same task run normally.

Exception: the user deliberately ran `/prompt-crafter` on a fuzzy task and wants an implementation brief. Produce it, and say that is what you are doing.
</scope>

<model_routing>
## Step 1 — Resolve the target and open its reference

Output (reply): the header line below, written only after the routed file is open.

Resolution order:
1. `$ARGUMENTS` (e.g. `/prompt-crafter opus-5`)
2. Named in conversation, in the draft prompt, or in surrounding code (a model ID string, an SDK call, a `model=` field, an Agent `model:` override)
3. Default: `generic`

| Accepted value | Route | Reference | Checklist items |
|----------------|-------|-----------|-----------------|
| `fable-5`, `fable`, `mythos-5`, `claude-fable-5` | Claude Fable 5 / Mythos 5 | `references/lint-fable-5.md` | 0–22 |
| `opus-5`, `opus`, `claude-opus-5` | Claude Opus 5 | `references/lint-opus-5.md` | 0–18 |
| `sonnet-5`, `sonnet`, `claude-sonnet-5` | Claude Sonnet 5 | `references/lint-sonnet-5.md` | 0–19 |
| `gpt-5.6`, `gpt-5.6-sol`, `sol`, `terra`, `luna` | GPT-5.6 | `references/lint-gpt-5-6.md` | 0–18 |
| `opus-4-8` | Claude Opus 4.8 | `references/lint-opus-4-8.md` | 0–15 |
| `opus-4-7` | Claude Opus 4.7 | `references/lint-opus-4-7.md` | 0–15 |
| `sonnet-4-6` | Claude Sonnet 4.6 | `references/lint-sonnet-4-6.md` | 0–12 |
| `generic` / unspecified | Model-agnostic | `references/lint-generic.md` | 1–8 |

Bare `opus` / `sonnet` resolve to the 5-series. Older models need the version suffix. GPT-5.1 / 5.2: hand off to the `prompt-gpt` skill.

**Multi-model systems** (orchestrator on one model, subagents on another): resolve each component separately and apply that profile to that component's instructions only. Forks inherit the parent model and cannot be overridden.

**Header line**, first line of the final reply on every path:

```
Target: <model> · Reference: references/<file> · Applied: "<one sentence copied verbatim from that file that governed the draft>"
```

The quote is a sentence that exists in the file, not a paraphrase of it. Copy from the opened file, not this skill or memory. Record its checklist item number internally and apply that item to the draft; a decorative quote is not evidence of application.

**Placeholders** in lint files are inferred, not asked:

| Placeholder | Source |
|-------------|--------|
| `<<AGENTIC>>`, `<<RUN_SHAPE>>`, `<<RISK_PROFILE>>` | The task's shape: `AGENTIC=yes` when the prompt directs tool use, phases, or dispatch; `RUN_SHAPE=long-horizon autonomous` for a `claude -p` string, run brief, or workflow agent, else `interactive`; `RISK_PROFILE=medium` unless the prompt touches prod, money, or deletion |
| `<<TOOLS>>`, `<<WEB_ENABLED>>`, `<<SUBAGENTS>>`, `<<MEMORY>>` | The harness or supplied configuration only: an SDK `tools` list, an Agent definition, a workflow `opts`, settings, or the user stating it. A task that mentions searching or phases does not make web or subagents available. When nothing states it: `unknown`; conditional items get `n/a: capability unstated`, and the Assumptions line names what the prompt presumes |
| `<<EFFORT>>`, `<<THINKING>>`, `<<MAX_TOKENS>>` | The API call or config; else `unset` |

For placeholders outside this table, use supplied configuration or `unknown` (`unset` for unspecified settings). `<<PROMPT>>` is the draft itself; identify it as supplied or newly authored rather than duplicating it in Assumptions. Ask only if no safe default preserves the requested deliverable.

**Which path:** "lint", "rewrite", "improve", or "fix" an existing prompt runs `<lint_path>`. "Review", "look at", "is this good", or a pasted prompt with a question runs `<feedback_path>`. Writing a new prompt runs `<authoring_path>`. Open the routed lint file on every path, including a one-line generic prompt. When authoring, use its checklist and pasteable clauses as source material; its lint-only deliverable does not switch paths. The routed 5-series lint file wins over this skill on disagreements about model guidance.
</model_routing>

<feedback_path>
## Feedback path

Output (reply): the header line, then findings ranked by effect on the first run, each one line: the issue, the line it sits on, the fix. At most 7. A prompt with nothing worth changing gets one line: `No changes needed: <what makes it work>`. No rewrite or checklist table. Stop after the findings; do not add an options menu.
</feedback_path>

<lint_path>
## Lint path

Output (reply): header and Assumptions, then the routed file's four sections. This format applies only to linting an existing prompt.

1. **Resolve inputs** → Output (internal): supplied draft and values for every placeholder in the opened file. Output (reply): one `Assumptions:` line under the header; label unknown capabilities rather than inventing them.
2. **Evaluate** → Output (reply): Summary verdict and Checklist results. Include every numbered item in the routed range, in order: PASS, WARN, FAIL, or `n/a` with a concrete reason. Unknown configuration is not evidence of a passing configuration check.
3. **Repair** → Output (reply): Minimal rewritten prompt in one fence, or `No changes needed`. Preserve user scope; config findings stay outside the prompt unless configuration is itself the deliverable.
4. **Record evidence** → Output (reply): Change evidence, at most five bullets mapping changed clauses to checklist items and a concrete acceptance observation. Do not claim a trial ran unless it did. Stop after section 4; no extra self-review phase or literal STOP token.
</lint_path>

<authoring_path>
## Authoring path

1. **Pin the task** → Output (internal, summarised in `Assumptions:`): surface from `<surfaces>`, requested deliverable, target, and any consequential default. Choose a reasonable default for reusable templates; ask only if the missing answer prevents a usable prompt.
2. **Ground embedded facts** → Output (reply): `Facts:` with each repo-specific name and its source (file:line or tool result). Distinguish verified facts, user-supplied literals, proposed output paths, and runtime inputs. A user-supplied `src/` is a requested scope, not proof that it exists here. For a reusable command, defer repo discovery to its execution; do not inspect an unrelated authoring repo or invent its test runner. If no repo facts are embedded: `Facts: none embedded` (append user-supplied scope or runtime inputs when present). Unavailable reads produce a labelled assumption and a runtime check, never a fabricated fact.
3. **Frame success** → Output (internal, included in the prompt): deliverable, scope, output shape, appropriate length, and observable stop condition. Define ambiguous labels operationally (for example, missing test association differs from zero measured coverage).
4. **Draft** → Output (reply): one ready-to-paste prompt using the selected surface. Carry the full task and required inputs; examples, if needed, demonstrate an otherwise ambiguous case. Runtime variables are allowed only when the prompt defines their source and empty-value behaviour.
5. **Apply the reference** → Output (internal): applicable item numbers, exact source clauses, filled slots, and deletions. Output (visible in the prompt): only clauses that change behaviour for this task, copied from the routed lint or an explicitly opened supporting reference. An already explicit rule needs no duplicate model clause. Conditions concern the future executor's task and capabilities, not the author's tools. Configuration-only findings are not prose instructions.
6. **Cut** → Output (reply): `Cuts:` with at most five removed rules and their reason, or `none`. Preserve every requirement that changes correctness; length targets never justify truncating the task or the reply contract.
7. **Emit** → Output (reply): exactly `<output_contract>` (multiple fences only when the user requests multiple instruction files). Fill every field before sending. A missing header, Facts, or Test it is an incomplete deliverable, even if the fenced prompt is good.
</authoring_path>

<principles>
## Craft principles

Output (internal): a draft that satisfies these criteria across every section and example; defects are fixed in the draft, not reported as a promised follow-up.

- **Observable success.** Name what appears, in what shape, and when work ends. Use a meaningful cap (one row per file, one paragraph per finding); arbitrary caps must not hide required results.
- **Complete task.** Provide intent, inputs, constraints, and done-when in one turn. Preserve existing authorisation. Add a question only where the answer changes the work and no safe default suffices.
- **Reasons and scope.** Explain non-obvious constraints; state which files, sections, or cases each rule covers. A reason must be supplied or grounded, never an invented CI or business policy.
- **Actionable wording.** Say what to do. Keep prohibitions for real boundaries, such as read-only inspection. Use normal-strength language.
- **Decision criteria.** Specify what counts; prescribe order only for real dependencies. Keep required tests and observable checks, remove generic self-critique and scripted internal reasoning on the 5-series.
- **Examples only when useful.** An example teaches a hard format or edge case. It must match all rules, including evidence requirements and empty results; no quota of examples.
- **Data boundaries.** Label untrusted input as data. In long prompts, put documents before the task; for a short prompt, lead with the task. Use XML only where it clarifies multiple components.
- **Lean scope.** Remove platitudes, redundant examples, repeated rules, and unsupported model claims. Soft drafting targets: interactive ask 5 lines, slash command 30, system prompt 150, CLAUDE.md / AGENTS.md 200. Completeness wins over these targets.
- **Bounded tools.** Name only available capabilities; supply a fallback for missing required access. For agentic work define permitted actions, an appropriate stop condition, and what a blocked result contains. Add budgets or delegation only when the task warrants them.
</principles>

<model_profiles>
## Model clauses come from the routed file

Output (internal): the applicable checklist items and their pasteable wording, read directly from `references/lint-<target>.md`. This section deliberately does not duplicate those clauses: opening the reference supplies both the header quote and the actual model-specific instruction.

Paste only when the item's condition holds and the draft lacks an equivalent control. Fill task slots without changing the surrounding wording. Delete irrelevant scaffolding rather than adding counter-rules. If no model clause helps, retain the task-specific draft and use an applied deletion or criterion for the header quote.

Treat effort, thinking, sampling, tokenizer limits, tool versions, and SDK fields as harness configuration. When the requested artifact includes such settings, verify them against supplied configuration or current official documentation and record the source; do not silently set unavailable knobs or turn guesses into API facts. For a slash-command template, omit unrelated API guidance.

For shared clauses, optionally open `references/clauses.md`; output (internal): chosen key plus exact clause, with its filled wording in the draft. For every optional reference below, opening it must produce a selected pattern and a concrete piece of the deliverable; do not read references merely to claim compliance.
</model_profiles>

<output_contract>
## Output contract (authoring path)

The labels below are outside the prompt fence. The first line is the header, and Test it is the last line. Explanatory placeholders below must be filled; runtime variables inside a reusable template keep their documented syntax.

````text
Target: <model> · Reference: references/<file> · Applied: "<sentence copied from the opened file>"
Assumptions: <surface; consequential defaults; executor capabilities presumed; unknown/unset settings relevant to the task>
Facts: <grounded repo facts and sources; or none embedded, with user-supplied literals/runtime inputs labelled>

```markdown
<complete ready-to-paste prompt>
```

Cuts: <removed rules and reasons, at most five; or none>
Test it: <exact invocation or message and the expected observable result; label as proposed unless actually run>
````

For slash commands, include the proposed save path in Assumptions so the invocation is usable. Test it describes a concrete acceptance run, including setup if needed, without requiring the author to execute the generated task. A filename heuristic alone cannot prove code has no coverage; reflect that distinction in the prompt and its test.
</output_contract>

<surfaces>
## Prompt surfaces

| Surface | Format | Key constraint |
|---------|--------|----------------|
| Interactive session | Natural language | Builds on context; state only the delta |
| CLAUDE.md | Flat markdown + XML sections | Loaded every session; every line is paid every turn |
| AGENTS.md | Markdown hierarchy, cascading | Merges down directory tree; `AGENTS.override.md` replaces parent rules |
| Slash command | Markdown template, `$ARGUMENTS` | Single purpose; `description:` frontmatter drives autocomplete |
| CLI (`claude -p`) | Single string or piped input | No follow-up; must carry facts, scope, done-when, and permission mode |
| Codex CLI / exec | Single string, flags (`-q`, `-a`) | Non-interactive execution; declare approval mode, sandbox bounds, and JSON schema |
| System prompt / API | XML-structured | Parsed programmatically; role, boundaries, output contract |
| Skill SKILL.md | Frontmatter + markdown | Description is the trigger; body under 500 lines; required reads produce an output that proves the read |
| Dispatch prompt / agent brief | XML task + constraints, one mission per agent | Self-contained (the agent has no history); every path verified; return conclusions, not file dumps |
| Workflow agent (script) | XML role + criteria + constraints | Shared BRIEF injected into every downstream agent; label/phase/effort set; schema for structured output |
</surfaces>

<patterns>
## Optional patterns

Use plain language for a short task. For a format the model cannot infer, open `references/xml-patterns.md`; output (internal): the selected example's name and a filled data/output boundary in the prompt. For an authorised multi-agent workflow or reusable project instructions, open `references/patterns.md`; output (internal): selected template name and its filled task/report contract. Example paths are illustrative, never verified facts about the user's repo.
</patterns>

<claude_md>
## CLAUDE.md

Output (reply, inside the prompt fence): project instructions containing only grounded commands and relevant rules. State precedence if rules can collide. Put scope-specific rules in the intended rule file, with `paths:` frontmatter; list each proposed file path outside its fence if the user requests multiple files. Keep imports resolvable from the destination and verify referenced files before claiming they exist. Use headings or flat XML for independent concerns; don't fill a fixed section inventory with boilerplate.
</claude_md>

<agents_md>
## AGENTS.md

Output (reply, inside the prompt fence): project or subsystem instructions containing verified build/test commands, environment constraints, and path boundaries. Respect the cascading hierarchy: `~/.codex/AGENTS.md` (global user) → `<repo>/AGENTS.md` (repo root) → `<subsystem>/AGENTS.md` (directory-specific rules). If a directory contains `AGENTS.override.md`, it completely replaces the inherited `AGENTS.md` chain for that directory. Do NOT use Claude-style glob frontmatter (`paths: [...]`) in `AGENTS.md`; Codex scoping is strictly directory-hierarchical. Keep rules terse, verified, and actionable.
</agents_md>

<slash_command>
## Slash command and CLI

Output (reply, inside the prompt fence): a complete Markdown template beginning with `description:` YAML frontmatter. Output (`Assumptions:`): proposed `.claude/commands/<name>.md` save path. If `$ARGUMENTS` is useful, define its meaning and default; omit it when the user's scope is fixed. Treat arguments as data, not shell code.

For inspection commands, specify the candidate set, evidence that includes or excludes a candidate, read-only boundaries, missing-access behaviour, empty-result text, and the final list shape. Discover the future repo's test configuration and tests wherever configured, not only beside source files. Distinguish confirmed zero coverage from no identified test association; imports, shared test helpers, integration tests, and differently named test files can invalidate filename-only guesses. Report inconclusive cases separately and avoid silently omitting files.

For CLI prompts, deliver a safely quoted invocation or stdin text. It must carry its inputs, scope, done-when, and blocked-result behaviour because there may be no follow-up. For Claude Code (`claude -p`), specify `--permission-mode` (`acceptEdits` or `plan`) and scope tools via `--allowedTools`; never add `--permission-mode bypassPermissions` without isolated sandboxing. For Codex CLI (`codex -q` or `codex exec`), declare approval mode (`-a suggest`, `auto-edit`, or `full-auto`), sandbox boundaries (`--cd`, `--add-dir`), and structured `--json` extraction. Do not add permission-bypass flags as boilerplate.
</slash_command>

<xml_reference>
## XML tags

| Tag | Use for |
|-----|---------|
| `<task>` | The specific thing to do |
| `<context>` | Background the model needs and would not infer |
| `<data>` / `<document>` | Input content, separated from instructions |
| `<examples>` / `<example>` | Few-shot demonstrations |
| `<constraints>` / `<boundaries>` | Limits, with reasons |
| `<done_when>` | Observable completion condition |
| `<output_format>` | Shape of the response |
| `<role>` / `<behaviour>` | Identity and observable behaviours |

Refer to data tags by name in the consuming instruction. Output (internal): each data block has a matching consumer and is labelled as data; output tags have a defined schema. Use only the nesting needed for that structure. XML is a boundary aid, not a guarantee that arbitrary embedded input is trusted.
</xml_reference>

## References

- Required on every path: the target's lint file from the unchanged routing table (`references/lint-<target>.md`).
- Optional shared wording: `references/clauses.md` → selected key and pasted clause (Codex approval/sandbox modes, Claude permissions/tool restrictions, subagent handoff, done-when, boundaries).
- Optional XML & JSON examples: `references/xml-patterns.md` → selected pattern and filled structure (evidence extraction, document comparison, structured agent JSON output schema for CLI/SDK, tool-call interceptor guard).
- Optional workflow/project templates: `references/patterns.md` → selected template and filled contract (`CLAUDE.md`, `AGENTS.md` hierarchy/overrides, Codex/Claude headless CLI automation, Claude Agent SDK subagents/hooks, environment hygiene).
