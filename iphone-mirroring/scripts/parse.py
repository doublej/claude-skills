#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "Pillow"]
# ///
"""Send a screenshot to the local OmniParser server and persist results."""
from __future__ import annotations
import argparse
import base64
import json
import os
import sys
from pathlib import Path

import httpx

SERVER = os.environ.get("OMNI_URL", "http://127.0.0.1:8765")
OUT_DIR = Path(os.environ.get("IPHONE_MIRROR_DIR", "/tmp/iphone-mirror"))


def parse(png: Path, box_threshold: float, iou_threshold: float) -> dict:
    with png.open("rb") as f:
        files = {"image": (png.name, f, "image/png")}
        params = {"box_threshold": box_threshold, "iou_threshold": iou_threshold}
        r = httpx.post(f"{SERVER}/parse", files=files, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("png", type=Path)
    ap.add_argument("--box-threshold", type=float, default=0.05)
    ap.add_argument("--iou-threshold", type=float, default=0.10)
    args = ap.parse_args()

    if not args.png.exists():
        print(f"parse.py: not found: {args.png}", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        result = parse(args.png, args.box_threshold, args.iou_threshold)
    except httpx.ConnectError:
        print(
            f"parse.py: cannot reach OmniParser at {SERVER}. "
            "Run: bash scripts/serve_omniparser.sh",
            file=sys.stderr,
        )
        return 3

    elements = result["elements"]
    (OUT_DIR / "elements.json").write_text(json.dumps(elements, indent=2))

    annotated_b64 = result.get("annotated_b64")
    if annotated_b64:
        (OUT_DIR / "annotated.png").write_bytes(base64.b64decode(annotated_b64))

    print(json.dumps({
        "elements": str(OUT_DIR / "elements.json"),
        "annotated": str(OUT_DIR / "annotated.png"),
        "count": len(elements),
        "interactable": sum(1 for e in elements if e.get("interactable")),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
