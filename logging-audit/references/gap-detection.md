# Gap Detection: Where to Add Logs

The scanner flags candidates mechanically. Use this guide to decide which gaps actually warrant a new log call.

<add_logs>
Add a log at these sites:

| Site | Level | Why |
|------|-------|-----|
| Error branches (`except`/`catch`/`if err != nil`/`Err(_)`) that produce side effects | `error` if unrecoverable, `warn` if handled | Silent failures are the hardest bugs to find |
| External calls (HTTP, DB, subprocess, queue publish) | `info` on success with timing, `error` on failure with reason | Cross-process boundaries need a paper trail |
| Retries / circuit breakers | `warn` per retry with attempt count and reason | Otherwise you can't tell "slow" from "10 silent retries" |
| State transitions on long-lived objects (job lifecycle, connection state, feature flag flips) | `info` with old → new | Replay-debuggable state |
| Auth events (login, logout, permission denied, token issued) | `info` for success, `warn` for denial | Security audit + abuse detection |
| Job/queue handlers at outcome | `info` with id + duration + outcome | Distinguishes "queue full" from "workers crashed" |
| Top-level handlers in long-running services (signal received, cron fired, websocket closed) | `info` | Lifecycle visibility |

**Where to put the log:** as close to the *outcome* as possible. After the operation, with the result in scope. Not before ("about to do X") and not in a `finally` that can't tell success from failure.
</add_logs>

<skip_logs>
Do **not** add logs at these sites — they create noise:

| Site | Reason |
|------|--------|
| Pure functions (no I/O, no mutation) | Output is deterministic from inputs; the caller already knows |
| Getters / property accessors | Nothing happens worth recording |
| Hot loops where the aggregate is already logged | One "processed N items" log beats N per-item logs |
| Trivial wrappers / passthroughs | The wrapped function is the right place |
| Validation that throws an exception caught and logged elsewhere | The catch site is the right place |
| Function entry where a span / `tracing::instrument` already covers it | Span lifecycle replaces entry/exit logs |
| Test code | Tests assert; they don't observe |
| Generated code (codegen, migrations) | Won't survive regeneration |

**Heuristic:** if the function is small and pure and reading its body tells you exactly what happens, no log helps. If the function calls out to something you don't control, a log helps.
</skip_logs>

<silent_error_branch>
Scanner flag: `silent_error_branch`. The handler ran but no log line records it.

**False positives:**
- Handler re-raises immediately — caller logs.
- Handler returns the error to a function that the caller will log.
- Handler is `pass` because the exception is genuinely expected (e.g., `json.JSONDecodeError` on optional config).

**Real fixes:**
```python
except StripeError as e:
    return False
```
becomes
```python
except StripeError as e:
    logger.error("payment.charge failed", extra={"user_id": user.id, "reason": str(e)})
    return False
```

For Go:
```go
if err := db.Exec(...); err != nil {
    return err
}
```
Add a log only if the caller cannot — wrap with context (`fmt.Errorf("db.exec: %w", err)`) and let the top of the call chain log once. **Don't double-log.**
</silent_error_branch>

<silent_external_call>
Scanner flag: `silent_external_call`. HTTP / DB / subprocess executed without surrounding observability.

**Decision tree:**
1. Is the call wrapped in a tracing span (OpenTelemetry, `tracing::instrument`, datadog APM)? → Skip; the span covers it.
2. Is the call inside a tight retry loop where the retry policy already logs? → Skip.
3. Otherwise → add an `info` log on success with timing, and an `error` log on failure with the reason.

**Pattern:**
```python
start = time.monotonic()
try:
    response = httpx.post(url, json=payload, timeout=10)
    response.raise_for_status()
    logger.info("api.checkout succeeded", extra={
        "endpoint": url, "ms": int((time.monotonic() - start) * 1000),
        "status": response.status_code,
    })
except httpx.HTTPError as e:
    logger.error("api.checkout failed", extra={
        "endpoint": url, "ms": int((time.monotonic() - start) * 1000),
        "reason": str(e),
    })
    raise
```

Keep timing in milliseconds (not seconds); ints are easier to histogram.
</silent_external_call>

<budget>
Even good logs are noise in aggregate. Per added log, ask:

1. **Will this fire >100/sec in production?** If yes, drop the level to `debug` or sample.
2. **Does the operator need this without a code change?** If no, leave it as a code comment instead.
3. **Is the same fact already in metrics / traces?** If yes, skip — duplication slows investigations.

When in doubt about adding a log: don't. The skill should err toward fewer, better logs, not more logs.
</budget>
