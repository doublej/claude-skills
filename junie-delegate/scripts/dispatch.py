#!/usr/bin/env python3
"""Run one Junie work order headless and print a context-cheap digest.

The raw JSON Junie emits embeds full before/after content of every changed file.
That is exactly what must not land in the planner's context, so it goes to a file
and only the summary, the changed paths, the session id and the cost are printed.
Read the actual work with `git diff`.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SETTINGS = Path.home() / ".junie" / "settings.json"
DEFAULT_MODEL = "gemini-3.8-flash"


def pinModel(model):
    """Junie has no --model flag; modelForLaunch in settings.json is the only lever."""
    settings = json.loads(SETTINGS.read_text()) if SETTINGS.exists() else {}
    if settings.get("modelForLaunch") == model:
        return False
    settings["modelForLaunch"] = model
    SETTINGS.write_text(json.dumps(settings, indent=4))
    return True


def runJunie(task, project, model, sessionId, outFile):
    cmd = ["junie", "--project", project, "--output-format", "json",
           "--json-output-file", str(outFile), "--skip-update-check"]
    if sessionId:
        cmd += ["--session-id", sessionId, "--resume"]
    cmd.append(task)
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc, round(time.time() - started)


def buildDigest(payload, elapsed, outFile):
    changes = payload.get("changes") or []
    usage = payload.get("llmUsage") or []
    return {
        "sessionId": payload.get("sessionId"),
        "taskName": payload.get("taskName"),
        "result": payload.get("result"),
        "changedFiles": sorted({c.get("afterRelativePath") or c.get("beforeRelativePath")
                                for c in changes if c.get("afterRelativePath") or c.get("beforeRelativePath")}),
        "models": sorted({u.get("model") for u in usage if u.get("model")}),
        "costUsd": round(sum(u.get("cost", 0) for u in usage), 4),
        "elapsedSeconds": elapsed,
        "rawJson": str(outFile),
    }


def main():
    parser = argparse.ArgumentParser(description="Dispatch one work order to Junie.")
    parser.add_argument("task", nargs="?", help="Work order text (omit when using --task-file)")
    parser.add_argument("--task-file", help="File holding the work order text")
    parser.add_argument("--project", default=os.getcwd(), help="Project directory (default: cwd)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Junie model (default: {DEFAULT_MODEL})")
    parser.add_argument("--session-id", help="Follow up on an earlier session instead of starting fresh")
    parser.add_argument("--json", action="store_true", help="Emit the digest as JSON")
    args = parser.parse_args()

    task = Path(args.task_file).read_text() if args.task_file else args.task
    if not task or not task.strip():
        parser.error("provide a work order as an argument or via --task-file")

    project = str(Path(args.project).resolve())
    switched = pinModel(args.model)

    outDir = Path(os.environ.get("TMPDIR", "/tmp")) / "junie-delegate"
    outDir.mkdir(parents=True, exist_ok=True)
    outFile = outDir / f"run-{int(time.time())}.json"

    proc, elapsed = runJunie(task, project, args.model, args.session_id, outFile)
    if not outFile.exists():
        sys.stderr.write(proc.stdout[-2000:] + proc.stderr[-2000:])
        sys.exit(f"\njunie produced no result file (exit {proc.returncode})")

    digest = buildDigest(json.loads(outFile.read_text()), elapsed, outFile)
    digest["modelPinned"] = args.model if switched else None

    if args.json:
        print(json.dumps(digest, indent=2))
        return
    print(f"session:  {digest['sessionId']}")
    print(f"task:     {digest['taskName']}")
    print(f"models:   {', '.join(digest['models'])}")
    print(f"cost:     ${digest['costUsd']} in {digest['elapsedSeconds']}s")
    print(f"files:    {', '.join(digest['changedFiles']) or '(none changed)'}")
    print(f"raw:      {digest['rawJson']}")
    print(f"\n{digest['result']}")


if __name__ == "__main__":
    main()
