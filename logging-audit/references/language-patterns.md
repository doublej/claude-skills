# Per-Language Logging Patterns

Idiomatic structured-field syntax per language. Use the project's existing logger when one is detected; only swap loggers if the user explicitly opts in.

<python>
## Python

### `logging` (stdlib) — use `extra=`
```python
logger.info("payment.charge failed", extra={"user_id": user.id, "amount": amount, "reason": "card_declined"})
```
Requires a JSON formatter or a `%(key)s`-aware format string to render the extras. If the project's handler doesn't render `extra`, fall back to f-string with explicit fields:
```python
logger.info("payment.charge failed user_id=%s amount=%s reason=card_declined", user.id, amount)
```

### `loguru`
```python
logger.bind(user_id=user.id, amount=amount).info("payment.charge failed reason=card_declined")
```

### `structlog` (preferred when present)
```python
log.info("payment.charge", outcome="failed", user_id=user.id, amount=amount, reason="card_declined")
```
The first positional arg is the event stem; everything else is fields. **Do not** reformat with f-strings — structlog merges kwargs into the JSON envelope.

### `print` swap
If a file uses `print` for diagnostics and another module in the same package uses a real logger, replace `print` with the same logger import. Never introduce a new logger framework — match the project.
</python>

<javascript_typescript>
## JavaScript / TypeScript

### `console`
Native console only formats the first argument. Pass an object literal for fields:
```js
console.warn("auth.login_throttled", { user_id, attempts, retry_after_ms });
```

### `pino`
```js
logger.info({ user_id, amount, reason: "card_declined" }, "payment.charge failed");
```
Pino convention: object first, message second. **Do not** swap the order — pino logs the first arg as `mergingObject`.

### `winston`
```js
logger.info("payment.charge failed", { user_id, amount, reason: "card_declined" });
```

### Avoid
- Template literals as the only message: `` `User ${id} did X` `` → loses the structured stem.
- `JSON.stringify(obj)` inside the message — let the logger serialize.
</javascript_typescript>

<rust>
## Rust

### `tracing` (preferred)
```rust
tracing::info!(user_id = %user.id, amount = amount, reason = "card_declined", "payment.charge failed");
```
- `%` = `Display`, `?` = `Debug`. Default for primitives is `Display`.
- Fields go before the message string (the trailing literal).
- Use `tracing::instrument` on functions to attach per-span fields automatically — preferred over logging entry/exit.

### `log` crate (legacy)
```rust
log::warn!("cache.evict reason=oom keys={}", evicted_count);
```
No native structured fields — interpolate explicitly.
</rust>

<go>
## Go

### `slog` (Go 1.21+, preferred)
```go
slog.Info("payment.charge failed", "user_id", user.ID, "amount", amount, "reason", "card_declined")
// or
slog.Info("payment.charge failed", slog.Int64("user_id", user.ID), slog.String("reason", "card_declined"))
```

### `zap`
```go
logger.Info("payment.charge failed",
    zap.Int64("user_id", user.ID),
    zap.Float64("amount", amount),
    zap.String("reason", "card_declined"),
)
```

### `zerolog`
```go
log.Info().
    Int64("user_id", user.ID).
    Float64("amount", amount).
    Str("reason", "card_declined").
    Msg("payment.charge failed")
```

### Avoid
- `log.Printf("user %d did X", id)` — no fields, no level beyond Print/Fatal/Panic.
- Mixing `fmt.Println` with `slog` — pick one per package.
</go>

<swift>
## Swift

### `os.Logger` (Apple platforms, preferred)
```swift
import os

let logger = Logger(subsystem: "com.example.payments", category: "charge")

logger.error("payment.charge failed user_id=\(user.id, privacy: .public) amount=\(amount) reason=card_declined")
```
- Privacy annotations are required for non-numeric values in production builds (default is `.private`).
- Use one `Logger` per (subsystem, category) — they're cheap.

### `print` swap
Same rule as Python: if any module in the target uses `Logger`, replace `print` with a matching `Logger`. Don't introduce SwiftLog unless the project already uses it on Linux.
</swift>

<framework_signals>
Detect the right framework before rewriting. Quick greps:

| Pattern in source | Framework |
|-------------------|-----------|
| `import logging` / `getLogger(` | Python stdlib `logging` |
| `from loguru import logger` | loguru |
| `import structlog` | structlog |
| `from 'pino'` / `require('pino')` | pino |
| `from 'winston'` | winston |
| `use tracing::` | tracing |
| `use log::` (without tracing) | log |
| `"log/slog"` | slog |
| `go.uber.org/zap` | zap |
| `import os` + `Logger(subsystem:` | os.Logger |

If multiple frameworks appear in one file, treat that as a separate gap to flag — not a swap to perform automatically.
</framework_signals>
