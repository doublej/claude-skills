# Claude Code Best Practices

> Anchored to Anthropic's official prompting guide (originally scoped to the Claude 4.x family; see 5-series deltas below).
> Source (4.x anchor): https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
> Source (5-series behavior shifts): prompt-crafter/references/lint-opus-5.md, lint-sonnet-5.md, lint-fable-5.md
> Currency is tracked by `best_practices_date` in METADATA.json — update it (not a date in this filename) when revising.

A CLAUDE.md is a persistent system prompt. The model behaviors below are what changed
with the Claude 5 series (Fable 5.1, Opus 5, Sonnet 5): they directly affect how a good CLAUDE.md is written.

## Models

| Model | ID | Use for |
|-------|-----|---------|
| Fable 5.1 | `claude-fable-5-1` | Most intelligent generally available model (Mythos-class tier, above Opus); Claude Mythos 5.1 is the same underlying model, available only to approved orgs; extra safety measures for dual-use capabilities. |
| Opus 5 | `claude-opus-5` | Default when Fable 5.1 isn't available; verifies its own work unprompted, delegates to subagents readily. |
| Sonnet 5 | `claude-sonnet-5` | Follows instructions literally, doesn't generalize scope on its own; agentic by default, less tool-eager only with thinking off. |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Quick/cheap, subagents, latency-sensitive. Still the current Haiku. |

- Most recent family is the Claude 5 series. Default new AI apps to the latest, most capable model: `claude-fable-5-1`, or `claude-opus-5` where Fable isn't available.
- Hardcoded superseded names/IDs ("Opus 4.5", "Opus 4.6", "Opus 4.7", "Opus 4.8", "Sonnet 4.5", "Sonnet 4.6", `claude-opus-4-7`, `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-sonnet-4-5-...`) are a red flag: flag them.

## High-impact CLAUDE.md review checklist (5-series behavior shifts)

These are the most common ways an older CLAUDE.md now mis-steers the model.

### 1. Dial back aggressive emphasis — the #1 stale pattern
The Claude 5 series (Opus 5, Sonnet 5, Fable 5.1) is still far more responsive to the system prompt
than models before Claude 4.5, so prompts tuned to fix *under*-triggering now cause *over*-triggering. Replace
shouty directives with normal phrasing.
- ❌ `CRITICAL: You MUST always use this tool when...` / `NEVER do X` / `ALWAYS do Y`
- ✅ `Use this tool when...`
Flag pervasive ALL-CAPS / MUST / ALWAYS / NEVER / CRITICAL. Keep emphasis only for genuine safety rails.

### 2. Tell Claude what to do, not what not to do
Positive instructions and positive examples steer better than prohibitions.
- ❌ `Do not use markdown` → ✅ `Write in smoothly flowing prose paragraphs.`
- ❌ `NEVER use ellipses` → ✅ `…because the output is read by TTS that can't pronounce them.`

### 3. Add the *why*
Stating the motivation behind a rule lets the model generalize correctly. A one-clause rationale
("…so the diff stays reviewable") beats a bare imperative.

### 4. State scope explicitly (literal instruction following)
Sonnet 5 interprets prompts literally: it will not silently generalize one instruction to other
items or infer requests you didn't make. If a rule should apply broadly,
say so: "Apply this to every section, not just the first."

### 5. Don't fight verbosity with bans
Opus 5's default user-facing replies and written documents run longer than prior Opus models, and
Sonnet 5 only needs a length override where the task actually requires it. To tune, add a positive
concision instruction (e.g. "Keep responses focused, brief, and concise; keep disclaimers and
caveats short, and spend most of the response on the main answer") rather than negative rules. For
files and reports, add a length-matching instruction ("cover the substance, but do not pad with
filler sections, redundant summaries, or boilerplate") instead of a ban. Show a positive example of
the desired concision.

### 6. Tool-use & parallelism are steerable, not forced
- Sonnet 5 is more agentic by default, but is markedly less tool-eager only with thinking off; name
  the tool and its trigger condition when execution depends on it.
- Parallel tool calls: name the rule explicitly: "If calls are independent,
  make them in parallel; if one depends on another's output, call sequentially; never guess params."
- Subagents: Opus 5 and Fable 5 now delegate MORE readily than prior versions by default (Fable 5 is
  dependable at parallel delegation). Give a cap, not encouragement: "Delegate only large,
  independent, parallelisable tracks; do work that fits in a handful of tool calls yourself; prefer
  one subagent over several, at most [N]."

### 7. Autonomy vs. safety — confirm before irreversible/outward actions
Without guidance the model may take hard-to-reverse or shared-system actions. A good CLAUDE.md
states: take local reversible actions freely (edit files, run tests); confirm before destructive
(`rm -rf`, drop tables, delete branches), hard-to-reverse (`git push --force`, `reset --hard`,
amending published commits), or outward-facing (push, PR/issue comments, messages) actions. Don't
bypass safety checks (`--no-verify`) as a shortcut.

### 8. Context awareness — don't stop early
Fable 5 can show context-budget anxiety when a token countdown is surfaced. In a
compacting harness (Claude Code), the CLAUDE.md can say: context auto-compacts, so don't stop early
for budget reasons; save progress/state to memory before the window refreshes; complete tasks fully,
finish the tool call, not just the plan for it.

### 9. Over-engineering guard (still relevant)
Fable 5 can gold-plate at high/xhigh effort (unrequested features, refactors, or abstractions) and
can overplan on ambiguous tasks, and Opus 5 can widen task scope
unprompted. A KISS/YAGNI section plus "don't add features, refactor, or introduce abstractions
beyond what the task requires; only validate at system boundaries; don't add comments to code you
didn't change" remains valuable.

### 10. Delete verification instructions for Opus 5
Opus 5 verifies its own work unprompted. Instructions like "double-check your answer", "re-verify
before responding", or "include a final verification step" now cause over-verification: delete
them, don't rewrite them. This inverts the usual "ask the model to self-check" advice from earlier
generations.

### 11. Give Fable 5 the goal, not the steps
Prompts and skills written for prior models are often too prescriptive for Fable 5.1 and degrade
its output. State the goal and constraints and let it choose the steps. A "show your reasoning" or
"explain your thought process" instruction can trigger a reasoning_extraction refusal; remove
reflection language instead.

### 12. Anti-hallucination / grounding
"Never speculate about code you haven't opened; read referenced files before answering" reliably
reduces hallucination in agentic coding.

### 13. Don't transcribe what the agent can discover
A CLAUDE.md that lists every subcommand of a CLI/help script, or every file inside a folder, costs
tokens, rots the moment something is renamed, and duplicates what the agent finds by itself. Name
that the tool/folder exists and how to learn more (`<cli> --help`, `just`, a `prime` command;
directory listing for folder contents) — the agent explores from there. Keep concrete top-level
build/test/lint commands and a top-level folder map (those orient); drop the exhaustive dumps.

## General principles (durable)

- **Be clear and direct.** Treat the model as a brilliant new hire lacking your context. Golden rule:
  if a colleague with no context would be confused by your prompt, so is the model.
- **Examples beat description.** 3–5 relevant, diverse examples wrapped in `<example>`/`<examples>` tags.
- **Structure with XML tags.** Consistent, descriptive tags (`<rules>`, `<context>`, `<input>`) reduce
  misinterpretation — matches this repo's prompt-structure convention.
- **Match prompt style to desired output.** Less markdown in the prompt → less markdown out.
- **Effort & thinking (API context).** Adaptive thinking is on by default; `thinking.budget_tokens`,
  `temperature`/`top_p`/`top_k`, and last-assistant-turn prefill all return HTTP 400 (removed, not
  deprecated). Depth is set only by `output_config.effort` (ladder: low / medium / high / xhigh / max); effort does
  not shorten visible output, so length still has to be set in the prompt. Mostly an API concern,
  but flag it if the CLAUDE.md hardcodes thinking config, temperature, or a prefill.

## Size targets (aims, not hard limits)
Functions ~5–10 lines (avoid >20); params ≤2 (avoid >3); nesting ≤1; files <150 lines;
one primary module/class/component per file.

## Git workflow
Commit before work; small atomic commits per discrete change; messages `verb: description`
(no AI attribution); never push unless asked; don't rewrite history unless asked; branch first on
the default branch.

## Quality gates
Smallest set of checks for confidence (tests, typecheck, lint, format). On failure iterate up to 3×
on the same check, then switch strategy and explain. Can't run? "not run" + reason + exact commands.

## Change philosophy
Minimal local diffs matching existing style; no drive-by refactors; no back-compat unless public
API/shared lib; split unwieldy files while preserving architecture.

## Output format
Lead with the answer. Then: what changed · where (`path:line`) · checks (or "not run" + why) · risks.

## Harness capabilities to reference (Claude Code, 2026)
- **Skills** via the `Skill` tool / `/<name>`; only invoke listed skills.
- **Subagents** via the `Agent` tool — parallel/background, resumable via `SendMessage`.
- **Agent fork**: a `fork` subagent type inherits the parent model.
- **Workflow tool**: deterministic multi-agent orchestration, opt-in via the word "ultracode".
- **Artifact tool**: publishes HTML pages as Artifacts.
- **Fast mode** via `/fast`: Opus with faster output.
- **Scheduling**: `/schedule` (cron remote agents), `/loop` (recurring/self-paced), `ScheduleWakeup`.
- **Deferred tools / ToolSearch**: resolve a tool's schema (`select:<name>`) before calling it.
- **File-based memory**: per-project dir + `MEMORY.md` index for durable facts.
- **consult-user-mcp** (if installed): `ask` (types confirm/pick/text/form), `notify`, `tweak`.
  Batch 2+ questions in one `form`; built-in `AskUserQuestion` is disabled in that setup.
- **Browser automation**: `mcp__claude-in-chrome__*` (load via ToolSearch; never trigger blocking JS dialogs).
- **MCP management**: prefer the repo's chosen tool (e.g. `mcp-pick`); scopes project vs user/local.

## Common pitfalls to flag in a CLAUDE.md
1. Hardcoded stale model names/IDs.
2. Pervasive ALL-CAPS / `MUST` / `NEVER` / `CRITICAL` (overtriggers on Claude 4.5 and later).
3. Negative phrasing where a positive instruction would steer better.
4. Rules with no rationale.
5. Instructions assuming the model will generalize scope it wasn't given.
6. Fighting verbosity/markdown with bans instead of positive examples.
7. Forcing tool use / parallelism with shouting instead of plain "use X when…".
8. "Unlimited context" claims: do not falsely promise unlimited context.
9. Outdated consult-user tool names (`ask_confirmation` vs `ask`+type `confirm`).
10. Auto-push / history-rewrite without an explicit ask.
11. Exhaustive transcription of a CLI's subcommands or a folder's file list — name the tool/folder and how to discover the rest (`--help`, `prime`, directory listing); the dump rots and the agent can read it.
12. "Double-check your work" / "verify before responding" lines: Opus 5 already verifies unprompted, so these cause over-verification loops.
13. Hardcoded thinking config (`budget_tokens`, `temperature`, `top_p`/`top_k`): the 5-series API returns HTTP 400 for all of them.

## When to update this skill
New model versions ship · Claude Code capabilities change materially · `best_practices_date`
exceeds ~6 weeks. Re-fetch the source guide above. Bump `version` in SKILL.md frontmatter and
`best_practices_date` in METADATA.json together. Keep this as the single source of truth — don't
accumulate parallel dated files.
