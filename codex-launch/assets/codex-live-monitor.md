# Live monitor for every Claude-to-Codex session

Whenever Claude starts, delegates to, or resumes Codex, give JJ a visible live
monitor of that exact session **in iTerm2**. This includes images, exec, rescue, reviews,
background jobs, plugin/app-server runs, and Codex subagents. Do not ask whether
to open it. A final answer, notification, job ID, or hidden tool transcript alone
does not satisfy this requirement.

- Read `~/.claude/skills/codex-launch/references/live-monitor.md` before starting
  Codex. Follow its direct-CLI or plugin workflow.
- For direct non-interactive commands, use
  `bash ~/.claude/skills/codex-launch/scripts/run_monitored.sh "<task>" <command> [args...]`.
  It opens a dedicated iTerm2 tab before execution and retains a live log.
  `codex-image/scripts/generate.sh` already does this; do not double-wrap it.
- An already visible interactive Codex terminal or app session is its own monitor.
  Verify it is the actual running session, not just an opened app or pasted prompt.
  Use iTerm2 for terminal sessions; another surface requires an explicit user choice.
- For plugin jobs, the main Claude thread opens the job's live log immediately
  after dispatch; the rescue forwarder keeps its single-call contract. Follow
  the same rule for review hooks and app-server jobs.
- Tell JJ where the monitor is and give the session/job ID and log path when
  available. Keep it visible through success, failure, or cancellation. Keep logs
  available afterwards. Closing the observer window must not cancel the job.
- If no visible surface can be opened, surface the concrete failure and provide
  the exact log-follow command. Never claim the monitor opened. Continue only
  under an explicit user instruction allowing a run without a visible monitor.
