# Log Style Guide

The contract for every log line written or rewritten by this skill.

<format>
**Hybrid: short imperative stem + structured fields.**

```
<event> [outcome] field=value field=value
```

Examples:

| Good | Bad |
|------|-----|
| `payment.charge failed user_id=42 amount=19.99 reason=card_declined` | `An error occurred while processing payment for user 42: card declined` |
| `db.query took ms=187 rows=1240 table=orders` | `Database query completed successfully` |
| `auth.login user_id=42 method=oauth provider=google` | `User logged in` |
| `cache.miss key=user:42 fallback=db` | `Cache miss, fetching from database` |
| `worker.shutdown reason=sigterm in_flight=3` | `Shutting down` |

**Rules:**
1. Stem is `noun.verb` or `verb.outcome` (≤4 tokens). Lowercase, dot-separated.
2. Fields use `key=value` (no quotes around values unless they contain spaces).
3. No trailing punctuation. Logs are records, not sentences.
4. Width target: ≤120 chars including fields. Truncate values, never the stem.
5. Stable field names within a module (`user_id` not `userID` then `uid`).
6. Time, level, file:line, request_id come from the logger framework — never bake them into the message.
</format>

<level_semantics>
| Level | Use for | Frequency budget |
|-------|---------|------------------|
| `error` | Action required by a human or pager. Data loss, repeated failure, security breach. | Rare. Every error log should be triageable. |
| `warn` | Recoverable degradation. Retried successfully, fallback used, deprecation hit. | Occasional. Should not fire steady-state. |
| `info` | Lifecycle events worth seeing in production: requests served, jobs completed, state transitions, external calls. | Steady but bounded. ≤ a few per request. |
| `debug` | Devloop noise. Variable dumps, branch traces, hot-loop iteration data. | Unbounded; off in prod. |
| `trace` | Per-instruction granularity. Reserved; rarely needed. | Off by default everywhere. |

**Mismatches to fix:**
- `info` in a `catch` / `except` block where the only outcome is failure → `error` (or `warn` if recoverable).
- `error` for a user-input rejection that the API surfaces as 4xx → `info` or `warn`.
- `debug` containing the word "fatal" / "panic" / "data loss" → `error`.
- `print` / `console.log` left in code that has a real logger imported elsewhere → swap to logger.
</level_semantics>

<scannability>
Logs are scanned, not read. Rules that make a 10k-line dump greppable:

1. **Stem first.** A human's eye lands on column 1. If `auth.login_failed` is consistent, `grep auth.login_failed` is the whole search.
2. **Stable verbs.** Pick one per outcome and reuse. `created` not `made/built/produced`. `failed` not `errored/broke/crashed`.
3. **No prose.** "User attempted to log in but failed" → `auth.login failed`. Eight words become two.
4. **Numbers as fields, never embedded.** `processed 42 items in 187ms` → `batch.processed count=42 ms=187`. `grep ms=` becomes a histogram source.
5. **One concept per line.** Don't combine "started job and queued 3 children". Two logs.
6. **No emojis, no ANSI in the message.** Renderer's job, not the logger's.
</scannability>

<context_fields>
Every log line should answer "what happened, to what, with what result." Required field discipline:

| Field type | Examples | When |
|-----------|----------|------|
| Subject id | `user_id`, `order_id`, `request_id`, `tenant_id` | Whenever the log refers to a specific entity |
| Outcome | `status`, `code`, `reason`, `attempt` | On any non-trivial completion |
| Magnitude | `ms`, `bytes`, `count`, `rows` | On anything timed or sized |
| Source | `path`, `endpoint`, `topic`, `queue` | When the same code handles many sources |

**Anti-patterns:**
- Logging an object's whole `__repr__` instead of selected fields.
- Logging secrets, tokens, full request bodies, PII unless explicitly redacted.
- Logging the same fact at two levels ("attempting" then "succeeded") — log only the outcome.
</context_fields>

<noise_to_remove>
Patterns that should be deleted, not rewritten:

- `info` logs at the start AND end of a function ("entering foo" / "exiting foo"). Keep only the outcome.
- Logs inside tight loops where the data is already in the aggregate result.
- Comment-style logs ("// TODO check this", "starting batch — should be fast"). Move to comment or delete.
- Debug logs that were left from a single past investigation.
- "Successfully" as the only differentiator from a sibling error log — the level already conveys that.
</noise_to_remove>
