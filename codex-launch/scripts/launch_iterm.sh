#!/usr/bin/env bash
set -euo pipefail

COMMAND_FILE="${1:?Usage: launch_iterm.sh <command_file> <label>}"
LABEL="${2:?A session label is required}"
command -v it2 >/dev/null
command -v timeout >/dev/null
printf -v COMMAND 'bash %q' "$COMMAND_FILE"
# iTerm 3.7.4 on macOS 27 crashes when it launches a new tab from a profile (Cmd+T,
# `it2 newtab`); three times on 2026-10-15 that took every session with it. With tmux session
# `main` up, the monitor becomes a tmux window, so no profile launch runs. It goes into its
# own session `codex` (created on first use) so monitors stay out of `main`'s tabs; view it
# with `tmux attach -t codex` or `tmux switch-client -t codex`.
# Prints the tmux pane id instead of an iTerm session id.
if command -v tmux >/dev/null && tmux has-session -t main 2>/dev/null; then
  if tmux has-session -t codex 2>/dev/null; then
    PANE="$(tmux new-window -P -F '#{pane_id}' -t codex: -n "$LABEL" "$COMMAND")"
  else
    PANE="$(tmux new-session -d -P -F '#{pane_id}' -s codex -n "$LABEL" "$COMMAND")"
  fi
  tmux set -w -t "$PANE" @group codex
  printf '%s\n' "$PANE"
  exit 0
fi
TAB_RESULT="$(timeout 20 it2 newtab --command "$COMMAND")"
TAB_ID="${TAB_RESULT##*Created new tab: }"
SESSION_ID="$(timeout 20 it2 session list --json | python3 -c '
import json, sys
matches = [s["id"] for s in json.load(sys.stdin) if str(s["tab_id"]) == sys.argv[1].strip()]
if len(matches) != 1:
    raise SystemExit("Cannot uniquely resolve the new iTerm2 session.")
print(matches[0])
' "$TAB_ID")"
timeout 20 it2 session set-name -s "$SESSION_ID" "$LABEL" >&2
timeout 20 it2 session focus "$SESSION_ID" >&2
printf '%s\n' "$SESSION_ID"
