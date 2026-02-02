#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat <<'USAGE'
Usage: tmux-run.sh -t target <command> [options]

Send a command to a tmux pane, wait for completion, and capture output.

Options:
  -t, --target    tmux target (session:window.pane), required
  -S, --socket    tmux socket path (passed to tmux -S)
  -w, --wait      fixed wait time in seconds (default: 2)
  -p, --pattern   wait for regex pattern instead of fixed time
  -T, --timeout   pattern timeout in seconds (default: 15)
  -l, --lines     history lines to capture (default: 200)
  -h, --help      show this help

Examples:
  tmux-run.sh -S /tmp/claude.sock -t sess:0.0 "echo hello" --wait 1
  tmux-run.sh -S /tmp/claude.sock -t sess:0.0 "pip install x" --pattern "Successfully"
USAGE
}

target=""
socket=""
wait_time=2
pattern=""
timeout=15
lines=200
command_text=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target)   target="${2-}"; shift 2 ;;
    -S|--socket)   socket="${2-}"; shift 2 ;;
    -w|--wait)     wait_time="${2-}"; shift 2 ;;
    -p|--pattern)  pattern="${2-}"; shift 2 ;;
    -T|--timeout)  timeout="${2-}"; shift 2 ;;
    -l|--lines)    lines="${2-}"; shift 2 ;;
    -h|--help)     usage; exit 0 ;;
    -*)            echo "Unknown option: $1" >&2; usage; exit 1 ;;
    *)             command_text="$1"; shift ;;
  esac
done

if [[ -z "$target" || -z "$command_text" ]]; then
  echo "target and command are required" >&2
  usage
  exit 1
fi

tmux_cmd=(tmux)
if [[ -n "$socket" ]]; then
  tmux_cmd+=(-S "$socket")
fi

# Send command text literally, then Enter
"${tmux_cmd[@]}" send-keys -t "$target" -l -- "$command_text"
"${tmux_cmd[@]}" send-keys -t "$target" Enter

# Wait: pattern-based or fixed
if [[ -n "$pattern" ]]; then
  wait_args=(-t "$target" -p "$pattern" -T "$timeout" -l "$lines")
  if [[ -n "$socket" ]]; then
    wait_args+=(-S "$socket")
  fi
  bash "$SCRIPT_DIR/wait-for-text.sh" "${wait_args[@]}"
else
  sleep "$wait_time"
fi

# Capture and print non-blank lines
"${tmux_cmd[@]}" capture-pane -p -J -t "$target" -S "-${lines}" | grep -v '^$' || true
