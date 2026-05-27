# Agent-Friendly CLI Evaluation Rubric

Score each of the 10 focus areas 0-2: 0=missing, 1=partial, 2=complete.
Each area maps to a section in `focus-areas.md` — consult it for what "complete" means.

## Checklist

### 1. Output & formatting (0-2)
- [ ] Auto-emits JSON when piped (non-TTY); color auto-off off-TTY / on `NO_COLOR`
- [ ] Raw scalar for single-value commands; stdout=data, stderr=diagnostics
- [ ] Dense tables (no box chrome); multiple machine formats (json/jsonl/tsv/csv)

### 2. Token economy (0-2)
- [ ] Default row limits + "showing N of M" truncation notice
- [ ] Field projection (`--fields`) and verbosity presets (`--view min|std|full`)
- [ ] Per-column truncation; noise suppressed by default with opt-in

### 3. Input ergonomics (0-2)
- [ ] Bare-arg intent routing (ID→inspect, string→search)
- [ ] Fuzzy/substring resolution; short flags & aliases
- [ ] Stable short IDs that survive re-query; `@1`/`@last` refs

### 4. Defaults & config (0-2)
- [ ] No-arg invocation does something useful (not a help dump)
- [ ] Zero-config baseline; persistent defaults shrink later calls
- [ ] Explicit flags override config; user-definable shortcuts

### 5. Discoverability & help (0-2)
- [ ] Every subcommand described; runnable examples block
- [ ] Inline argument semantics in signatures
- [ ] Generated shell completion from a single command model

### 6. Errors & feedback (0-2)
- [ ] Structured errors with code/message/hint (+ suggestion)
- [ ] Categories (user/transient/upstream/internal) + retryable flag
- [ ] Valid-options-on-failure; meaningful exit codes; fail-fast in non-TTY

### 7. Agent contract — `prime` (0-2)
- [ ] One-shot primer: commands, flags, output shapes, error codes
- [ ] Format-switches (XML/Markdown/JSON); self-described output contract
- [ ] Live "detected" env block; workflow + operational guardrails

### 8. Safety & writes (0-2)
- [ ] Atomic mutate-with-rollback; validate before commit
- [ ] Idempotent/guarded writes (`--force`); `--dry-run` before bulk
- [ ] Secrets injected via env, never printed; clear read/write separation

### 9. Round-trip reduction (0-2)
- [ ] Cache by full query shape with TTL + `--refresh`
- [ ] Read-only commands never hit the backend; compose from cache
- [ ] Embedded health probe in outcomes; graceful degradation when deps down

### 10. Automation & interop (0-2)
- [ ] Inject-and-exec (`run -- cmd`) mirroring child exit code
- [ ] Read-only query escape hatch (hardened allowlist); stdin (`-`) support
- [ ] Pipe-through workflows; auto-managed session lifecycle

## Scoring

| Score | Rating |
|-------|--------|
| 0-6   | Poor — agent will struggle significantly |
| 7-11  | Basic — usable but with friction |
| 12-15 | Good — most agent workflows supported |
| 16-20 | Excellent — fully agent-native |

## Priority order for improvements

1. **Output & formatting** — biggest immediate impact; agents stop scraping prose
2. **Safety & writes** — atomic/idempotent writes kill the verify-fix-retry loop
3. **Agent contract (`prime`)** — removes exploration and invented-flag failures
4. **Errors & feedback** — turns dead-ends into one-step corrections
5. **Token economy** — bounds worst-case context blowups
6. **Round-trip reduction** — enables free composition across calls
7. **Input ergonomics** — reduces memorization and lookups
8. **Defaults & config** — shrinks repeated invocations
9. **Discoverability & help** — lowers bootstrapping cost
10. **Automation & interop** — enables autonomous pipelines
