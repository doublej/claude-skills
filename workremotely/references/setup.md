# workremotely — setup & internals

## One-time install (user machine)

```bash
./scripts/install-hooks.sh
```

Appends a Bash matcher to both `hooks.PreToolUse` and `hooks.PostToolUse` in
`~/.claude/settings.json`, pointing to the scripts in this skill directory.
Idempotent — safe to re-run.

## Hook chain ordering

`settings.json` runs hooks in array order. For correct behavior:

- `strip-attribution.sh`
- `safe-rm.sh`
- `rtk-rewrite.sh`         ← rewrites `git log` → `rtk git log` etc.
- `workremotely/ssh-wrap.sh`  ← wraps the (possibly rewritten) command with ssh
- `package-manager-guard.sh`

If `package-manager-guard.sh` inspects `.tool_input.command` and does not
tolerate an `ssh …` prefix, either move it ABOVE `ssh-wrap.sh` or teach it to
strip the prefix before matching.

## Marker file format

`.workremotely` in the scope root:

```
host=nas
enabled_at=2026-04-22T10:12:00Z
```

Only `host=` is read. Everything else is informational.

Scope resolution: the PreToolUse hook walks upward from `tool_input.cwd` until
it finds a `.workremotely` file (like `.git` discovery). No marker → passthrough.

## Command wrapping shape

The PreToolUse hook rewrites the Bash command to:

```
ssh -o BatchMode=yes <host> bash -lc '<printf-quoted: cd <remote-cwd> && eval <printf-quoted: cmd>>'
```

The double `printf %q` lets the remote shell re-parse pipes, redirects,
heredocs, and $(…) correctly. `BatchMode=yes` prevents the hook from hanging
on an interactive password prompt — set up ssh keys + agent forwarding first.

`cd <remote-cwd> &&` assumes the remote filesystem mirrors the local path
(e.g. via sshfs, or matching `/Users/...` → `/home/.../` layout). If it does
not, edit `ssh-wrap.sh` to remap the path.

## 5-minute reminder

`reminder.sh` runs as PostToolUse Bash. Per-session state lives in
`$TMPDIR/claude-workremotely/<session_id>.last` — mtime tracks last reminder.
If ≥300s since last (or file missing), it emits:

```
[workremotely ACTIVE — host=<h> scope=<dir>. All Bash commands in this scope …]
```

via `hookSpecificOutput.additionalContext`. The text lands in Claude's next
turn, not visibly in the tool output.

## Caveats & scope

- **Only Bash is wrapped.** Read / Edit / Write stay local. Pair with sshfs
  if you need to edit remote files through those tools.
- **rtk on the remote.** If a command was rewritten to `rtk git …`, the remote
  needs `rtk` on its PATH. Otherwise the wrap will run `rtk git …` there and
  fail. Either install rtk remotely or exclude rtk from the chain when
  workremotely is active.
- **Interactive commands** (`vim`, `top`, prompts) — add `-t` to the ssh call
  in `ssh-wrap.sh` if you need a TTY. Default is non-interactive.
- **Secrets.** `printf %q` renders command strings verbatim into the ssh
  argv — they hit the remote host's shell history unless you disable it.
