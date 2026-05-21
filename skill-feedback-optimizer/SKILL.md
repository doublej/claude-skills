---
name: skill-feedback-optimizer
description: "Work the auto-analysis beads backlog: pick the highest-priority ticket created by skill-feedback-collector, apply the fix to the affected skill, install, commit, close. Designed for one-shot or /loop use."
---

# Skill Feedback Optimizer

Companion to `skill-feedback-collector`. Drains the backlog of auto-analysis tickets one at a time. Safe to run in `/loop` for autopilot.

<workflow>

### 1. Resolve paths

```bash
SKILLS_ROOT="$(dirname "$(readlink -f ~/.claude/skills/skill-feedback-optimizer)")"
cd "$SKILLS_ROOT"
```

Never hardcode paths.

### 2. Pick the next ticket

```bash
bash "$SKILLS_ROOT/skill-feedback-optimizer/scripts/next_ticket.sh"
```

Returns JSON with `id`, `title`, `description`, `priority`, `skill`, `kind`. Returns `{}` if the backlog is empty — in that case, tell the user "Backlog clean. Nothing to optimize." and exit.

### 3. Read the ticket + the affected skill

- Read the ticket description in full (`bd show <id>` if you need more detail than `next_ticket.sh` returned).
- Read `$SKILLS_ROOT/<skill>/SKILL.md` and any referenced scripts.
- Understand evidence and suggestion. The ticket description includes both.

### 4. Apply the fix

- Edit `SKILL.md` or bundled scripts to address the suggestion.
- Match the existing style of the skill — minimal diff, no drive-by refactors.
- If the fix touches scripts, ensure they remain executable (`chmod +x` if needed).

### 5. Install + commit

```bash
./install-skill.sh "<skill>"
git add "<skill>/"
git commit -m "fix(<skill>): <one-line summary> (bd-<id>)"
```

### 6. Close the ticket

```bash
bd close <id> -r "Fixed in commit <sha>. <one-line summary of change>."
```

### 7. Report back

Tell the user:
- Which ticket was worked
- What changed
- The commit sha
- Whether more tickets remain (`bd ready --label source:auto-analysis --json | jq length`)

</workflow>

<loop_use>

For autopilot, the user runs:

```
/loop 30m /skill-feedback-optimizer
```

In this mode:
- If backlog is empty, exit silently (do not chatter)
- Process exactly one ticket per invocation
- Never spawn nested loops

</loop_use>

<safety>

- **Never** auto-close a ticket you didn't actually fix
- **Never** commit + close if `install-skill.sh` failed — surface the error instead
- If the suggested fix conflicts with existing skill design, prefer skipping over forcing it: add a comment to the ticket via `bd update <id> --append-notes "skipped: <reason>"` and bail
- If the affected skill no longer exists, close the ticket with note "skill removed"
- Single-ticket runs only — do not loop internally

</safety>

<rules>

- One ticket per invocation
- Always run `install-skill.sh` after editing a skill
- Commit message format: `fix(<skill>): <summary> (bd-<id>)`
- Use `bd show`, `bd close`, `bd update` — never edit beads DB directly

</rules>
