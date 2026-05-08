#!/bin/bash
# Pretty-print the current Browser Router rules sorted by priority.
# Read-only; never edits config.yaml.

set -euo pipefail

CONFIG="$HOME/Library/Application Support/Browser Router/config.yaml"

if [ ! -f "$CONFIG" ]; then
    echo "config.yaml not found at: $CONFIG"
    exit 1
fi

python3 - "$CONFIG" <<'PY'
import re, sys

path = sys.argv[1]
text = open(path).read()

# Hand-rolled parser to match the app's two-space-indent grammar without
# requiring PyYAML. We only extract the keys we care about.

def parse_rules(block):
    rules = []
    cur = None
    in_port = False
    for raw in block.splitlines():
        if not raw.strip():
            continue
        # New rule starts with "  - id:"
        m = re.match(r'^  - id: "?([^"]+)"?\s*$', raw)
        if m:
            if cur is not None:
                rules.append(cur)
            cur = {"id": m.group(1)}
            in_port = False
            continue
        if cur is None:
            continue
        if re.match(r'^    portRange:\s*$', raw):
            in_port = True
            cur["portRange"] = {}
            continue
        if in_port:
            m = re.match(r'^      (start|end): (\d+)\s*$', raw)
            if m:
                cur["portRange"][m.group(1)] = int(m.group(2))
                continue
            in_port = False
        m = re.match(r'^    (\w+): (.*)$', raw)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        elif v in ("true", "false"):
            v = (v == "true")
        elif v.lstrip("-").isdigit():
            v = int(v)
        cur[k] = v
    if cur is not None:
        rules.append(cur)
    return rules

# Extract the rules: section.
m = re.search(r'^rules:\s*$([\s\S]*?)(?=^\S|\Z)', text, re.MULTILINE)
if not m or "- id:" not in m.group(1):
    print("No rules.")
    sys.exit(0)

rules = parse_rules(m.group(1))
rules.sort(key=lambda r: r.get("priority", 999))

# Routing enabled flag.
re_flag = re.search(r'^routingEnabled:\s*(true|false)\s*$', text, re.MULTILINE)
flag = re_flag.group(1) if re_flag else "?"
print(f"routingEnabled: {flag}\n")

# Header.
header = ("PRI", "PATTERN", "MATCH", "BROWSER", "PROFILE", "PORT", "ON", "ASK")
widths = [3, 28, 8, 36, 12, 11, 3, 3]
def fmt(row):
    return "  ".join(str(c).ljust(w) for c, w in zip(row, widths))
print(fmt(header))
print(fmt(["-" * w for w in widths]))

for r in rules:
    pri = r.get("priority", "?")
    pattern = r.get("pattern", "")
    mt = r.get("matchType", "")
    browser = r.get("browserID", "") or "(prompt)"
    profile = r.get("profileID", "")
    pr = r.get("portRange")
    if pr and "start" in pr and "end" in pr:
        port = f"{pr['start']}-{pr['end']}" if pr["start"] != pr["end"] else str(pr["start"])
    else:
        port = ""
    enabled = "yes" if r.get("enabled", True) else "no"
    ask = "yes" if r.get("promptUser", False) else ""
    print(fmt([pri, pattern, mt, browser, profile, port, enabled, ask]))
PY
