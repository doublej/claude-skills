#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["fastapi", "uvicorn"]
# ///
"""Live observability dashboard for the iphone-mirroring skill.

Watches /tmp/iphone-mirror/run-*/ and serves an auto-refreshing HTML page
showing every step's capture, OmniParser overlay, decision, and action.

  uv run scripts/dashboard.py        # binds 127.0.0.1:8766
  open http://127.0.0.1:8766
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

ROOT = Path(os.environ.get("IPHONE_MIRROR_DIR", "/tmp/iphone-mirror"))

app = FastAPI(title="iphone-mirroring dashboard")


def _runs() -> list[Path]:
    if not ROOT.exists():
        return []
    return sorted([p for p in ROOT.glob("run-*") if p.is_dir()], reverse=True)


def _steps(run: Path) -> list[dict]:
    out: list[dict] = []
    for step_dir in sorted(run.glob("step-*")):
        decision_path = step_dir / "decision.json"
        elements_path = step_dir / "elements.json"
        decision = json.loads(decision_path.read_text()) if decision_path.exists() else None
        elements_count = None
        if elements_path.exists():
            try:
                elements_count = len(json.loads(elements_path.read_text()))
            except Exception:
                pass
        out.append({
            "name": step_dir.name,
            "capture": (step_dir / "capture.png").exists(),
            "annotated": (step_dir / "annotated.png").exists(),
            "elements_count": elements_count,
            "decision": decision,
        })
    return out


@app.get("/api/state")
def state() -> JSONResponse:
    runs = _runs()
    if not runs:
        return JSONResponse({"runs": [], "active": None})
    active = runs[0]
    goal = (active / "goal.txt").read_text().strip() if (active / "goal.txt").exists() else ""
    return JSONResponse({
        "runs": [r.name for r in runs],
        "active": {
            "name": active.name,
            "goal": goal,
            "steps": _steps(active),
        },
    })


@app.get("/api/run/{run_name}")
def run_detail(run_name: str) -> JSONResponse:
    run = ROOT / run_name
    if not run.is_dir():
        raise HTTPException(404)
    goal = (run / "goal.txt").read_text().strip() if (run / "goal.txt").exists() else ""
    return JSONResponse({"name": run.name, "goal": goal, "steps": _steps(run)})


@app.get("/file/{run_name}/{step_name}/{filename}")
def file(run_name: str, step_name: str, filename: str) -> FileResponse:
    p = ROOT / run_name / step_name / filename
    if not p.is_file():
        raise HTTPException(404)
    return FileResponse(p)


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>iphone-mirroring</title>
<style>
:root { color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: #0b0d10; color: #e6e8eb; font: 13px/1.5 ui-monospace, SFMono-Regular, monospace; }
header { position: sticky; top: 0; z-index: 10; padding: 12px 20px; background: #11141a; border-bottom: 1px solid #222; display: flex; gap: 16px; align-items: baseline; }
header h1 { margin: 0; font-size: 14px; font-weight: 600; letter-spacing: 0.5px; }
header .goal { color: #9aa3b2; }
header .run { margin-left: auto; color: #6b7280; }
.steps { padding: 16px 20px 80px; display: flex; flex-direction: column; gap: 16px; }
.step { background: #11141a; border: 1px solid #1f242c; border-radius: 8px; padding: 12px; }
.step h2 { margin: 0 0 8px; font-size: 12px; color: #9aa3b2; font-weight: 500; display: flex; gap: 12px; align-items: center; }
.step h2 .badge { padding: 1px 6px; border-radius: 4px; background: #1f2937; color: #93c5fd; font-size: 11px; }
.step h2 .badge.done { background: #064e3b; color: #6ee7b7; }
.step h2 .badge.error { background: #4c1d24; color: #fca5a5; }
.row { display: grid; grid-template-columns: 220px 220px 1fr; gap: 12px; align-items: start; }
.row figure { margin: 0; background: #0b0d10; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; }
.row figure img { width: 100%; max-height: 380px; object-fit: contain; display: block; background: #000; }
.row figure figcaption { padding: 4px 8px; font-size: 11px; color: #6b7280; }
pre { margin: 0; background: #0b0d10; border-radius: 6px; padding: 8px 10px; font-size: 11px; max-height: 380px; overflow: auto; white-space: pre-wrap; word-break: break-word; }
.empty { padding: 60px 20px; color: #6b7280; text-align: center; }
.dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #34d399; margin-right: 6px; animation: pulse 1s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: 1 } 50% { opacity: 0.3 } }
</style>
</head>
<body>
<header>
  <h1><span class="dot"></span>iphone-mirroring</h1>
  <span class="goal" id="goal">…</span>
  <span class="run" id="run"></span>
</header>
<div id="root" class="steps"><div class="empty">waiting for first run…</div></div>
<script>
let lastSig = "";
async function tick() {
  try {
    const r = await fetch("/api/state");
    const s = await r.json();
    if (!s.active) {
      document.getElementById("goal").textContent = "no runs yet";
      document.getElementById("run").textContent = "";
      return;
    }
    document.getElementById("goal").textContent = s.active.goal || "(no goal)";
    document.getElementById("run").textContent = s.active.name;
    const sig = JSON.stringify(s.active.steps.map(x => [x.name, !!x.decision, x.elements_count]));
    if (sig === lastSig) return;
    lastSig = sig;
    const root = document.getElementById("root");
    root.innerHTML = "";
    if (s.active.steps.length === 0) {
      root.innerHTML = '<div class="empty">run started, waiting for first capture…</div>';
      return;
    }
    for (const st of s.active.steps.slice().reverse()) {
      const d = st.decision || {};
      const action = d.action || "…";
      const cls = action === "done" ? "done" : action === "error" ? "error" : "";
      const div = document.createElement("div");
      div.className = "step";
      const cap = st.capture ? `/file/${s.active.name}/${st.name}/capture.png` : "";
      const ann = st.annotated ? `/file/${s.active.name}/${st.name}/annotated.png` : "";
      const decisionPretty = st.decision ? JSON.stringify(st.decision, null, 2) : "(awaiting…)";
      div.innerHTML = `
        <h2>
          <span>${st.name}</span>
          <span class="badge ${cls}">${action}${d.element_id !== undefined ? " #" + d.element_id : ""}</span>
          <span style="color:#6b7280">elements: ${st.elements_count ?? "?"}</span>
          ${d.confidence !== undefined ? `<span style="color:#6b7280">conf: ${d.confidence}</span>` : ""}
        </h2>
        <div class="row">
          ${cap ? `<figure><img src="${cap}?t=${Date.now()}" loading="lazy"><figcaption>capture</figcaption></figure>` : "<div></div>"}
          ${ann ? `<figure><img src="${ann}?t=${Date.now()}" loading="lazy"><figcaption>omniparser overlay</figcaption></figure>` : "<div></div>"}
          <pre>${escapeHtml(decisionPretty)}</pre>
        </div>
      `;
      root.appendChild(div);
    }
  } catch (e) { console.error(e); }
}
function escapeHtml(s) { return s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"})[c]); }
tick();
setInterval(tick, 1000);
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(INDEX)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8766)
    args = ap.parse_args()
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
