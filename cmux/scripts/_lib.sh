#!/usr/bin/env bash
# Shared helpers for cmux-*.sh scripts. Sourced, not executed.
# All funcs: exit 1 on failure, log to stderr, emit structured values on stdout
# only when explicitly documented. Callers compose into JSON output.

set -euo pipefail

CMUX_ROLES=(code dev logs tests browser agent shell build db notes)

_log() { printf '[cmux] %s\n' "$*" >&2; }
_die() { printf '[cmux] ERROR: %s\n' "$*" >&2; exit 1; }

# _require_cmux
# Verify cmux CLI + jq are present and CMUX_SOCKET_PATH is set
# (cmux exports this into every workspace shell). Exit 1 with a helpful
# message if anything is missing.
_require_cmux() {
  command -v cmux >/dev/null 2>&1 || _die "cmux CLI not on PATH"
  command -v jq   >/dev/null 2>&1 || _die "jq required (brew install jq)"
  [[ -n "${CMUX_SOCKET_PATH:-}" ]] \
    || _die "CMUX_SOCKET_PATH unset — run from a cmux-spawned shell"
}

# _validate_role <role>
# Allow anything matching 'agent:<N>' or 'svc:<N>' plus the fixed role
# enum. 'agent:' is for AI subagents; 'svc:' is for dev services (backend,
# frontend, worker, etc.) inside multi-component workspaces.
_validate_role() {
  local role="$1"
  if [[ "$role" == agent:* ]]; then
    [[ "$role" =~ ^agent:[0-9A-Za-z_-]+$ ]] \
      || _die "agent role must match 'agent:<id>' (got: $role)"
    return 0
  fi
  if [[ "$role" == svc:* ]]; then
    [[ "$role" =~ ^svc:[0-9A-Za-z_-]+$ ]] \
      || _die "svc role must match 'svc:<slug>' (got: $role)"
    return 0
  fi
  local r
  for r in "${CMUX_ROLES[@]}"; do
    [[ "$r" == "$role" ]] && return 0
  done
  _die "unknown role '$role' (allowed: ${CMUX_ROLES[*]}, agent:<id>, or svc:<slug>)"
}

# _encode_cwd_for_claude <abs-path>
# Map an absolute path to the directory name under ~/.claude/projects/
# ('/' → '-'). Used to locate per-cwd session history.
_encode_cwd_for_claude() {
  local p="$1"
  printf '%s' "${p//\//-}"
}

# _workspace_by_name <name>
# Emit workspace JSON object on stdout, or exit 1 quietly if absent.
# Isolates cmux JSON shape to one place; if cmux changes 'name' to 'title',
# fix it here and every caller keeps working.
_workspace_by_name() {
  local name="$1"
  cmux list-workspaces --json \
    | jq -e --arg n "$name" '.workspaces[] | select(.name == $n)' 2>/dev/null
}

# _workspace_id_by_name <name>
_workspace_id_by_name() {
  _workspace_by_name "$1" | jq -r '.id'
}

# _surface_by_tab_name <workspace-id> <tab-name>
# Return surface JSON inside a workspace whose tab label equals <tab-name>.
_surface_by_tab_name() {
  local ws_id="$1" tab="$2"
  cmux list-pane-surfaces --workspace "$ws_id" --json \
    | jq -e --arg t "$tab" '.surfaces[] | select(.tab == $t)' 2>/dev/null
}

# _surface_id_by_tab_name <workspace-id> <tab-name>
_surface_id_by_tab_name() {
  _surface_by_tab_name "$1" "$2" | jq -r '.id'
}

# _json_escape <text>
# Minimal JSON string escape for building output without spawning python.
_json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}
