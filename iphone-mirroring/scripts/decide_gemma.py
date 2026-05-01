#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Ask Gemma 4 (running on Fractal via Ollama) which element to act on.

Endpoint:  http://192.168.178.197:11434/v1/chat/completions   (OpenAI-compatible)
Default model: gemma4-64k:latest
Override host with OLLAMA_URL, model with --model.

Inputs:
  --goal "Open Spotify"
  --annotated /tmp/iphone-mirror/annotated.png
  --elements /tmp/iphone-mirror/elements.json
  --history    optional path to JSON list of prior steps for context

Output (stdout, single JSON line):
  {"element_id": 7, "action": "tap", "args": {}, "confidence": 0.82, "reasoning": "..."}
or:
  {"action": "done", "confidence": 1.0, "reasoning": "goal reached"}
"""
from __future__ import annotations
import argparse
import base64
import json
import os
import sys
from pathlib import Path

import httpx

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://192.168.178.197:11434")
DEFAULT_MODEL = os.environ.get("GEMMA_MODEL", "gemma4-64k:latest")

SYSTEM = """You drive an iPhone via the macOS iPhone Mirroring app. \
Each turn you see an annotated screenshot with numbered overlays and a JSON list of elements.

You must respond with a SINGLE JSON object on one line, no markdown, no commentary:
  {"element_id": <int>, "action": "<verb>", "args": {}, "confidence": <0..1>, "reasoning": "<brief>"}

Valid actions:
  tap             — single tap on element_id
  long-press      — args: {"ms": 800}
  swipe           — args: {"direction": "up|down|left|right", "distance": 300}; element_id may be -1 for screen-center start
  type            — args: {"text": "..."}; element_id of the focused field, or -1 if already focused
  key             — args: {"name": "home|app-switcher|spotlight|notifications|control-center|back"}; element_id ignored
  done            — when the goal is reached. element_id ignored.

Rules:
- Pick the SINGLE next action that makes the most progress toward the goal.
- Prefer interactable=true elements. Don't tap text labels — find the parent button.
- If the goal is achieved, return action=done.
- Be honest about confidence; <0.6 means you're guessing.
"""


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build_user_message(goal: str, elements: list[dict], history: str, image_b64: str) -> dict:
    elements_text = "\n".join(
        f"  {e['id']}: {e.get('label','')!r} interactable={e.get('interactable')} type={e.get('type')}"
        for e in elements
    )
    text = (
        f"Goal: {goal}\n\n"
        f"Elements (id, label, interactable, type):\n{elements_text}"
        + (f"\n\nPrior steps:\n{history}" if history else "")
        + "\n\nReturn the JSON action."
    )
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--annotated", type=Path, required=True)
    ap.add_argument("--elements", type=Path, required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--history", type=Path)
    ap.add_argument("--temperature", type=float, default=0.1)
    ap.add_argument("--timeout", type=float, default=180.0)
    args = ap.parse_args()

    elements = json.loads(args.elements.read_text())
    history_text = args.history.read_text() if args.history and args.history.exists() else ""
    image_b64 = encode_image(args.annotated)

    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            build_user_message(args.goal, elements, history_text, image_b64),
        ],
        "temperature": args.temperature,
        "response_format": {"type": "json_object"},
    }

    try:
        r = httpx.post(
            f"{OLLAMA_URL}/v1/chat/completions",
            json=payload,
            timeout=args.timeout,
        )
        r.raise_for_status()
    except httpx.HTTPError as e:
        print(json.dumps({
            "action": "error",
            "confidence": 0.0,
            "reasoning": f"Ollama at {OLLAMA_URL} unreachable: {e}",
        }))
        return 1

    raw = r.json()["choices"][0]["message"]["content"].strip()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({
            "action": "error",
            "confidence": 0.0,
            "reasoning": f"non-json model output: {raw[:300]}",
        }))
        return 1

    obj.setdefault("args", {})
    obj.setdefault("confidence", 0.5)
    print(json.dumps(obj))
    return 0


if __name__ == "__main__":
    sys.exit(main())
