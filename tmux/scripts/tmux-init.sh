#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat <<'USAGE'
Usage: tmux-init.sh --name <session-name> [options]

Bootstrap a tmux session with an optional visible pane split next to the caller.

Options:
  -n, --name        session name (required, slug-like, no spaces)
  -S, --socket      socket path (default: $SOCKET_DIR/<name>.sock)
  --no-split        skip pane splitting
  --direction h|v   split direction (default: v)
  -h, --help        show this help

Output (JSON):
  socket, session, target, monitor_cmd, pane_id (if split)
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
pane_id=""

# Split the caller's tmux pane and attach the agent session in it.
# Falls back silently to no-split when $TMUX_PANE is unset (caller not inside tmux).
if [[ "$no_split" != true && -n "${TMUX_PANE:-}" ]]; then
  # v = side by side (tmux -h), h = stacked (tmux -v)
  if [[ "$direction" == "h" ]]; then split_flag="-v"; else split_flag="-h"; fi
  # env -u TMUX: tmux refuses to attach from inside another tmux session otherwise
  pane_id=$(tmux split-window "$split_flag" -d -t "$TMUX_PANE" -P -F '#{pane_id}' "env -u TMUX $monitor_cmd" 2>/dev/null) || pane_id=""
fi

# Build JSON output
result="{\"socket\":\"$socket\",\"session\":\"$name\",\"target\":\"$target\",\"monitor_cmd\":\"$monitor_cmd\""
if [[ -n "$pane_id" ]]; then
  result+=",\"pane_id\":\"$pane_id\""
fi
result+="}"

echo "$result"
