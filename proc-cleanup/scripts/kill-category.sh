#!/bin/bash
# Kill all processes in a category: claude, mcp, dev, port:<N>
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
PIDS=""

case "$CATEGORY" in
  claude)
    PIDS=$(ps aux | grep -E '[c]laude|[C]laude' | grep -v 'Claude\.app' | awk '{print $2}' || true)
    ;;
  mcp)
    PIDS=$(ps aux | grep -E '[m]cp-server|[m]cp_server|mcp-server\.cjs' | awk '{print $2}' || true)
    ;;
  dev)
    PIDS=$(ps aux | grep -E '[n]ode.*dev|[v]ite|[n]ext.*dev|[n]uxt|[u]vicorn|[f]astapi|[g]unicorn|[f]lask.*run|python.*[h]ttp\.server|[l]ive-server|[w]ebpack.*dev|[t]urbo.*dev|[b]un.*dev|[d]eno.*serve' | awk '{print $2}' || true)
    ;;
  port:*)
    PORT="${CATEGORY#port:}"
    PIDS=$(lsof -iTCP:"$PORT" -sTCP:LISTEN -P -n -t 2>/dev/null || true)
    ;;
  *)
    echo "Unknown category: $CATEGORY"
    echo "Valid: claude, mcp, dev, port:<PORT>"
    exit 1
    ;;
esac

if [ -z "$PIDS" ]; then
  echo "No processes found for category: $CATEGORY"
  exit 0
fi

echo "Found $(echo "$PIDS" | wc -w | tr -d ' ') process(es) for: $CATEGORY"
# shellcheck disable=SC2086
"$SCRIPT_DIR/kill.sh" $FORCE $PIDS
