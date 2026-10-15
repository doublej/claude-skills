# tmux Dev Session Recipes

Full pattern for managing tmux dev sessions from a Justfile. Adapt pane commands and process names per project.

Attaches through tmux only — it never spawns a terminal app window. Inside tmux (`$TMUX`) it uses `switch-client`; in an interactive shell it attaches; otherwise (agents, CI) it prints the attach command.

## Template

Replace `SESSION`, `LEFT_CMD`, `RIGHT_CMD` with project-specific values.

```just
# === tmux commands ===
_session := "SESSION"

# Launch dev in tmux with left and right panes, then attach
[group('develop')]
tmux-dev:
    #!/usr/bin/env bash
    set -euo pipefail
    if tmux has-session -t {{ _session }} 2>/dev/null; then
        echo "Session '{{ _session }}' already running."
    else
        tmux new-session -d -s {{ _session }} -c {{ justfile_directory() }}
        tmux send-keys -t {{ _session }} 'LEFT_CMD' Enter
        tmux split-window -h -t {{ _session }} -c {{ justfile_directory() }}
        tmux send-keys -t {{ _session }} 'RIGHT_CMD' Enter
        tmux select-pane -t {{ _session }}:0.0
        echo "Started tmux session '{{ _session }}' with left and right panes"
        sleep 0.5
    fi
    just _attach-window

# Attach to {{ _session }} through tmux (switch, attach, or print the command)
[private]
_attach-window:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -n "${TMUX:-}" ]; then
        tmux switch-client -t {{ _session }}
    elif [ -t 0 ]; then
        tmux attach -t {{ _session }}
    else
        echo "→ Attach: tmux attach -t {{ _session }}"
    fi

# Attach to running tmux session in current shell
[group('develop')]
tmux-attach:
    #!/usr/bin/env bash
    if tmux has-session -t {{ _session }} 2>/dev/null; then
        tmux attach -t {{ _session }}
    else
        echo "No session '{{ _session }}' found. Use 'just tmux-dev' to start."
    fi

# Kill tmux session
[group('develop')]
tmux-kill:
    #!/usr/bin/env bash
    if tmux has-session -t {{ _session }} 2>/dev/null; then
        tmux kill-session -t {{ _session }}
        echo "Killed session '{{ _session }}'"
    else
        echo "No session '{{ _session }}' to kill."
    fi

# Restart: kill and relaunch
[group('develop')]
tmux-restart: tmux-kill tmux-dev

# Show recent output from left pane
[group('develop')]
tmux-logs-left:
    #!/usr/bin/env bash
    if tmux has-session -t {{ _session }} 2>/dev/null; then
        tmux capture-pane -t {{ _session }}:0.0 -p -S -50
    else
        echo "No session '{{ _session }}' found."
    fi

# Show recent output from right pane
[group('develop')]
tmux-logs-right:
    #!/usr/bin/env bash
    if tmux has-session -t {{ _session }} 2>/dev/null; then
        tmux capture-pane -t {{ _session }}:0.1 -p -S -50
    else
        echo "No session '{{ _session }}' found."
    fi

# Show tmux session status
[group('develop')]
tmux-status:
    #!/usr/bin/env bash
    if tmux has-session -t {{ _session }} 2>/dev/null; then
        echo "Session '{{ _session }}' is running"
        tmux list-panes -t {{ _session }} -F "Pane #{pane_index}: #{pane_current_command}"
    else
        echo "No session '{{ _session }}' found."
    fi
```

## Attach dispatch reference

| Situation | Action |
|---|---|
| `$TMUX` set | `tmux switch-client -t SESSION` (nesting tmux inside tmux is rarely what you want) |
| `[ -t 0 ]` (interactive) | `tmux attach -t SESSION` |
| anything else | print `→ Attach: tmux attach -t SESSION` |

Do not add terminal-app arms (`osascript "iTerm"`, `open -na Ghostty`, WezTerm, kitty): opening profile windows crashes iTerm 3.7.4, and under iTerm's tmux integration tmux windows already show as tabs.

## Pane addressing

- `{{ _session }}:0.0` — window 0, pane 0 (left)
- `{{ _session }}:0.1` — window 0, pane 1 (right)
- For 3+ panes, use `split-window -v` for vertical splits

## Common pane layouts

| Layout | Left (0.0) | Right (0.1) |
|--------|-----------|-------------|
| Bun monorepo | `bun run dev:worker` | `bun run dev:client` |
| Python + frontend | `uv run python main.py` | `bun run dev` |
| API + UI | `bun run dev:api` | `bun run dev:ui` |

## Naming the log recipes

Name log recipes after what runs in each pane, not left/right:
- `tmux-logs-worker` / `tmux-logs-client`
- `tmux-logs-api` / `tmux-logs-ui`
- `tmux-logs-backend` / `tmux-logs-frontend`
