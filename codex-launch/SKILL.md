---
name: codex-launch
description: "Launch Codex with a visible live session, or add a live monitor to any Claude-to-Codex call, including images, exec, rescue, review, plugins, and background jobs. Use for /codex-launch, opening Codex, task handoffs, and monitoring Codex from Claude. Supports interactive app/terminal sessions and monitored result capture."
---

# Launch and monitor Codex

**Every Claude-to-Codex session gets a visible live monitor automatically.**
This includes image generation, exec, rescue, review, plugin/app-server jobs,
background work, and resumed sessions. Do not ask whether JJ wants a monitor.
A hidden tool call, progress notification, or final result alone is insufficient.

Read [live monitoring](references/live-monitor.md) and name the chosen observer
surface before dispatch. Use one actual session; do not create a second run to
watch the first. Preserve result capture when Claude needs Codex's answer.

## Choose the launch path

| Intent | Path |
| --- | --- |
| Claude needs to capture and use the result | Shared monitored command wrapper |
| User wants to interact in a terminal | `launch_cli.sh`; actual TUI is the monitor |
| User explicitly wants the desktop app | `launch_app.sh`; app is the monitor once the task is submitted |
| Plugin/rescue/review call | Preserve plugin dispatch; main Claude thread opens the exact job's log |
| Image generation from Claude | Use `codex-image`; its wrapper already opens the monitor |

If the user did not choose a surface, use a dedicated iTerm2 tab by default.
Use an explicitly targeted existing terminal pane when available and preferred.
Do not type executable text into an unknown frontmost application.

## Capture a result with a live monitor

```bash
bash ~/.claude/skills/codex-launch/scripts/run_monitored.sh "Codex review" \
  codex exec -C "$PWD" -s read-only --json -- "Review the current changes."
```

The wrapper opens iTerm2 before running, streams a unique retained log, and
returns the command's exit code. It preserves stdout for result capture; stderr
also appears in the log. Keep its Bash/tool job handle if launched in background.
Closing the observer does not cancel Codex. See the reference for plugin jobs.

## Interactive terminal

```bash
bash ~/.claude/skills/codex-launch/scripts/launch_cli.sh \
  "Review the current changes; report concrete defects." -C "$PWD" -s read-only
```

Opens a dedicated iTerm2 session running Codex with safely quoted prompt
and flags. Capture the printed launch-file path; verify the terminal actually
shows the intended Codex session. If verification is unavailable, say the
launch was requested, rather than claiming Codex is running.

Check the installed `codex --help` before choosing flags. Current CLI 0.159.2:

- `-C <path>` sets the working directory; a path in prose does not change it.
- `-m <session-model>` selects the agent model, not the image renderer.
- `-s read-only` / `workspace-write` sets filesystem sandbox behavior.
- `-a on-request` / `never` selects approval policy where supported.
- `--json` is for non-interactive `codex exec` event capture.

`-q` and `-a suggest`, `auto-edit`, `full-auto` are obsolete. Do not add permission
bypass flags as boilerplate. Preserve the user's authorized scope.

## Desktop app

```bash
bash ~/.claude/skills/codex-launch/scripts/launch_app.sh "<self-contained brief>"
```

Copies the brief to the clipboard and opens the Codex app. Report that the
handoff is **pending**: JJ must paste and submit it in the intended project.
Opening an app is not proof that a session started. Once submitted, keep the
actual conversation visible. Do not launch a duplicate terminal session.

## Briefing and completion

Include goal, verified working directory, inputs, allowed changes, constraints,
checks, and output contract. Codex has none of Claude's conversation context.
For image-model selection and image/session brief templates, read
`~/.claude/skills/codex-image/references/models.md` and
`~/.claude/skills/codex-image/references/session-briefs.md`.

Report observer location, session/job ID when exposed, retained log, and final
status. For handoffs, leave the user in control. For captured work, collect and
inspect the result before incorporating it. Surface launch failures directly.

Activate the monitor rule for all Claude projects with:

```bash
bash ~/.claude/skills/codex-launch/scripts/install_monitor_rule.sh
```
