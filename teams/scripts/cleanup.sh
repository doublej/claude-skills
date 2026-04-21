#!/usr/bin/env bash
# cleanup.sh — prune worktrees + remove team dir. Keeps the snapshot tag for rollback.
#
# Usage: cleanup.sh <team-name>

set -euo pipefail

TEAM="${1:-}"
if [[ -z "$TEAM" ]]; then
  echo "usage: cleanup.sh <team-name>" >&2
  exit 2
fi

SKILL_DIR="${TEAMS_SKILL_DIR:-$HOME/.claude/skills/teams}"
CONSULT="$SKILL_DIR/scripts/_consult.sh"

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "[teams:cleanup] not in a git repo; skipping worktree prune." >&2
else
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  WT_DIR="$REPO_ROOT/.claude/worktrees"

  if [[ -d "$WT_DIR" ]]; then
    for wt in "$WT_DIR"/*/; do
      [[ -d "$wt" ]] || continue
      name="$(basename "$wt")"

      # Safety: check for uncommitted changes before removing.
      dirty="$(git -C "$wt" status --porcelain 2>/dev/null || true)"
      if [[ -n "$dirty" ]]; then
        echo "[teams:cleanup] worktree '$name' has uncommitted changes." >&2
        choice="$("$CONSULT" pick "Worktree '$name' is dirty. Action?" "keep|force-remove|leave-for-user")" || choice="keep"
        case "$choice" in
          keep|leave-for-user) continue ;;
          force-remove) ;;
        esac
      fi

      git -C "$REPO_ROOT" worktree remove --force "$wt" 2>/dev/null || rm -rf "$wt"
      # Branch cleanup: only delete if merged or the user confirmed force.
      br="worktree-$name"
      if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$br"; then
        if git -C "$REPO_ROOT" branch --merged | grep -qE "[ *] $br\$"; then
          git -C "$REPO_ROOT" branch -d "$br" || true
        fi
      fi
      echo "[teams:cleanup] removed worktree: $name"
    done
  fi

  git -C "$REPO_ROOT" worktree prune 2>/dev/null || true
fi

# Remove team dir. TeamDelete (the tool) should already have done this; this is
# a belt-and-suspenders cleanup for abandoned teams.
TEAM_DIR="$HOME/.claude/teams/$TEAM"
if [[ -d "$TEAM_DIR" ]]; then
  rm -rf "$TEAM_DIR"
  echo "[teams:cleanup] removed $TEAM_DIR"
fi

# Snapshot tag: NOT deleted here. Surface its name so the user can delete it later.
SNAP="teams/${TEAM}-snapshot"
if git rev-parse -q --verify "refs/tags/$SNAP" >/dev/null 2>&1; then
  echo "[teams:cleanup] snapshot tag '$SNAP' preserved (rollback: git reset --hard $SNAP)."
  echo "[teams:cleanup] drop it when you're sure: git tag -d $SNAP"
fi
