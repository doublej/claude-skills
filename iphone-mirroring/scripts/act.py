#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Translate (element_id, action) into cliclick / AppleScript invocations.

Reads window.json + elements.json from $IPHONE_MIRROR_DIR (default /tmp/iphone-mirror).
"""
from __future__ import annotations
import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

DIR = Path(os.environ.get("IPHONE_MIRROR_DIR", "/tmp/iphone-mirror"))
KEY_SHORTCUTS = {
    "home": ("cmd", "1"),
    "app-switcher": ("cmd", "2"),
    "spotlight": ("cmd", "3"),
    "notifications": ("cmd+shift", "1"),
    "control-center": ("cmd+shift", "2"),
    "back": ("cmd", "["),
}


def load() -> tuple[dict, list[dict]]:
    win = json.loads((DIR / "window.json").read_text())
    els = json.loads((DIR / "elements.json").read_text()) if (DIR / "elements.json").exists() else []
    return win, els


def find(els: list[dict], eid: int) -> dict:
    for e in els:
        if e["id"] == eid:
            return e
    raise SystemExit(f"act.py: element id {eid} not in elements.json")


def to_screen(window: dict, bbox: list[float]) -> tuple[int, int]:
    x1, y1, x2, y2 = bbox
    cx_px = (x1 + x2) / 2
    cy_px = (y1 + y2) / 2
    scale = window["scale"]
    cx = window["x"] + cx_px / scale
    cy = window["y"] + cy_px / scale
    return int(round(cx)), int(round(cy))


def cliclick(*tokens: str) -> None:
    cmd = ["cliclick", *tokens]
    subprocess.run(cmd, check=True)


def cmd_tap(args) -> None:
    win, els = load()
    e = find(els, args.id)
    x, y = to_screen(win, e["bbox"])
    cliclick(f"c:{x},{y}")
    time.sleep(args.settle / 1000)


def cmd_long_press(args) -> None:
    win, els = load()
    e = find(els, args.id)
    x, y = to_screen(win, e["bbox"])
    cliclick(f"dd:{x},{y}", f"w:{args.ms}", f"du:{x},{y}")
    time.sleep(args.settle / 1000)


def cmd_swipe(args) -> None:
    win, els = load()
    if args.from_id is not None:
        e = find(els, args.from_id)
        sx, sy = to_screen(win, e["bbox"])
    else:
        sx, sy = win["x"] + win["w"] // 2, win["y"] + win["h"] // 2

    dist = args.distance
    dx, dy = {
        "up": (0, -dist),
        "down": (0, dist),
        "left": (-dist, 0),
        "right": (dist, 0),
    }[args.direction]
    ex, ey = sx + dx, sy + dy

    cliclick(
        f"m:{sx},{sy}",
        f"dd:{sx},{sy}",
        f"w:{args.hold}",
        f"m:{ex},{ey}",
        f"du:{ex},{ey}",
    )
    time.sleep(args.settle / 1000)


def cmd_type(args) -> None:
    if args.paste:
        subprocess.run(["pbcopy"], input=args.text.encode(), check=True)
        cliclick("kd:cmd", "t:v", "ku:cmd")
    else:
        cliclick(f"t:{args.text}")
    time.sleep(args.settle / 1000)


def cmd_key(args) -> None:
    if args.name not in KEY_SHORTCUTS:
        raise SystemExit(f"unknown key: {args.name}. valid: {list(KEY_SHORTCUTS)}")
    mods, char = KEY_SHORTCUTS[args.name]
    tokens: list[str] = []
    for m in mods.split("+"):
        tokens.append(f"kd:{m}")
    tokens.append(f"t:{char}")
    for m in reversed(mods.split("+")):
        tokens.append(f"ku:{m}")
    cliclick(*tokens)
    time.sleep(args.settle / 1000)


def cmd_xy(args) -> None:
    """Tap at raw screenshot pixel coords (debug / fallback)."""
    win, _ = load()
    cx = win["x"] + args.px / win["scale"]
    cy = win["y"] + args.py / win["scale"]
    cliclick(f"c:{int(round(cx))},{int(round(cy))}")
    time.sleep(args.settle / 1000)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--settle", type=int, default=300, help="ms to wait after action")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("tap"); sp.add_argument("--id", type=int, required=True); sp.set_defaults(fn=cmd_tap)

    sp = sub.add_parser("long-press"); sp.add_argument("--id", type=int, required=True)
    sp.add_argument("--ms", type=int, default=800); sp.set_defaults(fn=cmd_long_press)

    sp = sub.add_parser("swipe")
    sp.add_argument("--from-id", type=int)
    sp.add_argument("--direction", choices=["up", "down", "left", "right"], required=True)
    sp.add_argument("--distance", type=int, default=300)
    sp.add_argument("--hold", type=int, default=30)
    sp.set_defaults(fn=cmd_swipe)

    sp = sub.add_parser("type")
    sp.add_argument("--text", required=True)
    sp.add_argument("--paste", action="store_true", help="use clipboard paste for unicode/emoji")
    sp.set_defaults(fn=cmd_type)

    sp = sub.add_parser("key")
    sp.add_argument("--name", required=True, choices=list(KEY_SHORTCUTS))
    sp.set_defaults(fn=cmd_key)

    sp = sub.add_parser("xy")
    sp.add_argument("--px", type=int, required=True)
    sp.add_argument("--py", type=int, required=True)
    sp.set_defaults(fn=cmd_xy)

    args = p.parse_args()
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
