#!/usr/bin/env bash
# PostToolUse(Skill) hook — drops a marker for later analysis.
# Reads Claude Code hook payload from stdin, writes one JSONL line per skill
# invocation to state/markers/<session_id>.jsonl. Must be fast: no agent spawn.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MARKERS_DIR="$SKILL_DIR/state/markers"
mkdir -p "$MARKERS_DIR"

# Parse stdin payload via python — pipe input, read fields tab-separated.
FIELDS="$(python3 "$SKILL_DIR/scripts/parse_marker_payload.py")" || exit 0
IFS=$'\t' read -r SESSION_ID TRANSCRIPT_PATH SKILL_NAME CWD <<< "$FIELDS"

# Bail silently if we can't identify the skill
[ -z "${SKILL_NAME:-}" ] && exit 0
[ -z "${SESSION_ID:-}" ] && exit 0

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
MARKER_FILE="$MARKERS_DIR/$SESSION_ID.jsonl"

# Sequence index = count of existing lines
SEQ=0
[ -f "$MARKER_FILE" ] && SEQ=$(wc -l < "$MARKER_FILE" | tr -d ' ')

# Append a single line (atomic for short writes on POSIX)
printf '{"seq":%s,"ts":"%s","skill":"%s","cwd":"%s","transcript_path":"%s","analyzed":false}\n' \
  "$SEQ" "$TS" "$SKILL_NAME" "$CWD" "$TRANSCRIPT_PATH" >> "$MARKER_FILE"

exit 0
