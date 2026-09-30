#!/usr/bin/env bash
set -euo pipefail

COMMAND_FILE="${1:?Usage: launch_iterm.sh <command_file> <label>}"
LABEL="${2:?A session label is required}"
command -v it2 >/dev/null
command -v timeout >/dev/null
printf -v COMMAND 'bash %q' "$COMMAND_FILE"
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
