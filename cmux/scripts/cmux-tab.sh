#!/usr/bin/env bash
# cmux-tab.sh — find-or-create a tab named <project>:<role> inside the
# project workspace. Creates the workspace too if it does not exist.
#
# Usage:
#   cmux-tab.sh <project> <role> [cwd]
#
# Arguments:
#   project  workspace name
#   role     enum: code, dev, logs, tests, browser, shell, build, db, notes,
#            agent:<id>   (see _lib.sh CMUX_ROLES)
#   cwd      optional: initial working directory for the new tab's shell.
#            Sent as `cd <cwd>` immediately after creation. Ignored when the
#            tab already exists (we do not reset a live shell).
#
# Output (JSON on stdout):
#   { "workspace": "<id>", "tab": "<project>:<role>",
#     "surface": "<id>", "created": true|false }

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

_require_cmux

project="${1:-}"
role="${2:-}"
cwd="${3:-}"
[[ -n "$project" ]] || _die "project name required"
[[ -n "$role"    ]] || _die "role required"
_validate_role "$role"

tab_name="${project}:${role}"

ws_id="$(_workspace_id_by_name "$project" 2>/dev/null || true)"
if [[ -z "$ws_id" || "$ws_id" == "null" ]]; then
  _log "workspace '$project' missing — creating"
  ws_id="$(cmux new-workspace --name "$project" --json | jq -r '.id')"
  [[ -n "$ws_id" && "$ws_id" != "null" ]] || _die "new-workspace returned no id"
fi

surface_json="$(_surface_by_tab_name "$ws_id" "$tab_name" 2>/dev/null || true)"
created=false
if [[ -n "$surface_json" ]]; then
  surface_id="$(jq -r '.id' <<<"$surface_json")"
  _log "found tab: $tab_name ($surface_id)"
else
  _log "creating tab: $tab_name"
  surface_id="$(cmux new-split --workspace "$ws_id" --tab "$tab_name" --json \
                 | jq -r '.id')"
  [[ -n "$surface_id" && "$surface_id" != "null" ]] || _die "new-split returned no id"
  created=true

  if [[ -n "$cwd" ]]; then
    _log "cd -> $cwd"
    cmux send --surface "$surface_id" "cd $(printf '%q' "$cwd")" >/dev/null
    cmux send-key --surface "$surface_id" Return >/dev/null
  fi
fi

printf '{"workspace":"%s","tab":"%s","surface":"%s","created":%s}\n' \
  "$ws_id" "$(_json_escape "$tab_name")" "$surface_id" "$created"
