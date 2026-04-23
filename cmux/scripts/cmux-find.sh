#!/usr/bin/env bash
# cmux-find.sh — read-only lookup of a project workspace.
#
# Usage:
#   cmux-find.sh <project>
#
# Output (JSON on stdout) when found:
#   { "workspace": "<id>", "name": "<project>",
#     "tabs": [ { "tab": "<name>", "surface": "<id>" }, ... ] }
#
# Exit codes:
#   0   workspace exists
#   1   workspace missing (no JSON emitted)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

_require_cmux

project="${1:-}"
[[ -n "$project" ]] || _die "project name required"

ws_json="$(_workspace_by_name "$project" 2>/dev/null || true)"
if [[ -z "$ws_json" ]]; then
  _log "no workspace named '$project'"
  exit 1
fi

ws_id="$(jq -r '.id' <<<"$ws_json")"
tabs_json="$(cmux list-pane-surfaces --workspace "$ws_id" --json \
              | jq '[.surfaces[] | {tab, surface: .id}]')"

jq -n --arg id "$ws_id" --arg name "$project" --argjson tabs "$tabs_json" \
  '{workspace: $id, name: $name, tabs: $tabs}'
