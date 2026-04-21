#!/usr/bin/env bash
# _consult.sh — thin wrapper around consult-user-mcp for team scripts.
#
# Usage:
#   _consult.sh confirm "<body>"                    → exit 0 (yes) / 2 (no)
#   _consult.sh pick    "<body>" opt1|opt2|opt3     → echoes choice on stdout, exit 0
#   _consult.sh text    "<body>" [placeholder]      → echoes text on stdout, exit 0
#   _consult.sh notify  "<body>" [sound]            → fire-and-forget, exit 0
#
# Requires: `claude` CLI or `mcp` CLI. Falls back to a textual prompt on stderr
# if neither is available, so scripts don't hard-fail in degraded envs.
#
# Note: MCP is easiest to reach when the caller is Claude Code itself, via the
# mcp__consult-user-mcp__ask tool. This script is a fallback for direct shell
# invocations from hooks and preflight, where the MCP client is unavailable.

set -euo pipefail

MODE="${1:-}"
BODY="${2:-}"
shift 2 || true

fallback_prompt() {
  # When MCP isn't reachable from raw shell, print the question to stderr and
  # read from /dev/tty so the user can answer directly. Hooks run synchronously
  # and /dev/tty is available in an interactive Claude Code session.
  printf "\n[teams:_consult] %s\n" "$BODY" >&2
  case "$MODE" in
    confirm)
      printf "[teams:_consult] confirm [y/N]: " >&2
      local ans=""
      if [[ -r /dev/tty ]]; then read -r ans </dev/tty || true; fi
      case "$ans" in
        y|Y|yes|YES) exit 0 ;;
        *) exit 2 ;;
      esac
      ;;
    pick)
      local opts_raw="${1:-}"
      local IFS='|' ; read -ra opts <<< "$opts_raw"
      local i=1
      for o in "${opts[@]}"; do printf "  %d) %s\n" "$i" "$o" >&2; i=$((i+1)); done
      printf "[teams:_consult] pick [1-%d]: " "${#opts[@]}" >&2
      local n=""
      if [[ -r /dev/tty ]]; then read -r n </dev/tty || true; fi
      if [[ "$n" =~ ^[0-9]+$ ]] && (( n >= 1 && n <= ${#opts[@]} )); then
        echo "${opts[$((n-1))]}"
        exit 0
      fi
      echo "${opts[0]}"
      exit 0
      ;;
    text)
      local placeholder="${1:-}"
      printf "[teams:_consult] %s%s: " "$BODY" "${placeholder:+ ($placeholder)}" >&2
      local v=""
      if [[ -r /dev/tty ]]; then read -r v </dev/tty || true; fi
      echo "$v"
      exit 0
      ;;
    notify)
      printf "[teams:_consult] notify: %s\n" "$BODY" >&2
      exit 0
      ;;
    *)
      printf "[teams:_consult] unknown mode: %s\n" "$MODE" >&2
      exit 1
      ;;
  esac
}

# For now, always go through the fallback. The script is invoked from hooks and
# preflight scripts where we may or may not have a live MCP client. The calling
# lead (Claude Code) will generally bypass this helper and call the MCP tool
# directly — this wrapper exists for the script-only paths.
fallback_prompt "$@"
