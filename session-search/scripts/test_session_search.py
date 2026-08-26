#!/usr/bin/env python3
"""Self-check for session_search parsing rules. Run: python3 test_session_search.py"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import session_search as S  # noqa: E402

SCRIPT = Path(__file__).parent / "session_search.py"


def write_session(path: Path, entries: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(e) for e in entries))


def test_tool_use_is_searchable() -> None:
    """A phrase written inside a Write tool_use body must be findable (bd-1qg)."""
    with tempfile.TemporaryDirectory() as tmp:
        sf = Path(tmp) / "s.jsonl"
        write_session(sf, [{
            "type": "assistant", "uuid": "u1", "sessionId": "s",
            "timestamp": "2026-01-01T00:00:00Z",
            "message": {"content": [
                {"type": "text", "text": "Writing the file."},
                {"type": "tool_use", "name": "Write", "id": "t1",
                 "input": {"file_path": "/tmp/a.md", "content": "the magic phrase here"}},
            ]},
        }])

        plain = S.extract_messages(sf)
        assert "magic phrase" not in plain[0]["content"], "content must stay text-only"
        assert "tool_text" not in plain[0], "tool_text must be opt-in"

        withtools = S.extract_messages(sf, include_tool_text=True)
        assert "the magic phrase here" in withtools[0]["tool_text"]

        # A tool-only message (no text block) must still be emitted.
        write_session(sf, [{
            "type": "assistant", "uuid": "u2", "sessionId": "s",
            "timestamp": "2026-01-01T00:01:00Z",
            "message": {"content": [
                {"type": "tool_use", "name": "Bash", "id": "t2",
                 "input": {"command": "echo needle"}},
            ]},
        }])
        assert S.extract_messages(sf) == [], "tool-only message has no text content"
        only = S.extract_messages(sf, include_tool_text=True)
        assert len(only) == 1 and "needle" in only[0]["tool_text"]


def test_preview_anchors_on_match() -> None:
    regex = re.compile("needle", re.IGNORECASE)
    assert "needle" in S.preview_at_match("x" * 500 + "needle" + "y" * 500, regex)
    slim = S.slim_match(
        {"timestamp": "t", "type": "assistant", "session_id": "s",
         "content": "", "tool_text": "z" * 300 + "needle"},
        regex, in_tool=True,
    )
    assert slim["matched_in"] == "tool_use" and "needle" in slim["preview"]


def test_stale_index_does_not_hide_sessions() -> None:
    """A sessions-index.json pointing at vanished files must not zero out a
    project whose *.jsonl are on disk (bd-270l)."""
    with tempfile.TemporaryDirectory() as tmp:
        pdir = Path(tmp)
        real = pdir / "real.jsonl"
        real.write_text("")
        proj = {
            "project_dir": pdir,
            "project_path": "/p",
            "session_entries": [{"fullPath": str(pdir / "gone.jsonl"), "fileMtime": 0}],
        }
        found = [p.name for p in S.iter_sessions_for_project(proj)]
        assert found == ["real.jsonl"], found

        # A live index entry must not be yielded twice by the disk fallback.
        proj["session_entries"] = [{"fullPath": str(real), "fileMtime": 0}]
        assert [p.name for p in S.iter_sessions_for_project(proj)] == ["real.jsonl"]

        # agent-*.jsonl stay excluded from the fallback scan.
        (pdir / "agent-a1.jsonl").write_text("")
        proj["session_entries"] = None
        assert [p.name for p in S.iter_sessions_for_project(proj)] == ["real.jsonl"]


def test_dash_prefixed_query_needs_separator() -> None:
    """`--` lets a phrase starting with dashes through argparse (bd-ap45)."""
    bad = subprocess.run(
        [sys.executable, str(SCRIPT), "search", "--allow-live", "--only"],
        capture_output=True, text=True,
    )
    assert bad.returncode == 2 and "error:" in bad.stderr, bad.stderr

    # `--` ends flag parsing, so scope flags must come BEFORE it — everything
    # after is a query term. Reaching the scope check proves the dashed phrases
    # arrived as query terms rather than as flags.
    good = subprocess.run(
        [sys.executable, str(SCRIPT), "search", "-p", "/nonexistent-project-xyz",
         "--", "--allow-live", "--only"],
        capture_output=True, text=True,
    )
    assert good.stderr == "", good.stderr
    assert "No projects found for scope" in good.stdout, good.stdout

    # Flags placed after `--` are swallowed as query terms, not honoured.
    swallowed = subprocess.run(
        [sys.executable, str(SCRIPT), "search", "--", "--allow-live",
         "-p", "/nonexistent-project-xyz"],
        capture_output=True, text=True,
    )
    assert "No projects found for scope" not in swallowed.stdout, swallowed.stdout


def test_noise_prefixes() -> None:
    for noisy in ("<agent-message from=x>hi", "<task-notification>x",
                  "Stop hook feedback: x", "<command-message>x"):
        assert S.is_system_noise(noisy), noisy
    assert not S.is_system_noise("please fix the serif fallback")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all checks passed")
