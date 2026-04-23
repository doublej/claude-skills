---
name: cmux
description: "Drive cmux (terminal app) via CLI: enforce one workspace per
  project, named tabs by role (code/dev/logs/tests/browser/agent:N),
  predictable splits. Use when CMUX_SOCKET_PATH is set, asked to 'open in
  cmux', 'cmux project', 'cmux tab', 'add a cmux pane', spawn a cmux
  subagent, or organize a cmux session. Covers discovery, lifecycle,
  send/send-key I/O, status, browser automation, ssh workspaces,
  snapshot/restore. Reuse-before-create is the rule."
---

# cmux

cmux is a programmable, Ghostty-based terminal app built for AI coding
agents. This skill drives cmux via its CLI and **enforces one workspace
per project**. Every helper does find-or-create — no blind duplicates,
no tab graveyards across a long session.

## Prerequisites

- cmux installed (`brew install cmux` or from the app bundle).
- `CMUX_SOCKET_PATH` exported (cmux does this automatically in every
  shell it spawns). If unset, you're running outside cmux — most verbs
  fail hard with a clear error.
- `jq` available (`brew install jq`). Every helper uses it to parse
  cmux JSON output.

## Hierarchy: the one opinion

```
cmux app
└── workspace            (1 per project, name = project basename)
    └── tab              (name = <project>:<role>)
        └── split(s)     (row/column geometry inside the tab)
```

**Reuse before create. Always.** Every helper first looks up by name;
creation only happens when the lookup misses. That's the entire skill.

## Naming conventions

- **Workspace name** = project directory basename. `myproj`, not
  `myproj-2025-04` or `jj-myproj`. One project, one workspace, forever.
- **Tab name** = `<project>:<role>` where role is from the fixed enum
  below. Multi-agent tabs use `agent:<id>` (id is numeric or slug).
- **Role enum**: `code` (editor), `dev` (watcher/server), `logs`
  (tails/journals), `tests` (watcher), `browser` (cmux browser surface),
  `shell` (scratch), `build` (compiler output), `db` (repl), `notes`
  (scratch docs), `agent:<id>` (a Claude Code or similar subagent).

If a role you want isn't in the enum, pick `shell` — don't invent new
role names unless you add them to `scripts/_lib.sh` CMUX_ROLES.

## Discovery

| Verb | Purpose |
|------|---------|
| `cmux identify --json` | Daemon version, socket path, self-check |
| `cmux list-workspaces --json` | All workspaces + tab counts |
| `cmux list-pane-surfaces --workspace <id> --json` | Tabs in a workspace |
| `cmux tree --workspace <id>` | Human-readable split tree |
| `./scripts/cmux-find.sh <project>` | One-shot lookup → JSON, exit 1 if absent |

## Lifecycle

| Verb | Purpose |
|------|---------|
| `cmux new-workspace --name <n>` | Create workspace (prefer the helper) |
| `cmux new-split --workspace <id> --direction l\|r\|u\|d --tab <name>` | Add a split, optionally named |
| `cmux close-workspace --workspace <id> [--force]` | Close whole project |
| `cmux close-surface --surface <id> [--force]` | Close one tab |
| `cmux rename-workspace --workspace <id> <new-name>` | Rename |
| `cmux rename-tab --workspace <id> --index N <new-name>` | Rename tab |
| `cmux select-workspace --workspace <id>` | Focus it |

Directions `l`/`r`/`u`/`d` are left/right/up/down relative to the
current split. Splits are addressable via `list-pane-surfaces` once
named; without `--tab` they get an opaque `srf_…` id and are effectively
anonymous. **Always pass `--tab`.**

## I/O

| Verb | Purpose |
|------|---------|
| `cmux send --surface <id> -- <text>` | Raw text, no newline |
| `cmux send-key --surface <id> <KEY>` | Named key (Return, Escape, C-c, …) |
| `cmux read-screen --surface <id> [--scrollback N]` | Capture visible buffer |
| `cmux refresh-surfaces --workspace <id>` | Force a paint; call before every read |
| `./scripts/cmux-send.sh <project> <role> <text> [--enter\|--key KEY]` | Hides send vs send-key |

> **Trailing newline rule.** `cmux send` does NOT append Enter. To run a
> command, follow with `cmux send-key Return` — or use `cmux-send.sh`
> with `--enter`, which routes correctly. Forgetting this is the single
> most common mistake.

> **Refresh before read.** cmux renders asynchronously; `read-screen`
> can return stale output until the surface repaints. Always call
> `refresh-surfaces` (then a short sleep) before a read.

## Status & notifications

| Verb | Purpose |
|------|---------|
| `cmux set-status --surface <id> <text>` | Status line on the tab |
| `cmux set-progress --surface <id> <0-100>` | Progress indicator |
| `cmux log --surface <id> <text>` | Append to cmux log surface |
| `cmux notify --workspace <id> --title <t> --body <b>` | macOS notification |
| `cmux list-notifications --json` | Pending toasts |
| `cmux clear-notifications` | Dismiss all |

Use `set-status` for long jobs — it updates the tab chrome so you can
see "building… 3m" without switching tabs.

## Cross-workspace targeting

`--surface <id>` is always unambiguous — it globally identifies one
pane. `--workspace <id>` is for workspace-level verbs (list, rename,
close). **Never pass both.** If you need to act on a pane in a
different workspace, resolve the surface id by name first — don't rely
on focus:

```bash
WS=$(./scripts/cmux-find.sh myproj | jq -r .workspace)
SID=$(./scripts/cmux-find.sh myproj \
      | jq -r '.tabs[] | select(.tab == "myproj:dev") | .surface')
cmux refresh-surfaces --surface "$SID"
```

## Gotchas (read these before anything else breaks)

1. **`cmux send` has no newline.** Pair with `send-key Return` or use
   `cmux-send.sh --enter`. See `references/troubleshooting.md` §5.
2. **`read-screen` returns stale output.** Call `refresh-surfaces`
   first. See §2.
3. **PTY init race after `new-split`.** Sleep 500ms or wait for the
   shell prompt before sending. See §1.
4. **Browser refs invalidate on navigation.** Re-find after every
   `goto`/`back`/`reload`. See `references/browser.md`.
5. **Never pass both `--surface` and `--workspace`.** See §3.
6. **Workspace restart loses surfaces.** After a cmux daemon crash,
   `close-workspace --force` and rebuild via `cmux-restore.sh`. See §6.

## Workflow 1 — open or attach to a project

```bash
# Idempotent: reuses an existing workspace, only creates if missing.
./scripts/cmux-project.sh "$(basename "$PWD")" code-dev-logs

# Point each tab's shell at the project dir (no-op if tab already exists)
./scripts/cmux-tab.sh "$(basename "$PWD")" code  "$PWD"
./scripts/cmux-tab.sh "$(basename "$PWD")" dev   "$PWD"
./scripts/cmux-tab.sh "$(basename "$PWD")" logs  "$PWD"
```

Layouts (`single`, `code-dev`, `code-dev-logs`, `grid`) are only applied
on first create — they won't clobber a workspace you're already using.
Template details in `references/layouts.md`.

## Workflow 2 — subagent in a named tab

```bash
./scripts/cmux-tab.sh myproj agent:1 "$PWD"
./scripts/cmux-send.sh myproj agent:1 \
  "claude code --dangerously-skip-permissions" --enter
sleep 2
./scripts/cmux-send.sh myproj agent:1 "Implement docs/plan.md. Commit." --enter
```

Full lifecycle (trust-dialog handling, completion polling, harvest)
lives in `references/subagent-pattern.md`. For fan-out across 2×2:
`cmux-project.sh myproj grid`, then loop over `agent:0..3`.

## Workflow 3 — long-running process in a dedicated split

```bash
./scripts/cmux-tab.sh myproj dev "$PWD"
./scripts/cmux-send.sh myproj dev "bun dev" --enter

# Check status later
SID=$(./scripts/cmux-find.sh myproj \
      | jq -r '.tabs[] | select(.tab == "myproj:dev") | .surface')
cmux refresh-surfaces --surface "$SID"
cmux read-screen --surface "$SID" --scrollback 200 | tail -30
```

`refresh-surfaces` is required before every read (gotcha #2).

## Workflow 4 — snapshot / restore

```bash
mkdir -p .cmux
./scripts/cmux-snapshot.sh myproj > .cmux/myproj.json

# Later, or on a fresh machine:
./scripts/cmux-restore.sh myproj < .cmux/myproj.json

# Or clone the workspace under a new name:
./scripts/cmux-restore.sh myproj-2 < .cmux/myproj.json
```

Snapshot records the tab set and best-effort cwd per tab. Split geometry
comes from cmux's raw `list-pane-surfaces` output and is informational —
restore rebuilds canonical tabs, not pixel-perfect geometry.

## References

- `references/browser.md` — cmux browser verbs (navigate, find, click,
  fill, read, wait, eval) with ref-invalidation rules.
- `references/layouts.md` — the four canonical `cmux.json` templates
  (single, code-dev, code-dev-logs, grid) + ASCII previews.
- `references/ssh.md` — `cmux ssh` remote workspaces and the
  `host:project` naming rule.
- `references/socket-api.md` — V2 JSON-RPC over `$CMUX_SOCKET_PATH`
  when CLI overhead in tight loops becomes a problem.
- `references/subagent-pattern.md` — five-phase subagent lifecycle
  (spawn → trust → prompt → wait → harvest) in named tabs.
- `references/troubleshooting.md` — the six-item failure-mode table
  (PTY race, stale reads, surface vs workspace, ref invalidation,
  send+newline, orphan workspace).
