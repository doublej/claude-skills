#!/usr/bin/env bash
# Kill all processes in a category: claude, mcp, dev, port:<N>
# Enumeration is delegated to scan.py --pids (single source of truth).
# Usage: kill-category.sh [--force] <category>
set -euo pipefail

FORCE=""
CATEGORY=""

for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE="--force" ;;
    *) CATEGORY="$arg" ;;
  esac
done

if [ -z "$CATEGORY" ]; then
  echo "Usage: kill-category.sh [--force] <claude|mcp|dev|port:PORT>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PIDS=$(python3 "$SCRIPT_DIR/scan.py" --pids "$CATEGORY")

if [ -z "$PIDS" ]; then
  echo "No processes found for category: $CATEGORY"
  exit 0
fi

echo "Found $(echo "$PIDS" | wc -w | tr -d ' ') process(es) for: $CATEGORY"
# shellcheck disable=SC2086
"$SCRIPT_DIR/kill.sh" $FORCE $PIDS
