---
name: skill-feedback-collector
description: "Passive auto-analyzer that watches every Skill invocation, runs Sonnet over the transcript, and logs disconnects/improvements as beads tickets in the skills repo. Hook-based — not user-invoked."
---

# Skill Feedback Collector

Captures per-skill feedback automatically. Two Claude Code hooks do all the work:

1. **`PostToolUse(Skill)`** drops a tiny marker per invocation (session id, skill name, transcript path, timestamp). No agent spawn — runs in milliseconds.
2. **`Stop`** fires at the end of every Claude turn. Detaches a background Python analyzer that slices the transcript per marker, runs `claude -p --model claude-sonnet-4-6` on each slice, parses findings, and creates beads tickets.

Findings land as beads tickets in the `claude-skills` repo, labelled `skill:<name>`, `source:auto-analysis`, `kind:<disconnect|improvement|bug|naming|friction>`. The companion `skill-feedback-optimizer` skill processes the backlog.

<architecture>

```
PostToolUse(Skill) → hooks/mark_skill.sh → state/markers/<session>.jsonl
                                                 ↓
Stop (every turn) → hooks/analyze_turn.sh → nohup scripts/analyzer.py &
                                                 ↓
        per marker: slice transcript by timestamp → claude -p → parse JSON
                                                 ↓
              bd create with labels skill:* source:auto-analysis kind:*
```

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
| `state/markers/` | Runtime — JSONL per session. Gitignored. |
| `state/analyzed/` | Lockfiles for concurrent analyzer runs. Gitignored. |
| `state/logs/` | Background analyzer stdout/stderr. Gitignored. |
| `state/token_usage.jsonl` | One record per Sonnet call: tokens (in/out/cache) + cost. Gitignored. |

</files>

<installation>

After running `./install-skill.sh skill-feedback-collector`, register both hooks in `~/.claude/settings.json`:

**`PostToolUse` → matcher `"Skill"`** — add `mark_skill.sh` alongside the existing `skill-usage-tracker` hook:

```json
{
  "matcher": "Skill",
  "hooks": [
    { "type": "command", "command": "python3 /Users/jurrejan/Documents/development/_management/claude-skills/skill-usage-tracker/hooks/track_usage.py" },
    { "type": "command", "command": "/Users/jurrejan/Documents/development/_management/claude-skills/skill-feedback-collector/hooks/mark_skill.sh" }
  ]
}
```

**`Stop`** — add the analyzer dispatcher:

```json
"Stop": [
  {
    "hooks": [
      { "type": "command", "command": "/Users/jurrejan/Documents/development/_management/claude-skills/skill-feedback-collector/hooks/analyze_turn.sh" }
    ]
  }
]
```

</installation>

<inspection>

Check live state:

```bash
# Pending markers
ls skill-feedback-collector/state/markers/

# Recent analyzer runs
ls -lt skill-feedback-collector/state/logs/ | head

# Tickets created
bd list --label source:auto-analysis

# Token spend (all-time, per-skill + total)
python3 skill-feedback-collector/scripts/token_report.py
python3 skill-feedback-collector/scripts/token_report.py --since 2026-05-01
```

</inspection>

<rules>

- Hook scripts must NOT spawn agents synchronously — always background-detach
- Marker writes are append-only single lines (atomic on POSIX)
- The analyzer is calibrated to return empty findings for clean runs — most invocations produce zero tickets
- Dedup: existing open tickets with the same title for the same skill are not duplicated
- Every Sonnet call appends a token+cost record to `state/token_usage.jsonl` (append-only, gitignored)
- Fires a macOS notification (`osascript`) each time the analyzer begins processing new markers — not on empty Stop turns
- All paths resolved from `SKILL_DIR` — no hardcoded absolute paths inside scripts

</rules>
