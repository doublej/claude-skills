#!/usr/bin/env bash
# capture.sh — capture the iPhone Mirroring window to PNG and write its
# bounds + retina scale to JSON. Output dir defaults to /tmp/iphone-mirror.
set -euo pipefail

OUT_DIR="${IPHONE_MIRROR_DIR:-/tmp/iphone-mirror}"
mkdir -p "$OUT_DIR"
PNG="$OUT_DIR/capture.png"
META="$OUT_DIR/window.json"

# 1. Ensure the app is running
if ! pgrep -x "iPhone Mirroring" >/dev/null; then
  open -a "iPhone Mirroring"
  sleep 2
fi

# 2. Resolve window id + bounds via AppleScript
read -r WID WX WY WW WH < <(osascript <<'AS' || true
tell application "System Events"
    tell process "iPhone Mirroring"
        if not (exists window 1) then
            return ""
        end if
        set wid to id of window 1
        set {x, y} to position of window 1
        set {w, h} to size of window 1
        return (wid as string) & " " & x & " " & y & " " & w & " " & h
    end tell
end tell
AS
)

if [ -z "${WID:-}" ]; then
  echo "capture.sh: iPhone Mirroring has no window. Open it and unlock the iPhone." >&2
  exit 2
fi

# 3. Capture the window
screencapture -x -l "$WID" "$PNG"

if [ ! -s "$PNG" ]; then
  echo "capture.sh: screencapture wrote an empty file (Screen Recording perm?)" >&2
  exit 3
fi

# 4. Compute retina scale from actual PNG vs logical window size
read -r SHOT_W SHOT_H < <(python3 - <<PY "$PNG"
import sys
from PIL import Image
img = Image.open(sys.argv[1])
print(img.size[0], img.size[1])
PY
)

SCALE=$(python3 -c "print(round($SHOT_W / $WW, 4))")

# 5. Emit metadata
cat > "$META" <<JSON
{
  "id": $WID,
  "x": $WX,
  "y": $WY,
  "w": $WW,
  "h": $WH,
  "shot_w": $SHOT_W,
  "shot_h": $SHOT_H,
  "scale": $SCALE,
  "png": "$PNG"
}
JSON

echo "$PNG"
