#!/usr/bin/env bash
# cmux-project.sh — find-or-create the canonical workspace for a project.
#
# Usage:
#   cmux-project.sh <project> [layout]
#
# Arguments:
#   project  workspace name, typically $(basename "$PWD")
#   layout   optional: single | code-dev | code-dev-logs | grid
#            (applied only on first creation; see references/layouts.md)
#
# Output (JSON on stdout):
#   { "workspace": "<id>", "name": "<project>", "created": true|false,
#     "layout": "<layout-or-null>" }

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

_require_cmux

project="${1:-}"
layout="${2:-}"
[[ -n "$project" ]] || _die "project name required"

existing="$(_workspace_by_name "$project" || true)"
created=false
if [[ -n "$existing" ]]; then
  ws_id="$(jq -r '.id' <<<"$existing")"
  _log "found workspace: $project ($ws_id)"
else
  _log "creating workspace: $project"
  ws_id="$(cmux new-workspace --name "$project" --json | jq -r '.id')"
  [[ -n "$ws_id" && "$ws_id" != "null" ]] || _die "new-workspace returned no id"
  created=true

  if [[ -n "$layout" ]]; then
    _log "applying layout: $layout"
    case "$layout" in
      single)
        : ;;
      code-dev)
        cmux new-split --workspace "$ws_id" --direction r --tab "${project}:dev" >/dev/null
        cmux rename-tab --workspace "$ws_id" --index 0 "${project}:code" >/dev/null 2>&1 || true
        ;;
      code-dev-logs)
        cmux new-split --workspace "$ws_id" --direction r --tab "${project}:dev"  >/dev/null
        cmux new-split --workspace "$ws_id" --direction d --tab "${project}:logs" >/dev/null
        cmux rename-tab --workspace "$ws_id" --index 0 "${project}:code" >/dev/null 2>&1 || true
        ;;
      grid)
        cmux new-split --workspace "$ws_id" --direction r --tab "${project}:agent:1" >/dev/null
        cmux new-split --workspace "$ws_id" --direction d --tab "${project}:agent:2" >/dev/null
        cmux new-split --workspace "$ws_id" --direction d --tab "${project}:agent:3" >/dev/null
        cmux rename-tab --workspace "$ws_id" --index 0 "${project}:agent:0" >/dev/null 2>&1 || true
        ;;
      *)
        _die "unknown layout '$layout' (single|code-dev|code-dev-logs|grid)"
        ;;
    esac
  fi
fi

layout_json="null"
[[ -n "$layout" ]] && layout_json="\"$(_json_escape "$layout")\""
printf '{"workspace":"%s","name":"%s","created":%s,"layout":%s}\n' \
  "$ws_id" "$(_json_escape "$project")" "$created" "$layout_json"
