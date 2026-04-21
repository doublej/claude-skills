#!/usr/bin/env bash
# preflight-agent.sh — PreToolUse:Agent hook.
#
# Fires immediately before every Agent() call. When the call targets a team
# (team_name set), re-check dirty working directory as a last-line-of-defense.
#
# Exit codes: 0 = allow, 2 = block with feedback to lead.
# Feedback is written to stderr when blocking.

set -euo pipefail

payload="$(cat)"

# Only engage when the Agent call targets a team.
team_name="$(echo "$payload" | jq -r '.tool_input.team_name // empty' 2>/dev/null || true)"
if [[ -z "$team_name" ]]; then
  exit 0
fi

cwd="$(echo "$payload" | jq -r '.cwd // empty' 2>/dev/null || true)"
if [[ -n "$cwd" ]] && [[ -d "$cwd" ]]; then
  cd "$cwd"
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  exit 0
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
dirty="$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null || true)"

# Allow dirty if only our own skill's files are dirty (common during dogfooding).
# Filter out teams-skill paths; if anything else is dirty, block.
non_skill_dirty="$(echo "$dirty" | grep -v -E '(^|/)teams(/|$)' | grep -v '^[[:space:]]*$' || true)"
if [[ -n "$non_skill_dirty" ]]; then
  cat >&2 <<EOF
[teams:preflight-agent] BLOCKING Agent spawn for team '$team_name'.
Working directory is dirty:
$non_skill_dirty

Commit, stash, or reset before spawning. Or run:
  bash ~/.claude/skills/teams/scripts/preflight.sh
to handle interactively.
EOF
  exit 2
fi

exit 0
