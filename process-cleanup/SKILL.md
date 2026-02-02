---
name: process-cleanup
description: Clean up Claude Code, orphaned MCP servers, and dev server processes to free system resources. Use when system is slow, ports are occupied, or user asks to kill stale processes.
---

# Process Cleanup

Scan and kill stale Claude Code processes, orphaned MCP servers, and development servers on macOS.

## Scripts

All scripts are in `~/.claude/skills/process-cleanup/scripts/`.

### Scan

```bash
bash ~/.claude/skills/process-cleanup/scripts/scan.sh           # overview
bash ~/.claude/skills/process-cleanup/scripts/scan.sh --ports    # include port listeners
bash ~/.claude/skills/process-cleanup/scripts/scan.sh --json     # structured output
```

Shows: Claude processes, MCP servers, dev servers, top CPU hogs.

### Kill by PID

```bash
bash ~/.claude/skills/process-cleanup/scripts/kill.sh <pid> [pid...]        # SIGTERM → SIGKILL
bash ~/.claude/skills/process-cleanup/scripts/kill.sh --force <pid> [pid...]  # immediate SIGKILL
```

### Kill by Category

```bash
bash ~/.claude/skills/process-cleanup/scripts/kill-category.sh claude        # all Claude Code procs
bash ~/.claude/skills/process-cleanup/scripts/kill-category.sh mcp           # all MCP servers
bash ~/.claude/skills/process-cleanup/scripts/kill-category.sh dev           # all dev servers
bash ~/.claude/skills/process-cleanup/scripts/kill-category.sh port:3000     # everything on port 3000
```

Add `--force` for immediate SIGKILL.

## Workflow

1. Run `scan.sh` to see what's running
2. Present findings to user with PID, CPU%, MEM%, and command
3. Ask which processes/categories to kill (never kill without confirmation)
4. Run `kill.sh` or `kill-category.sh` as directed
5. Run `scan.sh` again to confirm cleanup

## Safety

- **Always confirm** before killing. Show the user what will die.
- Prefer category kills (`claude`, `mcp`, `dev`) over blanket cleanup.
- `Claude.app` (desktop) is excluded from Claude process matching.
- SIGTERM first (3s grace), SIGKILL only as fallback or with `--force`.
