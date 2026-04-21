#!/usr/bin/env bash
# task-created.sh — TaskCreated hook.
#
# Enforces every team task has an owner AND either a dependency or a deadline.
# Ignores non-team tasks (tasks without team_name in payload).
#
# Exit codes: 0 allow, 2 block.

set -euo pipefail

payload="$(cat)"

team_name="$(echo "$payload" | jq -r '.team_name // empty' 2>/dev/null || true)"
if [[ -z "$team_name" ]]; then
  exit 0
fi

owner="$(echo "$payload" | jq -r '.task.owner // empty' 2>/dev/null || true)"
blocked_by="$(echo "$payload" | jq -r '.task.blockedBy // [] | length' 2>/dev/null || echo 0)"
deadline="$(echo "$payload" | jq -r '.task.metadata.deadline // empty' 2>/dev/null || true)"

if [[ -z "$owner" ]]; then
  echo "[teams:task-created] team task for '$team_name' has no owner — assign one before creating." >&2
  exit 2
fi

if [[ "$blocked_by" == "0" ]] && [[ -z "$deadline" ]]; then
  echo "[teams:task-created] team task for '$team_name' has neither a dependency nor a deadline." >&2
  echo "[teams:task-created] Set addBlockedBy or metadata.deadline (ISO 8601) to prevent drift." >&2
  exit 2
fi

exit 0
