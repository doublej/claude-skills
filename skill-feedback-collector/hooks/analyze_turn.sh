#!/usr/bin/env bash
# Stop hook — spawns the analyzer in the background and exits fast.
# Hook payload (stdin) contains session_id + transcript_path + stop_hook_active.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$SKILL_DIR/state/logs"
mkdir -p "$LOG_DIR"

# Capture payload to a temp file so the backgrounded process can read it
PAYLOAD_FILE="$(mktemp -t skill-fb-payload.XXXXXX)"
cat > "$PAYLOAD_FILE"

# Fast exit if no markers exist anywhere — common case for sessions that didn't use skills
[ -z "$(ls -A "$SKILL_DIR/state/markers" 2>/dev/null)" ] && { rm -f "$PAYLOAD_FILE"; exit 0; }

# Background-detach the analyzer: disown, redirect IO, do not block Stop event
LOG_FILE="$LOG_DIR/analyzer-$(date +%s).log"
nohup python3 "$SKILL_DIR/scripts/analyzer.py" "$PAYLOAD_FILE" >> "$LOG_FILE" 2>&1 < /dev/null &
disown

exit 0
