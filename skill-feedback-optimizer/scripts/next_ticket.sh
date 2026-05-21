#!/usr/bin/env bash
# Pick the next ticket to work from the auto-analysis backlog.
# Prints JSON: {id, title, description, skill, kind, severity} or {} if none.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_ROOT="$(dirname "$SKILL_DIR")"

cd "$SKILLS_ROOT"

# bd ready returns issues whose deps are satisfied and status is open
# Filter by source:auto-analysis label and sort by priority (asc, 1=highest)
bd ready --json --label source:auto-analysis 2>/dev/null \
  | python3 -c "
import json, sys
try:
    items = json.load(sys.stdin)
except Exception:
    items = []
if not isinstance(items, list) or not items:
    print('{}')
    sys.exit(0)
items.sort(key=lambda x: (int(x.get('priority', 99)), x.get('id', '')))
top = items[0]
labels = top.get('labels') or []
def first_with_prefix(prefix):
    for l in labels:
        if l.startswith(prefix):
            return l.split(':', 1)[1] if ':' in l else ''
    return ''
out = {
    'id':          top.get('id', ''),
    'title':       top.get('title', ''),
    'description': top.get('description', '') or top.get('body', ''),
    'priority':    top.get('priority', ''),
    'type':        top.get('issue_type', '') or top.get('type', ''),
    'skill':       first_with_prefix('skill:'),
    'kind':        first_with_prefix('kind:'),
}
print(json.dumps(out))
"
