---
name: iterm2
description: "Manage iTerm2 via it2 CLI - create/close tabs, split panes,
  send text, read output, manage profiles, arrangements, and appearance.
  Use when organizing terminal workspace, automating iTerm2 layouts, or
  controlling terminal sessions. Triggers on 'iterm2', 'it2', 'split a
  pane', 'open a pane next to this session'."
---

# iTerm2 Terminal Management

Control iTerm2 via the `it2` CLI.

Shared driver discipline (send vs run, capture-after-settle, explicit pane targeting — with the it2/tmux/cmux command table): see `~/.claude/skills/tmux/references/terminal-driver-core.md`.

<prerequisites>
- iTerm2 with Python API enabled (Settings > General > Magic > Enable Python API)
- `it2` installed (`pip install it2` or `uv tool install it2`)
</prerequisites>

<commands>
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
| `it2 newtab [-p profile] [-c cmd] [-w window]` | Create tab (shortcut for `tab new`) — prints a **tab number**, not a session ID |
| `it2 split [-s ID] [-p profile]` | Split horizontally (shortcut for `session split`) |
| `it2 vsplit [-s ID] [-p profile]` | Split vertically (shortcut for `session split -v`) |
| `it2 tab select <id>` | Activate tab by ID or index |
| `it2 session focus <id>` | Activate session by ID |
| `it2 tab close [-f] [id]` | Close tab (use `-f` to force) |
| `it2 session close [-f] [-s ID]` | Close session (use `-f` to force) |
| `it2 session set-name [-s ID] <name>` | Set session name |

> `it2 tab move` moves a tab to its **own new window** — it does not reorder tabs. The CLI has no reorder command; see "Reordering tabs within a window" below.

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

> **Critical**: `split`/`vsplit` without `-s` targets the **currently focused** window, which may differ from the window running this script. Always pass the calling session's ID.

```bash
# vsplit returns the new session ID — capture it
SID=$(it2 vsplit -s "$ITERM_SESSION_ID" 2>&1 | grep -oE '[A-F0-9-]{36}')
it2 run -s "$SID" "echo hello"
```

`$ITERM_SESSION_ID` is set automatically by iTerm2 shell integration in each shell session. It identifies the **calling** session, so the split always opens next to it regardless of which window is focused.

### Session ID from `newtab` / `new`

Only `split`/`vsplit` print a session UUID (`Created new pane: <UUID>`). `newtab` prints `Created new tab: 71` and `new` prints `Created new window: pty-…` — **neither emits a session UUID**, so the grep above returns empty and later `-s "$SID"` calls silently hit the wrong session.

Resolve the tab number through `session list --json` (its `tab_id` field is a string):

```bash
TAB=$(it2 newtab 2>&1 | sed -n 's/^Created new tab: //p')
SID=$(it2 session list --json | jq -r --arg t "$TAB" '.[] | select(.tab_id == $t) | .id')
it2 run -s "$SID" "cd $(pwd) && echo hello"
```

Prefer `vsplit` whenever you just need a targetable session — it hands you the ID directly.

### Reordering tabs within a window

The `it2` CLI has no reorder command. Reordering needs the Python API directly:

```bash
~/.local/share/uv/tools/it2/bin/python - <<'PY'
import iterm2

async def main(connection):
    app = await iterm2.async_get_app(connection)
    w = app.current_terminal_window
    tabs = list(w.tabs)
    tabs.append(tabs.pop(0))          # any reordering of the same list works
    await w.async_set_tabs(tabs)

iterm2.run_until_complete(main)
PY
```

Use the `it2` tool's own interpreter if `import iterm2` fails in your default `python3`.

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
</commands>

<workflows>
## Default workflow: iTerm2 pane + tmux (see tmux skill)

When asked to "open a pane" or "run something next to this session", combine iTerm2 (visibility) with tmux (reliability):

```bash
# Split next to the calling session (not the focused window), inherit working dir
SID=$(it2 vsplit -s "$ITERM_SESSION_ID" 2>&1 | grep -oE '[A-F0-9-]{36}')
it2 run -s "$SID" "cd $(pwd) && tmux new -s dev-server"

# All further commands go through tmux (reliable, no focus issues)
tmux send-keys -t dev-server:0.0 -l -- 'npm run dev'
tmux send-keys -t dev-server:0.0 Enter
```

Or use the tmux skill's `tmux-init.sh` which does this workflow automatically.

### Workflow: Quick split (no tmux)

For simple, non-interactive commands where tmux is overkill:

```bash
# Split next to the calling session, start in the same working directory
SID=$(it2 vsplit -s "$ITERM_SESSION_ID" 2>&1 | grep -oE '[A-F0-9-]{36}')
it2 run -s "$SID" "cd $(pwd) && tail -f /var/log/app.log"
```

> `$(pwd)` captures the calling process's working directory. If the script runs from a different dir than intended, pass an explicit path instead.

## Workflow: Workspace with saved layout

```bash
it2 window list --json
it2 newtab
it2 session set-name "Tests"
it2 window arrange save "my-project"
```
</workflows>

<troubleshooting>
## When `it2` hangs

Wrap every `it2` call in `timeout 20 …` — a hang is the normal failure mode, not an error message.

**A close command hangs**: `it2 tab close` / `it2 session close` block on iTerm2's own "close session?" confirmation dialog, even with `-f`. The dialog also stalls every other `it2` call until it is answered. Answer it in the GUI, or suppress it in Settings > Profiles > Session > "Prompt before closing". A declined dialog surfaces as `RPCException: USER_DECLINED`.

**Every command hangs and prints the socket-downgrade error** ("you must manually delete the file at ~/Library/Application Support/iTerm2/private/socket"):

```bash
rm -f ~/Library/Application\ Support/iTerm2/private/socket
```

Then toggle the Python API off and on (Settings > General > Magic > Enable Python API) and retry. If it still hangs, fall back to AppleScript — it uses a separate channel and keeps working while the Python API is down.
</troubleshooting>

<applescript>
## AppleScript fallback (external automation)

Use this when the caller cannot shell out to `it2` — embedded `osascript` from Node/Python — or when the Python API is unreachable.

```applescript
tell application "iTerm2"
  set targetWindow to (create window with default profile)
  tell current session of current tab of targetWindow
    write text "cd /path/to/project && npm run dev"
    return id
  end tell
end tell
```

- `create tab with default profile` on an existing window instead of `create window` for a tab.
- `id of current session` returns the same UUID form `it2 -s` takes, so the two can be mixed.
- iTerm2 has no initial-working-directory setting here: `cd` must be part of the command you write.
- `write text` always submits (appends a newline) — there is no send-without-newline equivalent.
</applescript>

<remote_windows>
## Remote Windows Hosts (SSH/SCP)

Working with Windows machines over SSH has path gotchas: `scp` to `C:\...` paths always fails (colon parsed as host separator), small files are best written via SSH stdin, and quoting rules differ between `cmd /c` (backslashes) and PowerShell (forward slashes).
Full recipes: `~/.claude/skills/tmux/references/remote-windows-hosts.md`
</remote_windows>
