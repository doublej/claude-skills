#!/usr/bin/env python3
"""
Process monitor daemon - runs in background, monitors system resources,
and triggers reminders to Claude Code terminal.
"""

import subprocess
import time
import json
import os
import signal
import sys
from pathlib import Path
from datetime import datetime

INTERVAL_SECONDS = 300  # 5 minutes
PID_FILE = Path.home() / ".claude" / "process-monitor.pid"
LOG_FILE = Path.home() / ".claude" / "process-monitor.log"
SNAPSHOT_FILE = Path.home() / ".claude" / "process-monitor-snapshot.json"
TARGET_TAB_FILE = Path.home() / ".claude" / "process-monitor-target.txt"


def parse_float(s):
    """Parse float handling locale (comma vs dot decimal separator)."""
    return float(s.replace(",", "."))


def get_top_processes(limit=10):
    """Get top processes by CPU and memory usage."""
    result = subprocess.run(
        ["ps", "-Acro", "pid,pcpu,pmem,comm"],
        capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")[1:]  # Skip header

    processes = []
    for line in lines[:limit]:
        parts = line.split()
        if len(parts) >= 4:
            processes.append({
                "pid": parts[0],
                "cpu": parse_float(parts[1]),
                "mem": parse_float(parts[2]),
                "name": " ".join(parts[3:])
            })
    return processes


def get_system_stats():
    """Get overall system resource usage."""
    # CPU usage via top (snapshot)
    top_result = subprocess.run(
        ["top", "-l", "1", "-n", "0", "-s", "0"],
        capture_output=True, text=True
    )

    cpu_idle = 0.0
    mem_used = 0
    mem_total = 0

    for line in top_result.stdout.split("\n"):
        if "CPU usage" in line:
            # Parse: CPU usage: 5.26% user, 10.52% sys, 84.21% idle
            parts = line.split(",")
            for part in parts:
                if "idle" in part:
                    cpu_idle = parse_float(part.strip().split("%")[0].split()[-1])
        elif "PhysMem" in line:
            # Parse: PhysMem: 16G used (2048M wired), 123M unused.
            parts = line.replace("PhysMem:", "").split(",")
            for part in parts:
                part = part.strip()
                if "used" in part:
                    val = part.split()[0]
                    if "G" in val:
                        mem_used = int(float(val.replace("G", "")) * 1024)
                    elif "M" in val:
                        mem_used = int(val.replace("M", ""))
                elif "unused" in part:
                    val = part.split()[0]
                    if "G" in val:
                        mem_total = mem_used + int(float(val.replace("G", "")) * 1024)
                    elif "M" in val:
                        mem_total = mem_used + int(val.replace("M", ""))

    return {
        "cpu_usage": round(100 - cpu_idle, 1),
        "mem_used_mb": mem_used,
        "mem_total_mb": mem_total if mem_total > 0 else mem_used,
        "timestamp": datetime.now().isoformat()
    }


def save_snapshot():
    """Save current resource snapshot to file."""
    snapshot = {
        "system": get_system_stats(),
        "top_processes": get_top_processes(10)
    }

    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshot, f, indent=2)

    return snapshot


def send_reminder():
    """Send reminder to specific iTerm tab by name."""
    message = f"[Auto-reminder] Check system resources - {datetime.now().strftime('%H:%M')}"

    # Get target tab name
    if not TARGET_TAB_FILE.exists():
        log("No target tab configured")
        return

    target_name = TARGET_TAB_FILE.read_text().strip()

    # Find tab by name and inject message
    script = f'''
    tell application "iTerm"
        repeat with w in windows
            repeat with t in tabs of w
                repeat with s in sessions of t
                    if name of s contains "{target_name}" then
                        tell s to write text "{message}"
                        return
                    end if
                end repeat
            end repeat
        end repeat
    end tell
    '''

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        log(f"AppleScript error: {result.stderr}")


def log(msg):
    """Log message to file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {msg}\n")


def cleanup(signum=None, frame=None):
    """Cleanup on exit."""
    if PID_FILE.exists():
        PID_FILE.unlink()
    log("Daemon stopped")
    sys.exit(0)


def is_running():
    """Check if daemon is already running."""
    if not PID_FILE.exists():
        return False

    pid = int(PID_FILE.read_text().strip())
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        PID_FILE.unlink()
        return False


def start_daemon():
    """Start the daemon in background."""
    if is_running():
        print("Daemon already running")
        return

    # Fork to background
    pid = os.fork()
    if pid > 0:
        print(f"Daemon started with PID {pid}")
        return

    # Child process
    os.setsid()

    # Write PID file
    PID_FILE.write_text(str(os.getpid()))

    # Setup signal handlers
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    log("Daemon started")

    while True:
        try:
            snapshot = save_snapshot()
            log(f"Snapshot saved - CPU: {snapshot['system']['cpu_usage']}%, MEM: {snapshot['system']['mem_used_mb']}MB")
            send_reminder()
        except Exception as e:
            log(f"Error: {e}")

        time.sleep(INTERVAL_SECONDS)


def stop_daemon():
    """Stop the running daemon."""
    if not PID_FILE.exists():
        print("Daemon not running")
        return

    pid = int(PID_FILE.read_text().strip())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Stopped daemon (PID {pid})")
    except OSError:
        print("Daemon not running")
        PID_FILE.unlink()


def status():
    """Check daemon status."""
    if is_running():
        pid = int(PID_FILE.read_text().strip())
        print(f"Daemon running (PID {pid})")
    else:
        print("Daemon not running")


def set_target(tab_name):
    """Set target tab name for reminders."""
    TARGET_TAB_FILE.write_text(tab_name)
    print(f"Target tab set to: {tab_name}")


def list_tabs():
    """List all iTerm tab/session names."""
    script = '''
    tell application "iTerm"
        set output to ""
        repeat with w in windows
            repeat with t in tabs of w
                repeat with s in sessions of t
                    set output to output & (name of s) & "\n"
                end repeat
            end repeat
        end repeat
        return output
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode == 0:
        print("Available iTerm sessions:")
        for line in result.stdout.strip().split("\n"):
            if line:
                print(f"  - {line}")
    else:
        print(f"Error: {result.stderr}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process monitor daemon")
    parser.add_argument("command", choices=["start", "stop", "status", "snapshot", "target", "list"],
                       help="Command to execute")
    parser.add_argument("value", nargs="?", help="Tab name for 'target' command")

    args = parser.parse_args()

    if args.command == "start":
        start_daemon()
    elif args.command == "stop":
        stop_daemon()
    elif args.command == "status":
        status()
    elif args.command == "snapshot":
        snapshot = save_snapshot()
        print(json.dumps(snapshot, indent=2))
    elif args.command == "target":
        if args.value:
            set_target(args.value)
        elif TARGET_TAB_FILE.exists():
            print(f"Current target: {TARGET_TAB_FILE.read_text().strip()}")
        else:
            print("No target set. Use: daemon.py target <tab-name>")
    elif args.command == "list":
        list_tabs()
