---
name: tmux
description: "Remote-control tmux sessions: send keystrokes, scrape pane
  output, and drive interactive CLIs (REPLs, debuggers, servers) reliably.
  Use when running or debugging an interactive terminal program, keeping a
  long-lived process observable, or asked to 'use tmux', 'open a session',
  'monitor a pane', or debug with lldb/gdb."
license: Vibecoded
---

# tmux Skill

Use tmux as a programmable terminal multiplexer for interactive work. Works on Linux and macOS with stock tmux; avoid custom config by using a private socket.

Shared driver discipline (send vs run, capture-after-settle, explicit pane targeting — with the it2/tmux/cmux command table): see `references/terminal-driver-core.md`.

<quickstart>

### One-command bootstrap (recommended)

```bash
# Creates session, waits for shell, splits visible iTerm2 pane next to agent
eval "$(./scripts/tmux-init.sh --name claude-py | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'{k.upper()}={v!r}') for k,v in d.items()]")"

# Send commands with one call
./scripts/tmux-run.sh -S "$SOCKET" -t "$TARGET" "python3 -q" --pattern ">>>"
./scripts/tmux-run.sh -S "$SOCKET" -t "$TARGET" "print('hello')" --wait 1

# Clean up
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

</quickstart>

<manual_setup>

```bash
SOCKET_DIR=${TMPDIR:-/tmp}/claude-tmux-sockets  # well-known dir for all agent sockets
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/claude.sock"                # keep agent sessions separate from your personal tmux
SESSION=claude-python                           # slug-like names; avoid spaces
tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'python3 -q' Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200  # watch output
tmux -S "$SOCKET" kill-session -t "$SESSION"                   # clean up
```

</manual_setup>

<visibility>

When iTerm2 is available (macOS), **always open tmux sessions in a visible iTerm2 pane**. The easiest way is `tmux-init.sh` which handles this automatically:

```bash
./scripts/tmux-init.sh --name claude-py  # splits pane next to agent, attaches tmux
```

This uses the `it2` CLI to split next to the calling session (`it2 vsplit -s "$ITERM_SESSION_ID"`), then attaches tmux in the new pane via `it2 run`. Use `--no-split` to skip; the script also falls back to no-split automatically when `it2` or `$ITERM_SESSION_ID` is unavailable.

**Fallback** (non-iTerm2 or remote): print a monitor command for the user to copy-paste:

```
To monitor this session yourself:
  tmux -S "$SOCKET" attach -t claude-lldb

Or to capture the output once:
  tmux -S "$SOCKET" capture-pane -p -J -t claude-lldb:0.0 -S -200
```

This must ALWAYS be printed right after a session was started and once again at the end of the tool loop.

</visibility>

<socket_convention>

- Agents MUST place tmux sockets under `CLAUDE_TMUX_SOCKET_DIR` (defaults to `${TMPDIR:-/tmp}/claude-tmux-sockets`) and use `tmux -S "$SOCKET"` so we can enumerate/clean them. Create the dir first: `mkdir -p "$CLAUDE_TMUX_SOCKET_DIR"`.
- Default socket path to use unless you must isolate further: `SOCKET="$CLAUDE_TMUX_SOCKET_DIR/claude.sock"`.

</socket_convention>

<targeting_panes>

- Target format: `{session}:{window}.{pane}`, defaults to `:0.0` if omitted. Keep names short (e.g., `claude-py`, `claude-gdb`).
- Use `-S "$SOCKET"` consistently to stay on the private socket path. If you need user config, drop `-f /dev/null`; otherwise `-f /dev/null` gives a clean config.
- Inspect: `tmux -S "$SOCKET" list-sessions`, `tmux -S "$SOCKET" list-panes -a`.

</targeting_panes>

<finding_sessions>

- List sessions on your active socket with metadata: `./scripts/find-sessions.sh -S "$SOCKET"`; add `-q partial-name` to filter.
- Scan all sockets under the shared directory: `./scripts/find-sessions.sh --all` (uses `CLAUDE_TMUX_SOCKET_DIR` or `${TMPDIR:-/tmp}/claude-tmux-sockets`).

</finding_sessions>

<sending_input>

> **Never use `\n` to submit commands.** In bash double-quotes `\n` is two literal characters, not a newline. Always use `Enter` as a separate `send-keys` argument.

The canonical two-step pattern — `-l` for literal text, then bare `Enter`:

```bash
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -l -- "$cmd"
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 Enter
```

The `-l` flag sends text literally (no key interpretation), which means `Enter` won't work inline. Always send `Enter` as a separate `send-keys` call.

- When composing inline commands, use single quotes or ANSI C quoting to avoid expansion: `tmux -S "$SOCKET" send-keys -t target -- $'python3 -m http.server 8000' Enter`.
- To send control keys: `tmux -S "$SOCKET" send-keys -t target C-c`, `C-d`, `C-z`, `Escape`, etc.

</sending_input>

<watching_output>

- Capture recent history (joined lines to avoid wrapping artifacts): `tmux -S "$SOCKET" capture-pane -p -J -t target -S -200`.
- For continuous monitoring, poll with the helper script (below) instead of `tmux wait-for` (which does not watch pane output).
- You can also temporarily attach to observe: `tmux -S "$SOCKET" attach -t "$SESSION"`; detach with `Ctrl+b d`.
- When giving instructions to a user, **explicitly print a copy/paste monitor command** alongside the action don't assume they remembered the command.

</watching_output>

<spawning_processes>

Some special rules for processes:

- when asked to debug, use lldb by default
- when starting a python interactive shell, always set the `PYTHON_BASIC_REPL=1` environment variable. This is very important as the non-basic console interferes with your send-keys.

</spawning_processes>

<waiting_for_prompts>

**Required step**: before sending commands to a new session, always wait for the shell prompt. `tmux-init.sh` handles this automatically. For manual setup, use `wait-for-text.sh`:

```bash
# Manual: wait for shell prompt after creating session
tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
./scripts/wait-for-text.sh -S "$SOCKET" -t "$SESSION":0.0 -p '^\$' -T 15 -l 4000

# Use tmux-run.sh for send + wait + capture in one call
./scripts/tmux-run.sh -S "$SOCKET" -t "$SESSION":0.0 "python3 -q" --pattern ">>>"
./scripts/tmux-run.sh -S "$SOCKET" -t "$SESSION":0.0 "print('hello')" --wait 1
```

- After every command, verify output before sending the next — don't blindly chain commands.
- For long-running commands, poll for completion text (`"Type quit to exit"`, `"Program exited"`, etc.) before proceeding.

</waiting_for_prompts>

<interactive_recipes>

- **Python REPL**: `tmux ... send-keys -- 'python3 -q' Enter`; wait for `^>>>`; send code with `-l`; interrupt with `C-c`. Always with `PYTHON_BASIC_REPL`.
- **gdb**: `tmux ... send-keys -- 'gdb --quiet ./a.out' Enter`; disable paging `tmux ... send-keys -- 'set pagination off' Enter`; break with `C-c`; issue `bt`, `info locals`, etc.; exit via `quit` then confirm `y`.
- **Other TTY apps** (ipdb, psql, mysql, node, bash): same pattern—start the program, poll for its prompt, then send literal text and Enter.

</interactive_recipes>

<cleanup>

- Kill a session when done: `tmux -S "$SOCKET" kill-session -t "$SESSION"`.
- Kill all sessions on a socket: `tmux -S "$SOCKET" list-sessions -F '#{session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t`.
- Remove everything on the private socket: `tmux -S "$SOCKET" kill-server`.

</cleanup>

<helpers>

`./scripts/tmux-init.sh` bootstraps a complete tmux session in one call. Creates the session, waits for shell ready, and optionally splits a visible iTerm2 pane next to the agent.

```bash
./scripts/tmux-init.sh --name claude-py
# → {"socket":"/.../claude-py.sock","session":"claude-py","target":"claude-py:0.0","monitor_cmd":"tmux -S ... attach -t claude-py","iterm2_session_id":"..."}
```

| Option | Description |
|--------|-------------|
| `-n`/`--name` | Session name (required, slug-like) |
| `-S`/`--socket` | Socket path (default: `$SOCKET_DIR/<name>.sock`) |
| `--no-split` | Skip iTerm2 pane splitting |
| `--direction h\|v` | Split direction (default: v) |

Cross-skill: uses the `it2` CLI (see the iterm2 skill). Falls back to `--no-split` mode when `it2` or `$ITERM_SESSION_ID` is unavailable.

</helpers>

<helper_scripts>

`./scripts/tmux-run.sh` sends a command, waits for completion, and captures output — all in one call.

```bash
./scripts/tmux-run.sh -S "$SOCKET" -t "$TARGET" "echo hello" --wait 1
./scripts/tmux-run.sh -S "$SOCKET" -t "$TARGET" "pip install x" --pattern "Successfully"
```

| Option | Description |
|--------|-------------|
| `-t`/`--target` | Pane target (required) |
| `-S`/`--socket` | Socket path |
| `-w`/`--wait` | Fixed wait seconds (default: 2) |
| `-p`/`--pattern` | Wait for regex instead of fixed time |
| `-T`/`--timeout` | Pattern timeout seconds (default: 15) |
| `-l`/`--lines` | History lines to capture (default: 200) |

</helper_scripts>

<wait_for_text>

`./scripts/wait-for-text.sh` polls a pane for a regex (or fixed string) with a timeout. Works on Linux/macOS with bash + tmux + grep.

```bash
./scripts/wait-for-text.sh -S "$SOCKET" -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]
```

- `-S`/`--socket` socket path (for private sockets)
- `-t`/`--target` pane target (required)
- `-p`/`--pattern` regex to match (required); add `-F` for fixed string
- `-T` timeout seconds (integer, default 15)
- `-i` poll interval seconds (default 0.5)
- `-l` history lines to search from the pane (integer, default 1000)
- Exits 0 on first match, 1 on timeout. On failure prints the last captured text to stderr to aid debugging.

</wait_for_text>

<windows_hosts>

When using tmux sessions to work with Windows machines over SSH: `scp` to `C:\...` paths always fails (colon parsed as host separator), small files are best written via SSH stdin, and quoting rules differ between `cmd /c` (backslashes) and PowerShell (forward slashes).
Full recipes: `references/remote-windows-hosts.md` (installed: `~/.claude/skills/tmux/references/remote-windows-hosts.md`)

</windows_hosts>
