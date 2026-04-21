#!/usr/bin/env bash
# task-completed.sh — TaskCompleted hook.
#
# For team tasks, check the owning teammate's worktree is clean. Skip if
# metadata.leave_dirty is true (for edge cases where the caller wants to keep
# WIP across task boundaries).
#
# Exit codes: 0 allow, 2 block.

set -euo pipefail

payload="$(cat)"

team_name="$(echo "$payload" | jq -r '.team_name // empty' 2>/dev/null || true)"
if [[ -z "$team_name" ]]; then
  exit 0
fi

leave_dirty="$(echo "$payload" | jq -r '.task.metadata.leave_dirty // false' 2>/dev/null || echo false)"
if [[ "$leave_dirty" == "true" ]]; then
  exit 0
fi

worktree="$(echo "$payload" | jq -r '.task.metadata.worktree // empty' 2>/dev/null || true)"
if [[ -z "$worktree" ]]; then
  # Task didn't claim a worktree; nothing to check.
  exit 0
fi

# Resolve relative paths against the repo root if present.
if [[ ! -d "$worktree" ]]; then
  if [[ -n "${CLAUDE_PROJECT_DIR:-}" ]] && [[ -d "$CLAUDE_PROJECT_DIR/$worktree" ]]; then
    worktree="$CLAUDE_PROJECT_DIR/$worktree"
  elif git rev-parse --show-toplevel >/dev/null 2>&1; then
    root="$(git rev-parse --show-toplevel)"
    [[ -d "$root/$worktree" ]] && worktree="$root/$worktree"
  fi
fi

if [[ ! -d "$worktree" ]]; then
  # Can't verify; don't block.
  exit 0
fi

dirty="$(git -C "$worktree" status --porcelain 2>/dev/null || true)"
if [[ -n "$dirty" ]]; then
  cat >&2 <<EOF
[teams:task-completed] BLOCKING task completion for team '$team_name'.
Worktree '$worktree' has uncommitted changes:
$dirty

Commit, amend, or set task metadata.leave_dirty=true before completing.
EOF
  exit 2
fi

exit 0
