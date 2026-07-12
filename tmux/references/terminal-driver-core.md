# Terminal Driver Core Discipline

Shared rules for every terminal driver skill (iterm2 / tmux / cmux). Each
skill documents its own commands in detail; this file captures the discipline
they all share, so the rules are stated once. It is an index, not a
replacement for the per-skill sections.

## The three rules

### 1. Send-without-newline vs send-and-run

Every driver separates "type text" from "press Enter". Sending text does NOT
execute it. To run a command you must either use the tool's run form or send
the Enter/Return key as a **separate** call. Never embed `\n` in the text —
in bash double-quotes it is two literal characters, and `-l`/raw-send modes
transmit it literally, not as a keypress.

### 2. Capture-after-settle

Output is asynchronous. After sending a command, wait (fixed sleep, or poll
for a prompt/pattern) before capturing, and always capture to **verify**
before sending the next command. Never blindly chain sends. cmux adds a
twist: its renderer is lazy, so force a repaint (`refresh-surfaces`) before
every read or you get stale output.

### 3. Target the explicit pane, never the focused one

Focus is user state and can change at any moment. Always address the exact
pane/session/surface by ID: capture the ID at creation time (split/new
returns it) and pass it on every subsequent call. Commands that default to
"the active session" will hit whatever the user happens to be looking at.

## Per-tool command table

| Action | it2 (iterm2) | tmux | cmux |
|---|---|---|---|
| Send text, no newline | `it2 send -s "$SID" "text"` | `tmux -S "$SOCKET" send-keys -t tgt -l -- "text"` | `cmux send --surface "$SID" -- "text"` |
| Run a command (text + Enter) | `it2 run -s "$SID" "cmd"` | `send-keys -l -- "cmd"` then `send-keys Enter` (two calls) | `cmux send …` then `cmux send-key --surface "$SID" Return` |
| Control keys | `it2 send -s "$SID" $'\x03'` (Ctrl-C) | `send-keys -t tgt C-c` | `cmux send-key --surface "$SID" C-c` |
| Settle before read | `sleep 1` | `sleep` or `wait-for-text.sh` (poll pattern) | `cmux refresh-surfaces` + short sleep |
| Capture output | `it2 session read -s "$SID" -n 200` | `capture-pane -p -J -t tgt -S -200` | `cmux read-screen --surface "$SID" --scrollback 200` |
| Explicit target | `-s <session-id>` (from `$ITERM_SESSION_ID` / split output) | `-S "$SOCKET"` + `-t session:win.pane` | `--surface <srf_id>` (never `--workspace` for pane I/O) |
| Capture new-pane ID | `SID=$(it2 vsplit -s "$ITERM_SESSION_ID" 2>&1 \| grep -oE '[A-F0-9-]{36}')` | pane target is deterministic: `session:0.0` | `cmux new-split … --tab <name>`, then look up surface by tab name |

## Where the detail lives

- iterm2: `~/.claude/skills/iterm2/SKILL.md` (session targeting, control chars, profiles)
- tmux: `~/.claude/skills/tmux/SKILL.md` (sockets, wait-for-text, tmux-run.sh)
- cmux: `~/.claude/skills/cmux/SKILL.md` (workspace/tab naming, refresh-before-read, helpers)
