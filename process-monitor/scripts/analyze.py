#!/usr/bin/env python3
"""
Analyze system resources and provide actionable insights.
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

SNAPSHOT_FILE = Path.home() / ".claude" / "process-monitor-snapshot.json"


def parse_float(s):
    """Parse float handling locale (comma vs dot decimal separator)."""
    return float(s.replace(",", "."))


def get_live_snapshot():
    """Get live system snapshot."""
    # Top CPU processes
    ps_result = subprocess.run(
        ["ps", "-Acro", "pid,pcpu,pmem,comm"],
        capture_output=True, text=True
    )

    processes = []
    for line in ps_result.stdout.strip().split("\n")[1:15]:
        parts = line.split()
        if len(parts) >= 4:
            processes.append({
                "pid": parts[0],
                "cpu": parse_float(parts[1]),
                "mem": parse_float(parts[2]),
                "name": " ".join(parts[3:])
            })

    # System overview
    top_result = subprocess.run(
        ["top", "-l", "1", "-n", "0", "-s", "0"],
        capture_output=True, text=True
    )

    cpu_user = cpu_sys = cpu_idle = 0.0
    mem_used = mem_wired = mem_unused = 0

    for line in top_result.stdout.split("\n"):
        if "CPU usage" in line:
            parts = line.split(",")
            for part in parts:
                if "user" in part:
                    cpu_user = parse_float(part.strip().split("%")[0].split()[-1])
                elif "sys" in part:
                    cpu_sys = parse_float(part.strip().split("%")[0].split()[-1])
                elif "idle" in part:
                    cpu_idle = parse_float(part.strip().split("%")[0].split()[-1])
        elif "PhysMem" in line:
            # Parse memory
            pass

    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": {
            "user": cpu_user,
            "system": cpu_sys,
            "idle": cpu_idle,
            "total_used": round(cpu_user + cpu_sys, 1)
        },
        "top_processes": processes
    }


def format_report(snapshot):
    """Format snapshot as readable report."""
    lines = [
        f"System Resources @ {snapshot['timestamp'][:19]}",
        f"{'='*45}",
        f"CPU: {snapshot['cpu']['total_used']}% used ({snapshot['cpu']['user']}% user, {snapshot['cpu']['system']}% sys)",
        "",
        "Top Processes by CPU:",
    ]

    for i, proc in enumerate(snapshot["top_processes"][:10], 1):
        lines.append(f"  {i:2}. {proc['name'][:25]:<25} CPU: {proc['cpu']:5.1f}%  MEM: {proc['mem']:5.1f}%")

    # Find resource hogs
    cpu_hogs = [p for p in snapshot["top_processes"] if p["cpu"] > 50]
    mem_hogs = [p for p in snapshot["top_processes"] if p["mem"] > 10]

    if cpu_hogs or mem_hogs:
        lines.append("")
        lines.append("Alerts:")
        for p in cpu_hogs:
            lines.append(f"  - HIGH CPU: {p['name']} using {p['cpu']}%")
        for p in mem_hogs:
            lines.append(f"  - HIGH MEM: {p['name']} using {p['mem']}%")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Analyze system resources")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--cached", action="store_true", help="Use cached snapshot")

    args = parser.parse_args()

    if args.cached and SNAPSHOT_FILE.exists():
        with open(SNAPSHOT_FILE) as f:
            snapshot = json.load(f)
        # Convert to expected format
        snapshot = {
            "timestamp": snapshot["system"]["timestamp"],
            "cpu": {
                "total_used": snapshot["system"]["cpu_usage"],
                "user": snapshot["system"]["cpu_usage"],
                "system": 0,
                "idle": 100 - snapshot["system"]["cpu_usage"]
            },
            "top_processes": snapshot["top_processes"]
        }
    else:
        snapshot = get_live_snapshot()

    if args.json:
        print(json.dumps(snapshot, indent=2))
    else:
        print(format_report(snapshot))


if __name__ == "__main__":
    main()
