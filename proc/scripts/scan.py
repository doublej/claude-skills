#!/usr/bin/env python3
"""Unified process scanner for macOS.

Enumerates Claude Code processes, MCP servers, and dev servers; optionally
port listeners, system CPU/memory overview, and resource-hog alerts.
Single source of truth for process enumeration — kill-category.sh gets its
PIDs from `scan.py --pids <category>`.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SNAPSHOT_FILE = Path.home() / ".claude" / "proc-monitor-snapshot.json"
LEGACY_SNAPSHOT_FILE = Path.home() / ".claude" / "process-monitor-snapshot.json"

DEV_PORTS = [3000, 3001, 4173, 5173, 5174, 8000, 8080, 8888, 9000, 4200, 4321]

CATEGORY_PATTERNS = {
    "claude": re.compile(r"claude", re.IGNORECASE),
    "mcp": re.compile(r"mcp-server|mcp_server|mcp-server\.cjs"),
    "dev": re.compile(
        r"node.*dev|vite|next.*dev|nuxt|uvicorn|fastapi|gunicorn|flask.*run"
        r"|python.*http\.server|live-server|webpack.*dev|turbo.*dev"
        r"|bun.*dev|deno.*serve"
    ),
}

# Exclusions applied to the "claude" category (and self-matches everywhere)
CLAUDE_EXCLUDE = re.compile(r"Claude\.app")
SELF_EXCLUDE = re.compile(r"scan\.py|grep")


def migrate_legacy_snapshot():
    """One-time migration: rename old process-monitor-* snapshot to proc-monitor-*."""
    if LEGACY_SNAPSHOT_FILE.exists() and not SNAPSHOT_FILE.exists():
        LEGACY_SNAPSHOT_FILE.rename(SNAPSHOT_FILE)


def parse_float(s):
    """Parse float handling locale (comma vs dot decimal separator)."""
    return float(s.replace(",", "."))


def list_processes():
    """Return all processes as dicts: pid, cpu, mem, cmd."""
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    procs = []
    own_pid = str(os.getpid())
    for line in result.stdout.strip().split("\n")[1:]:
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        pid, cpu, mem, cmd = parts[1], parts[2], parts[3], parts[10]
        if pid == own_pid or SELF_EXCLUDE.search(cmd):
            continue
        procs.append({"pid": int(pid), "cpu": cpu, "mem": mem, "cmd": cmd})
    return procs


def match_category(category, procs=None):
    """Return processes matching a category (claude|mcp|dev)."""
    if procs is None:
        procs = list_processes()
    pattern = CATEGORY_PATTERNS[category]
    matched = [p for p in procs if pattern.search(p["cmd"])]
    if category == "claude":
        matched = [p for p in matched if not CLAUDE_EXCLUDE.search(p["cmd"])]
    return matched


def port_pids(port):
    """Return PIDs listening on a TCP port."""
    result = subprocess.run(
        ["lsof", f"-iTCP:{port}", "-sTCP:LISTEN", "-P", "-n", "-t"],
        capture_output=True, text=True,
    )
    return sorted({int(pid) for pid in result.stdout.split() if pid.isdigit()})


def port_listeners():
    """Return listeners on common dev ports: port, pid, name."""
    listeners = []
    seen = set()
    for port in DEV_PORTS:
        result = subprocess.run(
            ["lsof", f"-iTCP:{port}", "-sTCP:LISTEN", "-P", "-n"],
            capture_output=True, text=True,
        )
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) < 9:
                continue
            key = (port, parts[1])
            if key in seen:
                continue
            seen.add(key)
            listeners.append({"port": port, "pid": int(parts[1]), "name": parts[0]})
    return listeners


def resource_hogs(procs, limit=10):
    """Top processes by CPU."""
    def cpu_key(p):
        try:
            return parse_float(p["cpu"])
        except ValueError:
            return 0.0
    return sorted(procs, key=cpu_key, reverse=True)[:limit]


def get_system_snapshot():
    """Live system snapshot: overall CPU + top processes (by CPU)."""
    ps_result = subprocess.run(
        ["ps", "-Acro", "pid,pcpu,pmem,comm"],
        capture_output=True, text=True,
    )
    processes = []
    for line in ps_result.stdout.strip().split("\n")[1:15]:
        parts = line.split()
        if len(parts) >= 4:
            processes.append({
                "pid": parts[0],
                "cpu": parse_float(parts[1]),
                "mem": parse_float(parts[2]),
                "name": " ".join(parts[3:]),
            })

    top_result = subprocess.run(
        ["top", "-l", "1", "-n", "0", "-s", "0"],
        capture_output=True, text=True,
    )
    cpu_user = cpu_sys = cpu_idle = 0.0
    for line in top_result.stdout.split("\n"):
        if "CPU usage" in line:
            for part in line.split(","):
                if "user" in part:
                    cpu_user = parse_float(part.strip().split("%")[0].split()[-1])
                elif "sys" in part:
                    cpu_sys = parse_float(part.strip().split("%")[0].split()[-1])
                elif "idle" in part:
                    cpu_idle = parse_float(part.strip().split("%")[0].split()[-1])

    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": {
            "user": cpu_user,
            "system": cpu_sys,
            "idle": cpu_idle,
            "total_used": round(cpu_user + cpu_sys, 1),
        },
        "top_processes": processes,
    }


def get_cached_snapshot():
    """Read the daemon's latest snapshot and normalize to live-snapshot shape."""
    with open(SNAPSHOT_FILE) as f:
        snapshot = json.load(f)
    return {
        "timestamp": snapshot["system"]["timestamp"],
        "cpu": {
            "total_used": snapshot["system"]["cpu_usage"],
            "user": snapshot["system"]["cpu_usage"],
            "system": 0,
            "idle": 100 - snapshot["system"]["cpu_usage"],
        },
        "top_processes": snapshot["top_processes"],
    }


def system_alerts(snapshot):
    """Resource hogs from a system snapshot: >50% CPU or >10% memory."""
    cpu_hogs = [p for p in snapshot["top_processes"] if p["cpu"] > 50]
    mem_hogs = [p for p in snapshot["top_processes"] if p["mem"] > 10]
    return cpu_hogs, mem_hogs


def print_proc_section(title, procs):
    print(f"=== {title} ===")
    if procs:
        for p in procs:
            print(f"  PID {p['pid']:<7} CPU: {p['cpu']:>5}%  MEM: {p['mem']:>5}%  {p['cmd']}")
    else:
        print("  (none)")
    print()


def print_system_section(snapshot):
    print(f"=== System @ {snapshot['timestamp'][:19]} ===")
    cpu = snapshot["cpu"]
    print(f"  CPU: {cpu['total_used']}% used ({cpu['user']}% user, {cpu['system']}% sys)")
    print()
    print("  Top Processes by CPU:")
    for i, proc in enumerate(snapshot["top_processes"][:10], 1):
        print(f"  {i:2}. {proc['name'][:25]:<25} CPU: {proc['cpu']:5.1f}%  MEM: {proc['mem']:5.1f}%")
    cpu_hogs, mem_hogs = system_alerts(snapshot)
    if cpu_hogs or mem_hogs:
        print()
        print("  Alerts:")
        for p in cpu_hogs:
            print(f"  - HIGH CPU: {p['name']} using {p['cpu']}%")
        for p in mem_hogs:
            print(f"  - HIGH MEM: {p['name']} using {p['mem']}%")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Scan macOS for Claude/MCP/dev-server processes and resource usage"
    )
    parser.add_argument("--json", action="store_true", help="Structured JSON output")
    parser.add_argument("--ports", action="store_true",
                        help="Include listeners on common dev ports")
    parser.add_argument("--system", action="store_true",
                        help="Include system CPU overview and hog alerts")
    parser.add_argument("--cached", action="store_true",
                        help="With --system: use the daemon's latest snapshot instead of live data")
    parser.add_argument("--pids", metavar="CATEGORY",
                        help="Print only PIDs for a category (claude|mcp|dev|port:<N>), one per line")
    args = parser.parse_args()

    migrate_legacy_snapshot()

    if args.pids:
        category = args.pids
        if category.startswith("port:"):
            pids = port_pids(int(category.split(":", 1)[1]))
        elif category in CATEGORY_PATTERNS:
            pids = [p["pid"] for p in match_category(category)]
        else:
            print(f"Unknown category: {category} (valid: claude, mcp, dev, port:<N>)",
                  file=sys.stderr)
            sys.exit(1)
        for pid in pids:
            print(pid)
        return

    procs = list_processes()
    result = {
        "claude": match_category("claude", procs),
        "mcp_servers": match_category("mcp", procs),
        "dev_servers": match_category("dev", procs),
        "top_cpu": resource_hogs(procs),
    }
    if args.ports:
        result["port_listeners"] = port_listeners()
    if args.system:
        if args.cached and SNAPSHOT_FILE.exists():
            result["system"] = get_cached_snapshot()
        else:
            result["system"] = get_system_snapshot()

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print_proc_section("Claude Code Processes", result["claude"])
    print_proc_section("MCP Servers", result["mcp_servers"])
    print_proc_section("Dev Servers", result["dev_servers"])
    if args.ports:
        print("=== Port Listeners (dev ports) ===")
        if result["port_listeners"]:
            for l in result["port_listeners"]:
                print(f"  PID {l['pid']:<7} :{l['port']} → {l['name']}")
        else:
            print("  (none)")
        print()
    print_proc_section("Top CPU Hogs", result["top_cpu"])
    if args.system:
        print_system_section(result["system"])


if __name__ == "__main__":
    main()
