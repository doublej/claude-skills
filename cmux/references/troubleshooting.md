# Troubleshooting

Six failure modes in order of how often they bite. Recipes are
copy-pasteable.

## 1. PTY init race (cmux issue #1472)

**Symptom.** `cmux send` immediately after `new-split` lands in a half-
initialized shell. Commands get truncated or dropped; the tab shows no
prompt. `cmux-tab.sh` is not affected *as long as the shell is idle* —
only fast back-to-back spawn+send breaks.

**Fix.** Sleep 500ms between `new-split` and the first send, OR wait for
the shell prompt via `read-screen`:

```bash
./scripts/cmux-tab.sh myproj dev
for _ in $(seq 1 20); do
  out=$(cmux read-screen --surface "$SID" 2>/dev/null | tail -1)
  [[ "$out" =~ [\$#\>]\ *$ ]] && break
  sleep 0.1
done
./scripts/cmux-send.sh myproj dev "bun dev" --enter
```

**AppleScript workaround (macOS only, last resort).** If the PTY just
refuses to spawn (cmux window stuck at "Starting…"), poke it:

```applescript
osascript -e 'tell application "cmux" to activate' \
          -e 'tell application "System Events" to keystroke " "'
```

Run that from bash, not from inside cmux — the spacebar needs to hit the
frozen surface, so focus it first. Brittle, macOS-version-specific, not
worth scripting. Copy-paste when needed and move on.

## 2. `read-screen` returns stale output

**Symptom.** You sent a command, waited, read the screen — but output is
from 30 seconds ago. cmux renders asynchronously and the internal buffer
isn't flushed until the window paints.

**Fix.** `cmux refresh-surfaces --surface <id>` before every read. The
helper scripts don't force this (they're write-path); your polling code
has to:

```bash
cmux refresh-surfaces --surface "$SID"
sleep 0.1
cmux read-screen --surface "$SID" --scrollback 500
```

Always `--scrollback` when looking for completion markers — the visible
screen only holds ~30 lines, and your marker scrolled off two seconds ago.

## 3. `--surface` vs `--workspace` targeting

**Symptom.** `cmux send --surface <id>` works; `cmux send --workspace <id>`
errors with "ambiguous surface". Or vice-versa.

**Rule.**

| Scope | Flag |
|-------|------|
| One specific pane | `--surface <id>` |
| Workspace-level op (close, rename, list) | `--workspace <id>` |
| Cross-workspace by name | resolve name → id first, then `--workspace` |

Never pass both. Never pass `--workspace` to a verb that addresses a
single pane (`send`, `send-key`, `read-screen`, `refresh-surfaces`).

## 4. Browser ref invalidation

**Symptom.** `browser click --ref <ref>` returns "node detached" or
"ref not found" after a page navigation or SPA route change.

**Fix.** Refs are bound to a DOM snapshot. Any `goto`, `back`, `forward`,
`reload`, or route-level nav invalidates every outstanding ref. Re-find
the element after navigation:

```bash
cmux browser click --surface "$BS" --ref "$LOGIN_BTN"
cmux browser wait-for-url --surface "$BS" --pattern '.*/dashboard'

# $WELCOME was resolved on the login page — stale. Re-find.
WELCOME=$(cmux browser find --surface "$BS" --role heading --name "Welcome" --json \
          | jq -r .ref)
```

## 5. `send` without newline

**Symptom.** `cmux send --surface <id> "bun dev"` returns success but
nothing happens. The text is sitting in the input buffer, no Enter was
pressed.

**Fix.** `cmux send` is input-only. Use `cmux send-key Return` after, or
use this skill's `cmux-send.sh … --enter` which handles both.

```bash
# CLI direct
cmux send     --surface "$SID" "bun dev"
cmux send-key --surface "$SID" Return

# Or, via the skill
./scripts/cmux-send.sh myproj dev "bun dev" --enter
```

## 6. Orphan workspace after crash

**Symptom.** cmux restarted (daemon crash, system reboot) and you see
a workspace in `list-workspaces` whose tabs all show "(disconnected)"
or whose `surface.state == "orphan"`.

**Fix.** The backing PTYs are gone; the workspace record is metadata
only. Close and recreate:

```bash
WS_ID=$(./scripts/cmux-find.sh myproj | jq -r .workspace)
cmux close-workspace --workspace "$WS_ID" --force

./scripts/cmux-project.sh myproj code-dev-logs   # rebuild
```

If you have an up-to-date `.cmux/myproj.json` snapshot, use
`cmux-restore.sh` instead — it rebuilds with the canonical tab set:

```bash
cmux close-workspace --workspace "$WS_ID" --force
./scripts/cmux-restore.sh myproj < .cmux/myproj.json
```

## Quick diagnostic checklist

Before escalating anything:

1. `echo $CMUX_SOCKET_PATH` — set? points at a live socket?
2. `cmux identify --json` — does cmux itself respond?
3. `cmux list-workspaces --json | jq .` — expected workspaces present?
4. `cmux refresh-surfaces --workspace <id>` then re-read screens.
5. Last resort: restart cmux daemon, rebuild via `cmux-restore.sh`.
