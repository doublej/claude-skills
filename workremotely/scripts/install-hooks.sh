#!/usr/bin/env bash
# Install the workremotely PreToolUse + PostToolUse hooks into
# ~/.claude/settings.json. Idempotent: checks for existing entries first.
set -euo pipefail

SETTINGS="${CLAUDE_SETTINGS_PATH:-$HOME/.claude/settings.json}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PRE="$SKILL_DIR/scripts/ssh-wrap.sh"
POST="$SKILL_DIR/scripts/reminder.sh"

if [ ! -f "$SETTINGS" ]; then
  echo '{}' > "$SETTINGS"
fi

chmod +x "$PRE" "$POST" "$SKILL_DIR/scripts/enable.sh" \
  "$SKILL_DIR/scripts/disable.sh" "$SKILL_DIR/scripts/status.sh"

TMP="$(mktemp)"
jq --arg pre "$PRE" --arg post "$POST" '
  .hooks //= {}
  | .hooks.PreToolUse //= []
  | .hooks.PostToolUse //= []
  | .hooks.PreToolUse |= (
      if any(.[]?; .matcher == "Bash" and any(.hooks[]?; .command == $pre))
      then .
      else . + [{matcher: "Bash", hooks: [{type: "command", command: $pre}]}]
      end
    )
  | .hooks.PostToolUse |= (
      if any(.[]?; .matcher == "Bash" and any(.hooks[]?; .command == $post))
      then .
      else . + [{matcher: "Bash", hooks: [{type: "command", command: $post}]}]
      end
    )
' "$SETTINGS" > "$TMP"

mv "$TMP" "$SETTINGS"
echo "installed hooks into $SETTINGS"
echo "  PreToolUse  (Bash): $PRE"
echo "  PostToolUse (Bash): $POST"
