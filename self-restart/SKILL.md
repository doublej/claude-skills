---
name: self-restart
description: "Restart the current Claude Code session in its own terminal pane and resume the same conversation, with the same launch flags, so changes that only load at startup take effect: new or edited MCP servers, hooks, settings.json, env vars, plugins, a Claude Code update. Works in iTerm2 and tmux on macOS. Use when the user says 'restart yourself', 'restart claude', 'reload and continue', 'self-restart', '/self-restart', or when a change you just made needs a restart to load. Not for background sessions (`claude respawn`)."
---

# Self Restart

One script restarts the session. It finds the `claude` process, reads its exact launch argv, and spawns a detached watcher. After `--delay` seconds the watcher sends SIGTERM and waits for the exit. It then types `cd <cwd> && claude <same flags> --resume <session-id> '<prompt>'` into the same iTerm2 session or tmux pane. The first prompt of the original launch and any `--resume`/`--continue`/`--session-id` flags are dropped.

<presentation>
Nothing prints after the restart, so banner and report together replace the one-line notice in step 2, written before the script call (session id from `$CLAUDE_CODE_SESSION_ID`):

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   SELF RESTART                                               ║
║   Relaunch this session in its pane and resume it            ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

SELF RESTART  ──  <session-id>   pane: <iterm2|tmux>   delay: <n>s

WHY       <the one-line reason: what needs a restart to load>
PROMPT    <resume prompt | default | idle>

github.com/doublej
```

On `error: not in iTerm2 or tmux`, print the block with `pane: ✗` and the relaunch command under it.
</presentation>

<workflow>
1. Finish or checkpoint the work in flight. The restart ends this turn, and a running tool call or subagent dies with the process.
2. Tell the user in one line that you are restarting and why. Text written after the script call can be cut off.
3. Run the script as the last tool call of the turn:
   ```bash
   python3 ~/.claude/skills/self-restart/scripts/restart.py --prompt "<what to verify and continue with>"
   ```
   Put the concrete next step in `--prompt`, for example "Restarted to load the linear MCP server. Run /mcp to confirm it is connected, then continue the ticket triage." Omit `--prompt` for the generic default. Pass `--prompt ''` to resume idle.
4. End the turn. Make no more tool calls and write no text after the script's output.
</workflow>

<options>
- `--dry-run --json`: print pid, argv, target and the exact relaunch command without restarting. Use it first when unsure what will be relaunched.
- `--delay N`: seconds before SIGTERM (default 5). Raise it only if the end of the last message gets cut.
- The watcher log is at `$TMPDIR/self-restart/<session-id>.log`, and the script prints its path.
</options>

<failure_modes>
- Exit 1 with `error: not in iTerm2 or tmux`: the script prints the relaunch command. Tell the user to quit and run it. Nothing was killed.
- A resumed session started after `/clear` can reopen the pre-clear conversation if `CLAUDE_CODE_SESSION_ID` was not updated. Check the `session_id` in `--dry-run` output against the current transcript.
- Flags the `claude --help` parser does not know are kept, but their values are dropped as positionals. Check `command` in `--dry-run`.
</failure_modes>
