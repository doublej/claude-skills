#!/usr/bin/env bash
# status.sh — list active teams + members from ~/.claude/teams/
set -euo pipefail

TEAMS_DIR="$HOME/.claude/teams"

if [[ ! -d "$TEAMS_DIR" ]]; then
  echo "No active teams (${TEAMS_DIR} does not exist)."
  exit 0
fi

count=0
for d in "$TEAMS_DIR"/*/; do
  [[ -f "$d/config.json" ]] || continue
  count=$((count+1))
  team="$(basename "$d")"
  echo "== $team =="
  if command -v jq >/dev/null 2>&1; then
    jq -r '
      "  created: \(.created_at // "unknown")",
      "  members:",
      (.members[]? | "    - \(.name) [\(.status // "unknown")] \(.agent_id // "")")
    ' "$d/config.json" 2>/dev/null || cat "$d/config.json"
  else
    cat "$d/config.json"
  fi
  echo
done

if (( count == 0 )); then
  echo "No active teams."
fi
