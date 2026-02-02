#!/bin/bash
# Kill processes by PID(s) with SIGTERM, fallback to SIGKILL
# Usage: kill.sh [--force] <pid> [pid...]
set -euo pipefail

FORCE=false
PIDS=()

for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=true ;;
    *) PIDS+=("$arg") ;;
  esac
done

if [ ${#PIDS[@]} -eq 0 ]; then
  echo "Usage: kill.sh [--force] <pid> [pid...]"
  exit 1
fi

for pid in "${PIDS[@]}"; do
  if ! ps -p "$pid" > /dev/null 2>&1; then
    echo "PID $pid: not running (skipped)"
    continue
  fi

  cmd=$(ps -p "$pid" -o command= 2>/dev/null || echo "unknown")
  echo "PID $pid: $cmd"

  if $FORCE; then
    kill -9 "$pid" 2>/dev/null && echo "  SIGKILL sent" || echo "  Failed (permission denied?)"
    continue
  fi

  kill -15 "$pid" 2>/dev/null || { echo "  SIGTERM failed (permission denied?)"; continue; }
  echo "  SIGTERM sent, waiting 3s..."

  for i in 1 2 3; do
    sleep 1
    if ! ps -p "$pid" > /dev/null 2>&1; then
      echo "  Terminated"
      break
    fi
  done

  if ps -p "$pid" > /dev/null 2>&1; then
    echo "  Still running, sending SIGKILL..."
    kill -9 "$pid" 2>/dev/null && echo "  SIGKILL sent" || echo "  Failed (permission denied?)"
  fi
done
