---
name: agent-friendly-cli
description: Design, refactor, or audit CLIs optimized for LLM/agent consumption — structured output, token economy, self-describing primers, atomic writes. Use when building a CLI agents will drive, making an existing CLI agent-friendly, or scoring one's agent-friendliness.
---

# Agent-Friendly CLI

Build CLIs that minimize agent memory burden, token usage, and repair loops.

For the full briefed checklist of every area to focus on, read
`references/focus-areas.md`. The map below is the index into it.

<core_properties>
An agent-friendly CLI is:

1. **Self-describing** — one command returns a complete machine-readable guide
2. **Intent-oriented** — commands match goals, not memorized syntax
3. **Structured** — outputs and errors are machine-parseable
4. **Recoverable** — failures include actionable repair hints
5. **State-aware** — prior results and defaults are reusable
6. **Infrastructure-buffered** — rate limits, cache, sessions internalized
7. **Batch-capable** — one command replaces repetitive loops
8. **Workflow-complete** — full task lifecycle inside the CLI
</core_properties>

<focus_areas>
Ten areas to design and audit against. Each is briefed bullet-by-bullet in
`references/focus-areas.md` — open it for the detail.

1. **Output & formatting** — auto-JSON on pipe, color-off off-TTY, raw scalars, stdout=data/stderr=diagnostics, dense tables.
2. **Token economy** — output caps + truncation notice, field projection, verbosity presets, compact tokens, fingerprints over values.
3. **Input ergonomics** — bare-arg intent routing, fuzzy resolution, short aliases, target shorthands, stable short IDs, `@`-refs.
4. **Defaults & config** — useful no-arg action, zero-config baseline, persistent defaults that shrink calls, flags override config.
5. **Discoverability & help** — described subcommands, runnable examples, inline arg semantics, generated completion, one source of truth.
6. **Errors & feedback** — structured code/message/hint, categories, retryable flag, valid-options-on-failure, meaningful exit codes, fail-fast non-TTY.
7. **Agent contract (`prime`)** — one-shot full primer, Markdown by default (`--json`/`--xml` opt-in), self-described output contract, detected env block, workflow + guardrails.
8. **Safety & writes** — atomic mutate-with-rollback, validate-before-commit, idempotent/guarded, `--dry-run`, secrets via env not stdout.
9. **Round-trip reduction** — cache by query shape, read-only never hits backend, compose from cache, embedded health probe, graceful degradation.
10. **Automation & interop** — inject-and-exec, read-only query escape hatch, pipe-through loops, stdin `-`, session lifecycle.

Prioritize when time-limited: structured output → atomic writes → `prime` → structured errors → caps/density → state & cache. See the "Highest-leverage first" section in the reference.
</focus_areas>

<workflow>
Determine the task type:

**Building a new CLI:**
1. Gather requirements (what agents will do with this CLI)
2. Design the command surface using the design template below
3. Implement with structured output, error model, and state management
4. Audit with `references/evaluation-rubric.md`

**Refactoring existing CLI for agents:**
1. Audit current CLI against `references/evaluation-rubric.md`
2. Identify gaps (usually: structured output, error model, self-description)
3. Add agent-friendly layers without breaking human UX
4. Re-audit

**Auditing a CLI:**
1. Run through `references/evaluation-rubric.md` checklist
2. Report findings with priority ranking
</workflow>

<design_template>
When designing a CLI, address each layer:

### 1. Entry Surface
- Natural invocation (argument shape implies intent)
- Explicit subcommands as escape hatches
- `prime` (or `guide`) command for self-description — Markdown by default, `--json`/`--xml` opt-in

### 2. Data Contract
- `--format json|jsonl|table|csv` (default: json when piped, table when TTY)
- `--fields` for field projection
- `--verbose` / `--brief` verbosity tiers
- Stable schemas — breaking changes require version bump

### 3. State Model
- Ephemeral IDs (short, recent-context references like `@1`, `@last`)
- Persistent references for cross-command reuse
- Config file for defaults (`~/.config/<tool>/config.toml`)

### 4. Execution Model
- Built-in throttling for API-backed commands
- Transparent caching with `--no-cache` / `--refresh` overrides
- Auto-retry with backoff for transient failures
- `--dry-run` for destructive operations

### 5. Error Model

```json
{
  "error": {
    "code": "INVALID_DATE_FORMAT",
    "message": "Cannot parse '2025-13-01' as a date",
    "hint": "Use ISO 8601 format: YYYY-MM-DD",
    "retryable": false,
    "suggestion": "mytool search --date 2025-01-13"
  }
}
```

Categories: `user_error`, `transient`, `upstream`, `internal`

### 6. Composition Model
- IDs from output pass directly into next command
- Batch operations: `mytool inspect @1 @2 @3` or `mytool search --grid "a,b" "x,y"`
- Compare primitives: `mytool diff @1 @2`

### 7. Workflow Model
- discover → inspect → refine → export → resume
- Full lifecycle without leaving the CLI
</design_template>

<routing_examples>
## Intent-First Routing Examples

```
mytool ABC123          # identifier → inspect
mytool "search term"   # string → search
mytool file.json       # file → import/process
mytool @1 @2           # refs → compare
mytool                 # no args → interactive/status
```
</routing_examples>

<self_description>
## Self-Description Command

Every CLI should have a `prime` (or `guide`) command that emits its full contract.

**Default to Markdown, unconditionally.** Unlike data commands (which auto-JSON on
a pipe), the primer's consumer is the agent's reasoning, not a parser — Markdown
delineates the contract cheaply and stays human-readable, so emit it whether stdout
is a TTY or piped. Offer `--json` for machine ingest and optionally `--xml` for
tag-structured consumption.

```markdown
# mytool v1.0.0
One-sentence purpose.

## Commands
- `search <query>` — find records; emits JSON when piped
- `inspect <id|@n>` — full record for one result

## Workflows
1. search → inspect → export

## Output contract
- Data commands emit JSON on pipe, dense table on TTY
- Errors: `{code, message, hint, retryable}` in machine mode

## Error codes
- `NOT_FOUND` — no match; lists valid options
- `RATE_LIMITED` — retryable; back off and retry smaller

## Config
~/.config/mytool/config.toml — keys: currency, default_limit

## Detected
cwd=… · config=found · next: `mytool search "…"`
```

Same model backs `--json`:

```json
{ "name": "mytool", "version": "1.0.0", "purpose": "…",
  "commands": [], "workflows": [], "error_codes": [],
  "config": { "path": "~/.config/mytool/config.toml", "keys": [] } }
```
</self_description>

<shared_learnings>
## Shared Learnings Loop (advanced)

The ten focus areas optimize a *single* agent's interaction. This pattern optimizes
*across* agents and sessions: let agents persist hard-won strategies, vote on them,
and surface the top-voted ones in `prime` — so the next agent starts where the last
one left off instead of rediscovering the same heuristics (and re-paying the same
round-trips). Worth it for CLIs many agents drive repeatedly over time; skip it for
one-shot tools.

### Commands

```
mytool learn "Tue/Wed departures ~15% cheaper on longhaul"   # record (idempotent by text hash)
mytool vote <ID> up | mytool vote <ID> down                  # upvote / downvote
mytool learnings [--limit N] [--fmt jsonl]                   # list top by score
```

### Design

- **Storage** — a global file (`~/.config/mytool/learnings.json`), separate from the
  query cache so it survives sessions and cache clears.
- **Stable ID** — `L + sha1(text)[:6]`: identical learnings dedup to the same ID, so
  `learn` is idempotent and a vote always addresses the same entry.
- **Ranking** — net score (up − down), tie-break by upvotes, then recency.

### `prime` integration (the surfacing)

- Add a `LEARNINGS` entry to the commands reference so the agent knows the loop exists.
- Render the **top N by score** as a dynamic block at the end of the primer.
- Add a short protocol telling the agent to **apply → record → vote** each session:
  use the surfaced learnings, record any new insight, and up/downvote ones it
  confirmed or disproved.

This turns `prime` from a static contract into a self-improving one — collective
experience compounds, and the cost is one small JSON file.
</shared_learnings>

<input_normalization>
Accept flexibly, emit strictly:
- Dates: `2025-01-13`, `jan 13 2025`, `13/01/2025` → always output ISO 8601
- IDs: case-insensitive input → canonical case output
- Amounts: `1000`, `1,000`, `1k` → normalized number
</input_normalization>

<antipatterns>
## Key Anti-Patterns

- Prose-only output with no structured option
- Opaque error messages ("Something went wrong")
- Requiring docs lookup to use basic features
- Agent must manage sleep/retry/cache externally
- No way to reference previous results
- N identical calls where one batch call suffices
</antipatterns>
