#!/usr/bin/env python3
"""Summarize the collector's token spend from state/token_usage.jsonl.

Usage: token_report.py            # all-time totals + per-skill breakdown
       token_report.py --since 2026-05-01   # only records on/after a date
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

USAGE_LOG = Path(__file__).resolve().parent.parent / "state" / "token_usage.jsonl"
TOKEN_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
)


def load_records(since: str) -> list[dict]:
    if not USAGE_LOG.exists():
        return []
    out = []
    for line in USAGE_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if since and (rec.get("ts", "") < since):
            continue
        out.append(rec)
    return out


def totals(records: list[dict]) -> tuple[collections.Counter, float]:
    tok = collections.Counter()
    cost = 0.0
    for r in records:
        for field in TOKEN_FIELDS:
            tok[field] += r.get(field) or 0
        cost += r.get("cost_usd") or 0.0
    return tok, cost


def fmt(tok: collections.Counter, cost: float, calls: int) -> str:
    return (
        f"{calls:>4} calls  in={tok['input_tokens']:>8}  out={tok['output_tokens']:>7}  "
        f"cache_w={tok['cache_creation_input_tokens']:>9}  cache_r={tok['cache_read_input_tokens']:>9}  "
        f"${cost:.4f}"
    )


def main() -> int:
    since = ""
    if "--since" in sys.argv:
        i = sys.argv.index("--since")
        since = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""

    records = load_records(since)
    if not records:
        print("No token usage logged yet.")
        return 0

    by_skill: dict[str, list[dict]] = collections.defaultdict(list)
    for r in records:
        by_skill[r.get("skill", "?")].append(r)

    print(f"== Collector token spend{f' since {since}' if since else ''} ==\n")
    for skill in sorted(by_skill, key=lambda s: -totals(by_skill[s])[1]):
        tok, cost = totals(by_skill[skill])
        print(f"  {skill:<28} {fmt(tok, cost, len(by_skill[skill]))}")

    tok, cost = totals(records)
    print("\n  " + "-" * 100)
    print(f"  {'TOTAL':<28} {fmt(tok, cost, len(records))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
