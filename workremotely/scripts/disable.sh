#!/usr/bin/env bash
# Disable workremotely mode. Walks up from cwd (or given path) to find marker.
# Usage: disable.sh [--at <path>]
set -euo pipefail

START="$PWD"
while [ $# -gt 0 ]; do
  case "$1" in
    --at) START="${2:?}"; shift 2 ;;
    --at=*) START="${1#--at=}"; shift ;;
    *) shift ;;
  esac
done

DIR="$(cd "$START" && pwd)"
while [ "$DIR" != "/" ]; do
  if [ -f "$DIR/.workremotely" ]; then
    rm -f "$DIR/.workremotely"
    echo "workremotely DISABLED (removed $DIR/.workremotely)"
    exit 0
  fi
  DIR="$(dirname "$DIR")"
done

echo "workremotely was not active in any parent of $START"
exit 0
