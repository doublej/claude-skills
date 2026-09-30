#!/usr/bin/env bash
set -euo pipefail

LABEL="${1:?Usage: run_monitored.sh <label> <command> [args...]}"
shift
[ "$#" -gt 0 ] || { printf 'A command is required.\n' >&2; exit 2; }
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-run.XXXXXX")"
LOG_FILE="$RUN_DIR/session.log"
EXIT_FILE="$RUN_DIR/exit-code"
printf 'Starting: %s\n' "$LABEL" > "$LOG_FILE"
bash "$SCRIPT_DIR/open_monitor.sh" "$LOG_FILE" "$EXIT_FILE" "$LABEL"
trap 'printf "%s\n" "$?" > "$EXIT_FILE"' EXIT
set +e
"$@" 2>&1 | tee -a "$LOG_FILE"
RUN_STATUS="${PIPESTATUS[0]}"
set -e
exit "$RUN_STATUS"
