#!/usr/bin/env python3
"""Self-check for catchup_digest. Run: python3 test_catchup_digest.py"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import catchup_digest as C  # noqa: E402


def msg(kind: str, text: str, minute: int) -> dict:
    return {
        "type": kind,
        "uuid": f"u{minute}",
        "sessionId": "s",
        "timestamp": f"2026-01-01T00:{minute:02d}:00Z",
        "message": {"content": text},
    }


def test_goal_tail_and_ending() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        sf = Path(tmp) / "abc.jsonl"
        sf.write_text(
            "\n".join(
                json.dumps(e)
                for e in [
                    msg("user", "<system-reminder>noise</system-reminder>", 0),
                    msg("user", "Build the thing", 1),
                    msg("assistant", "Built it.", 2),
                    msg("user", "Now ship it", 3),
                ]
            )
        )
        d = C.digest_session(sf, tmp, tail=2, clip_at=5)
        assert d["goal"] == "Build …", d["goal"]  # first real prompt, noise skipped, clipped
        assert d["user_messages"] == 2
        assert d["ended_on"] == "user"  # last prompt never answered
        assert [m["type"] for m in d["tail"]] == ["assistant", "user"]
        assert d["resume"].endswith("claude --resume abc")


def test_noise_only_session_dropped() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        sf = Path(tmp) / "n.jsonl"
        sf.write_text(json.dumps(msg("user", "<command-name>/clear", 0)))
        assert C.digest_session(sf, tmp, tail=6, clip_at=700) is None


if __name__ == "__main__":
    test_goal_tail_and_ending()
    test_noise_only_session_dropped()
    print("ok")
