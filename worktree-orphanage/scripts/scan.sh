#!/usr/bin/env bash
# worktree-orphanage phase-1 scanner. Read-only.
# usage: scan.sh [--branches|-b] [target-branch...]
#   default targets: auto-detect main master develop
#   --branches: also scan local branches not checked out in any worktree
#
# Against every target branch, commits ahead are bucketed:
#   cherry   — patch-id identical in target (git cherry "-")
#   absorbed — diff already present in target tree (reverse-apply check;
#              catches squash merges and edited cherry-picks)
#   unmerged — genuinely not in target
# Orphaned only if unmerged commits vs ANY target, or a dirty tree.
# Ahead-but-all-absorbed => likely-merged.
set -uo pipefail

include_branches=0
cand=()
for a in "$@"; do
  case "$a" in
    --branches|-b) include_branches=1;;
    *) cand+=("$a");;
  esac
done
[ ${#cand[@]} -eq 0 ] && cand=(main master develop)

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

stash_count() { # $1=branch
  git stash list --format=%gs 2>/dev/null | grep -cE "([Oo]n|WIP on) ${1}(:|$)" || true
}

# bucket $1=sha against all targets; prints ahead\tcherry\tabsorbed\tunmerged\tany_unmerged\tany_ahead
bucket() {
  local sha=$1 T ahead cherry absorbed unmerged i cline
  local ahead_s="" cherry_s="" abs_s="" unm_s="" any_unmerged=0 any_ahead=0
  for T in "${targets[@]}"; do
    ahead=$(git rev-list --count --no-merges "$T..$sha" 2>/dev/null || echo 0)
    cherry=0; absorbed=0; unmerged=0
    if [ "$ahead" -gt 0 ]; then
      any_ahead=1
      # squash-merge defense: whole branch diff already in target's tree?
      if patch_in_target "$T" "$(git diff "$T...$sha" 2>/dev/null)"; then
        absorbed=$ahead
      else
        local plus=()
        while IFS= read -r cline; do
          case "$cline" in
            -*) cherry=$((cherry+1));;
            +*) plus+=("${cline#+ }");;
          esac
        done < <(git cherry "$T" "$sha" 2>/dev/null)
        # ponytail: cap reverse-apply probes at 20 commits; rest counted unmerged
        i=0
        for p in "${plus[@]:-}"; do
          [ -z "$p" ] && continue
          if [ $i -lt 20 ] && patch_in_target "$T" "$(git show "$p" --format= --patch 2>/dev/null)"; then
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
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ahead_s" "$cherry_s" "$abs_s" "$unm_s" "$any_unmerged" "$any_ahead"
}

# --- iterate worktrees -----------------------------------------------------
echo -e "WORKTREE\tBRANCH\tAHEAD\tCHERRY\tABSORBED\tUNMERGED\tDIRTY\tSTASH\tLAST_ACTIVITY\tCLASS"
first=1
wt_path="" wt_sha="" wt_branch="" wt_flags="" wt_branches=" "
emit() {
  [ -z "$wt_path" ] && return
  [ -n "$wt_branch" ] && wt_branches+="$wt_branch "
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
  [ -n "$wt_branch" ] && stash=$(stash_count "$wt_branch")

  local ahead_s="-" cherry_s="-" abs_s="-" unm_s="-" any_unmerged=0 any_ahead=0
  [ -z "$class" ] && \
    IFS=$'\t' read -r ahead_s cherry_s abs_s unm_s any_unmerged any_ahead < <(bucket "$wt_sha")

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

# --- local branches with no worktree folder (--branches) -------------------
if [ $include_branches -eq 1 ]; then
  while IFS= read -r br; do
    case " ${targets[*]} " in *" $br "*) continue;; esac
    case "$wt_branches" in *" $br "*) continue;; esac
    sha=$(git rev-parse --verify --quiet "refs/heads/$br") || continue
    IFS=$'\t' read -r a_s c_s ab_s u_s anyu anya < <(bucket "$sha")
    last=$(git log -1 --format=%cs "$br" 2>/dev/null || echo "-")
    stash=$(stash_count "$br")
    if [ "$anyu" -eq 1 ]; then class="orphaned"
    elif [ "$anya" -eq 1 ]; then class="likely-merged"
    else class="clean"; fi
    echo -e "(no worktree)\t$br\t$a_s\t$c_s\t$ab_s\t$u_s\t0\t$stash\t$last\t$class"
  done < <(git for-each-ref --format='%(refname:short)' refs/heads)
fi
