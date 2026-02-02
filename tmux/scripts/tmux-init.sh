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

# Try to split iTerm2 pane for visibility
if [[ "$no_split" != true ]]; then
  iterm2_skill_dir="${HOME}/.claude/skills/iterm2/scripts"
  iterm2_python="${iterm2_skill_dir}/.venv/bin/python3"
  iterm2_script="${iterm2_skill_dir}/iterm2_run.py"

  if [[ -x "$iterm2_python" && -f "$iterm2_script" ]]; then
    split_result=$("$iterm2_python" "$iterm2_script" split-and-run \
      --direction "$direction" \
      --title "$name" \
      "$monitor_cmd" \
      --wait 2 2>/dev/null) || split_result=""
    if [[ -n "$split_result" ]]; then
      iterm2_sid=$(echo "$split_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null) || iterm2_sid=""
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
