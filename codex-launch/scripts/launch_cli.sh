#!/bin/bash
# Spawn `codex "<prompt>"` in whatever terminal is currently frontmost.
# Works across iTerm2, Ghostty, Terminal.app, Warp, etc. — uses System Events
# to keystroke into the focused window. The user sees Codex start live.
#
# Usage: launch_cli.sh "<prompt text>" [extra codex flags...]

set -e

PROMPT="${1:?prompt required}"
shift || true
EXTRA_FLAGS="$*"

# Escape double quotes and backslashes for shell-safe single-line keystroke.
ESCAPED=$(printf '%s' "$PROMPT" | sed 's/\\/\\\\/g; s/"/\\"/g')

if [ -n "$EXTRA_FLAGS" ]; then
  CMD="codex $EXTRA_FLAGS \"$ESCAPED\""
else
  CMD="codex \"$ESCAPED\""
fi

# Identify the frontmost app so we can report it back.
FRONT_APP=$(osascript -e 'tell application "System Events" to name of first application process whose frontmost is true')

# AppleScript-escape the command for the keystroke call.
APPLESCRIPT_CMD=$(printf '%s' "$CMD" | sed 's/\\/\\\\/g; s/"/\\"/g')

osascript <<EOF
tell application "System Events"
  keystroke "$APPLESCRIPT_CMD"
  key code 36
end tell
EOF

echo "✓ Sent codex command to frontmost app: $FRONT_APP"
