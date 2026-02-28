# tmux Dev Session Recipes

Full pattern for managing tmux dev sessions from a Justfile. Adapt pane commands and process names per project.

## Template

Replace `SESSION`, `LEFT_CMD`, `RIGHT_CMD` with project-specific values.

```just
# === tmux commands ===
_session := "SESSION"

# Launch dev in tmux with left and right panes, open iTerm
tmux-dev:
    @if tmux has-session -t {{_session}} 2>/dev/null; then \
        echo "Session '{{_session}}' already running. Opening iTerm..."; \
        osascript -e 'tell application "iTerm" to create window with default profile command "/opt/homebrew/bin/tmux attach -t {{_session}}"'; \
    else \
        tmux new-session -d -s {{_session}} -c {{justfile_directory()}}; \
        tmux send-keys -t {{_session}} 'LEFT_CMD' Enter; \
        tmux split-window -h -t {{_session}} -c {{justfile_directory()}}; \
        tmux send-keys -t {{_session}} 'RIGHT_CMD' Enter; \
        tmux select-pane -t {{_session}}:0.0; \
        echo "Started tmux session '{{_session}}' with left and right panes"; \
        sleep 0.5; \
        osascript -e 'tell application "iTerm" to create window with default profile command "/opt/homebrew/bin/tmux attach -t {{_session}}"'; \
    fi

# Attach to running tmux session
tmux-attach:
    @if tmux has-session -t {{_session}} 2>/dev/null; then \
        tmux attach -t {{_session}}; \
    else \
        echo "No session '{{_session}}' found. Use 'just tmux-dev' to start."; \
    fi

# Kill tmux session
tmux-kill:
    @if tmux has-session -t {{_session}} 2>/dev/null; then \
        tmux kill-session -t {{_session}}; \
        echo "Killed session '{{_session}}'"; \
    else \
        echo "No session '{{_session}}' to kill."; \
    fi

# Restart: kill and relaunch
tmux-restart: tmux-kill tmux-dev

# Show recent output from left pane
tmux-logs-left:
    @if tmux has-session -t {{_session}} 2>/dev/null; then \
        tmux capture-pane -t {{_session}}:0.0 -p -S -50; \
    else \
        echo "No session '{{_session}}' found."; \
    fi

# Show recent output from right pane
tmux-logs-right:
    @if tmux has-session -t {{_session}} 2>/dev/null; then \
        tmux capture-pane -t {{_session}}:0.1 -p -S -50; \
    else \
        echo "No session '{{_session}}' found."; \
    fi

# Show tmux session status
tmux-status:
    @if tmux has-session -t {{_session}} 2>/dev/null; then \
        echo "Session '{{_session}}' is running"; \
        tmux list-panes -t {{_session}} -F "Pane #{pane_index}: #{pane_current_command}"; \
    else \
        echo "No session '{{_session}}' found."; \
    fi
```

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
