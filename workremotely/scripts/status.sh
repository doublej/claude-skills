#!/usr/bin/env bash
# Show workremotely state for current (or given) directory.
# Usage: status.sh [--at <path>]
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
    HOST="$(grep -E '^host=' "$DIR/.workremotely" | cut -d= -f2-)"
    echo "workremotely ACTIVE"
    echo "  host:  $HOST"
    echo "  scope: $DIR"
    echo "  marker: $DIR/.workremotely"
    exit 0
  fi
  DIR="$(dirname "$DIR")"
done

echo "workremotely INACTIVE (no .workremotely marker in $START or parents)"
