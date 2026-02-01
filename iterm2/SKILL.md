---
name: iterm2
description: >-
  Manage iTerm2 via Python API - create/close tabs, split panes, send text, read output,
  manage profiles, key bindings, arrangements, and color presets. Use when organizing
  terminal workspace, automating iTerm2 layouts, or controlling terminal sessions.
---

# iTerm2 Terminal Management

Control iTerm2 programmatically via the Python API.

## Prerequisites

- iTerm2 with Python API enabled (Settings > General > Magic > Enable Python API)
- Run setup once: `bash {{SKILL_DIR}}/scripts/setup.sh`

## Runner

Use the wrapper script directly — no function definition needed:

```bash
ITERM2="{{SKILL_DIR}}/scripts/iterm2"

"$ITERM2" list-windows
"$ITERM2" split-and-run --title "Test" "echo hello"
```

> **Always store the path in `ITERM2` and call `"$ITERM2" <command>`.** Do NOT define an inline bash function with `{ }` — it breaks in zsh when chained with `&&` or pipes.

## Commands

### Discovery

| Command | Description |
|---------|-------------|
| `list-windows` | JSON of all windows, tabs, sessions (IDs, titles, paths, grid sizes) |
| `list-profiles` | Available profiles with GUIDs |
| `list-arrangements` | Saved window arrangements |
| `get-key-mappings` | Key bindings for current session's profile |
| `find-self` | Find this agent's own iTerm2 session by TTY matching |

### Window/Tab/Pane Management

| Command | Description |
|---------|-------------|
| `new-window [profile]` | Create window (optional profile name) |
| `new-tab [profile]` | Create tab in current window |
| `split-h [profile]` | Split current session horizontally |
| `split-v [profile]` | Split current session vertically |
| `focus-tab <id>` | Activate tab by ID (from list-windows) |
| `focus-session <id>` | Activate session by ID |
| `close-tab <id>` | Close tab (force, no confirmation) |
| `close-session <id>` | Close session (force) |
| `set-title <title>` | Set current tab's title |

### Terminal I/O

| Command | Description |
|---------|-------------|
| `send [--session ID] <text>` | Send text to a session (default: current) |
| `read [--session ID] [lines]` | Read terminal screen (default: current, 50 lines) |
| `ctrl [--session ID] <char>` | Send control character (e.g., `C` for Ctrl-C, **`M` for Enter**) |
| `run [--session ID] <cmd> [--wait N]` | Send command + Enter, wait N seconds (default 2), read non-blank output |
| `split-and-run [options] <cmd>` | Split pane next to self, run command, return session ID + output |

### Session targeting with `--session`

> **Critical**: after `split-v`/`split-h`, the new pane gets a session ID but `send`/`read`/`ctrl` without `--session` still target the **original** pane (Claude Code's session). You MUST use `--session <id>` to target the new pane.

```bash
# split-v returns the new session ID — capture it
"$ITERM2" split-v                              # → {"session_id": "ABC-123..."}
"$ITERM2" send --session "ABC-123..." "echo hi" # targets the new pane
"$ITERM2" ctrl --session "ABC-123..." "M"       # sends Enter to the new pane
```

### Submitting commands

> **`\n` does NOT submit commands.** Bash double-quotes pass `\n` as two literal characters, not a newline. **`ctrl ""` crashes** (empty string is not a character).

Always use: `ctrl "M"` (Ctrl-M = carriage return = Enter).

```bash
"$ITERM2" send --session "$SID" "cd ~/project && npm run dev"
"$ITERM2" ctrl --session "$SID" "M"
```

### Verifying output

After sending a command, always `read` to verify it executed. Use a **high line count** (e.g., 200) because screen content sits at the top with blank lines below.

```bash
sleep 1
"$ITERM2" read --session "$SID" 200 | grep -v '^$'
```

### Profiles & Appearance

| Command | Description |
|---------|-------------|
| `set-colors <preset>` | Apply color preset to current session |
| `set-font-size <size> [--profile name]` | Set font size on all profiles + open sessions (or specific profile) |

### Arrangements

| Command | Description |
|---------|-------------|
| `save-arrangement <name>` | Save current layout |
| `restore-arrangement <name>` | Restore saved layout |

## Key Mapping Format

Key codes are `"0x<keycode>-0x<modifiers>"`. Modifier bitmask:

| Modifier | Hex |
|----------|-----|
| Shift | `0x20000` |
| Control | `0x40000` |
| Option | `0x80000` |
| Command | `0x100000` |

Action codes: 0=next tab, 10=escape seq, 11=hex code, 12=send text, 13=ignore,
25=menu item, 26=new window, 27=new tab, 28/29=split h/v, 60=invoke script, 63=snippet.

### `split-and-run` options

| Option | Description |
|--------|-------------|
| `--direction h\|v` | Split direction (default: `v` vertical) |
| `--session ID` | Source session to split (default: auto-detect via `find-self`) |
| `--title <title>` | Set tab title for the new pane |
| `--wait N` | Seconds to wait before reading output (default: 2) |

## Default workflow: iTerm2 pane + tmux (see tmux skill)

When asked to "open a pane" or "run something next to this session", **always** combine iTerm2 (visibility) with tmux (reliability). Use `split-and-run` for one-call setup:

```bash
# One-liner: split next to this agent, start tmux, get session ID
"$ITERM2" split-and-run --title "Dev Server" "tmux new -s dev-server"

# All further commands go through tmux (reliable, no focus issues)
tmux send-keys -t dev-server:0.0 -l -- 'cd ~/project && npm run dev'
tmux send-keys -t dev-server:0.0 Enter
```

Or use the tmux skill's `tmux-init.sh` which does this entire workflow automatically (see tmux skill).

## Workflow: Quick split (no tmux)

For simple, non-interactive commands where tmux is overkill:

```bash
# One call: splits next to agent, runs command, returns output
"$ITERM2" split-and-run --title "Logs" "tail -f /var/log/app.log"

# Or use run for an existing session:
"$ITERM2" run --session "$SID" "echo hello" --wait 1
```

## Workflow: Workspace with saved layout

```bash
"$ITERM2" list-windows
"$ITERM2" new-tab
"$ITERM2" set-title "Tests"
"$ITERM2" save-arrangement "my-project"
```

## Remote Windows Hosts (SSH/SCP)

When working with Windows machines over SSH:

### SCP path gotcha

`scp` to Windows absolute paths **always fails** — the `C:` colon is parsed as a host separator:

```bash
# BROKEN — all of these fail:
scp file.txt user@host:"C:/Projects/foo/file.txt"
scp file.txt user@host:"C:\\Projects\\foo\\file.txt"

# WORKS — scp to home dir, then move via SSH:
scp file.txt user@host:file.txt
ssh user@host "move file.txt C:\\Projects\\foo\\file.txt"
```

### Writing file content directly

For small files, skip scp entirely and write via SSH stdin:

```bash
ssh user@host "cmd /c \"copy con C:\\Projects\\foo\\file.txt\"" < local-file.txt
# Or use PowerShell:
cat local-file.txt | ssh user@host "powershell -c \"[IO.File]::WriteAllText('C:\\Projects\\foo\\file.txt', \$input)\""
```

### Windows path rules in SSH commands

- Use **backslashes** inside `cmd /c` commands: `C:\\Projects\\foo`
- Use **forward slashes** inside PowerShell: `C:/Projects/foo`
- Always double-escape backslashes in bash strings

## Error Handling

All commands output JSON. Errors include `{"error": "message"}`.
Connection failures mean iTerm2 isn't running or Python API is disabled.
