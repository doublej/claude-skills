#!/usr/bin/env bash
# cmux-send.sh — send input to a project:role tab without caring whether
# it's a text payload or a named key. Routes `--enter` / `--key` correctly.
#
# Usage:
#   cmux-send.sh <project> <role> <text>          # text only, no Enter
#   cmux-send.sh <project> <role> <text> --enter  # text + Return (run cmd)
#   cmux-send.sh <project> <role> ''     --key Escape
#
# `--enter` is sugar for `--key Return` after the text. Use `--key` alone
# with empty text to send a named key (Escape, Tab, C-c, etc.). cmux's
# send-key names follow terminfo.
#
# Output (JSON on stdout):
#   { "workspace": "<id>", "tab": "<name>", "surface": "<id>",
#     "sent": "<text>", "key": "<key-or-null>" }

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

_require_cmux

project="${1:-}"
role="${2:-}"
text="${3-}"
[[ -n "$project" ]] || _die "project required"
[[ -n "$role"    ]] || _die "role required"
_validate_role "$role"

enter=false
key=""
shift 3 || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --enter) enter=true; shift ;;
    --key)   key="${2:-}"; shift 2 ;;
    *)       _die "unknown flag: $1" ;;
  esac
done

tab_name="${project}:${role}"
ws_id="$(_workspace_id_by_name "$project" 2>/dev/null || true)"
[[ -n "$ws_id" && "$ws_id" != "null" ]] \
  || _die "workspace '$project' not found — create with cmux-project.sh first"

surface_id="$(_surface_id_by_tab_name "$ws_id" "$tab_name" 2>/dev/null || true)"
[[ -n "$surface_id" && "$surface_id" != "null" ]] \
  || _die "tab '$tab_name' not found — create with cmux-tab.sh first"

if [[ -n "$text" ]]; then
  cmux send --surface "$surface_id" -- "$text" >/dev/null
fi
if $enter; then
  cmux send-key --surface "$surface_id" Return >/dev/null
fi
if [[ -n "$key" ]]; then
  cmux send-key --surface "$surface_id" "$key" >/dev/null
fi

key_json="null"
[[ -n "$key" ]] && key_json="\"$(_json_escape "$key")\""
$enter && key_json="\"Return\""

printf '{"workspace":"%s","tab":"%s","surface":"%s","sent":"%s","key":%s}\n' \
  "$ws_id" "$(_json_escape "$tab_name")" "$surface_id" \
  "$(_json_escape "$text")" "$key_json"
