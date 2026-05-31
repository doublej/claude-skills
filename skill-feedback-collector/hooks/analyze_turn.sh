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

# Fast exit unless THIS session has a marker with pending (unanalyzed) work.
# Checking the global markers dir would never be empty (stale files accumulate),
# so we key on the session_id from the payload — most Stop events do no work.
SESSION_ID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("session_id",""))' "$PAYLOAD_FILE" 2>/dev/null || true)"
MARKER_FILE="$SKILL_DIR/state/markers/$SESSION_ID.jsonl"
if [ -z "$SESSION_ID" ] || [ ! -f "$MARKER_FILE" ] || ! grep -q '"analyzed": *false' "$MARKER_FILE"; then
  rm -f "$PAYLOAD_FILE"
  exit 0
fi

# Background-detach the analyzer: disown, redirect IO, do not block Stop event
LOG_FILE="$LOG_DIR/analyzer-$(date +%s).log"
nohup python3 "$SKILL_DIR/scripts/analyzer.py" "$PAYLOAD_FILE" >> "$LOG_FILE" 2>&1 < /dev/null &
disown

exit 0
