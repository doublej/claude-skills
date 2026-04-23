#!/usr/bin/env bash
# PostToolUse hook. If workremotely is active in the tool's cwd AND at least
# 5 minutes have passed since the last reminder for this session, inject a
# one-line reminder via additionalContext. Silent otherwise.
set -euo pipefail

INPUT="$(cat)"
SESSION="$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"')"
CWD="$(printf '%s' "$INPUT" | jq -r '.cwd // .tool_input.cwd // empty')"
[ -z "$CWD" ] && CWD="$PWD"

SCOPE=""
DIR="$CWD"
while [ -n "$DIR" ] && [ "$DIR" != "/" ]; do
  if [ -f "$DIR/.workremotely" ]; then
    SCOPE="$DIR"
    break
  fi
  DIR="$(dirname "$DIR")"
done
[ -z "$SCOPE" ] && exit 0

HOST="$(grep -E '^host=' "$SCOPE/.workremotely" 2>/dev/null | cut -d= -f2-)"
[ -z "$HOST" ] && HOST="nas"

STATE_DIR="${TMPDIR:-/tmp}/claude-workremotely"
mkdir -p "$STATE_DIR"
STAMP="$STATE_DIR/$SESSION.last"

NOW="$(date +%s)"
LAST=0
if [ -f "$STAMP" ]; then
  LAST="$(stat -f %m "$STAMP" 2>/dev/null || stat -c %Y "$STAMP" 2>/dev/null || echo 0)"
fi

if [ $((NOW - LAST)) -lt 300 ]; then
  exit 0
fi

touch "$STAMP"

MSG="[workremotely ACTIVE — host=$HOST scope=$SCOPE. All Bash commands in this scope are executed via ssh. Run scripts/disable.sh to turn off.]"
jq -n --arg m "$MSG" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$m}}'
