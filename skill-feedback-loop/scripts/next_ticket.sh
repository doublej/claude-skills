#!/usr/bin/env bash
# Pick the next ticket to work from the auto-analysis backlog.
# Prints JSON: {id, title, description, priority, type, skill, kind, created_at,
#               possibly_stale, skill_commits_since_report} or {} if none.
#
# Date-awareness: the collector analyzes transcripts from an *earlier* moment than
# when the ticket is filed, so a fix can already have shipped before created_at.
# We surface commits touching the skill from a margin before created_at onward so
# the optimizer can reconcile against git history before applying a redundant fix.

set -euo pipefail

# pwd -P resolves the ~/.claude/skills/skill-feedback-loop symlink to the repo dir
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
SKILLS_ROOT="$(dirname "$SKILL_DIR")"

cd "$SKILLS_ROOT"

# How far before created_at to look for an already-shipped fix (collector lag margin).
STALE_LOOKBACK_HOURS="${STALE_LOOKBACK_HOURS:-24}"

# bd ready returns issues whose deps are satisfied and status is open.
# Filter by source:auto-analysis label; sort by priority (asc, 1=highest) then oldest first.
bd ready --json --label source:auto-analysis 2>/dev/null \
  | SKILLS_ROOT="$SKILLS_ROOT" STALE_LOOKBACK_HOURS="$STALE_LOOKBACK_HOURS" python3 -c '
import json, sys, os, subprocess
from datetime import datetime, timedelta

SKILLS_ROOT = os.environ["SKILLS_ROOT"]
LOOKBACK_H = int(os.environ.get("STALE_LOOKBACK_HOURS", "24"))

try:
    items = json.load(sys.stdin)
except Exception:
    items = []
if not isinstance(items, list) or not items:
    print("{}")
    sys.exit(0)

# Highest priority first, then oldest report first (date-aware tiebreak).
items.sort(key=lambda x: (int(x.get("priority", 99)), x.get("created_at", ""), x.get("id", "")))
top = items[0]
labels = top.get("labels") or []

def first_with_prefix(prefix):
    for l in labels:
        if l.startswith(prefix):
            return l.split(":", 1)[1] if ":" in l else ""
    return ""

skill = first_with_prefix("skill:")
created_at = top.get("created_at", "") or ""

# Commits touching the skill from (created_at - lookback) onward.
commits_since = []
possibly_stale = False
if skill and created_at:
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        cutoff = (dt - timedelta(hours=LOOKBACK_H)).strftime("%Y-%m-%dT%H:%M:%S%z")
        proc = subprocess.run(
            ["git", "log", "--since", cutoff, "--format=%h\t%cI\t%s", "--", f"{skill}/"],
            capture_output=True, text=True, cwd=SKILLS_ROOT, timeout=15,
        )
        for line in proc.stdout.strip().splitlines():
            parts = line.split("\t", 2)
            if len(parts) == 3:
                commits_since.append({"sha": parts[0], "date": parts[1], "subject": parts[2]})
        possibly_stale = bool(commits_since)
    except Exception:
        pass

out = {
    "id":          top.get("id", ""),
    "title":       top.get("title", ""),
    "description": top.get("description", "") or top.get("body", ""),
    "priority":    top.get("priority", ""),
    "type":        top.get("issue_type", "") or top.get("type", ""),
    "skill":       skill,
    "kind":        first_with_prefix("kind:"),
    "created_at":  created_at,
    "possibly_stale": possibly_stale,
    "skill_commits_since_report": commits_since,
}
print(json.dumps(out))
'
