---
name: proc
description: "Scan, monitor, and kill macOS processes: kill orphaned MCP servers, dev servers, and Claude Code processes to free ports; find CPU/memory hogs; run a background monitor daemon with periodic health reminders. Use for any process cleanup or resource-usage question — 'what's eating my CPU', 'kill everything on port 3000', 'clean up stale MCP servers', 'free up port 5173', 'monitor system resources', 'why is my Mac slow'. Replaces proc-cleanup and proc-monitor."
---

# Process Management (scan / monitor / kill)

Scan, monitor, and kill processes on macOS: stale Claude Code processes, orphaned MCP servers, dev servers, port squatters, and CPU/memory hogs. Optional background daemon sends periodic health reminders.

All scripts are in `~/.claude/skills/proc/scripts/`. Process enumeration lives in one place: `scan.py` — the kill scripts get their PIDs from it.

<scan>
## Scan

```bash
python3 ~/.claude/skills/proc/scripts/scan.py            # Claude, MCP, dev servers, top CPU hogs
python3 ~/.claude/skills/proc/scripts/scan.py --ports    # + listeners on common dev ports
python3 ~/.claude/skills/proc/scripts/scan.py --system   # + system CPU overview and hog alerts (>50% CPU, >10% MEM)
python3 ~/.claude/skills/proc/scripts/scan.py --json     # structured output (combines with any flags)
python3 ~/.claude/skills/proc/scripts/scan.py --system --cached   # use daemon's latest snapshot instead of live data
python3 ~/.claude/skills/proc/scripts/scan.py --pids mcp          # PIDs only for a category: claude|mcp|dev|port:<N>
```
</scan>

<kill>
## Kill

By PID (SIGTERM with 3s grace, then SIGKILL):
```bash
bash ~/.claude/skills/proc/scripts/kill.sh <pid> [pid...]
bash ~/.claude/skills/proc/scripts/kill.sh --force <pid> [pid...]   # immediate SIGKILL
```

By category (enumerates via `scan.py --pids`):
```bash
bash ~/.claude/skills/proc/scripts/kill-category.sh claude      # all Claude Code procs
bash ~/.claude/skills/proc/scripts/kill-category.sh mcp         # all MCP servers
bash ~/.claude/skills/proc/scripts/kill-category.sh dev         # all dev servers
bash ~/.claude/skills/proc/scripts/kill-category.sh port:3000   # everything listening on port 3000
```

Add `--force` for immediate SIGKILL.
</kill>

<monitor>
## Monitor Daemon

Background monitoring: saves a resource snapshot and sends a reminder to the configured iTerm tab every 5 minutes.

```bash
python3 ~/.claude/skills/proc/scripts/daemon.py start      # start in background
python3 ~/.claude/skills/proc/scripts/daemon.py stop
python3 ~/.claude/skills/proc/scripts/daemon.py status
python3 ~/.claude/skills/proc/scripts/daemon.py snapshot   # one-off snapshot, prints JSON
python3 ~/.claude/skills/proc/scripts/daemon.py target <tab-name>   # which iTerm tab gets reminders
python3 ~/.claude/skills/proc/scripts/daemon.py list       # list iTerm session names
```

Manual message injection into a terminal (for testing):
```bash
python3 ~/.claude/skills/proc/scripts/inject_message.py "your message here"
```
</monitor>

<responding>
## Responding to Auto-Reminders

When you see `[Auto-reminder] Check system resources`:

1. Run `scan.py --system` to get current state
2. Report any processes using >50% CPU or >10% memory
3. Compare with previous snapshot (`--cached`) if pattern seems abnormal
4. Suggest killing runaway processes if appropriate
</responding>

<workflow>
## Cleanup Workflow

1. Run `scan.py` to see what's running
2. Present findings to user with PID, CPU%, MEM%, and command
3. Use `consult-user-mcp` `ask` (type `pick`, `multi: true`) to let user select which processes/categories to kill — never kill without confirmation
4. Run `kill.sh` or `kill-category.sh` as directed
5. Run `scan.py` again to confirm cleanup
</workflow>

<safety>
- **Always confirm** before killing. Show the user what will die.
- Prefer category kills (`claude`, `mcp`, `dev`) over blanket cleanup.
- `Claude.app` (desktop) is excluded from Claude process matching.
- SIGTERM first (3s grace), SIGKILL only as fallback or with `--force`.
</safety>

<files>
Runtime artifacts:
- `~/.claude/proc-monitor.pid` - daemon PID
- `~/.claude/proc-monitor.log` - daemon log
- `~/.claude/proc-monitor-snapshot.json` - latest resource snapshot
- `~/.claude/proc-monitor-target.txt` - iTerm tab name for reminders

Legacy `~/.claude/process-monitor.*` files (pre-rename) are migrated automatically: on startup, daemon.py and scan.py rename any old file to its new name if the new one doesn't exist yet.
</files>
