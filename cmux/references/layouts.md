# Layout templates

Four canonical shapes. Pick by project type:

- **single**   — no split, just a shell. Quick scripts, one-task sessions.
- **code-dev** — editor pane + dev server pane. Frontend / backend / anything with a watcher.
- **code-dev-logs** — editor + dev + logs/tailer. Full-stack with external services.
- **grid**     — four-up. Multi-agent work, claude-team layouts.

Each template includes the `cmux.json` that ships it, an ASCII preview, and
the `cmux-project.sh` invocation. cmux resolves `cmux.json` in the project
root on workspace creation.

---

## 1. `single`

```
┌────────────────────────┐
│  project:shell         │
│                        │
│                        │
└────────────────────────┘
```

```json
{
  "workspace": { "name": "{{project}}" },
  "tabs": [ { "name": "{{project}}:shell" } ]
}
```

```bash
./scripts/cmux-project.sh myproj single
```

No split. Useful when the workspace is mainly for running one long command
or for keeping a SHELL scoped to a project directory.

---

## 2. `code-dev`

```
┌────────────┬────────────┐
│ :code      │ :dev       │
│ (editor)   │ (server)   │
│            │            │
└────────────┴────────────┘
```

```json
{
  "workspace": { "name": "{{project}}" },
  "splits": [
    { "tab": "{{project}}:code", "direction": "row" },
    { "tab": "{{project}}:dev",  "direction": "row", "parent": "root" }
  ]
}
```

```bash
./scripts/cmux-project.sh myproj code-dev
./scripts/cmux-send.sh     myproj dev  "bun dev" --enter
```

Classic web/backend layout. Editor left, dev server right. Typically
`:code` gets `$EDITOR .` and `:dev` gets the project's start command.

---

## 3. `code-dev-logs`

```
┌────────────┬────────────┐
│ :code      │ :dev       │
│            │            │
│            ├────────────┤
│            │ :logs      │
└────────────┴────────────┘
```

```json
{
  "workspace": { "name": "{{project}}" },
  "splits": [
    { "tab": "{{project}}:code", "direction": "row" },
    { "tab": "{{project}}:dev",  "direction": "row",    "parent": "root" },
    { "tab": "{{project}}:logs", "direction": "column", "parent": "dev"  }
  ]
}
```

```bash
./scripts/cmux-project.sh myproj code-dev-logs
./scripts/cmux-send.sh     myproj dev  "bun dev" --enter
./scripts/cmux-send.sh     myproj logs "tail -F logs/app.log" --enter
```

Full-stack shape. `:logs` is where you aim `docker compose logs -f`,
`stern`, `tail -F`, or whatever external signal you need next to the
dev server without losing screen real estate to a third vertical.

---

## 4. `grid` (claude-team, 2×2)

```
┌────────────┬────────────┐
│ :agent:0   │ :agent:1   │
├────────────┼────────────┤
│ :agent:2   │ :agent:3   │
└────────────┴────────────┘
```

```json
{
  "workspace": { "name": "{{project}}" },
  "splits": [
    { "tab": "{{project}}:agent:0", "direction": "row" },
    { "tab": "{{project}}:agent:1", "direction": "row",    "parent": "root"    },
    { "tab": "{{project}}:agent:2", "direction": "column", "parent": "agent:0" },
    { "tab": "{{project}}:agent:3", "direction": "column", "parent": "agent:1" }
  ]
}
```

```bash
./scripts/cmux-project.sh myproj grid
for i in 0 1 2 3; do
  ./scripts/cmux-send.sh myproj "agent:$i" "claude code --dangerous" --enter
done
```

Four-up for competing agents, review panels, parallel refactors. Pair
with `references/subagent-pattern.md` for lifecycle.

---

## Picking a layout

| You want to… | Use |
|---|---|
| Run one script | `single` |
| Edit + dev server | `code-dev` |
| Edit + dev + tail | `code-dev-logs` |
| Run N agents side-by-side | `grid` |

If you need something else, don't build an NxM generator — it's almost
always a sign that the workspace is doing too much. Split into two
workspaces instead.
