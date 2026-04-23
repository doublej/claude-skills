#!/usr/bin/env bash
# cmux-restore.sh — rebuild a workspace from a snapshot. Idempotent:
# re-running against an existing workspace fills in missing tabs only.
#
# Usage:
#   cmux-restore.sh <project> < snapshot.json
#
# The first arg is the *target* workspace name — usually the snapshot's
# original name, but you can restore under a new name (e.g. to clone a
# workspace). Split geometry from the snapshot is informational; tabs are
# recreated in snapshot order via cmux-tab.sh so roles stay canonical.
#
# Output (JSON on stdout):
#   { "workspace": "<id>", "name": "<project>",
#     "restored_tabs": [ { "role": "...", "created": true|false } ... ] }

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

_require_cmux

project="${1:-}"
[[ -n "$project" ]] || _die "target project name required"
[[ -t 0 ]] && _die "pipe a snapshot JSON on stdin"

snapshot="$(cat)"
[[ -n "$snapshot" ]] || _die "empty snapshot"

# Find-or-create target workspace via cmux-project.sh so blast radius stays
# in one place if the create contract changes.
proj_out="$("$SCRIPT_DIR/cmux-project.sh" "$project")"
ws_id="$(jq -r '.workspace' <<<"$proj_out")"

results="["
first=true
while read -r tab; do
  role="$(jq -r '.role' <<<"$tab")"
  cwd="$(jq -r '.cwd // ""' <<<"$tab")"
  [[ -n "$role" && "$role" != "null" ]] || continue
  tab_out="$("$SCRIPT_DIR/cmux-tab.sh" "$project" "$role" "$cwd")"
  created="$(jq -r '.created' <<<"$tab_out")"
  $first || results+=","
  first=false
  results+="$(jq -n --arg role "$role" --argjson created "$created" \
    '{role: $role, created: $created}')"
done < <(jq -c '.tabs[]' <<<"$snapshot")
results+="]"

jq -n --arg id "$ws_id" --arg name "$project" --argjson tabs "$results" \
  '{workspace: $id, name: $name, restored_tabs: $tabs}'
