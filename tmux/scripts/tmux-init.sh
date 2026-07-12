#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat <<'USAGE'
Usage: tmux-init.sh --name <session-name> [options]

Bootstrap a tmux session with optional visible iTerm2 pane.

Options:
  -n, --name        session name (required, slug-like, no spaces)
  -S, --socket      socket path (default: $SOCKET_DIR/<name>.sock)
  --no-split        skip iTerm2 pane splitting
  --direction h|v   split direction (default: v)
  -h, --help        show this help

Output (JSON):
  socket, session, target, monitor_cmd, iterm2_session_id (if split)
USAGE
}

name=""
socket=""
no_split=false
direction="v"
socket_dir="${CLAUDE_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/claude-tmux-sockets}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name)       name="${2-}"; shift 2 ;;
    -S|--socket)     socket="${2-}"; shift 2 ;;
    --no-split)      no_split=true; shift ;;
    --direction)     direction="${2-}"; shift 2 ;;
    -h|--help)       usage; exit 0 ;;
    *)               echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$name" ]]; then
  echo "session name is required" >&2
  usage
  exit 1
fi

mkdir -p "$socket_dir"
if [[ -z "$socket" ]]; then
  socket="$socket_dir/${name}.sock"
fi

# Create detached tmux session
tmux -S "$socket" new -d -s "$name" -n shell

# Wait for shell prompt
bash "$SCRIPT_DIR/wait-for-text.sh" -S "$socket" -t "${name}:0.0" -p '^\$' -T 15 -l 4000 || true

monitor_cmd="tmux -S $socket attach -t $name"
target="${name}:0.0"
iterm2_sid=""

# Try to split a visible iTerm2 pane via the it2 CLI.
# Falls back silently to no-split when it2 or $ITERM_SESSION_ID is unavailable.
if [[ "$no_split" != true ]]; then
  if command -v it2 >/dev/null 2>&1 && [[ -n "${ITERM_SESSION_ID:-}" ]]; then
    if [[ "$direction" == "h" ]]; then
      split_verb="split"
    else
      split_verb="vsplit"
    fi
    # it2 split/vsplit prints the new pane's session ID — capture it
    iterm2_sid=$(it2 "$split_verb" -s "$ITERM_SESSION_ID" 2>&1 | grep -oE '[A-F0-9-]{36}') || iterm2_sid=""
    if [[ -n "$iterm2_sid" ]]; then
      # Attach tmux in the new pane (it2 run appends the newline)
      it2 run -s "$iterm2_sid" "$monitor_cmd" >/dev/null 2>&1 || true
    fi
  fi
fi

# Build JSON output
result="{\"socket\":\"$socket\",\"session\":\"$name\",\"target\":\"$target\",\"monitor_cmd\":\"$monitor_cmd\""
if [[ -n "$iterm2_sid" ]]; then
  result+=",\"iterm2_session_id\":\"$iterm2_sid\""
fi
result+="}"

echo "$result"
