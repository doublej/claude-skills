#!/usr/bin/env python3
"""Copy the exact structured Codex image result without overwriting assets."""
import argparse
import json
import os
import shutil
from pathlib import Path


def resolve_image(result):
    if result.get("error"):
        raise SystemExit(f"Codex image error: {result['error']}")
    image_path = result.get("image_path")
    if not image_path or not Path(image_path).is_absolute():
        raise SystemExit("Codex did not return an absolute image path.")
    source = Path(image_path).resolve()
    root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    if not source.is_relative_to((root / "generated_images").resolve()):
        raise SystemExit("Image result is outside Codex's generated_images directory.")
    if not source.is_file() or source.suffix.lower() not in {".png", ".webp", ".jpg", ".jpeg"}:
        raise SystemExit("Codex's returned image is missing or has an unsupported format.")
    return source


def copy_image(args):
    source = resolve_image(json.loads(args.result.read_text()))
    destination = args.destination.resolve() / source.name
    with destination.open("xb") as output, source.open("rb") as image:
        shutil.copyfileobj(image, output)
    print(json.dumps({"image_path": str(destination)}))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("destination", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    copy_image(parse_args())
