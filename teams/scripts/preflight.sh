#!/usr/bin/env bash
# preflight.sh — env + repo sanity checks before a team spawn.
#
# Exit codes:
#   0 = clean to spawn
#   1 = clean with warning (stderr contains details; caller may continue)
#   2 = hard abort
#
# Side effects: none. Reads git state and env only. Consult calls defer to
# _consult.sh which falls back to /dev/tty if MCP isn't reachable.

set -euo pipefail

SKILL_DIR="${TEAMS_SKILL_DIR:-$HOME/.claude/skills/teams}"
CONSULT="$SKILL_DIR/scripts/_consult.sh"

say() { printf "[teams:preflight] %s\n" "$*" >&2; }

# 1. Env gate — experimental flag + git.
if [[ "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-0}" != "1" ]]; then
  say "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 is required for teammate mode."
  say "Set it in ~/.claude/settings.json env, or export it before launching Claude Code."
  exit 2
fi

if ! command -v git >/dev/null 2>&1; then
  say "git not found on PATH."
  exit 2
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  say "not inside a git repository."
  exit 2
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

# 2. Repo gate — dirty working directory.
DIRTY="$(git -C "$REPO_ROOT" status --porcelain)"
if [[ -n "$DIRTY" ]]; then
  say "working directory is dirty. Choose action:"
  choice="$("$CONSULT" pick "Dirty working directory detected. How to proceed before team spawn?" "commit|stash|abort")" && rc=0 || rc=$?
  if (( rc == 3 )); then
    say "consult unavailable (no MCP client and no readable /dev/tty)."
    say "Refusing to auto-commit or auto-stash. Resolve the dirty working directory manually (git commit / git stash) and retry preflight."
    exit 2
  fi
  case "$choice" in
    commit)
      msg="$("$CONSULT" text "Commit message for pending changes" "wip: pre-team snapshot")"
      if [[ -z "$msg" ]]; then msg="wip: pre-team snapshot"; fi
      git -C "$REPO_ROOT" add -A
      git -C "$REPO_ROOT" commit -m "$msg"
      say "committed pending changes."
      ;;
    stash)
      git -C "$REPO_ROOT" stash push -u -m "teams: pre-spawn stash"
      say "stashed pending changes (pop with: git stash pop)."
      ;;
    abort|*)
      say "aborted by user."
      exit 2
      ;;
  esac
fi

# 3. Repo gate — protected branch.
case "$BRANCH" in
  main|master|production|release/*)
    "$CONSULT" confirm "Current branch is '$BRANCH'. Spawn a team here anyway?" && rc=0 || rc=$?
    if (( rc == 3 )); then
      say "consult unavailable (no MCP client and no readable /dev/tty); cannot confirm protected branch."
      say "Re-run preflight from an interactive session."
      exit 2
    fi
    if (( rc != 0 )); then
      say "aborted — protected branch."
      exit 2
    fi
    ;;
esac

# 4. Orphan check — ~/.claude/teams entries without a live process.
TEAMS_DIR="$HOME/.claude/teams"
if [[ -d "$TEAMS_DIR" ]]; then
  # If any team subdir has config.json older than ~1 hour and no matching claude pid, offer cleanup.
  # We can't reliably map team to pid from outside; just surface count.
  stale=0
  for d in "$TEAMS_DIR"/*/; do
    [[ -f "$d/config.json" ]] || continue
    # Older than 1 hour
    if [[ $(find "$d/config.json" -mmin +60 -print 2>/dev/null) ]]; then
      stale=$((stale+1))
    fi
  done
  if (( stale > 0 )); then
    say "$stale stale team dir(s) in $TEAMS_DIR (older than 1h)."
    if "$CONSULT" confirm "Clean up stale team directories?"; then
      for d in "$TEAMS_DIR"/*/; do
        [[ -f "$d/config.json" ]] || continue
        if [[ $(find "$d/config.json" -mmin +60 -print 2>/dev/null) ]]; then
          rm -rf "$d"
          say "removed $d"
        fi
      done
    fi
  fi
fi

say "OK — repo=$REPO_ROOT branch=$BRANCH"
exit 0
