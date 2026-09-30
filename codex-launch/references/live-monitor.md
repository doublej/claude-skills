# Live monitoring from Claude

This applies whenever Claude uses Codex: interactive, background, images,
rescue, review, resumed threads, plugins, and automatic review hooks.
Open a visible observer of the real session; keep Claude's result capture too.

## Direct CLI commands

Use the shared wrapper, preserving arguments as separate shell words:

```bash
bash ~/.claude/skills/codex-launch/scripts/run_monitored.sh "Codex review" \
  codex exec -C "$PWD" -s read-only --json -- "Review the current changes."
```

The wrapper opens a dedicated iTerm2 tab before running the command,
streams stdout/stderr into a unique retained log, and returns Codex's exit code.
It verifies that the observer started before Codex runs. Each tab has a task
label and an explicit iTerm2 session ID; the finished output stays visible.
The observer displays the end status without owning or cancelling the job.
Use a background Bash/tool job when Claude must keep working, and retain its
handle for completion and cancellation. Do not launch a second Codex run for
the monitor. Raw `--json` events remain available for result capture.

`codex-image` opens this observer itself. For an interactive TUI or desktop app,
the actual visible Codex session satisfies the requirement. Use an explicitly
targeted existing terminal surface when available; the bundled CLI launcher
otherwise opens a dedicated iTerm2 tab rather than typing into unknown focus.
Verify the session started. A clipboard handoff is pending until the user submits it.

## Codex plugin / rescue / app-server jobs

Keep the installed plugin's dispatch contract. The main Claude thread owns
the observer; do not add polling or extra calls inside its thin rescue subagent.

1. Dispatch the intended task/review once. Prefer the plugin's background mode
   when the foreground helper buffers progress until the task ends.
2. Capture the returned job ID. Resolve the installed plugin root from Claude's
   plugin context or `~/.claude/plugins/installed_plugins.json`. Run:

   ```bash
   node "$plugin_root/scripts/codex-companion.mjs" status "$job_id" --json
   ```

   The installed plugin 1.0.2 returns `job.logFile` and `job.threadId`.
   Inspect the returned shape; do not guess a global latest-job path.
3. Open the exact job log immediately:

   ```bash
   bash ~/.claude/skills/codex-launch/scripts/open_monitor.sh \
     "$job_log" "" "Codex: $job_id"
   ```

4. Keep the observer open. Use the plugin's status/result/cancel commands from
   the main Claude thread for lifecycle management. Report terminal status;
   this log-only observer remains open until JJ closes it.

Apply this to automatic review-gate and app-server jobs too: attach to their
actual log or visible native session, rather than starting a duplicate review.
If the plugin exposes no live log, use its supported event stream in a visible
surface or use the monitored direct CLI path for a new task. An existing hidden
session requires a real observer; `resume` is a control session, not a passive tail.

## Failure and installation

Requires iTerm2 with its Python API enabled, `it2`, `python3`, and `timeout`.
The launcher creates a dedicated tab, resolves its session ID from the tab ID,
and names/focuses only that session. Each `it2` call has a 20-second timeout.
For diagnosis, use `timeout 20 it2 session read -s "$session_id" -n 200`.
Do not send commands into the active session without an explicit ID.

If the iTerm2 launcher fails, stop before a direct run starts and report the error.
For an already dispatched plugin job, explain the observer failure immediately
and restore a visible observer; do not silently leave the job hidden.
The fallback command is `tail -n +1 -f "$job_log"` in JJ's visible terminal.
Do not expose credentials in command arguments or logs.

Activate the requirement across all Claude projects:

```bash
bash ~/.claude/skills/codex-launch/scripts/install_monitor_rule.sh
```

This symlinks the tracked rule into `~/.claude/rules/`. New Claude sessions load
it automatically. In an existing session, read the rule explicitly.
