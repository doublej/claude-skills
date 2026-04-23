# Workspace spec (`.cmux/workspace.json`)

`cmux-workspace.sh` resolves the tab set + launch commands from a single
declarative input. This doc covers that input — where it comes from, its
schema, and how it interacts with Claude Code session resume.

## Resolution order

For `cmux-workspace.sh <project>`, the script searches in order and uses
the first hit:

1. **Config file** — `<project-path>/.cmux/workspace.json` (or
   `--config <path>` override). Explicit, version-controllable, wins.
2. **Ecosystem table** — `references/ecosystems.json`, keyed by project
   name. Ships the three documented ecosystems (`project-atlas`,
   `pimpelmees`, `remotevr`).
3. **Atlas auto-derive** — `GET http://localhost:47891/api/projects`,
   match by name, infer a `[code, dev]` spec from `runner`/`framework`/
   `justRecipes`.
4. **Minimal fallback** — one `code` tab at the project root.

The winning source is echoed to stderr and appears as `"source"` in the
final JSON output.

## Schema

```json
{
  "layout": "grid",
  "base":   "multi-stack/project-atlas",
  "tabs": [
    {
      "role":          "svc:api",
      "cwd":           "atlas-api",
      "cmd":           "bun dev",
      "autoLaunch":    true,
      "claudeResume":  false
    }
  ]
}
```

### Fields

| Key | Type | Notes |
|---|---|---|
| `layout` | string, optional | `single` \| `code-dev` \| `code-dev-logs` \| `grid`. User `--layout` wins over this. If absent, the script auto-picks based on tab roles. |
| `base` | string, optional | Ecosystems only (`ecosystems.json`). Relative to `$DEV_ROOT` (`~/Documents/development`). Config files don't use this — the project path IS the config's directory. |
| `tabs` | array, required | One entry per tab. Order is preserved; tabs are created/reused left-to-right. |
| `tabs[].role` | string, required | From the cmux role enum, or `svc:<slug>` for dev services, or `agent:<id>` for AI subagents. See SKILL.md §Naming conventions. |
| `tabs[].cwd` | string, optional | Relative (from project path) or absolute. Default `"."`. Sent as `cd <cwd>` on first creation; ignored on reuse. |
| `tabs[].cmd` | string, optional | Command sent with Enter after the cwd is set. **Only fires on newly created tabs** — existing tabs keep whatever is running. |
| `tabs[].autoLaunch` | bool, default `true` | Set to `false` to create the tab (with cwd) but skip sending `cmd`. Use for "ready but don't start yet" tabs like `tests --watch`. |
| `tabs[].claudeResume` | bool, default `false` | On the `code` tab only: if `true`, on first creation the most recent Claude session for that cwd is resumed via `claude -r <id>`. See below. |

### Layout auto-pick

When neither `--layout` nor spec `layout` is set, the script maps tab
roles to a safe layout:

| Roles (set-equal) | Layout picked |
|---|---|
| `{code, dev, logs}` | `code-dev-logs` |
| `{code, dev}` | `code-dev` |
| any other shape | `single` |

`single` is the safe default because it doesn't pre-create named tabs
that the spec might not use (`grid` would leave `agent:0..3` orphans
when the spec has `svc:*` tabs instead).

## Example: monorepo with two services + logs

`.cmux/workspace.json`:

```json
{
  "layout": "code-dev-logs",
  "tabs": [
    { "role": "code",         "cwd": ".",     "claudeResume": true },
    { "role": "svc:backend",  "cwd": "./api", "cmd": "uv run uvicorn main:app --reload" },
    { "role": "svc:frontend", "cwd": "./web", "cmd": "bun dev" },
    { "role": "logs",         "cwd": ".",     "cmd": "tail -F logs/app.log" },
    { "role": "tests",        "cwd": ".",     "cmd": "bun test --watch", "autoLaunch": false }
  ]
}
```

`./scripts/cmux-workspace.sh myproj` spins the workspace, starts both
services + log tail, leaves the `tests` tab idle (you hit `just test-watch`
when you want it), and resumes the last Claude Code session in the
`code` tab.

## Example: ecosystem entry (`ecosystems.json`)

Ecosystem entries in the bundled table use the same tab schema but add a
`base` relative to `$DEV_ROOT`, because the ecosystem name itself doesn't
map to a single project:

```json
"project-atlas": {
  "base": "multi-stack/project-atlas",
  "layout": "grid",
  "tabs": [
    { "role": "code",         "cwd": ".",              "claudeResume": true },
    { "role": "svc:api",      "cwd": "atlas-api",      "cmd": "bun dev" },
    { "role": "svc:watchdog", "cwd": "atlas-watchdog", "cmd": "bun dev" },
    { "role": "svc:picker",   "cwd": "atlas-picker",   "cmd": "just check", "autoLaunch": false }
  ]
}
```

## Claude Code session resume

Resume-on-launch is opt-in via CLI flag or spec field, and only touches
the `code` tab.

| Trigger | Behavior |
|---|---|
| `--resume-claude` (CLI) | Always fires this run. Reads `~/.claude/projects/<encoded-cwd>/sessions-index.json`, picks the most recent primary (non-sidechain) session, sends `claude -r <id>` to the `code` tab. |
| `--continue-claude` (CLI) | Sends `claude -c` (resume by cwd, built-in to the Claude CLI). |
| `claudeResume: true` in spec | Only fires when the `code` tab was just created. Rerunning the launcher on an existing workspace never re-triggers — respect whatever's live in that tab. |
| neither | Nothing is sent to the `code` tab (it's cd'd and left for the user to start however they want). |

If no prior session exists for the cwd, the script logs a warning and
sends plain `claude` instead.

**Path encoding**: `/` → `-` AND `_` → `-`. A path like
`/Users/me/dev/_management/project` becomes
`-Users-me-dev--management-project`. This matches Claude Code's own
encoding (see `session-search/scripts/session_search.py`
`encode_project_path`).

## Flags cheat sheet

```
cmux-workspace.sh <project> [flags]

-r, --resume-claude    resume most recent session in code tab
--continue-claude      use claude -c instead
--no-launch            create tabs + cd, but skip sending commands
--layout <name>        single | code-dev | code-dev-logs | grid
--config <path>        explicit workspace.json, skips lookup order
--dry-run              print the plan as JSON, don't touch cmux
```

`--dry-run` is the fastest way to validate a new `.cmux/workspace.json`
— it prints exactly which tabs would be created and which commands sent,
without creating anything. Pair with `jq .` for a readable view.

## Rerun semantics

The launcher is idempotent: on the second run against a live workspace
it finds every tab (`created: false`) and skips every `cmd` send. That
means you can run it mid-session to add a new tab from an updated spec
without clobbering running processes. Tabs that were already there keep
running whatever they're running; new tabs in the spec get created and
launched fresh.

The one exception is `--resume-claude`/`--continue-claude` — those fire
unconditionally because you asked for them explicitly this run.
