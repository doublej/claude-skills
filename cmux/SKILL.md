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

<prerequisites>
- cmux installed (`brew install cmux` or from the app bundle).
- `CMUX_SOCKET_PATH` exported (cmux does this automatically in every
  shell it spawns). If unset, you're running outside cmux — most verbs
  fail hard with a clear error.
- `jq` available (`brew install jq`). Every helper uses it to parse
  cmux JSON output.
</prerequisites>

<hierarchy>
```
cmux app
└── workspace            (1 per project, name = project basename)
    └── tab              (name = <project>:<role>)
        └── split(s)     (row/column geometry inside the tab)
```

**Reuse before create. Always.** Every helper first looks up by name;
creation only happens when the lookup misses. That's the entire skill.
</hierarchy>

<naming_conventions>

- **Workspace name** = project directory basename. `myproj`, not
  `myproj-2025-04` or `jj-myproj`. One project, one workspace, forever.
- **Tab name** = `<project>:<role>` where role is from the fixed enum
  below. Multi-agent tabs use `agent:<id>` (id is numeric or slug).
- **Role enum**: `code` (editor), `dev` (watcher/server), `logs`
  (tails/journals), `tests` (watcher), `browser` (cmux browser surface),
  `shell` (scratch), `build` (compiler output), `db` (repl), `notes`
  (scratch docs), `agent:<id>` (a Claude Code or similar subagent),
  `svc:<slug>` (a named dev service inside a multi-component workspace —
  `svc:backend`, `svc:webui`, etc.).

If a role you want isn't in the enum, pick `shell` — don't invent new
role names unless you add them to `scripts/_lib.sh` CMUX_ROLES.
</naming_conventions>

<discovery>

| Verb | Purpose |
|------|---------|
| `cmux identify --json` | Daemon version, socket path, self-check |
| `cmux list-workspaces --json` | All workspaces + tab counts |
| `cmux list-pane-surfaces --workspace <id> --json` | Tabs in a workspace |
| `cmux tree --workspace <id>` | Human-readable split tree |
| `./scripts/cmux-find.sh <project>` | One-shot lookup → JSON, exit 1 if absent |
</discovery>

<lifecycle>

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
</lifecycle>

<io>

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
</io>

<status_notifications>

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
</status_notifications>

<cross_workspace_targeting>

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
</cross_workspace_targeting>

<gotchas>

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
</gotchas>

<workflow_1_project_access>

**Preferred entry point:** one command spins the whole workspace from
either a `.cmux/workspace.json` in the repo, a bundled ecosystem spec,
or atlas-derived defaults — and can resume the last Claude Code session:

```bash
./scripts/cmux-workspace.sh "$(basename "$PWD")" --resume-claude
```

Resolution order: `<project>/.cmux/workspace.json` → `references/ecosystems.json`
→ atlas API (`localhost:47891/api/projects`) → minimal fallback. Use
`--dry-run` to preview the plan without touching cmux. Full schema +
flags in `references/workspace-spec.md`.

If you need finer control, compose the primitives directly:

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
</workflow_1_project_access>

<workflow_2_subagent>

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
</workflow_2_subagent>

<workflow_3_long_running>

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
</workflow_3_long_running>

<workflow_4_snapshot_restore>

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
</workflow_4_snapshot_restore>

<feedback_loop>

This skill evolves from real usage friction — the only source of signal
the user has is **you** logging what broke or confused you.

**Before ending any turn that used a cmux verb**, ask yourself:

1. Did a documented flag/verb behave differently than SKILL.md said?
2. Did you have to retry, guess args, or read source to find the shape?
3. Was an error message vague, misleading, or missing a fix hint?
4. Did you wish for a helper that doesn't exist, or write an awkward
   inline workaround?
5. Did you almost clobber running state (re-sent to a live tab, lost a
   session id, etc.)?

**If any answer is yes → append one entry to `cmux/FEEDBACK.md`** via
the Edit tool. Use this exact template; one entry is enough:

```markdown
### YYYY-MM-DD — <1-line subject line, imperative>
**Tried:**   <command or intent — 1 line>
**Broke:**   <concrete friction — error text, surprise, missing helper>
**Fix idea:** <doc line / new helper / clearer error / schema change>
```

**If all answers are no → skip silently.** Don't log "everything was
fine" — absence of entries is the positive signal.

The log lives in the skill source, not per-project, so every session
harvests into the same pile. Do not gate this on task size — a 2-verb
task that surprised you deserves a log entry just as much as a 20-verb
one. Rule of thumb: if you muttered "huh" once, write it down.
</feedback_loop>

<references>

- `references/workspace-spec.md` — `.cmux/workspace.json` schema,
  resolution order, Claude session resume rules (read this before
  hand-authoring a spec or tweaking `ecosystems.json`).
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
</references>
