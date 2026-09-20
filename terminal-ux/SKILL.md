---
name: terminal-ux
description: "CLI/TUI spinners, progress bars, task trees, prompts in Python/Node/Go/Rust"
---

# Terminal UX

## CLI vs TUI Decision

**CLI + rich status** when:
- Output may be piped to files or other commands
- Mostly linear flow (steps A -> B -> C)
- Multiple concurrent statuses without needing persistent panels

**Full-screen TUI** when:
- Persistent panels, tables, navigation, keybindings needed
- Complex interactive state (forms, trees, live data)

## Hard Rules

### 1. Separate data from status
- Machine-readable output -> **stdout**
- Animated status (spinners/progress) -> **stderr**
- Always support `--json` (stdout only), `--quiet`, `--no-progress`, `--no-color`

### 2. TTY awareness
- If not a TTY: disable animations, print plain log lines
- Never write control characters to logs/files
```python
# Python
import sys
use_color = sys.stderr.isatty()
```
```typescript
// Node
const isTTY = process.stderr.isTTY;
```

### 3. Progress lifecycle
1. Start spinner/progress
2. Update status text frequently (cheap writes)
3. Stop + render final stable result line (success/fail + summary)

### 4. Task state model
Use a registry: each task has `id, label, state, progress?, detail?`
UI layer renders current snapshot; business logic updates state.

```
pending -> running -> success | failed | skipped
```

## UX Patterns

### Multi-step task tree (best for "many statuses" without full TUI)
- Steps as list with states: pending -> running -> success/fail
- Nest subtasks when useful
- Final summary section

### Indeterminate vs determinate progress
- **Indeterminate**: spinner when total unknown
- **Determinate**: bar when total known; show ETA/throughput if possible

### Logging tiers
| Tier | Destination | Visibility |
|------|------------|------------|
| `info` | stderr | Always (safe for non-TTY) |
| `status` | stderr | TTY-only, ephemeral |
| `debug` | stderr | `--verbose` or env var |
| `data` | stdout | Always (machine output) |

## Stack-Specific References

Detailed patterns, templates, and API examples per stack:

- **Python** (Rich, Textual): `references/python.md`
- **Node/TypeScript** (ora, listr2, Ink): `references/node.md`
- **Go** (Bubble Tea, lipgloss): `references/go.md`
- **Rust** (Ratatui, indicatif): `references/rust.md`

## Minimum Implementation Checklist

- [ ] `--help` is concise, grouped by command
- [ ] Exit codes: 0 success, non-zero failure (distinct codes for common modes)
- [ ] Supports `--json`, `--quiet`, `--no-color`, `--no-progress`
- [ ] TTY detection disables animations in non-interactive mode
- [ ] No flicker: avoid full redraws outside TUI frameworks
- [ ] Ctrl+C handled gracefully (cleanup, restore terminal)
