#!/usr/bin/env python3
"""Background analyzer for skill invocations.

Usage: analyzer.py <hook_payload_file>

Reads markers for the session, slices the transcript per skill invocation,
runs Sonnet via `claude -p` for each unanalyzed marker, parses findings,
and creates beads tickets in the claude-skills repo.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILLS_ROOT = SKILL_DIR.parent
MARKERS_DIR = SKILL_DIR / "state" / "markers"
ANALYZED_DIR = SKILL_DIR / "state" / "analyzed"
PROMPT_FILE = SKILL_DIR / "scripts" / "prompts" / "analyzer_prompt.md"
USAGE_LOG = SKILL_DIR / "state" / "token_usage.jsonl"

# Skills can live in three places; the analyzer resolves SKILL.md across all of them.
CLAUDE_SKILLS_DIR = Path.home() / ".claude" / "skills"
PLUGINS_DIR = Path.home() / ".claude" / "plugins"

ANALYZER_MODEL = "claude-sonnet-4-6"

# A transient Sonnet/CLI failure must not consume a marker — retry up to this many
# times across subsequent Stop events, then give up so a bad marker can't loop forever.
MAX_ATTEMPTS = 3
# Housekeeping: drop fully-analyzed marker files older than this so the dir stays small.
MARKER_TTL_DAYS = 30

SEVERITY_TO_PRIORITY = {"high": "1", "medium": "2", "low": "3"}
KIND_TO_BD_TYPE = {
    "bug": "bug",
    "disconnect": "feature",
    "improvement": "feature",
    "naming": "feature",
    "friction": "feature",
}


def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"[{ts}] {msg}", flush=True)


def notify(title: str, message: str) -> None:
    """Best-effort macOS notification. Never raises into the analyzer."""
    try:
        script = (
            f"display notification {json.dumps(message)} "
            f"with title {json.dumps(title)} sound name \"Tink\""
        )
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=10)
    except Exception as e:
        log(f"notify failed: {e}")


def load_payload(path: str) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def slice_transcript(transcript_path: str, since_ts: str) -> str:
    """Return lines from the transcript with timestamp >= since_ts."""
    if not transcript_path or not Path(transcript_path).exists():
        return ""
    lines = []
    with open(transcript_path, "r") as f:
        for raw in f:
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue
            ts = entry.get("timestamp") or entry.get("ts") or ""
            if ts >= since_ts:
                lines.append(raw.rstrip("\n"))
    return "\n".join(lines)


def find_skill_md(skill_name: str) -> Path | None:
    """Resolve a skill name to its SKILL.md across every install location.

    Searches the claude-skills repo, the global ~/.claude/skills dir, and plugin
    skill dirs. Namespaced names (``plugin:skill``) resolve on their suffix.
    Returns None for things that have no SKILL.md (e.g. slash-commands), which
    the caller skips quietly.
    """
    suffix = skill_name.split(":", 1)[1] if ":" in skill_name else skill_name
    for base in (SKILLS_ROOT, CLAUDE_SKILLS_DIR):
        for name in (skill_name, suffix):
            cand = base / name / "SKILL.md"
            if cand.exists():
                return cand
    # Plugin skills: ~/.claude/plugins/**/skills/<suffix>/SKILL.md
    for cand in PLUGINS_DIR.glob(f"**/skills/{suffix}/SKILL.md"):
        return cand
    return None


def log_token_usage(skill_name: str, session_id: str, result_obj: dict[str, Any]) -> None:
    """Append one token-usage record per Sonnet analyzer call. Append-only JSONL."""
    usage = result_obj.get("usage") or {}
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "skill": skill_name,
        "session_id": session_id,
        "model": ANALYZER_MODEL,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
        "cost_usd": result_obj.get("total_cost_usd"),
        "duration_ms": result_obj.get("duration_ms"),
    }
    try:
        USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError as e:
        log(f"Failed to write token usage: {e}")


def run_sonnet(skill_name: str, skill_md_text: str, transcript_slice: str, session_id: str) -> dict[str, Any]:
    """Invoke `claude -p` with Sonnet to analyze a single skill invocation.

    Uses --output-format json so token usage is captured (and logged) per call.
    """
    prompt_template = PROMPT_FILE.read_text()
    full_prompt = (
        f"{prompt_template}\n\n"
        f"---\n\n"
        f"## skill_name\n\n{skill_name}\n\n"
        f"## skill_md\n\n```markdown\n{skill_md_text}\n```\n\n"
        f"## transcript_slice\n\n```jsonl\n{transcript_slice}\n```\n"
    )

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(full_prompt)
        prompt_path = f.name

    try:
        # claude -p with file-based prompt via stdin to avoid shell-arg length limits
        proc = subprocess.run(
            [
                "claude",
                "-p",
                "--model", ANALYZER_MODEL,
                "--output-format", "json",
            ],
            stdin=open(prompt_path, "r"),
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(SKILLS_ROOT),
        )
    finally:
        os.unlink(prompt_path)

    if proc.returncode != 0:
        log(f"claude -p failed (rc={proc.returncode}): {proc.stderr[:500]}")
        return {"findings": [], "ok": False}

    # --output-format json emits an array of events; the final type=result object
    # carries both the model's text (result) and token usage.
    try:
        events = json.loads(proc.stdout)
    except json.JSONDecodeError:
        log(f"Could not parse claude -p envelope. Raw (first 500): {proc.stdout[:500]}")
        return {"findings": [], "ok": False}

    events = events if isinstance(events, list) else [events]
    result_obj = next(
        (e for e in reversed(events) if isinstance(e, dict) and e.get("type") == "result"),
        None,
    )
    if result_obj is None:
        log("No result event in claude -p output")
        return {"findings": [], "ok": False}

    log_token_usage(skill_name, session_id, result_obj)

    raw = (result_obj.get("result") or "").strip()
    # Strip markdown fences if Sonnet ignored instructions
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.endswith("```"):
            raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    result = _parse_findings(raw)
    if result is None:
        log(f"Could not parse Sonnet findings as JSON. Raw (first 500): {raw[:500]}")
        return {"findings": [], "ok": False}

    result["ok"] = True
    return result


def _parse_findings(raw: str) -> dict[str, Any] | None:
    """Parse the model's findings JSON. Falls back to extracting the first {...}
    object when the model wraps it in prose. Returns None if no valid object."""
    for candidate in (raw, _first_json_object(raw)):
        if not candidate:
            continue
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj.get("findings"), list):
            return obj
    return None


def _first_json_object(raw: str) -> str | None:
    start, end = raw.find("{"), raw.rfind("}")
    return raw[start : end + 1] if start != -1 and end > start else None


def existing_titles_for_skill(skill_name: str) -> set[str]:
    """Fetch open beads ticket titles labelled skill:<name> for dedup."""
    try:
        proc = subprocess.run(
            ["bd", "list", "--json", "--label", f"skill:{skill_name}"],
            capture_output=True, text=True, timeout=30, cwd=str(SKILLS_ROOT),
        )
        if proc.returncode != 0:
            return set()
        items = json.loads(proc.stdout)
        return {item.get("title", "") for item in items if item.get("status") in ("open", "ready", "in_progress")}
    except (subprocess.SubprocessError, json.JSONDecodeError):
        return set()


def create_beads_ticket(skill_name: str, finding: dict[str, Any]) -> str | None:
    """Run `bd create` for one finding. Returns ticket ID or None."""
    title = (finding.get("title") or "").strip()
    if not title:
        return None
    kind = finding.get("kind", "improvement")
    severity = finding.get("severity", "medium")
    evidence = finding.get("evidence", "")
    suggestion = finding.get("suggestion", "")

    bd_type = KIND_TO_BD_TYPE.get(kind, "feature")
    priority = SEVERITY_TO_PRIORITY.get(severity, "3")

    description = (
        f"**Skill:** `{skill_name}`\n"
        f"**Kind:** {kind} · **Severity:** {severity}\n\n"
        f"### Evidence\n{evidence}\n\n"
        f"### Suggestion\n{suggestion}\n"
    )

    labels = f"skill:{skill_name},source:auto-analysis,kind:{kind}"

    try:
        proc = subprocess.run(
            [
                "bd", "create", title,
                "-t", bd_type,
                "-p", priority,
                "-d", description,
                "-l", labels,
                "--silent",
            ],
            capture_output=True, text=True, timeout=30, cwd=str(SKILLS_ROOT),
        )
    except subprocess.SubprocessError as e:
        log(f"bd create failed: {e}")
        return None
    if proc.returncode != 0:
        log(f"bd create failed (rc={proc.returncode}): {proc.stderr[:300]}")
        return None
    return proc.stdout.strip()


def process_session(session_id: str) -> None:
    marker_path = MARKERS_DIR / f"{session_id}.jsonl"
    if not marker_path.exists():
        log(f"No marker file for session {session_id}")
        return

    ANALYZED_DIR.mkdir(parents=True, exist_ok=True)

    # Lock the marker file so concurrent analyzers don't double-process
    lock_path = ANALYZED_DIR / f"{session_id}.lock"
    with open(lock_path, "w") as lock_fp:
        try:
            fcntl.flock(lock_fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            log(f"Another analyzer already running for session {session_id}; skipping")
            return

        markers = []
        with open(marker_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    markers.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        unanalyzed = [m for m in markers if not m.get("analyzed")]
        if not unanalyzed:
            log(f"All markers already analyzed for {session_id}")
            return

        # Resolve up front: things with no SKILL.md (slash-commands, unknown names)
        # are skipped quietly so the notification reflects real analysis work only.
        resolved: list[tuple[dict[str, Any], Path]] = []
        for marker in unanalyzed:
            skill_md_path = find_skill_md(marker.get("skill", ""))
            if skill_md_path is None:
                log(f"Could not resolve SKILL.md for '{marker.get('skill', '')}' — skipping")
                marker["analyzed"] = True
                marker["skip_reason"] = "skill_not_found"
            else:
                resolved.append((marker, skill_md_path))

        if resolved:
            skills = ", ".join(sorted({m.get("skill", "?") for m, _ in resolved}))
            log(f"Analyzing {len(resolved)} marker(s) for session {session_id}")
            notify("Skill analysis started", f"{len(resolved)} invocation(s): {skills}")

        dedup_cache: dict[str, set[str]] = {}

        for marker, skill_md_path in resolved:
            skill_name = marker.get("skill", "")
            since_ts = marker.get("ts", "")
            transcript_path = marker.get("transcript_path", "")

            skill_md_text = skill_md_path.read_text()
            slice_text = slice_transcript(transcript_path, since_ts)
            if not slice_text.strip():
                log(f"Empty transcript slice for {skill_name} — skipping")
                marker["analyzed"] = True
                marker["skip_reason"] = "empty_slice"
                continue

            result = run_sonnet(skill_name, skill_md_text, slice_text, session_id)
            if not result.get("ok"):
                attempts = marker.get("attempts", 0) + 1
                marker["attempts"] = attempts
                if attempts >= MAX_ATTEMPTS:
                    marker["analyzed"] = True
                    marker["skip_reason"] = "max_retries"
                    log(f"  {skill_name}: analysis failed {attempts}x — giving up")
                else:
                    log(f"  {skill_name}: analysis failed (attempt {attempts}/{MAX_ATTEMPTS}) — will retry")
                continue

            findings = result.get("findings", [])
            log(f"  {skill_name}: {len(findings)} finding(s)")

            if skill_name not in dedup_cache:
                dedup_cache[skill_name] = existing_titles_for_skill(skill_name)

            created_ids = []
            for finding in findings:
                title = (finding.get("title") or "").strip()
                if not title or title in dedup_cache[skill_name]:
                    continue
                tid = create_beads_ticket(skill_name, finding)
                if tid:
                    created_ids.append(tid)
                    dedup_cache[skill_name].add(title)

            marker["analyzed"] = True
            marker["tickets_created"] = created_ids

        # Atomic rewrite of marker file
        tmp_path = marker_path.with_suffix(".jsonl.tmp")
        with open(tmp_path, "w") as f:
            for m in markers:
                f.write(json.dumps(m) + "\n")
        shutil.move(str(tmp_path), str(marker_path))
        log(f"Done with session {session_id}")


def prune_old_markers() -> None:
    """Delete fully-analyzed marker files (and their locks) older than the TTL.
    Best-effort housekeeping; never raises into the analyzer."""
    cutoff = time.time() - MARKER_TTL_DAYS * 86400
    for mf in MARKERS_DIR.glob("*.jsonl"):
        try:
            if mf.stat().st_mtime >= cutoff:
                continue
            lines = [ln for ln in mf.read_text().splitlines() if ln.strip()]
            if any(not json.loads(ln).get("analyzed", False) for ln in lines):
                continue
            mf.unlink(missing_ok=True)
            (ANALYZED_DIR / f"{mf.stem}.lock").unlink(missing_ok=True)
        except (OSError, json.JSONDecodeError):
            continue


def main() -> int:
    if len(sys.argv) < 2:
        log("Usage: analyzer.py <payload_file>")
        return 1
    payload_path = sys.argv[1]
    try:
        payload = load_payload(payload_path)
    except Exception as e:
        log(f"Failed to load payload: {e}")
        return 1
    finally:
        try:
            os.unlink(payload_path)
        except OSError:
            pass

    session_id = payload.get("session_id", "")
    if not session_id:
        log("No session_id in payload")
        return 1

    try:
        process_session(session_id)
    except Exception as e:
        log(f"process_session failed: {e}")
        return 1
    finally:
        prune_old_markers()
    return 0


if __name__ == "__main__":
    sys.exit(main())
