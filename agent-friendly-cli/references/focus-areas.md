# Agent-Friendly CLI — Focus Areas

The complete set of globally relevant properties to design or audit against. Each
bullet is **Property — one-line brief (what it is + why it matters for an agent)**.
Pair with `../SKILL.md` (design scaffold) and `evaluation-rubric.md` (scoring).

The throughline: make the human default dense, switch to structured/raw on a pipe,
ship a one-shot contract, and make writes atomic + idempotent so the agent never
needs a verify-fix-retry loop. The biggest token savings come from eliminating
round-trips, not from formatting.

<output_and_formatting>
## 1. Output & formatting
- **Human default, structured on demand** — Pretty for a terminal, but every command can emit machine format so agents never scrape prose.
- **Auto-switch to JSON when piped** — Detect non-TTY stdout and emit JSON with no flag, so captured output is parseable by default.
- **Auto-disable color off-TTY / on `NO_COLOR`** — Strip ANSI when piped or when `NO_COLOR` is set; color bytes are pure noise to an agent.
- **Raw scalar for single values** — When the answer is one value, print just the value (no envelope) so it pipes straight into the next command.
- **stdout = data, stderr = diagnostics** — Send notices, progress, and warnings to stderr so stdout stays a clean payload for piping.
- **Multiple machine formats** — Offer `json`, `jsonl` (line-parse/streaming), `tsv`, `csv`; `jsonl` is ideal for large result sets.
- **Dense tables, no box chrome** — Use computed column widths and space separators, not `│`/`─` grids, to maximize signal per token.
- **One record per line** — Prefer flat line-oriented records over nested multi-line blocks for scannability and grep-ability.
- **ANSI-aware width math** — Compute padding on visible length so colored tables still align and degrade cleanly.
</output_and_formatting>

<token_economy>
## 2. Token economy
- **Hard output caps with truncation notice** — Default a `--limit` and print "showing N of M" so the agent knows output was capped and how to widen it.
- **Sensible default row limits** — Every list defaults to a bounded count so an unscoped call can't dump thousands of rows into context.
- **Per-column truncation with ellipsis** — Cap free-text fields so one long value can't blow the row width and token budget.
- **Verbosity presets & field projection** — Offer `--view min|std|full` and `--fields a,b,c` so the agent pulls only the columns it needs.
- **Collapse state into compact tokens** — Reduce verbose status into short symbols (`up`, `down(3)`, `no-pm2`) instead of raw nested JSON.
- **Middot one-line summaries** — Summarize with `a · b · c` one-liners rather than multi-sentence prose.
- **Bare value when that's the whole answer** — Emit just the integer/string for single-fact commands (e.g. next free port) so no parsing is needed.
- **Suppress noise by default, opt-in to show** — Hide stale/irrelevant rows (and system env) by default, with a footer flag (`--all`) to reveal.
- **Fingerprint instead of value** — For secrets or large blobs, expose a `sha256:…` so the agent can compare without ingesting the content.
</token_economy>

<input_ergonomics>
## 3. Input ergonomics
- **Bare-arg intent routing** — Infer the command from the argument's shape (ID→inspect, string→search, file→import) so common actions skip the subcommand.
- **Substring / fuzzy resolution** — Resolve entities by name fragment instead of requiring exact IDs the agent would have to look up first.
- **Short flags + single-letter aliases** — Provide terse forms (`-d`, `brief`→`b`) to cut tokens on repeated invocations.
- **Target shorthands** — Expand compact tokens to real targets (`:5173`→LAN IP, `nas:port`→gateway) so the agent doesn't compute them.
- **Flexible value parsing** — Accept `today`/`tomorrow` and multiple date/number formats on input; emit one canonical form on output (accept loose, emit strict).
- **Stable short IDs that survive re-query** — Derive IDs from a content hash so the same token addresses a result across filter, sort, and re-search.
- **Cross-reference syntax** — Support `@1`/`@last` for recent results and `REF:ID` for cross-session lookups so prior output feeds the next call.
</input_ergonomics>

<defaults_and_config>
## 4. Defaults & config
- **Useful no-arg action** — `tool` with no args does something productive (a snapshot or status), not a help dump.
- **Zero-config baseline** — Ship working defaults so the CLI runs before any setup; setup only refines.
- **Persistent defaults that shrink calls** — Let users save currency/format/limits so repeated flags disappear from every invocation.
- **Explicit flags override config** — A flag always wins over a stored default; inject defaults only when the flag is unset.
- **User-definable shortcuts** — Allow saved aliases for long names (`-a biz` → full account name).
- **XDG paths, secret-free config, mode 0600** — Store config/state under `~/.config`, keep secrets out of it, and lock file modes for state.
</defaults_and_config>

<discoverability_and_help>
## 5. Discoverability & help
- **Every subcommand has a one-line description** — No bare command names; each line says what it does.
- **Copy-pasteable examples block** — Include runnable examples, not just option grammar.
- **Each example explains its effect** — Pair every example with what it accomplishes so intent is unambiguous.
- **Footer points to per-command help** — End top-level help with "run `<cmd> <sub> --help`" for drill-down.
- **Argument semantics in the signature** — Document accepted formats inline (`target: :port | host:port`) so the shape is self-evident.
- **Generated shell completion** — Ship bash/zsh/fish completion for fast, correct invocation.
- **Single source of truth for help/completion/primer** — Derive all three from one command model so they can't drift from the real CLI.
</discoverability_and_help>

<errors_and_feedback>
## 6. Errors & feedback
- **Structured errors** — Emit `code` + `message` + `hint` (+ `suggestion`) as JSON in machine mode so failures are parseable, not prose.
- **Categories** — Tag errors `user_error`/`transient`/`upstream`/`internal` so the agent knows whether to fix input, retry, or stop.
- **Retryable flag** — State explicitly whether retrying could succeed, so agents don't loop on permanent failures.
- **Map upstream errors to typed codes** — Translate raw tool/API stderr into your own actionable codes and hints.
- **List valid options on failed lookup** — When an ID/name isn't found, print what does exist so the agent self-corrects in one step.
- **Meaningful exit codes** — Use distinct exit codes (e.g. `1` on drift) so scripts and agents branch without parsing text.
- **Fail fast in non-TTY** — Refuse interactive prompts when not a TTY (require `--yes`/`--value-stdin`) so an agent gets an error instead of a hang.
- **Live progress for slow ops** — Show sub-step progress on long operations, suppressed in machine mode.
</errors_and_feedback>

<agent_contract>
## 7. Agent contract (`prime` / `guide`)
- **One-shot full primer** — A single command emits the whole contract — role, rules, commands, flags, output shapes, error codes — so the agent never explores or guesses.
- **Markdown by default** — `prime` emits Markdown unconditionally (TTY or piped), because its consumer is the agent's reasoning, not a parser; Markdown delineates sections cheaply and stays human-readable. This is the one place the auto-JSON-on-pipe rule does not apply. Offer `--json` (machine ingest) and optionally `--xml` (tag-structured) as opt-ins.
- **Self-described output contract** — State when JSON triggers and the raw-vs-envelope shapes so the agent can depend on them.
- **Per-command output schema + error codes** — Enumerate each command's return shape and every error code inside the primer.
- **Live "detected" environment block** — Append cwd/config/env state and a next-step hint, gated to real projects so a primer from `$HOME` stays generic.
- **"Use only documented commands"** — Tell the agent not to invent flags; it should rely solely on the primer.
- **Response-format directives** — Tell the agent how to present results (lead with a session line, show top 3–5 with IDs).
- **Workflow guidance** — Encode a gated multi-phase flow (resolve → search → shortlist → compose → deliver) so the agent sequences correctly.
- **Operational guardrails** — State rate-limit rules ("never parallelize; on BLOCKED sleep and retry smaller") directly in the primer.
- **Self-improving learnings loop (advanced)** — Let agents `learn`/`vote` on cross-session strategies stored in a global file, and render the top-voted ones in `prime`, so the next agent inherits hard-won heuristics instead of rediscovering them. See the "Shared Learnings Loop" section in `../SKILL.md`.
</agent_contract>

<safety_and_writes>
## 8. Safety & writes
- **Atomic mutations with rollback** — snapshot → write → validate → apply, restoring on any failure so the system is never left broken.
- **Validate before commit** — Check the new state before activating it; never apply a config that fails validation.
- **Idempotent, guarded writes** — Re-running is safe; refuse to clobber existing state without `--force`.
- **`--dry-run` before bulk writes** — Show the plan for batch or destructive ops before executing.
- **Inject secrets into child env, never print** — Provide `run -- cmd` that passes secrets via env so values never reach stdout/logs.
- **Materialize secret files to 0600 temp + auto-clean** — When a file is required, write a locked tempfile and delete it on exit.
- **Treat metadata as sensitive** — Names, titles, and inventories enumerate dependencies; scope listings and avoid dumping them into shared context.
- **Optional confirm-on-write gate** — Provide an env switch to pause for approval on every mutation for unattended agents.
- **Clear read/write separation** — Make it obvious which commands mutate so an agent can default to read-only.
</safety_and_writes>

<round_trip_reduction>
## 9. Round-trip reduction
- **Cache by full query shape with TTL** — Cache results keyed on all inputs so repeats are free; expose `--refresh` to bypass.
- **Read-only commands never hit the backend** — Inspect and compose from cache without new network/API calls.
- **Compose from cache** — Build richer artifacts (itineraries, reports) from already-fetched results with zero new calls.
- **One-line outcome with embedded probe** — Return the result plus a health/status check in one line (`url → target (health: 200)`).
- **Graceful degradation** — Return partial data when a dependency is down (mark rows `n/a`) instead of failing the whole command.
- **Auto-discover values** — Compute things the agent would otherwise look up (next free port, current quarter).
- **Reuse prior state on repeat** — On re-run, reuse the existing port/session so identity stays stable across calls.
</round_trip_reduction>

<automation_and_interop>
## 10. Automation & interop
- **Inject-and-exec** — `run -- cmd` runs a child with env/context injected and mirrors the child's exit code.
- **Read-only query escape hatch** — Offer a hardened SQL/query mode (select-only allowlist) for filters the typed CLI doesn't expose.
- **Pipe-through workflows** — Make one mode's output feed another (`--suggest --json | … --bulk -`) for closed loops.
- **Rule engine, user-overridable** — Ship default rules with user overrides ("user wins on first match") for repeatable classification.
- **Self-referential LLM loop** — An `ask` command pipes the tool's own output into an LLM with a constrained prompt that suggests further subcommands.
- **stdin support (`-`)** — Accept `-` wherever a file or value is taken so the CLI composes in pipelines.
- **Session lifecycle** — Auto-manage state across commands (auto-start, auto-close on export) so the agent doesn't track it.
</automation_and_interop>

<highest_leverage>
## Highest-leverage first
When time is limited, prioritize in this order:
1. **Structured output + auto-JSON-on-pipe** — unlocks everything else; agents stop scraping prose.
2. **Atomic, idempotent writes** — kills the verify-fix-retry loop, the largest hidden token sink.
3. **One-shot `prime` contract** — removes exploration and "invented flag" failures.
4. **Structured errors with hints** — turns dead-ends into one-step corrections.
5. **Output caps + dense formatting** — bounds worst-case context blowups.
6. **State/refs + caching** — enables free composition across calls.
</highest_leverage>
