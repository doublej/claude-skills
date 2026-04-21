#!/usr/bin/env bash
# shutdown.sh — print a lead-executable plan to gracefully shut down a team.
#
# This script does NOT itself call SendMessage / TeamDelete (those tools live
# in Claude Code's runtime, not shell). It prints the exact sequence the lead
# should execute. The scripted layer is for presentation; the tool calls are
# for the lead.
#
# Usage: shutdown.sh <team-name>

set -euo pipefail

TEAM="${1:-}"
if [[ -z "$TEAM" ]]; then
  echo "usage: shutdown.sh <team-name>" >&2
  exit 2
fi

TEAM_DIR="$HOME/.claude/teams/$TEAM"
if [[ ! -d "$TEAM_DIR" ]]; then
  echo "[teams:shutdown] team '$TEAM' not found in ~/.claude/teams/" >&2
  exit 2
fi

echo "[teams:shutdown] Lead — execute the following tool calls in order:"
echo

if command -v jq >/dev/null 2>&1 && [[ -f "$TEAM_DIR/config.json" ]]; then
  members=$(jq -r '.members[]?.name // empty' "$TEAM_DIR/config.json" 2>/dev/null)
  while IFS= read -r name; do
    [[ -z "$name" ]] && continue
    echo "  SendMessage({to: \"$name\", message_type: \"shutdown_request\", message: \"Please wrap up and ack.\"})"
  done <<< "$members"
  echo "  # wait for each to reply with shutdown_response"
  echo "  TeamDelete({team_name: \"$TEAM\"})"
else
  echo "  # config.json unreadable — broadcast shutdown and delete:"
  echo "  SendMessage({to: \"broadcast\", team_name: \"$TEAM\", message_type: \"shutdown_request\", message: \"wrap up\"})"
  echo "  TeamDelete({team_name: \"$TEAM\"})"
fi

echo
echo "[teams:shutdown] After TeamDelete, run:"
echo "  bash ${0%shutdown.sh}cleanup.sh $TEAM"
