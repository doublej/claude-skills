#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Goal-driven capture → parse → decide → act → verify loop.

Trajectory is written to /tmp/iphone-mirror/run-<ts>/ for offline review.

Backends:
  gemma    — runs decide_gemma.py against Ollama on Fractal (192.168.178.197)
             with model gemma4-64k:latest by default.
  claude   — emits decision-request files and pauses; the parent Claude Code
             agent reads annotated.png + elements.json, writes decision.json,
             then signals continue. Useful when running this skill from
             inside a Claude Code session.

Example:
  uv run scripts/loop.py --goal "Open Spotify and play Deftones" \
      --backend gemma --max-steps 12
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).parent
RUN_ROOT = Path("/tmp/iphone-mirror")


def step_capture(step_dir: Path) -> None:
    subprocess.run(["bash", str(SCRIPTS / "capture.sh")], check=True)
    shutil.copy("/tmp/iphone-mirror/capture.png", step_dir / "capture.png")
    shutil.copy("/tmp/iphone-mirror/window.json", step_dir / "window.json")


def step_parse(step_dir: Path) -> dict:
    out = subprocess.run(
        ["uv", "run", str(SCRIPTS / "parse.py"), str(step_dir / "capture.png")],
        check=True, capture_output=True, text=True,
    )
    shutil.copy("/tmp/iphone-mirror/elements.json", step_dir / "elements.json")
    shutil.copy("/tmp/iphone-mirror/annotated.png", step_dir / "annotated.png")
    return json.loads(out.stdout)


def step_decide_gemma(step_dir: Path, goal: str, history: Path, model: str) -> dict:
    out = subprocess.run(
        [
            "uv", "run", str(SCRIPTS / "decide_gemma.py"),
            "--goal", goal,
            "--annotated", str(step_dir / "annotated.png"),
            "--elements", str(step_dir / "elements.json"),
            "--history", str(history),
            "--model", model,
        ],
        check=True, capture_output=True, text=True,
    )
    decision = json.loads(out.stdout.splitlines()[-1])
    (step_dir / "decision.json").write_text(json.dumps(decision, indent=2))
    return decision


def step_decide_claude(step_dir: Path, goal: str, history: Path) -> dict:
    """Pause the loop and wait for the Claude agent to drop decision.json."""
    request = {
        "goal": goal,
        "annotated": str(step_dir / "annotated.png"),
        "elements": str(step_dir / "elements.json"),
        "history": str(history),
    }
    (step_dir / "decision_request.json").write_text(json.dumps(request, indent=2))
    decision_path = step_dir / "decision.json"

    print(
        f"[loop] waiting for Claude decision at {decision_path} "
        "(Read annotated.png + elements.json, write decision.json)"
    )
    while not decision_path.exists():
        time.sleep(1)
    return json.loads(decision_path.read_text())


def step_act(decision: dict) -> None:
    action = decision["action"]
    args = decision.get("args", {}) or {}
    eid = decision.get("element_id")
    cmd = ["uv", "run", str(SCRIPTS / "act.py")]

    if action == "tap":
        cmd += ["tap", "--id", str(eid)]
    elif action == "long-press":
        cmd += ["long-press", "--id", str(eid), "--ms", str(args.get("ms", 800))]
    elif action == "swipe":
        cmd += ["swipe", "--direction", args["direction"], "--distance", str(args.get("distance", 300))]
        if eid is not None and eid >= 0:
            cmd += ["--from-id", str(eid)]
    elif action == "type":
        cmd += ["type", "--text", args["text"]]
        if args.get("paste"):
            cmd += ["--paste"]
    elif action == "key":
        cmd += ["key", "--name", args["name"]]
    else:
        raise SystemExit(f"loop: unknown action {action}")

    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--backend", choices=["gemma", "claude"], default="gemma")
    ap.add_argument("--model", default="gemma4-64k:latest")
    ap.add_argument("--max-steps", type=int, default=12)
    ap.add_argument("--min-confidence", type=float, default=0.5)
    args = ap.parse_args()

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUN_ROOT / f"run-{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)
    history = run_dir / "history.json"
    history.write_text("[]")
    (run_dir / "goal.txt").write_text(args.goal)

    history_log: list[dict] = []

    for step in range(1, args.max_steps + 1):
        step_dir = run_dir / f"step-{step:02d}"
        step_dir.mkdir()

        step_capture(step_dir)
        parse_summary = step_parse(step_dir)

        if args.backend == "gemma":
            decision = step_decide_gemma(step_dir, args.goal, history, args.model)
        else:
            decision = step_decide_claude(step_dir, args.goal, history)

        history_log.append({
            "step": step,
            "decision": decision,
            "elements_count": parse_summary.get("count"),
        })
        history.write_text(json.dumps(history_log, indent=2))

        action = decision.get("action")
        print(f"[step {step}] action={action} id={decision.get('element_id')} "
              f"conf={decision.get('confidence')}  -- {decision.get('reasoning','')}")

        if action == "done":
            print(f"[loop] goal reached in {step} steps. Trajectory: {run_dir}")
            return 0
        if action == "error":
            print(f"[loop] decision error: {decision.get('reasoning')}", file=sys.stderr)
            return 2
        if decision.get("confidence", 1.0) < args.min_confidence:
            print(f"[loop] confidence {decision.get('confidence')} < {args.min_confidence}; aborting")
            return 3

        step_act(decision)
        time.sleep(0.4)

    print(f"[loop] hit max-steps={args.max_steps} without done. Trajectory: {run_dir}")
    return 4


if __name__ == "__main__":
    sys.exit(main())
