---
name: process-monitor
description: Monitor macOS system resources with auto-reminders. Use when user asks to monitor processes, check CPU/memory usage, find resource hogs, or wants periodic reminders to check system health. Responds to "[Auto-reminder] Check system resources" messages by analyzing current resource state.
---

# Process Monitor

Monitor macOS processes and system resources with optional auto-reminders.

## Quick Commands

Analyze current resources:
```bash
uv run python ~/.claude/skills/process-monitor/scripts/analyze.py
```

Get JSON output:
```bash
uv run python ~/.claude/skills/process-monitor/scripts/analyze.py --json
```

## Daemon Control

Start background monitoring (sends reminders every 5 min):
```bash
uv run python ~/.claude/skills/process-monitor/scripts/daemon.py start
```

Stop daemon:
```bash
uv run python ~/.claude/skills/process-monitor/scripts/daemon.py stop
```

Check status:
```bash
uv run python ~/.claude/skills/process-monitor/scripts/daemon.py status
```

## Responding to Auto-Reminders

When you see `[Auto-reminder] Check system resources`:

1. Run analyze.py to get current state
2. Report any processes using >50% CPU or >10% memory
3. Compare with previous if pattern seems abnormal
4. Suggest killing runaway processes if appropriate

## Manual Injection

Send a message to terminal (for testing):
```bash
uv run python ~/.claude/skills/process-monitor/scripts/inject_message.py "your message here"
```

## Files

- `~/.claude/process-monitor.pid` - Daemon PID
- `~/.claude/process-monitor.log` - Daemon log
- `~/.claude/process-monitor-snapshot.json` - Latest resource snapshot
