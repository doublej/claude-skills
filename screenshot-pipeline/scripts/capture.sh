#!/usr/bin/env bash
# capture.sh — Helper for common screenshot capture commands
# Usage: ./capture.sh <command> [args]
set -euo pipefail

usage() {
  cat <<EOF
Usage: capture.sh <command> [args]

Commands:
  simulator [output.png]      Capture booted iOS simulator
  window <app-name> [out.png] Capture macOS app window (no shadow)
  screen [output.png]         Capture full screen
  list-simulators             List booted simulators
EOF
  exit 1
}

cmd="${1:-}"
shift || true

case "$cmd" in
  simulator)
    out="${1:-simulator.png}"
    xcrun simctl io booted screenshot "$out"
    echo "Captured simulator → $out"
    ;;
  window)
    app="${1:?App name required}"
    out="${2:-window.png}"
    wid=$(osascript -e "tell app \"$app\" to id of window 1" 2>/dev/null) || {
      echo "Error: Could not find window for '$app'. Is it running?" >&2
      exit 1
    }
    screencapture -o -l "$wid" "$out"
    echo "Captured $app window → $out"
    ;;
  screen)
    out="${1:-screen.png}"
    screencapture -x "$out"
    echo "Captured screen → $out"
    ;;
  list-simulators)
    xcrun simctl list devices booted
    ;;
  *)
    usage
    ;;
esac
