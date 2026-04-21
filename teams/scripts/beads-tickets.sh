#!/usr/bin/env bash
# beads-tickets.sh — pull open bd tickets and print a distribution plan for a beads-pm team.
#
# Usage: beads-tickets.sh [team-name]
# Output: JSON to stdout — { "tickets": [...], "distribution": [{impl-1: ticket-id}, ...] }

set -euo pipefail

TEAM="${1:-beads-pm}"

if ! command -v bd >/dev/null 2>&1; then
  echo "[teams:beads] bd binary not on PATH." >&2
  exit 2
fi

TEAM_DIR="$HOME/.claude/teams/$TEAM"

# Determine implementer names from config.json if present; default to impl-1..3
impls=()
if command -v jq >/dev/null 2>&1 && [[ -f "$TEAM_DIR/config.json" ]]; then
  while IFS= read -r name; do
    [[ "$name" == impl-* ]] && impls+=("$name")
  done < <(jq -r '.members[]?.name // empty' "$TEAM_DIR/config.json")
fi
if (( ${#impls[@]} == 0 )); then
  impls=(impl-1 impl-2 impl-3)
fi

# Pull open tickets sorted by priority (falls back to status open order).
tickets_json="$(bd list --status open --json 2>/dev/null || true)"
if [[ -z "$tickets_json" ]] || [[ "$tickets_json" == "null" ]]; then
  tickets_json="[]"
fi

# Take top N where N = #impls.
N=${#impls[@]}
python3 - <<PY
import json, sys
tickets = json.loads("""$tickets_json""") if """$tickets_json""".strip() else []
tickets = tickets[: $N ]
impls = ${impls[@]@Q} .split() if False else [${impls[@]@Q}]
# The above line fails on zsh list quoting; build via env instead.
import os
impls = os.environ.get("IMPLS_JOINED", "").split() or ["impl-1","impl-2","impl-3"]
dist = []
for i, t in enumerate(tickets):
    owner = impls[i % len(impls)]
    tid = t.get("id") or t.get("ticket_id") or t.get("number") or "?"
    title = t.get("title") or t.get("subject") or ""
    dist.append({"owner": owner, "ticket_id": tid, "title": title})
print(json.dumps({"tickets": tickets, "distribution": dist}, indent=2))
PY
