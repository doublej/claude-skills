#!/bin/bash
# Browser Router app lifecycle helper.
#
# Usage:
#   app-control.sh quit       # quit the app and wait until it's gone
#   app-control.sh running    # exit 0 if running, 1 otherwise
#   app-control.sh relaunch   # open -a "Browser Router"

set -euo pipefail

APP_NAME="Browser Router"

is_running() {
    pgrep -x "$APP_NAME" >/dev/null
}

cmd_running() {
    if is_running; then
        echo "running"
        exit 0
    else
        echo "not running"
        exit 1
    fi
}

cmd_quit() {
    if ! is_running; then
        echo "not running"
        return 0
    fi

    osascript -e 'quit app "Browser Router"' 2>/dev/null || true

    # Wait up to 5s for graceful quit.
    for _ in $(seq 1 25); do
        if ! is_running; then
            echo "quit"
            return 0
        fi
        sleep 0.2
    done

    # Fallback: SIGTERM, then SIGKILL if still alive.
    pkill -x "$APP_NAME" 2>/dev/null || true
    sleep 0.5
    if is_running; then
        pkill -9 -x "$APP_NAME" 2>/dev/null || true
        sleep 0.3
    fi

    if is_running; then
        echo "ERROR: $APP_NAME did not quit" >&2
        exit 1
    fi
    echo "quit (forced)"
}

cmd_relaunch() {
    open -a "$APP_NAME"
    echo "launched"
}

case "${1:-}" in
    quit)     cmd_quit ;;
    running)  cmd_running ;;
    relaunch) cmd_relaunch ;;
    *)
        echo "Usage: $0 {quit|running|relaunch}" >&2
        exit 2
        ;;
esac
