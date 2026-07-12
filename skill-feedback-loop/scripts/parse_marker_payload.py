#!/usr/bin/env python3
"""Read a Claude Code hook payload from stdin, emit tab-separated fields:
session_id, transcript_path, skill_name, cwd."""

import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 1
    session_id = payload.get("session_id", "") or ""
    transcript_path = payload.get("transcript_path", "") or ""
    cwd = payload.get("cwd", "") or ""
    tool_input = payload.get("tool_input") or {}
    skill_name = tool_input.get("skill", "") or ""
    print(f"{session_id}\t{transcript_path}\t{skill_name}\t{cwd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
