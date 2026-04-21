#!/usr/bin/env bash
# teammate-idle.sh — TeammateIdle hook.
#
# Default: no-op (exit 0).
# Preset-aware: reads ~/.claude/teams/<team>/config.json for a .teams_meta.hooks.teammate_idle
# marker (populated out-of-band — optional). If marker is enforce_verdict or
# enforce_severity, checks the teammate's last message text for the expected field.
#
# Exit codes: 0 allow, 2 block with feedback to lead.

set -euo pipefail

payload="$(cat)"
team_name="$(echo "$payload" | jq -r '.team_name // empty' 2>/dev/null || true)"
if [[ -z "$team_name" ]]; then
  exit 0
fi

cfg="$HOME/.claude/teams/$team_name/config.json"
mode=""
if [[ -f "$cfg" ]]; then
  mode="$(jq -r '.teams_meta.hooks.teammate_idle // empty' "$cfg" 2>/dev/null || true)"
fi

# Fallback: infer from team-name prefix (since presets set default_team_name_prefix).
if [[ -z "$mode" ]]; then
  case "$team_name" in
    plan-committee*|bug-debug-panel*) mode="enforce_verdict" ;;
    pr-review-squad*|security-audit*) mode="enforce_severity" ;;
    *) mode="none" ;;
  esac
fi

if [[ "$mode" == "none" ]] || [[ -z "$mode" ]]; then
  exit 0
fi

last_msg="$(echo "$payload" | jq -r '.teammate.last_message.text // .teammate.last_message // empty' 2>/dev/null || true)"
teammate="$(echo "$payload" | jq -r '.teammate.name // "unknown"' 2>/dev/null || echo unknown)"

case "$mode" in
  enforce_verdict)
    if ! echo "$last_msg" | grep -qiE '(^|\s)verdict[:=]' ; then
      echo "[teams:teammate-idle] '$teammate' went idle without a 'verdict:' field. Ask for one." >&2
      exit 2
    fi
    ;;
  enforce_severity)
    if ! echo "$last_msg" | grep -qiE '(^|\s)severity[:=]' ; then
      echo "[teams:teammate-idle] '$teammate' went idle without a 'severity:' field. Ask for one." >&2
      exit 2
    fi
    ;;
esac

exit 0
