#!/usr/bin/env python3
"""Print one line per distinct viewport state the device reported."""
import json, sys

rows, seen = [], set()
for line in open(sys.argv[1] if len(sys.argv) > 1 else "reports.jsonl"):
    d = json.loads(line)
    w, s, v, i = d["window"], d["screen"], d["viewportUnits"], d["safeAreaInsets"]
    key = (w["innerWidth"], w["innerHeight"], tuple(i.values()))
    if key in seen:
        continue
    seen.add(key)
    rows.append((d["tag"], s["orientationType"], w["innerWidth"], w["innerHeight"], s["dpr"],
                 v["vh"], v["svh"], v["lvh"], v["dvh"],
                 i["top"], i["right"], i["bottom"], i["left"],
                 "standalone" if d["displayMode"]["standalone"] else "browser"))

hdr = ("tag", "orientation", "w", "h", "dpr", "vh", "svh", "lvh", "dvh",
       "sa-t", "sa-r", "sa-b", "sa-l", "mode")
fmt = "{:<16}{:<20}{:>6}{:>6}{:>5}{:>7}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}  {}"
print(fmt.format(*hdr))
for r in rows:
    print(fmt.format(*[str(x) for x in r]))
