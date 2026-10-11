#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyobjc-framework-Quartz", "pyobjc-framework-Vision", "pyobjc-framework-Cocoa", "pillow"]
# ///
"""Drive a device through Xcode's Device Hub screen-share window, deterministically.

Recognition is Apple Vision OCR (text + boxes), not a vision model. The phone
screen is located by its black bezel in each capture, so every coordinate is
relative to the phone screen (0..1, top-left) and survives window resizes.
Input goes through cliclick; Device Hub forwards mouse as touch.

  devicehub.py ocr                    # JSON lines: text, x/y/w/h (screen-relative)
  devicehub.py page                   # matching PAGES entry, or "unknown"
  devicehub.py tap --text Likes       # tap OCR'd text
  devicehub.py tap --rel 0.40 0.918   # tap a screen-relative point
  devicehub.py swipe left --rel-y 0.37
  devicehub.py overlay                # click-through HUD over the window (run in background)
  devicehub.py feeld-hunt --max 40    # pass on Discover cards until a Likes name shows up
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import Quartz
import Vision
from Foundation import NSURL
from PIL import Image

OWNER = "Device Hub"
STATE = Path(os.environ.get("IPHONE_MIRROR_DIR", "/tmp/iphone-mirror")) / "devicehub-overlay.json"

# page name -> text anchors that must all be on screen (case-insensitive substring)
PAGES: dict[str, list[str]] = {
    "feeld.discover": ["Desires", "Location"],
    "feeld.likes": ["Likes", "Pings"],
    "feeld.paywall": ["Majestic membership"],
}

# screen-relative points for controls without text
FEELD = {
    "tab.discover": (0.204, 0.918),
    "tab.likes": (0.40, 0.918),
    "card": (0.5, 0.37),
    "paywall.close": (0.891, 0.102),
    "scroll.lane": 0.97,  # x of the empty right margin: drags here scroll without tapping a card
}

BEZEL_LUMA = 40  # bezel pixels are darker than this
BEZEL_MIN_PX = 6  # shortest dark run that counts as bezel (text strokes are thinner)
PHONE_ASPECT = 402 / 874  # iPhone 17 Pro points; screen rect must match within 0.03


# ---------- capture + recognition ----------


def device_window() -> dict | None:
    wins = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
        Quartz.kCGNullWindowID,
    )
    cands = [w for w in wins if w.get("kCGWindowOwnerName") == OWNER and w.get("kCGWindowLayer", 0) == 0]
    if not cands:
        return None
    w = max(cands, key=lambda w: w["kCGWindowBounds"]["Width"] * w["kCGWindowBounds"]["Height"])
    b = w["kCGWindowBounds"]
    return {"id": int(w["kCGWindowNumber"]), "x": b["X"], "y": b["Y"], "w": b["Width"], "h": b["Height"]}


def find_window() -> dict:
    win = device_window()
    if not win:
        raise SystemExit(f"devicehub: no on-screen {OWNER!r} window; start screen sharing in Device Hub")
    return win


def dark_runs(vals: list[int]) -> list[tuple[int, int]]:
    runs, start = [], None
    for i, v in enumerate([*vals, 255]):
        if v < BEZEL_LUMA and start is None:
            start = i
        elif v >= BEZEL_LUMA and start is not None:
            if i - start >= BEZEL_MIN_PX:
                runs.append((start, i - 1))
            start = None
    return runs


def detect_screen(png: str, win: dict) -> dict | None:
    """Phone screen rect inside the window, in window points; None if the bezel isn't found."""
    # ponytail: assumes light pixels just inside the bezel; a black app edge widens the run
    im = Image.open(png).convert("L")
    W, H = im.size
    row = dark_runs([im.getpixel((x, int(H * 0.6))) for x in range(W)])
    if len(row) < 2:
        return None
    left, right = row[0][1] + 1, row[-1][0] - 1
    cx = int(left + 0.3 * (right - left))
    col = dark_runs([im.getpixel((cx, y)) for y in range(H)])
    if len(col) < 2:
        return None
    top, bottom = col[0][1] + 1, col[-1][0] - 1
    if abs((right - left) / (bottom - top) - PHONE_ASPECT) > 0.03:
        return None
    s = W / win["w"]
    return {"x": left / s, "y": top / s, "w": (right - left) / s, "h": (bottom - top) / s}


def capture(win: dict, png: str) -> dict:
    """Capture the window and locate the phone screen; mutates win to the live bounds (it may be moved/resized)."""
    for _ in range(5):  # a capture taken mid move/resize has no clean bezel; settle and retry
        win.update(find_window())
        subprocess.run(["screencapture", "-x", "-o", "-l", str(win["id"]), png], check=True)
        scr = detect_screen(png, win)
        if scr:
            return scr
        time.sleep(0.4)
    raise SystemExit(f"devicehub: phone screen not found in {png} (bezel scan or aspect check failed)")


def ocr(win: dict, png: str | None = None) -> tuple[dict, list[dict]]:
    """Capture + OCR; returns (screen rect, texts with screen-relative centers/sizes)."""
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        png = png or tmp.name
        scr = capture(win, png)
        req = Vision.VNRecognizeTextRequest.alloc().init()
        req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
        req.setUsesLanguageCorrection_(False)
        handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(NSURL.fileURLWithPath_(png), None)
        ok, err = handler.performRequests_error_([req], None)
        if not ok:
            raise RuntimeError(f"Vision OCR failed: {err}")
    out = []
    for obs in req.results() or []:
        (x, y), (w, h) = obs.boundingBox()
        # Vision: normalized to the image, bottom-left origin -> window points -> screen-relative
        px, py = (x + w / 2) * win["w"], (1 - y - h / 2) * win["h"]
        rx, ry = (px - scr["x"]) / scr["w"], (py - scr["y"]) / scr["h"]
        if 0 <= rx <= 1 and 0 <= ry <= 1:
            out.append(
                {
                    "text": obs.topCandidates_(1)[0].string(),
                    "x": round(rx, 4),
                    "y": round(ry, 4),
                    "w": round(w * win["w"] / scr["w"], 4),
                    "h": round(h * win["h"] / scr["h"], 4),
                }
            )
    return scr, sorted(out, key=lambda t: (t["y"], t["x"]))


def match_page(texts: list[dict]) -> str:
    blob = [t["text"].lower() for t in texts]
    for name, anchors in PAGES.items():
        if all(any(a.lower() in t for t in blob) for a in anchors):
            return name
    return "unknown"


# ---------- overlay state ----------


def emit(**kw) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    state.update(kw)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state))
    os.replace(tmp, STATE)


def show(scr: dict, texts: list[dict], page: str, hits: set[str] = frozenset(), status: str = "") -> None:
    emit(screen=scr, page=page, status=status, boxes=[{**t, "hit": t["text"] in hits} for t in texts])


# ---------- input ----------


def at(p: tuple[int, int]) -> str:
    """cliclick point; '=' marks absolute negatives (displays left of / above the main one)."""
    return ",".join(f"={v}" if v < 0 else str(v) for v in p)


def to_global(win: dict, scr: dict, rx: float, ry: float) -> tuple[int, int]:
    return round(win["x"] + scr["x"] + rx * scr["w"]), round(win["y"] + scr["y"] + ry * scr["h"])


def activate() -> None:
    subprocess.run(
        ["osascript", "-e", f'tell application "System Events" to set frontmost of process "{OWNER}" to true'],
        check=True,
        capture_output=True,
    )
    time.sleep(0.15)


def tap(win: dict, scr: dict, rx: float, ry: float) -> None:
    emit(gesture={"kind": "tap", "path": [[rx, ry]], "t0": time.time(), "dur": 0.1})
    subprocess.run(["cliclick", f"c:{at(to_global(win, scr, rx, ry))}"], check=True)


def swipe(
    win: dict,
    scr: dict,
    direction: str,
    rx: float = 0.5,
    ry: float = 0.5,
    span: float = 0.7,
    steps: int = 14,
    step_ms: int = 20,
    hold_ms: int = 0,
) -> None:
    """hold_ms > 0 pauses before lift-off so scroll views stop dead instead of flinging."""
    dx, dy = {"left": (-span, 0), "right": (span, 0), "up": (0, -span / 2), "down": (0, span / 2)}[direction]
    sx, sy = rx - dx / 2, ry - dy / 2
    path = [[sx + dx * i / steps, sy + dy * i / steps] for i in range(steps + 1)]
    emit(gesture={"kind": "swipe", "path": path, "t0": time.time(), "dur": (steps * step_ms + hold_ms) / 1000})
    pts = [to_global(win, scr, *p) for p in path]
    hold = [f"w:{hold_ms}"] if hold_ms else []
    cmds = [f"dd:{at(pts[0])}", *[f"dm:{at(p)}" for p in pts[1:]], *hold, f"du:{at(pts[-1])}"]
    subprocess.run(["cliclick", "-w", str(step_ms), *cmds], check=True)


# ---------- overlay (HUD) ----------


def run_overlay() -> None:
    import AppKit
    from AppKit import NSBezierPath, NSColor, NSFont, NSMakeRect, NSString, NSTimer, NSView, NSWindow

    st: dict = {}

    def col(name: str, a: float):
        return getattr(NSColor, name)().colorWithAlphaComponent_(a)

    def draw_gesture(g, P, k):  # plain function: pyobjc treats methods as selectors; k = HUD scale
        if not g:
            return
        t = time.time() - g["t0"]
        fade = 1 if t < g["dur"] else 1 - (t - g["dur"]) / 1.2
        if fade <= 0:
            return
        pts = [P(*p) for p in g["path"]]
        i = max(1, round(min(1, t / g["dur"]) * (len(pts) - 1))) if len(pts) > 1 else 0
        if i:
            trail = NSBezierPath.bezierPath()
            trail.moveToPoint_(pts[0])
            for p in pts[1 : i + 1]:
                trail.lineToPoint_(p)
            trail.setLineWidth_(3 * k)
            col("systemOrangeColor", 0.9 * fade).set()
            trail.stroke()
        x, y = pts[i]
        r = k * (9 + (14 * min(1, t / 0.5) if g["kind"] == "tap" else 0))
        col("systemOrangeColor", 0.45 * fade).set()
        NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(x - r, y - r, 2 * r, 2 * r)).fill()

    class HUD(NSView):
        def isFlipped(self):
            return True

        def drawRect_(self, _rect):
            scr = live.get("screen") or st.get("screen")
            if not scr:
                return
            k = scr["w"] / 300  # everything drawn scales with the phone screen

            def P(rx, ry):
                return (scr["x"] + rx * scr["w"], scr["y"] + ry * scr["h"])

            col("systemBlueColor", 0.5).set()
            outline = NSBezierPath.bezierPathWithRect_(NSMakeRect(scr["x"], scr["y"], scr["w"], scr["h"]))
            outline.setLineWidth_(k)
            outline.stroke()
            for b in st.get("boxes", []):
                x, y = P(b["x"] - b["w"] / 2, b["y"] - b["h"] / 2)
                path = NSBezierPath.bezierPathWithRect_(NSMakeRect(x, y, b["w"] * scr["w"], b["h"] * scr["h"]))
                path.setLineWidth_(k * (2.5 if b["hit"] else 1))
                col("systemGreenColor" if b["hit"] else "systemTealColor", 0.95 if b["hit"] else 0.6).set()
                path.stroke()
            label = NSString.stringWithString_(f" {st.get('page', '?')}  {st.get('status', '')} ")
            attrs = {
                AppKit.NSFontAttributeName: NSFont.monospacedSystemFontOfSize_weight_(10 * k, 0.4),
                AppKit.NSForegroundColorAttributeName: NSColor.whiteColor(),
                AppKit.NSBackgroundColorAttributeName: col("blackColor", 0.7),
            }
            label.drawAtPoint_withAttributes_((scr["x"] + 4 * k, scr["y"] + scr["h"] * 0.055), attrs)
            draw_gesture(st.get("gesture"), P, k)

    app = AppKit.NSApplication.sharedApplication()
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
    win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(0, 0, 10, 10), AppKit.NSWindowStyleMaskBorderless, AppKit.NSBackingStoreBuffered, False
    )
    win.setOpaque_(False)
    win.setBackgroundColor_(NSColor.clearColor())
    win.setIgnoresMouseEvents_(True)
    win.setHasShadow_(False)
    win.setLevel_(AppKit.NSStatusWindowLevel)
    win.setCollectionBehavior_(
        AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces | AppKit.NSWindowCollectionBehaviorStationary
    )
    view = HUD.alloc().initWithFrame_(NSMakeRect(0, 0, 10, 10))
    win.setContentView_(view)
    win.orderFrontRegardless()

    seen = {"mtime": 0.0, "frame": 0.0, "size": None}
    live: dict = {}  # screen rect re-detected here whenever the window is resized
    shot = str(STATE.with_name("overlay-probe.png"))

    def tick(_timer):
        now = time.time()
        if now - seen["frame"] > 0.3:
            seen["frame"] = now
            dw = device_window()
            if dw:
                top = AppKit.NSScreen.screens()[0].frame().size.height
                win.setFrame_display_(NSMakeRect(dw["x"], top - dw["y"] - dw["h"], dw["w"], dw["h"]), True)
                if (dw["w"], dw["h"]) != seen["size"]:
                    subprocess.run(["screencapture", "-x", "-o", "-l", str(dw["id"]), shot], check=True)
                    live["screen"] = detect_screen(shot, dw)
                    seen["size"] = (dw["w"], dw["h"]) if live["screen"] else None  # retry until it settles
            win.setAlphaValue_(1 if dw else 0)
        if STATE.exists() and STATE.stat().st_mtime != seen["mtime"]:
            seen["mtime"] = STATE.stat().st_mtime
            st.clear()
            st.update(json.loads(STATE.read_text()))
        view.setNeedsDisplay_(True)

    NSTimer.scheduledTimerWithTimeInterval_repeats_block_(1 / 30, True, tick)
    app.run()


# ---------- feeld hunt ----------

AGE_LINE = re.compile(r"^\d{2}\s*[•·]")


def card_name(texts: list[dict]) -> dict | None:
    """Discover card: the name is the leftmost text on the row right above the 'NN • Woman' line."""
    age = next((t for t in texts if AGE_LINE.match(t["text"])), None)
    if not age:
        return None
    above = [t for t in texts if 0 < age["y"] - t["y"] < 0.06]
    if not above:
        return None
    row_y = max(t["y"] for t in above)
    name = min((t for t in above if abs(t["y"] - row_y) < 0.01), key=lambda t: t["x"])
    # names sit flush left; anything else (e.g. the "LAST SEEN" badge when OCR missed the name) is unreadable
    return name if 0.03 <= name["x"] - name["w"] / 2 <= 0.08 else None


def next_card(win: dict, last: str | None, png: str, timeout: float = 3.0) -> tuple[dict, list[dict], dict | None]:
    """Poll Discover until a readable card other than `last` is up (mid-animation frames have no age line)."""
    deadline = time.time() + timeout
    while True:
        scr, texts = look(win, "feeld.discover", png)
        card = card_name(texts)
        if (card and norm(card["text"]) != last) or time.time() > deadline:
            return scr, texts, card


def profile_names(texts: list[dict]) -> list[dict]:
    """Profile names on Feeld cards: one word, big type, flush with the card's left edge (~0.05)."""
    # y > 0.42: below the pinned Likes header, whose Majestic "M" badge would otherwise count
    return [
        t
        for t in texts
        if " " not in t["text"].strip() and 0.03 <= t["x"] - t["w"] / 2 <= 0.08 and t["h"] >= 0.02 and t["y"] > 0.42
    ]


def look(win: dict, expect: str, png: str | None = None) -> tuple[dict, list[dict]]:
    """OCR, closing the Majestic paywall if a stray touch opened it; stop on any other page than expected."""
    for _ in range(2):
        scr, texts = ocr(win, png)
        page = match_page(texts)
        if page != "feeld.paywall":
            break
        show(scr, texts, page, status="paywall: closing")
        tap(win, scr, *FEELD["paywall.close"])
        time.sleep(1.2)
    if page != expect:
        show(scr, texts, page, status=f"expected {expect}; stop")
        raise SystemExit(f"devicehub: expected {expect}, saw {page}")
    return scr, texts


def scroll_until_still(win: dict, direction: str, max_scrolls: int, on_frame=None) -> None:
    """Scroll the Likes list in the margin lane until two frames in a row don't change (some drags don't register)."""
    prev, still = None, 0
    for _ in range(max_scrolls):
        scr, texts = look(win, "feeld.likes")
        if on_frame:
            on_frame(scr, texts)
        now = [t["text"] for t in texts]
        still = still + 1 if now == prev else 0
        if still >= 2:
            return
        prev = now
        if direction == "up":  # ~0.25 screen per step with no fling, so every name crosses the visible band
            swipe(win, scr, "up", rx=FEELD["scroll.lane"], ry=0.6, span=0.5, hold_ms=300)
        else:  # starts below the pinned header; fling is fine on the way to the top
            swipe(win, scr, "down", rx=FEELD["scroll.lane"], ry=0.65, span=0.6)
        time.sleep(0.8)


def feeld_likes(win: dict, max_scrolls: int = 30) -> list[str]:
    """Open the Likes tab, scroll to the top, then step down to the end collecting card names."""
    activate()
    scr, _ = ocr(win)
    tap(win, scr, *FEELD["tab.likes"])
    time.sleep(1.5)
    names: dict[str, str] = {}
    expected = [0]

    def collect(scr: dict, texts: list[dict]) -> None:
        count = next((m for t in texts if (m := re.match(r"(\d+)\s*Likes", t["text"]))), None)
        expected[0] = int(count.group(1)) if count else expected[0]
        found = profile_names(texts)
        names.update({norm(t["text"]): t["text"] for t in found})
        status = f"likes {len(names)}/{expected[0]}: {', '.join(names.values())}"
        show(scr, texts, "feeld.likes", {t["text"] for t in found}, status)

    for _ in range(3):  # single-letter names OCR flakily; repeat passes until the header count is met
        scroll_until_still(win, "down", max_scrolls)
        scroll_until_still(win, "up", max_scrolls, collect)
        if len(names) >= expected[0]:
            break
    if len(names) < expected[0]:
        print(f"devicehub: found {len(names)} of {expected[0]} likes", file=sys.stderr)
    return list(names.values())


def norm(name: str) -> str:
    return re.sub(r"[^\w]", "", name.split(",")[0]).lower()


def feeld_hunt(win: dict, max_cards: int, names: list[str] | None) -> int:
    run = Path(os.environ.get("IPHONE_MIRROR_DIR", "/tmp/iphone-mirror")) / f"run-{time.strftime('%Y%m%d-%H%M%S')}"
    run.mkdir(parents=True)
    names = names or feeld_likes(win)
    if not names:
        raise SystemExit("devicehub: no names found on the Likes tab")
    targets = {norm(n) for n in names}
    activate()
    scr, _ = ocr(win)
    tap(win, scr, *FEELD["tab.discover"])
    time.sleep(1.5)
    print(f"targets: {names}  trajectory: {run}")
    last = None
    for step in range(1, max_cards + 1):
        png = str(run / f"step-{step:03}.png")
        scr, texts, card = next_card(win, last, png)
        page = "feeld.discover"
        (run / f"step-{step:03}.json").write_text(json.dumps({"page": page, "card": card, "texts": texts}))
        if not card:
            show(scr, texts, page, status=f"#{step} name unreadable; stop")
            print(f"{step}\tstop\t—\tname unreadable, see {png}")
            return 2
        name = norm(card["text"])
        if name in targets:
            show(scr, texts, page, {card["text"]}, f"#{step} MATCH {card['text']}")
            print(f"{step}\tMATCH\t{card['text']}")
            return 0
        if name == last:
            show(scr, texts, page, {card["text"]}, f"#{step} {card['text']} still here; stop")
            print(f"{step}\tstop\t{card['text']}\tswipe did not advance")
            return 3
        show(scr, texts, page, {card["text"]}, f"#{step} {card['text']}: pass")
        print(f"{step}\tswipe\t{card['text']}")
        swipe(win, scr, "left", *FEELD["card"], span=0.8, steps=5, step_ms=8)  # quick flick
        last = name
    print(f"max {max_cards} reached")
    return 4


def selftest() -> None:
    """Name rules against OCR rows captured from the real app."""
    discover = [
        {"text": "Desires v", "x": 0.1833, "y": 0.1165, "w": 0.1779, "h": 0.0173},
        {"text": "Liz", "x": 0.0943, "y": 0.6183, "w": 0.0863, "h": 0.0248},
        {"text": "LAST SEEN", "x": 0.8544, "y": 0.6183, "w": 0.1617, "h": 0.0149},
        {"text": "40 • Woman • Heteroflexible", "x": 0.3073, "y": 0.6518, "w": 0.5121, "h": 0.0173},
        {"text": "6G Looking for good times. Connection,", "x": 0.4394, "y": 0.7334, "w": 0.7772, "h": 0.0274},
    ]
    likes = [
        {"text": "M", "x": 0.1466, "y": 0.2709, "w": 0.058, "h": 0.0267},
        {"text": "J", "x": 0.0647, "y": 0.7794, "w": 0.027, "h": 0.0248},
        {"text": "R.", "x": 0.0836, "y": 0.8674, "w": 0.0647, "h": 0.0273},
        {"text": "Charles", "x": 0.1617, "y": 0.7237, "w": 0.2325, "h": 0.0284},
        {"text": "LAST SEEN", "x": 0.8543, "y": 0.8653, "w": 0.1628, "h": 0.0157},
        {"text": "→ Uplift your profile", "x": 0.6927, "y": 0.8274, "w": 0.4111, "h": 0.0281},
    ]
    assert card_name(discover)["text"] == "Liz"
    assert card_name([t for t in discover if t["text"] != "Liz"]) is None  # only LAST SEEN left on the row
    assert [t["text"] for t in profile_names(discover)] == ["Liz"]
    assert [t["text"] for t in profile_names(likes)] == ["J", "R.", "Charles"]
    assert norm("R.") == "r" and norm("Liz, 40") == "liz"
    assert at((-1412, 659)) == "=-1412,659" and at((10, -5)) == "10,=-5"
    print("selftest ok")


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ocr")
    sub.add_parser("page")
    sub.add_parser("overlay")
    sub.add_parser("selftest")
    sp = sub.add_parser("tap")
    sp.add_argument("--text")
    sp.add_argument("--rel", nargs=2, type=float)
    sp = sub.add_parser("swipe")
    sp.add_argument("direction", choices=["left", "right", "up", "down"])
    sp.add_argument("--rel-y", type=float, default=0.5)
    sp = sub.add_parser("feeld-hunt")
    sp.add_argument("--max", type=int, default=40)
    sp.add_argument("--names", nargs="+", help="skip collecting from the Likes tab")
    sub.add_parser("feeld-likes")
    args = p.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    if args.cmd == "selftest":
        selftest()
        return 0
    if args.cmd == "overlay":
        run_overlay()
        return 0
    win = find_window()
    if args.cmd == "feeld-likes":
        print("\n".join(feeld_likes(win)))
        return 0
    if args.cmd == "feeld-hunt":
        return feeld_hunt(win, args.max, args.names)
    scr, texts = ocr(win)
    page = match_page(texts)
    show(scr, texts, page)
    if args.cmd == "ocr":
        for t in texts:
            print(json.dumps(t, ensure_ascii=False))
    elif args.cmd == "page":
        print(page)
    else:
        activate()
        if args.cmd == "tap" and args.text:
            hits = [t for t in texts if args.text.lower() in t["text"].lower()]
            if not hits:
                raise SystemExit(f"devicehub: text {args.text!r} not on screen")
            tap(win, scr, hits[0]["x"], hits[0]["y"])
        elif args.cmd == "tap":
            tap(win, scr, *args.rel)
        else:
            swipe(win, scr, args.direction, ry=args.rel_y)
    return 0


if __name__ == "__main__":
    sys.exit(main())
