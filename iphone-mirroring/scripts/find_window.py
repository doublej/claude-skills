#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyobjc-framework-Quartz"]
# ///
"""Print the CGWindowID + bounds of the iPhone Mirroring window.

CGWindowIDs let `screencapture -l <id>` grab the window's pixels regardless of
occlusion (browser/IDE on top, partially offscreen, etc.) — unlike `-R x,y,w,h`
which captures whatever's at those screen coordinates.

Output: `<id> <x> <y> <w> <h>` (single line) or exit non-zero with a message.
"""
from __future__ import annotations
import sys

from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGNullWindowID,
    kCGWindowListExcludeDesktopElements,
    kCGWindowListOptionOnScreenOnly,
)

OWNER = "iPhone Mirroring"


def main() -> int:
    opts = kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements
    wins = CGWindowListCopyWindowInfo(opts, kCGNullWindowID)
    candidates = [
        w for w in wins
        if w.get("kCGWindowOwnerName") == OWNER and w.get("kCGWindowLayer", 0) == 0
    ]
    if not candidates:
        print(f"find_window: no on-screen window for {OWNER!r}", file=sys.stderr)
        return 2
    # Largest area wins (skips tiny indicator/tooltip windows).
    candidates.sort(
        key=lambda w: w["kCGWindowBounds"]["Width"] * w["kCGWindowBounds"]["Height"],
        reverse=True,
    )
    w = candidates[0]
    b = w["kCGWindowBounds"]
    print(int(w["kCGWindowNumber"]), int(b["X"]), int(b["Y"]), int(b["Width"]), int(b["Height"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
