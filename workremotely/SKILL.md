---
name: workremotely
description: Toggle transparent SSH forwarding for Bash commands in a chosen directory scope. Use when the user says "work remotely", "/workremotely", "go remote", "run on nas", wants commands to execute on a remote host without manually prefixing each one, or asks to turn remote mode on/off. Bash commands under the scoped directory get wrapped with ssh to a configured host; a reminder surfaces every 5 minutes while active. Read/Edit/Write tools stay local.
---

# workremotely

Session-scoped remote Bash execution. Toggled on/off by creating or deleting a `.workremotely` marker file in the directory whose subtree should run remotely. A PreToolUse hook walks upward from each Bash call's cwd to find the marker; if found, the command is rewritten as `ssh <host> bash -lc '<cmd>'` before Claude Code sends it.

<setup>

## First-time setup

Check whether hooks are already installed:

```bash
grep -q "workremotely/scripts/ssh-wrap.sh" ~/.claude/settings.json && echo installed || echo missing
```

If missing:

```bash
~/.claude/skills/workremotely/scripts/install-hooks.sh
```

Registers the PreToolUse + PostToolUse Bash hooks in `~/.claude/settings.json`. Idempotent.

</setup>

<control>

## Enable / disable / status

Enable for the current directory (default host `nas`):

```bash
~/.claude/skills/workremotely/scripts/enable.sh
```

Enable with a different host:

```bash
~/.claude/skills/workremotely/scripts/enable.sh ubuntu-server
```

Enable for a specific folder other than cwd:

```bash
~/.claude/skills/workremotely/scripts/enable.sh nas --at /Users/jurrejan/Documents/development/multi-stack/project-atlas
```

Check state (walks up from cwd):

```bash
~/.claude/skills/workremotely/scripts/status.sh
```

Disable (removes the nearest ancestor marker):

```bash
~/.claude/skills/workremotely/scripts/disable.sh
```

</control>

<behavior>

## Behavior while active

- Bash tool calls under the scope are rewritten to `ssh <host> bash -lc '…'`.
- Bash tool calls outside the scope pass through unchanged.
- Read, Edit, Write, Grep, Glob still act on the **local** filesystem. Use sshfs if remote file editing is needed.
- Every 5 minutes of active use, a `[workremotely ACTIVE — host=… scope=…]` reminder is appended to tool output.

</behavior>

<migration>

## Replacing the old /workremotely slash command

The previous `~/.claude/commands/workremotely.md` was a prompt-only command that asked Claude to manually prefix commands with `ssh nas`. This skill supersedes it. Delete or shorten that command file once the skill is installed.

</migration>

<troubleshooting>

## When something looks wrong

- **Commands run locally despite enable:** run `status.sh`. If it says INACTIVE, the tool's cwd is outside the scope. Check the hook is in `settings.json`.
- **`ssh: Permission denied`:** keys/agent not set up for the host. `BatchMode=yes` is on, so passwords won't prompt. Fix ssh first, then retry.
- **Remote `cd` fails:** the wrap assumes remote FS mirrors local paths. Edit `scripts/ssh-wrap.sh` to remap `$REMOTE_CWD`.
- **Interactive tools hang:** add `-t` to the `ssh` call in `ssh-wrap.sh`.
- **rtk errors on remote:** install rtk on the host, or reorder the hook chain so `ssh-wrap.sh` runs BEFORE `rtk-rewrite.sh`.

</troubleshooting>

<references>

See `references/setup.md` for hook chain ordering, marker format, and wrapping internals.

</references>
