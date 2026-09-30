#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="${1:?Usage: open_monitor.sh <log_file> [exit_file] [label]}"
EXIT_FILE="${2:-}"
LABEL="${3:-Codex live monitor}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
command -v python3 >/dev/null
mkdir -p "$(dirname "$LOG_FILE")"
touch "$LOG_FILE"
LOG_FILE="$(cd "$(dirname "$LOG_FILE")" && pwd -P)/$(basename "$LOG_FILE")"
MONITOR_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-monitor.XXXXXX")"
COMMAND_FILE="$MONITOR_DIR/monitor.command"
READY_FILE="$MONITOR_DIR/ready"
{
  printf '#!/usr/bin/env bash\n'
  printf '%q %q %q %q %q %q\n' "$(command -v python3)" \
    "$SCRIPT_DIR/follow_log.py" "$LOG_FILE" "$EXIT_FILE" "$LABEL" "$READY_FILE"
  printf 'read -r -p "Press Enter to close this monitor."\n'
} > "$COMMAND_FILE"
chmod 700 "$COMMAND_FILE"
SESSION_ID="$(bash "$SCRIPT_DIR/launch_iterm.sh" "$COMMAND_FILE" "$LABEL")"
for ATTEMPT in {1..50}; do
  [ ! -f "$READY_FILE" ] || break
  sleep 0.1
done
[ -f "$READY_FILE" ] || { printf 'iTerm2 observer did not start.\n' >&2; exit 1; }
printf 'Codex live monitor in iTerm2: %s\nSession: %s\nLog: %s\n' \
  "$LABEL" "$SESSION_ID" "$LOG_FILE" >&2
