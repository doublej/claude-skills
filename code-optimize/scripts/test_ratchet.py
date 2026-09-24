#!/usr/bin/env python3
"""Self-check for ratchet.py: ceilings only go down, and a raised count is caught."""

from ratchet import lower, violations

base = {"smells": {"ceiling": 10}, "perf:send": {"cmd": "echo 5"}}

after = lower(base, {"smells": 7, "perf:send": 5, "logging": 40, "arch": None})
assert after["smells"]["ceiling"] == 7, "lower drops the ceiling"
assert after["perf:send"] == {"cmd": "echo 5", "ceiling": 5}, "custom entry without ceiling gets one, keeps cmd"
assert after["logging"]["ceiling"] == 40, "new dimension starts at its count"
assert "arch" not in after, "unmeasurable count is skipped"
assert base["smells"]["ceiling"] == 10, "input baseline is not mutated"

assert lower(after, {"smells": 12})["smells"]["ceiling"] == 7, "lower never raises"

assert violations(after, {"smells": 8, "logging": 40}) == {"smells": {"count": 8, "ceiling": 7}}
assert violations(after, {"smells": 7, "arch": None, "new": 99}) == {}, "equal, unmeasured, and unknown are not violations"

print("ratchet self-check: ok")
