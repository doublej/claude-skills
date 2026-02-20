---
name: iterm2
description: >-
  Manage iTerm2 via it2 CLI - create/close tabs, split panes, send text, read output,
  manage profiles, arrangements, and appearance. Use when organizing terminal workspace,
  automating iTerm2 layouts, or controlling terminal sessions.
---

# iTerm2 Terminal Management

Control iTerm2 via the `it2` CLI.

## Prerequisites

- iTerm2 with Python API enabled (Settings > General > Magic > Enable Python API)
- `it2` installed (`pip install it2` or `uv tool install it2`)

## Commands

### Discovery

| Command | Description |
|---------|-------------|
| `it2 window list --json` | JSON of all windows with IDs |
| `it2 session list --json` | JSON of all sessions with IDs |
| `it2 tab list` | List all tabs |
| `it2 profile list` | Available profiles |
| `it2 window arrange list` | Saved window arrangements |
| `it2 app get-focus` | Currently focused window/tab/session |

### Window/Tab/Pane Management

| Command | Description |
|---------|-------------|
| `it2 new [-p profile] [-c cmd]` | Create window (shortcut for `window new`) |
| `it2 newtab [-p profile] [-c cmd] [-w window]` | Create tab (shortcut for `tab new`) |
| `it2 split [-s ID] [-p profile]` | Split horizontally (shortcut for `session split`) |
| `it2 vsplit [-s ID] [-p profile]` | Split vertically (shortcut for `session split -v`) |
| `it2 tab select <id>` | Activate tab by ID or index |
| `it2 session focus <id>` | Activate session by ID |
| `it2 tab close [-f] [id]` | Close tab (use `-f` to force) |
| `it2 session close [-f] [-s ID]` | Close session (use `-f` to force) |
| `it2 session set-name [-s ID] <name>` | Set session name |

### Terminal I/O

| Command | Description |
|---------|-------------|
| `it2 send [-s ID] <text>` | Send text **without** newline |
| `it2 run [-s ID] <cmd>` | Send command **with** newline (executes it) |
| `it2 session read [-s ID] [-n lines]` | Read terminal screen |
| `it2 session capture [-s ID] -o file [--history]` | Capture screen to file |
| `it2 session clear [-s ID]` | Clear screen |

### Session targeting with `-s`

> **Critical**: after `split`/`vsplit`, the new pane gets a session ID but `send`/`read` without `-s` still target the **active** session. You MUST use `-s <id>` to target the new pane.

```bash
# vsplit returns the new session ID — capture it
SID=$(it2 vsplit 2>&1 | grep -oE '[A-F0-9-]{36}')
it2 run -s "$SID" "echo hello"
```

### Submitting commands

Use `it2 run` — it appends a newline automatically:

```bash
it2 run -s "$SID" "cd ~/project && npm run dev"
```

For text without Enter (e.g., partial input), use `it2 send`:

```bash
it2 send -s "$SID" "partial text"
```

### Sending control characters

`it2 send` accepts raw bytes via bash `$'...'` syntax:

```bash
it2 send -s "$SID" $'\x03'   # Ctrl-C (interrupt)
it2 send -s "$SID" $'\x04'   # Ctrl-D (EOF)
it2 send -s "$SID" $'\x1a'   # Ctrl-Z (suspend)
it2 send -s "$SID" $'\x0c'   # Ctrl-L (clear)
```

### Verifying output

After sending a command, always `read` to verify. Use a high line count because screen content sits at the top with blank lines below.

```bash
sleep 1
it2 session read -s "$SID" -n 200
```

### Profiles & Appearance

| Command | Description |
|---------|-------------|
| `it2 app theme [light\|dark\|automatic\|minimal]` | Show or set theme |
| `it2 profile set <name> font-size <size>` | Set font size |
| `it2 profile set <name> font-family <family>` | Set font family |
| `it2 profile set <name> bg-color <hex>` | Set background colour |
| `it2 profile set <name> fg-color <hex>` | Set foreground colour |
| `it2 profile set <name> transparency <0.0-1.0>` | Set transparency |
| `it2 profile set <name> cursor-color <hex>` | Set cursor colour |
| `it2 profile apply <name>` | Apply profile to current session |
| `it2 load <name>` | Load custom profile from config |

### Arrangements

| Command | Description |
|---------|-------------|
| `it2 window arrange save <name>` | Save current layout |
| `it2 window arrange restore <name>` | Restore saved layout |
| `it2 window arrange list` | List saved arrangements |

### Window Positioning

| Command | Description |
|---------|-------------|
| `it2 window move <x> <y> [window_id]` | Move window |
| `it2 window resize <w> <h> [window_id]` | Resize window |
| `it2 window fullscreen` | Toggle fullscreen |
| `it2 tab move [tab_id]` | Move tab to its own window |

### Broadcasting

| Command | Description |
|---------|-------------|
| `it2 app broadcast on` | Broadcast input to all sessions in current tab |
| `it2 app broadcast off` | Disable broadcasting |
| `it2 app broadcast add` | Create broadcast group with specific sessions |

### Monitoring

| Command | Description |
|---------|-------------|
| `it2 monitor activity` | Monitor session activity |
| `it2 monitor output` | Monitor session output |
| `it2 monitor prompt` | Monitor shell prompts (requires shell integration) |
| `it2 monitor keystroke` | Monitor keystrokes |
| `it2 monitor variable` | Monitor variable changes |

### Session Variables

| Command | Description |
|---------|-------------|
| `it2 session get-var [-s ID] <var>` | Get session variable |
| `it2 session set-var [-s ID] <var> <val>` | Set session variable |

## Default workflow: iTerm2 pane + tmux (see tmux skill)

When asked to "open a pane" or "run something next to this session", combine iTerm2 (visibility) with tmux (reliability):

```bash
# Split, capture new session ID, start tmux
SID=$(it2 vsplit 2>&1 | grep -oE '[A-F0-9-]{36}')
it2 run -s "$SID" "tmux new -s dev-server"

# All further commands go through tmux (reliable, no focus issues)
tmux send-keys -t dev-server:0.0 -l -- 'cd ~/project && npm run dev'
tmux send-keys -t dev-server:0.0 Enter
```

Or use the tmux skill's `tmux-init.sh` which does this workflow automatically.

## Workflow: Quick split (no tmux)

For simple, non-interactive commands where tmux is overkill:

```bash
# Split and run a command
SID=$(it2 vsplit 2>&1 | grep -oE '[A-F0-9-]{36}')
it2 run -s "$SID" "tail -f /var/log/app.log"

# Or run in an existing session:
it2 run -s "$SID" "echo hello"
```

## Workflow: Workspace with saved layout

```bash
it2 window list --json
it2 newtab
it2 session set-name "Tests"
it2 window arrange save "my-project"
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
