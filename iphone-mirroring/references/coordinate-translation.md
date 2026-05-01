# Coordinate Translation

Three coordinate spaces are involved. Getting them confused is the #1 source of off-target taps.

```
A. Screenshot pixels  — what OmniParser returns. Origin top-left of the PNG.
B. Window pixels      — same as A iff you captured exactly the window with -l <id>.
C. Screen logical pts — what cliclick + AppleScript take. Origin top-left of the main display.
D. iPhone logical pts — irrelevant to us; iPhone Mirroring handles this internally.
```

## The math

`screencapture -l <window-id>` writes a PNG sized at the **device pixel** dimensions of the window.
`AppleScript ... get position of window 1` returns the **logical-point** origin on the main display.

Retina scale = `screenshot_height / window_logical_height`. Usually 2.0; can be 1.0 if the user has scaled their display down.

```
window.json  = {x, y, w, h}        # logical points (from AppleScript)
screenshot   = capture.png         # PNG of size (w*scale, h*scale) device pixels
elements[i].bbox = [x1,y1,x2,y2]   # device pixels in the screenshot

# 1. Pick the bbox center in screenshot pixels
cx_px = (x1 + x2) / 2
cy_px = (y1 + y2) / 2

# 2. Down-convert to window logical points
cx_win = cx_px / scale
cy_win = cy_px / scale

# 3. Add window origin to get screen logical points
cx_screen = window.x + cx_win
cy_screen = window.y + cy_win

# 4. Click
cliclick c:cx_screen,cy_screen
```

`act.py` does exactly this. Don't redo the math elsewhere — call `act.py`.

## How to compute scale reliably

```python
from PIL import Image
img = Image.open("/tmp/iphone-mirror/capture.png")
shot_w, shot_h = img.size
scale_w = shot_w / window["w"]
scale_h = shot_h / window["h"]
# They should match within 1px. If they don't, the window resized between
# AppleScript and screencapture — re-capture.
assert abs(scale_w - scale_h) < 0.02, "non-uniform scale, recapture"
scale = scale_w
```

## iPhone Mirroring scaling presets

iPhone Mirroring offers three window sizes (Small/Medium/Large), stored in:
```
defaults read com.apple.ScreenContinuity lastWindowScalingPreset
# 0 = small, 1 = medium, 2 = large
```

Each preset changes the **window** size, not the iPhone's logical pixels. Our pipeline doesn't care — we always recompute scale from the actual capture. But: changing preset mid-session invalidates any cached `window.json`. Re-capture.

## Window can sit on a secondary display

`window.x` may be negative if the iPhone Mirroring window is on a display to the left of the main one. cliclick accepts negative coordinates and routes correctly to the secondary display, but **`screencapture -l` returns pixels from the actual window regardless of display**. No special handling needed — just don't filter out negative `x`.

Example from a real setup:
```json
{"id": 12345, "x": -817, "y": 133, "w": 418, "h": 920, "scale": 2.0}
```

Center of the window: cliclick gets `c:-608,593` and clicks on the left-side display correctly.

## Sanity checks before tapping

1. `0 <= cx_px <= shot_w` and `0 <= cy_px <= shot_h` — the bbox is inside the screenshot
2. `bbox` width and height ≥ 6 px after scale-down — anything smaller is probably noise
3. `interactable == true` — non-interactable elements (text labels) are tap-unsafe; tap a parent button instead
4. After cliclick, sleep 250–600ms before re-capturing for animations to settle
