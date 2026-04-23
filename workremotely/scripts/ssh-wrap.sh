#!/usr/bin/env bash
# PreToolUse hook for Bash. Wraps the command with ssh to the marker's host
# when the tool's cwd is inside a .workremotely-scoped directory tree.
#
# Reads hook JSON on stdin, emits hookSpecificOutput with updatedInput on stdout.
# Exits 0 with no body when inactive (passthrough).
set -euo pipefail

INPUT="$(cat)"

CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"
CWD="$(printf '%s' "$INPUT" | jq -r '.cwd // .tool_input.cwd // empty')"
[ -z "$CMD" ] && exit 0
[ -z "$CWD" ] && CWD="$PWD"

# Management escape hatch: never wrap calls to the workremotely scripts
# themselves, or a bare `rm` on the marker file. Otherwise you can't turn it
# off without ssh reaching whichever host the marker points to.
case "$CMD" in
  *workremotely/scripts/*) exit 0 ;;
  *.workremotely*) exit 0 ;;
esac

# Walk up from CWD to find a .workremotely marker.
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

# Remote cwd mirrors local cwd path (assumes sshfs/matching layout; user's call).
REMOTE_CWD="$CWD"

# Use bash -lc with a single quoted arg. printf %q makes the command safe
# to re-parse once on the remote side.
QUOTED_CMD="$(printf '%q' "$CMD")"
WRAPPED="ssh -o BatchMode=yes $(printf '%q' "$HOST") bash -lc $(printf '%q' "cd $(printf '%q' "$REMOTE_CWD") && eval $QUOTED_CMD")"

UPDATED="$(printf '%s' "$INPUT" | jq --arg c "$WRAPPED" '.tool_input | .command=$c')"
jq -n --argjson u "$UPDATED" '{hookSpecificOutput:{hookEventName:"PreToolUse",updatedInput:$u}}'
