#!/usr/bin/env bash
# snapshot.sh — tag HEAD so the team's work can be rolled back cleanly.
#
# Usage: snapshot.sh <team-name>
#
# Creates lightweight tag teams/<team-name>-snapshot. Not pushed.
# Not auto-deleted by cleanup.sh — rollback target survives teardown.

set -euo pipefail

TEAM_NAME="${1:-}"
if [[ -z "$TEAM_NAME" ]]; then
  printf "[teams:snapshot] usage: snapshot.sh <team-name>\n" >&2
  exit 2
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  printf "[teams:snapshot] not in a git repo.\n" >&2
  exit 2
fi

TAG="teams/${TEAM_NAME}-snapshot"

# Tag may already exist if spawn is retried; overwrite to point at current HEAD.
if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  git tag -d "$TAG" >/dev/null
fi

git tag "$TAG" HEAD
SHA="$(git rev-parse HEAD)"
printf "[teams:snapshot] tagged HEAD=%s as %s\n" "$SHA" "$TAG" >&2
printf "[teams:snapshot] rollback with: git reset --hard %s\n" "$TAG" >&2
echo "$TAG"
