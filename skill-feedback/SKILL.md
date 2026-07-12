---
name: skill-feedback
description: 'Report feedback on a skill via spawned session. args: "<skillname> <feedback>"'
arguments: "<skillname> <feedback>"
---

# Skill Feedback

Report feedback (bugs, improvements, ideas) on any skill — from whatever project you're in.
Hands off to a new Claude session in the skills project, then resumes yours.

<path_resolution>

Resolve the skills project root from this skill's install symlink:

```bash
SKILLS_ROOT="$(dirname "$(readlink -f ~/.claude/skills/skill-feedback)")"
```

Use `$SKILLS_ROOT` for all operations below. Never hardcode paths.

</path_resolution>

<workflow>

### 1. Parse arguments

`$ARGUMENTS` format: `<skillname> <feedback text>`

If `$ARGUMENTS` is empty, use consult-user-mcp `ask` with a form:
- **skill** (text): Which skill? (name or folder)
- **feedback** (text): What's the issue or improvement?

### 2. Validate skill

Check that `$SKILLS_ROOT/<skillname>/SKILL.md` exists.

If not found, list available skills and ask user to pick:

```bash
ls -d "$SKILLS_ROOT"/*/SKILL.md 2>/dev/null | xargs -I{} dirname {} | xargs -I{} basename {}
```

### 3. Validate environment

Check that `$ITERM_SESSION_ID` is set. If empty, abort with:
> "ITERM_SESSION_ID not set — this skill requires iTerm2."

### 4. Hand off

Run the handoff script:

```bash
bash "$SKILLS_ROOT/skill-feedback/scripts/handoff.sh" \
  "$SKILLS_ROOT" \
  "$PWD" \
  "$ITERM_SESSION_ID" \
  "<skillname>" \
  "<feedback>"
```

**Important:** Pass feedback as a single quoted argument. The script writes it to a temp file internally to avoid shell escaping issues.

### 5. Inform user

After launching the handoff script, tell the user:

> Feedback session launched in a new iTerm2 tab. Your current session continues normally.
> When the feedback is processed, a completion message will be sent to this session.

</workflow>

<rules>

- Always resolve `$SKILLS_ROOT` dynamically — never hardcode
- Never continue after launching the handoff — exit immediately
- The handoff script runs in the background; do not wait for it
- All feedback text flows through temp files, never inline shell args

</rules>
