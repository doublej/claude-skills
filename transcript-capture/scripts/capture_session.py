#!/usr/bin/env python3
"""Capture Claude Code session transcript from JSONL session files."""

import json
import os
import sys
import argparse
from pathlib import Path



def get_session_dir(project_path: str | None = None) -> Path:
    if project_path:
        encoded = project_path.replace("/", "-")
        return Path.home() / ".claude" / "projects" / encoded
    # Try current working directory
    cwd = os.getcwd()
    encoded = cwd.replace("/", "-")
    candidates = [
        Path.home() / ".claude" / "projects" / encoded,
        Path.home() / ".claude" / "projects" / f"-{encoded.lstrip('-')}",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"No session dir found for {cwd}. Pass --project-path explicitly.")


def latest_session(session_dir: Path) -> Path:
    sessions = sorted(session_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not sessions:
        raise FileNotFoundError(f"No .jsonl files in {session_dir}")
    return sessions[0]


def extract_transcript(jsonl_path: Path, role_filter: str = "assistant") -> list[dict]:
    entries = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg = obj.get("message", obj)
            role = msg.get("role", "")
            if role_filter and role != role_filter:
                continue

            content = msg.get("content", [])
            if isinstance(content, str):
                entries.append({"role": role, "text": content, "ts": obj.get("timestamp", "")})
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "").strip()
                    if text:
                        entries.append({"role": role, "text": text, "ts": obj.get("timestamp", "")})
    return entries


def format_for_video(entries: list[dict], max_chars: int = 80) -> list[str]:
    """Trim and format entries for video overlay display."""
    lines = []
    for e in entries:
        text = e["text"]
        # Take first N chars, clean whitespace
        preview = " ".join(text.split())[:max_chars]
        if len(text) > max_chars:
            preview += "..."
        lines.append(f"[AI] {preview}")
    return lines


def main():
    parser = argparse.ArgumentParser(description="Capture Claude session transcript")
    parser.add_argument("--session", help="Specific .jsonl file path")
    parser.add_argument("--project-path", help="Project path (defaults to cwd)")
    parser.add_argument("--out", help="Output file (default: stdout)")
    parser.add_argument("--role", default="assistant", help="Role to filter (default: assistant)")
    parser.add_argument("--video-format", action="store_true", help="Format for video overlay")
    args = parser.parse_args()

    if args.session:
        jsonl_path = Path(args.session)
    else:
        session_dir = get_session_dir(args.project_path)
        jsonl_path = latest_session(session_dir)
        print(f"# Session: {jsonl_path.name}", file=sys.stderr)

    entries = extract_transcript(jsonl_path, role_filter=args.role)

    if args.video_format:
        lines = format_for_video(entries)
        output = "\n".join(lines)
    else:
        parts = []
        for e in entries:
            ts = e.get("ts", "")
            parts.append(f"[{e['role']}]{' @ ' + ts if ts else ''}\n{e['text']}\n")
        output = "\n---\n".join(parts)

    if args.out:
        Path(args.out).write_text(output)
        print(f"Wrote {len(entries)} entries to {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
