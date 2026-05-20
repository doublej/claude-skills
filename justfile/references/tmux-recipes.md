# tmux Dev Session Recipes

Full pattern for managing tmux dev sessions from a Justfile. Adapt pane commands and process names per project.

Works across **iTerm, Ghostty, and macOS Terminal**. Falls back to a "attach manually" message for unrecognized terminals. Also detects if you're already inside tmux (`$TMUX`) and uses `switch-client` instead of opening a new window.

## Template

Replace `SESSION`, `LEFT_CMD`, `RIGHT_CMD` with project-specific values.

```just
# === tmux commands ===
_session := "SESSION"

# Launch dev in tmux with left and right panes, open a terminal window
[group('develop')]
tmux-dev:
    #!/usr/bin/env bash
    set -euo pipefail
    if tmux has-session -t {{_session}} 2>/dev/null; then
        echo "Session '{{_session}}' already running."
    else
        tmux new-session -d -s {{_session}} -c {{justfile_directory()}}
        tmux send-keys -t {{_session}} 'LEFT_CMD' Enter
        tmux split-window -h -t {{_session}} -c {{justfile_directory()}}
        tmux send-keys -t {{_session}} 'RIGHT_CMD' Enter
        tmux select-pane -t {{_session}}:0.0
        echo "Started tmux session '{{_session}}' with left and right panes"
        sleep 0.5
    fi
    just _attach-window

# Open a terminal window attached to {{_session}} — auto-detects iTerm/Ghostty/Terminal
[private]
_attach-window:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -n "${TMUX:-}" ]; then
        # Already inside tmux — switch instead of nesting
        tmux switch-client -t {{_session}}
    elif [ "${TERM_PROGRAM:-}" = "iTerm.app" ]; then
        osascript -e 'tell application "iTerm" to create window with default profile command "tmux attach -t {{_session}}"'
    elif [ "${TERM_PROGRAM:-}" = "ghostty" ]; then
        open -na Ghostty --args --command="tmux attach -t {{_session}}"
    elif [ "${TERM_PROGRAM:-}" = "Apple_Terminal" ]; then
        osascript -e 'tell application "Terminal" to do script "tmux attach -t {{_session}}"'
    else
        echo "→ Attach manually: tmux attach -t {{_session}}"
    fi

# Attach to running tmux session in current shell
[group('develop')]
tmux-attach:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux attach -t {{_session}}
    else
        echo "No session '{{_session}}' found. Use 'just tmux-dev' to start."
    fi

# Kill tmux session
[group('develop')]
tmux-kill:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux kill-session -t {{_session}}
        echo "Killed session '{{_session}}'"
    else
        echo "No session '{{_session}}' to kill."
    fi

# Restart: kill and relaunch
[group('develop')]
tmux-restart: tmux-kill tmux-dev

# Show recent output from left pane
[group('develop')]
tmux-logs-left:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux capture-pane -t {{_session}}:0.0 -p -S -50
    else
        echo "No session '{{_session}}' found."
    fi

# Show recent output from right pane
[group('develop')]
tmux-logs-right:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux capture-pane -t {{_session}}:0.1 -p -S -50
    else
        echo "No session '{{_session}}' found."
    fi

# Show tmux session status
[group('develop')]
tmux-status:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        echo "Session '{{_session}}' is running"
        tmux list-panes -t {{_session}} -F "Pane #{pane_index}: #{pane_current_command}"
    else
        echo "No session '{{_session}}' found."
    fi
```

## Terminal dispatch reference

| `$TERM_PROGRAM` | Spawn command |
|---|---|
| `iTerm.app` | `osascript -e 'tell application "iTerm" to create window with default profile command "tmux attach -t SESSION"'` |
| `ghostty` | `open -na Ghostty --args --command="tmux attach -t SESSION"` |
| `Apple_Terminal` | `osascript -e 'tell application "Terminal" to do script "tmux attach -t SESSION"'` |
| anything else | print `→ Attach manually: tmux attach -t SESSION` |

If `$TMUX` is set (already inside tmux), use `tmux switch-client -t SESSION` instead — nesting tmux inside tmux is rarely what you want.

### Verifying the detection works

```sh
echo "$TERM_PROGRAM"   # iTerm.app | ghostty | Apple_Terminal | WezTerm | ...
echo "${TMUX:-not set}" # path to socket if inside tmux, else "not set"
```

### Adding a new terminal (e.g. WezTerm, Alacritty, kitty)

Add another `elif` arm to `_attach-window`. Examples:

- WezTerm: `wezterm cli spawn -- tmux attach -t {{_session}}` (if already running) or `open -na WezTerm --args start -- tmux attach -t {{_session}}`
- kitty: `open -na kitty --args tmux attach -t {{_session}}`
- Alacritty: `open -na Alacritty --args -e tmux attach -t {{_session}}`

## Pane addressing

- `{{_session}}:0.0` — window 0, pane 0 (left)
- `{{_session}}:0.1` — window 0, pane 1 (right)
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
