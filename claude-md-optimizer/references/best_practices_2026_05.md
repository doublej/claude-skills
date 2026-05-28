# Claude Code Best Practices (May 2026)

> Anchored to Anthropic's official prompting guide for the Claude 4.x family.
> Source: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
> Update `best_practices_date` in METADATA.json when revising.

A CLAUDE.md is a persistent system prompt. The model behaviors below are what changed
with Claude Opus 4.7 / Sonnet 4.6 — and they directly affect how a good CLAUDE.md is written.

## Models (May 2026)

| Model | ID | Use for |
|-------|-----|---------|
| Opus 4.7 | `claude-opus-4-7` | Most capable; long-horizon agentic, coding, knowledge work, vision, memory. 1M-context variant. |
| Sonnet 4.6 | `claude-sonnet-4-6` | Balanced; defaults to `high` effort. Fast turnaround / cost. |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Quick/cheap, subagents, latency-sensitive. |

- Most recent family is Claude 4.X. Default new AI apps to `claude-opus-4-7`.
- Hardcoded older names/IDs ("Opus 4.5", "Sonnet 4.5", `claude-sonnet-4-5-...`) are a red flag — flag them.

## High-impact CLAUDE.md review checklist (4.6/4.7 behavior shifts)

These are the most common ways an older CLAUDE.md now mis-steers the model.

### 1. Dial back aggressive emphasis — the #1 stale pattern
4.6/4.7 are far more responsive to the system prompt than earlier models, so prompts tuned
to fix *under*-triggering now cause *over*-triggering. Replace shouty directives with normal phrasing.
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
4.7 interprets prompts more literally and will not silently generalize one instruction to other items.
If a rule should apply broadly, say so: "Apply this to every section, not just the first."

### 5. Don't fight verbosity with bans
4.7 calibrates length to task complexity (short on lookups, long on open-ended work). To tune,
add a positive concision instruction ("Provide concise, focused responses; skip non-essential
context") rather than negative rules. Show a positive example of the desired concision.

### 6. Tool-use & parallelism are steerable, not forced
- 4.7 uses tools *less* and reasons more by default. If you want more tool use, describe when/how
  to use a specific tool (don't shout). Effort level also raises tool usage.
- Parallel tool calls: a short rule reliably pushes success to ~100% — "If calls are independent,
  make them in parallel; if one depends on another's output, call sequentially; never guess params."
- Subagents: 4.7 spawns *fewer* by default. Give explicit when-to-delegate guidance if you want them.

### 7. Autonomy vs. safety — confirm before irreversible/outward actions
Without guidance the model may take hard-to-reverse or shared-system actions. A good CLAUDE.md
states: take local reversible actions freely (edit files, run tests); confirm before destructive
(`rm -rf`, drop tables, delete branches), hard-to-reverse (`git push --force`, `reset --hard`,
amending published commits), or outward-facing (push, PR/issue comments, messages) actions. Don't
bypass safety checks (`--no-verify`) as a shortcut.

### 8. Context awareness — don't stop early
4.6/4.5 track remaining token budget and may wrap up prematurely. In a compacting harness
(Claude Code), the CLAUDE.md can say: context auto-compacts, so don't stop early for budget reasons;
save progress/state to memory before the window refreshes; complete tasks fully.

### 9. Over-engineering guard (still relevant)
Opus 4.5/4.6 tend to overengineer (extra files, abstractions, unrequested flexibility, defensive
code, docstrings on untouched code). A KISS/YAGNI section plus "only validate at boundaries; don't
add comments to code you didn't change" remains valuable.

### 10. Anti-hallucination / grounding
"Never speculate about code you haven't opened; read referenced files before answering" reliably
reduces hallucination in agentic coding.

## General principles (durable)

- **Be clear and direct.** Treat the model as a brilliant new hire lacking your context. Golden rule:
  if a colleague with no context would be confused by your prompt, so is the model.
- **Examples beat description.** 3–5 relevant, diverse examples wrapped in `<example>`/`<examples>` tags.
- **Structure with XML tags.** Consistent, descriptive tags (`<rules>`, `<context>`, `<input>`) reduce
  misinterpretation — matches this repo's prompt-structure convention.
- **Match prompt style to desired output.** Less markdown in the prompt → less markdown out.
- **Effort & thinking (API context).** Adaptive thinking + the `effort` parameter (`low`→`max`, plus
  `xhigh`) replace `budget_tokens`. `xhigh` for coding/agentic; ≥`high` for intelligence-sensitive work.
  Mostly an API concern, but note it if the CLAUDE.md hardcodes thinking config.

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
- **Plan mode** (`ExitPlanMode`) for design-before-build.
- **Scheduling**: `/schedule` (cron remote agents), `/loop` (recurring/self-paced), `ScheduleWakeup`.
- **Deferred tools / ToolSearch**: resolve a tool's schema (`select:<name>`) before calling it.
- **File-based memory**: per-project dir + `MEMORY.md` index for durable facts.
- **consult-user-mcp** (if installed): `ask` (types confirm/pick/text/form), `notify`, `tweak`.
  Batch 2+ questions in one `form`; built-in `AskUserQuestion` is disabled in that setup.
- **Browser automation**: `mcp__claude-in-chrome__*` (load via ToolSearch; never trigger blocking JS dialogs).
- **MCP management**: prefer the repo's chosen tool (e.g. `mcp-pick`); scopes project vs user/local.

## Common pitfalls to flag in a CLAUDE.md
1. Hardcoded stale model names/IDs.
2. Pervasive ALL-CAPS / `MUST` / `NEVER` / `CRITICAL` (overtriggers 4.6/4.7).
3. Negative phrasing where a positive instruction would steer better.
4. Rules with no rationale.
5. Instructions assuming the model will generalize scope it wasn't given.
6. Fighting verbosity/markdown with bans instead of positive examples.
7. Forcing tool use / parallelism with shouting instead of plain "use X when…".
8. "Unlimited context" claims (it's summarization + a 1M variant).
9. Outdated consult-user tool names (`ask_confirmation` vs `ask`+type `confirm`).
10. Auto-push / history-rewrite without an explicit ask.

## When to update this skill
New model versions ship · Claude Code capabilities change materially · `best_practices_date`
exceeds ~6 weeks. Re-fetch the source guide above. Bump VERSION and `best_practices_date` together.
Keep this as the single source of truth — don't accumulate parallel dated files.
