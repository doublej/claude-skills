#!/usr/bin/env bash
# cmux-snapshot.sh — serialize a project workspace into JSON for replay.
#
# Usage:
#   cmux-snapshot.sh <project> [> snapshot.json]
#
# The snapshot records the workspace name, tab roles, and the split tree
# (direction + parent) as cmux reports it. Tab cwd is best-effort: we echo
# $PWD into each shell and read it back. Tabs whose shells do not respond
# within 300ms get cwd:null.
#
# Output (JSON on stdout):
#   { "name": "<project>", "tabs": [ { "role": "...", "cwd": "..." } ... ],
#     "splits": [...raw cmux surface tree...] }

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

_require_cmux

project="${1:-}"
[[ -n "$project" ]] || _die "project required"

ws_id="$(_workspace_id_by_name "$project" 2>/dev/null || true)"
[[ -n "$ws_id" && "$ws_id" != "null" ]] \
  || _die "workspace '$project' not found"

surfaces_json="$(cmux list-pane-surfaces --workspace "$ws_id" --json)"

_pwd_probe() {
  # Print PWD into the surface, read last line of screen, parse marker.
  local sid="$1"
  local marker="__CMUXPWD_$RANDOM__"
  cmux send --surface "$sid" -- "echo $marker:\$PWD" >/dev/null 2>&1 || { echo ""; return; }
  cmux send-key --surface "$sid" Return >/dev/null 2>&1 || { echo ""; return; }
  sleep 0.3
  cmux refresh-surfaces --workspace "$ws_id" >/dev/null 2>&1 || true
  cmux read-screen --surface "$sid" 2>/dev/null \
    | grep -oE "${marker}:[^ ]*" | tail -1 | sed "s/^${marker}://" || echo ""
}

tabs_json="["
first=true
while read -r row; do
  tab="$(jq -r '.tab'     <<<"$row")"
  sid="$(jq -r '.id'      <<<"$row")"
  role="${tab#${project}:}"
  cwd="$(_pwd_probe "$sid" || true)"
  $first || tabs_json+=","
  first=false
  tabs_json+="$(jq -n --arg role "$role" --arg cwd "$cwd" \
    '{role: $role, cwd: (if $cwd == "" then null else $cwd end)}')"
done < <(jq -c '.surfaces[]' <<<"$surfaces_json")
tabs_json+="]"

jq -n \
  --arg name "$project" \
  --argjson tabs "$tabs_json" \
  --argjson splits "$surfaces_json" \
  '{name: $name, tabs: $tabs, splits: $splits}'
