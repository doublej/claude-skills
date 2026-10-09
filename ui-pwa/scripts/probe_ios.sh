#!/usr/bin/env bash
# Run the PWA probe page in an iOS Simulator and print what the device actually reports.
#
#   ./probe_ios.sh                      # boots "iPhone 17 Pro", portrait + landscape
#   ./probe_ios.sh "iPhone Air"         # a different device
#   ./probe_ios.sh "iPad Pro 11-inch (M5)" 8791
#
# Writes reports.jsonl + screenshots next to the probe assets.
set -euo pipefail

DEVICE="${1:-iPhone 17 Pro}"
PORT="${2:-8791}"
HERE="$(cd "$(dirname "$0")" && pwd)"
PROBE="$HERE/../assets/probe"

command -v xcrun >/dev/null || { echo "Xcode command line tools required" >&2; exit 1; }

UDID=$(xcrun simctl list devices available -j \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(next(x['udid'] for r in d['devices'].values() for x in r if x['name']=='$DEVICE'))")
echo "device: $DEVICE ($UDID)"

# --- serve -------------------------------------------------------------------
pkill -f "probe_server.py $PORT" 2>/dev/null || true
: > "$PROBE/reports.jsonl"
python3 "$HERE/probe_server.py" "$PORT" --root "$PROBE" > "$PROBE/server.log" 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1

# --- boot --------------------------------------------------------------------
xcrun simctl boot "$UDID" 2>/dev/null || true
open -a Simulator
xcrun simctl bootstatus "$UDID" >/dev/null

# TRAP: the simulator resolves "localhost" to ::1. A python http.server binds
# IPv4 only, so localhost silently fails to connect. Always use 127.0.0.1.
xcrun simctl openurl "$UDID" "http://127.0.0.1:$PORT/" >/dev/null 2>&1 || true

for _ in $(seq 30); do
  [ -s "$PROBE/reports.jsonl" ] && break
  sleep 1
done
[ -s "$PROBE/reports.jsonl" ] || { echo "no report received — is the page loading?" >&2; exit 1; }

xcrun simctl io "$UDID" screenshot "$PROBE/portrait.png" >/dev/null 2>&1

# --- landscape ---------------------------------------------------------------
osascript -e 'tell application "Simulator" to activate' \
          -e 'delay 1' \
          -e 'tell application "System Events" to key code 124 using command down' >/dev/null
sleep 5
xcrun simctl io "$UDID" screenshot "$PROBE/landscape.png" >/dev/null 2>&1
osascript -e 'tell application "System Events" to tell process "Simulator" to key code 123 using command down' >/dev/null
sleep 3

python3 "$HERE/summarize_reports.py" "$PROBE/reports.jsonl"
echo
echo "screenshots: $PROBE/portrait.png  $PROBE/landscape.png"
echo "raw:         $PROBE/reports.jsonl"
