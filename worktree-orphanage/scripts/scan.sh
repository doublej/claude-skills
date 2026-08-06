#!/usr/bin/env bash
# worktree-orphanage phase-1 scanner. Read-only.
# usage: scan.sh [target-branch...]   (default: auto-detect main master develop)
#
# Per worktree, against every target branch, commits ahead are bucketed:
#   cherry   — patch-id identical in target (git cherry "-")
#   absorbed — diff already present in target tree (reverse-apply check;
#              catches squash merges and edited cherry-picks)
#   unmerged — genuinely not in target
# A worktree is orphaned only if it has unmerged commits vs ANY target,
# or a dirty tree. Ahead-but-all-absorbed => likely-merged.
set -uo pipefail

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "NOT_A_REPO" >&2; exit 2; }
cd "$repo_root"

# --- resolve targets -------------------------------------------------------
targets=()
resolve() {
  if git rev-parse --verify --quiet "refs/heads/$1" >/dev/null; then echo "$1"
  elif git rev-parse --verify --quiet "refs/remotes/origin/$1" >/dev/null; then echo "origin/$1"
  fi
}
if [ $# -gt 0 ]; then cand=("$@"); else cand=(main master develop); fi
for c in "${cand[@]}"; do
  r=$(resolve "$c"); [ -n "$r" ] && targets+=("$r")
done
[ ${#targets[@]} -eq 0 ] && { echo "NO_TARGET_BRANCH (tried: ${cand[*]})" >&2; exit 2; }

# --- reverse-apply check: is a patch already present in target's tree? -----
tmpidx=$(mktemp); trap 'rm -f "$tmpidx"' EXIT
patch_in_target() { # $1=target, $2=patch text
  [ -z "$2" ] && return 0                          # empty patch: no content to lose
  GIT_INDEX_FILE=$tmpidx git read-tree "$1" 2>/dev/null || return 1
  printf '%s\n' "$2" | GIT_INDEX_FILE=$tmpidx git apply --cached --check --reverse 2>/dev/null
}

# --- iterate worktrees -----------------------------------------------------
echo -e "WORKTREE\tBRANCH\tAHEAD\tCHERRY\tABSORBED\tUNMERGED\tDIRTY\tSTASH\tLAST_ACTIVITY\tCLASS"
first=1
wt_path="" wt_sha="" wt_branch="" wt_flags=""
emit() {
  [ -z "$wt_path" ] && return
  if [ $first -eq 1 ]; then first=0; return; fi   # skip primary checkout

  local class="" dirty=0 stash=0 last="-"
  if [ -n "$wt_flags" ] || [ ! -d "$wt_path" ]; then
    class="broken"
  elif [ -z "$wt_branch" ]; then
    class="detached"
  fi

  if [ -d "$wt_path" ]; then
    dirty=$(git -C "$wt_path" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    last=$(git -C "$wt_path" log -1 --format=%cs 2>/dev/null || echo "-")
  fi
  [ -n "$wt_branch" ] && \
    stash=$(git stash list --format=%gs 2>/dev/null | grep -cE "([Oo]n|WIP on) ${wt_branch}(:|$)" || true)

  local ahead_s="" cherry_s="" abs_s="" unm_s="" any_unmerged=0 any_ahead=0
  if [ -n "$class" ]; then
    ahead_s="-"; cherry_s="-"; abs_s="-"; unm_s="-"
  else
    for T in "${targets[@]}"; do
      local ahead cherry absorbed unmerged
      ahead=$(git rev-list --count --no-merges "$T..$wt_sha" 2>/dev/null || echo 0)
      cherry=0; absorbed=0; unmerged=0
      if [ "$ahead" -gt 0 ]; then
        any_ahead=1
        # squash-merge defense: whole branch diff already in target's tree?
        if patch_in_target "$T" "$(git diff "$T...$wt_sha" 2>/dev/null)"; then
          absorbed=$ahead
        else
          local plus=() cline
          while IFS= read -r cline; do
            case "$cline" in
              -*) cherry=$((cherry+1));;
              +*) plus+=("${cline#+ }");;
            esac
          done < <(git cherry "$T" "$wt_sha" 2>/dev/null)
          # ponytail: cap reverse-apply probes at 20 commits; rest counted unmerged
          local i=0
          for sha in "${plus[@]:-}"; do
            [ -z "$sha" ] && continue
            if [ $i -lt 20 ] && patch_in_target "$T" "$(git show "$sha" --format= --patch 2>/dev/null)"; then
              absorbed=$((absorbed+1))
            else
              unmerged=$((unmerged+1))
            fi
            i=$((i+1))
          done
        fi
      fi
      [ "$unmerged" -gt 0 ] && any_unmerged=1
      ahead_s+="${ahead_s:+,}$T:$ahead"
      cherry_s+="${cherry_s:+,}$cherry"
      abs_s+="${abs_s:+,}$absorbed"
      unm_s+="${unm_s:+,}$unmerged"
    done
  fi

  if [ -z "$class" ]; then
    if [ "$any_unmerged" -eq 1 ] || [ "$dirty" -gt 0 ]; then class="orphaned"
    elif [ "$any_ahead" -eq 1 ]; then class="likely-merged"
    else class="clean"; fi
  fi
  echo -e "$wt_path\t${wt_branch:-<detached>}\t$ahead_s\t$cherry_s\t$abs_s\t$unm_s\t$dirty\t$stash\t$last\t$class"
}
while IFS= read -r line; do
  case "$line" in
    worktree\ *) emit; wt_path="${line#worktree }"; wt_sha=""; wt_branch=""; wt_flags="";;
    HEAD\ *)     wt_sha="${line#HEAD }";;
    branch\ *)   wt_branch="${line#branch refs/heads/}";;
    detached)    wt_branch="";;
    prunable*)   wt_flags="prunable";;
  esac
done < <(git worktree list --porcelain)
emit
