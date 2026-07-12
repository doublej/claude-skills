---
name: skill-feedback-loop
description: "Closed-loop skill quality: a hook-driven collector watches every Skill invocation, runs Sonnet over the transcript, and files disconnects/improvements as beads tickets (label source:auto-analysis); invoking this skill works that backlog — pick the highest-priority ticket, apply the fix to the affected skill, install, commit, close. Designed for one-shot or /loop use (e.g. /loop 30m /skill-feedback-loop). The collector half is hook-based and never user-invoked. Distinct from skill-feedback, which is an interactive iTerm2 handoff. Triggers: /skill-feedback-loop, 'work the skill feedback backlog', 'drain auto-analysis tickets'."
---

# Skill Feedback Loop

One skill, two halves over the same beads queue (`source:auto-analysis`):

- **Collector (producer, hook-driven — never user-invoked):** two Claude Code hooks capture per-skill feedback automatically and file beads tickets.
- **Optimizer (consumer — what runs when you invoke `/skill-feedback-loop`):** drains the backlog one ticket per invocation. Safe to run in `/loop` for autopilot.

<architecture>

```
PostToolUse(Skill) → hooks/mark_skill.sh → state/markers/<session>.jsonl
                                                 ↓
Stop (every turn) → hooks/analyze_turn.sh → nohup scripts/analyzer.py &
                                                 ↓
        per marker: slice transcript by timestamp → claude -p → parse JSON
                                                 ↓
              bd create with labels skill:* source:auto-analysis kind:*
                                                 ↓
   /skill-feedback-loop → scripts/next_ticket.sh → fix → install → commit → bd close
```

Findings land as beads tickets in the `claude-skills` repo, labelled `skill:<name>`, `source:auto-analysis`, `kind:<disconnect|improvement|bug|naming|friction>`.

</architecture>

<files>

| Path | Purpose |
|------|---------|
| `hooks/mark_skill.sh` | PostToolUse hook. Drops marker. Fast. |
| `hooks/analyze_turn.sh` | Stop hook. Detaches background analyzer. Exits immediately. |
| `scripts/parse_marker_payload.py` | Helper used by `mark_skill.sh` to extract fields from the hook payload. |
| `scripts/analyzer.py` | Background worker. Reads markers, slices transcript, runs Sonnet, logs token spend, creates beads tickets. |
| `scripts/prompts/analyzer_prompt.md` | Sonnet prompt — strict JSON output, calibrated to return empty findings for clean runs. |
| `scripts/token_report.py` | Summarize token spend from the usage log (all-time or `--since <date>`). |
| `scripts/next_ticket.sh` | Optimizer entry — picks the next backlog ticket, emits JSON with staleness hints. |
| `state/markers/` | Runtime — JSONL per session. Gitignored. |
| `state/analyzed/` | Lockfiles for concurrent analyzer runs. Gitignored. |
| `state/logs/` | Background analyzer stdout/stderr. Gitignored. |
| `state/token_usage.jsonl` | One record per Sonnet call: tokens (in/out/cache) + cost. Gitignored. |

</files>

<optimizer_workflow>

### 1. Resolve paths

```bash
SKILLS_ROOT="$(dirname "$(readlink -f ~/.claude/skills/skill-feedback-loop)")"
cd "$SKILLS_ROOT"
```

Never hardcode paths.

### 2. Pick the next ticket

```bash
bash ~/.claude/skills/skill-feedback-loop/scripts/next_ticket.sh
```

Returns JSON with `id`, `title`, `description`, `priority`, `skill`, `kind`, plus date-awareness fields:

- `created_at` — when the ticket was filed.
- `possibly_stale` — `true` if the skill was committed to around/after the report (the collector analyzes *older* transcript moments, so a fix may already have shipped).
- `skill_commits_since_report` — list of `{sha, date, subject}` for those commits.

Returns `{}` if the backlog is empty — in that case, tell the user "Backlog clean. Nothing to optimize." and exit.

Tickets are ordered by priority (highest first), then oldest report first.

### 3. Read the ticket + the affected skill

- Read the ticket description in full (`bd show <id>` if you need more detail than `next_ticket.sh` returned).
- Read `$SKILLS_ROOT/<skill>/SKILL.md` and any referenced scripts.
- Understand evidence and suggestion. The ticket description includes both.

### 3.5 Reconcile against skill history (date-awareness)

The collector files tickets against a transcript moment that predates `created_at`, so a fix may already have shipped. **Before editing, decide whether the finding still applies.**

- If `possibly_stale` is `true`, inspect each commit in `skill_commits_since_report`:
  ```bash
  git show --stat <sha>   # what that commit changed
  ```
- Re-read the *current* `SKILL.md` / scripts and check whether the evidence in the ticket is still reproducible.
- **If already addressed** by a recent commit, close the ticket as stale instead of re-fixing:
  ```bash
  bd close <id> -r "Stale: already addressed in <sha> (filed <created_at>). <one-line why>."
  ```
  Report it as a stale close and exit — do not commit a redundant edit.
- **If still valid** (the commits touched unrelated parts), proceed to step 4 as normal.
- When `possibly_stale` is `false`, do a quick sanity re-read but proceed.

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

</optimizer_workflow>

<loop_use>

For autopilot, the user runs:

```
/loop 30m /skill-feedback-loop
```

In this mode:
- If backlog is empty, exit silently (do not chatter)
- Process exactly one ticket per invocation
- Never spawn nested loops

</loop_use>

<installation>

After running `./install-skill.sh skill-feedback-loop`, register both collector hooks in `~/.claude/settings.json`:

**`PostToolUse` → matcher `"Skill"`** — add `mark_skill.sh` alongside the existing `skill-usage-tracker` hook:

```json
{
  "matcher": "Skill",
  "hooks": [
    { "type": "command", "command": "python3 /Users/jurrejan/Documents/development/_management/claude-skills/skill-usage-tracker/hooks/track_usage.py" },
    { "type": "command", "command": "/Users/jurrejan/Documents/development/_management/claude-skills/skill-feedback-loop/hooks/mark_skill.sh" }
  ]
}
```

**`Stop`** — add the analyzer dispatcher:

```json
"Stop": [
  {
    "hooks": [
      { "type": "command", "command": "/Users/jurrejan/Documents/development/_management/claude-skills/skill-feedback-loop/hooks/analyze_turn.sh" }
    ]
  }
]
```

</installation>

<inspection>

Check live collector state:

```bash
# Pending markers
ls ~/.claude/skills/skill-feedback-loop/state/markers/

# Recent analyzer runs
ls -lt ~/.claude/skills/skill-feedback-loop/state/logs/ | head

# Tickets created
bd list --label source:auto-analysis

# Token spend (all-time, per-skill + total)
python3 ~/.claude/skills/skill-feedback-loop/scripts/token_report.py
python3 ~/.claude/skills/skill-feedback-loop/scripts/token_report.py --since 2026-05-01
```

</inspection>

<collector_rules>

- Hook scripts must NOT spawn agents synchronously — always background-detach
- Marker writes are append-only single lines (atomic on POSIX)
- The analyzer is calibrated to return empty findings for clean runs — most invocations produce zero tickets
- Dedup: existing open tickets with the same title for the same skill are not duplicated
- Every Sonnet call appends a token+cost record to `state/token_usage.jsonl` (append-only, gitignored)
- Fires a macOS notification (`osascript`) each time the analyzer begins processing new markers — not on empty Stop turns
- All paths resolved from `SKILL_DIR` — no hardcoded absolute paths inside scripts

</collector_rules>

<optimizer_safety>

- **Never** apply a redundant fix to a stale ticket — reconcile against `skill_commits_since_report` first (step 3.5) and close-as-stale when already addressed
- **Never** auto-close a ticket you didn't actually fix
- **Never** commit + close if `install-skill.sh` failed — surface the error instead
- If the suggested fix conflicts with existing skill design, prefer skipping over forcing it: add a comment to the ticket via `bd update <id> --append-notes "skipped: <reason>"` and bail
- If the affected skill no longer exists, close the ticket with note "skill removed"
- Single-ticket runs only — do not loop internally
- One ticket per invocation; always run `install-skill.sh` after editing a skill
- Commit message format: `fix(<skill>): <summary> (bd-<id>)`
- Use `bd show`, `bd close`, `bd update` — never edit beads DB directly

</optimizer_safety>
