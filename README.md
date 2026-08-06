# claude-skills

Personal collection of [Claude Code](https://docs.claude.com/claude-code) skills — 140 `SKILL.md` packages covering design, code analysis, dev tooling, content, and infra automation.

## Layout

Flat, one directory per skill:

```
<skill-name>/
├── SKILL.md          # required entrypoint (YAML frontmatter + instructions)
├── scripts/           # executable helpers
├── references/        # docs loaded on demand
└── assets/            # templates, output files
```

See [skills_spec.md](skills_spec.md) for the full `SKILL.md` format and [NAMING.md](NAMING.md) for the family-prefix naming convention (`code-*`, `ui-*`, `stream-*`, …).

## Install

```bash
./install-skill.sh <skill-name>   # symlink one skill into ~/.claude/skills/
./install-skill.sh --all          # symlink everything
```

`.skillignore` lists directories that are repo infrastructure, not skills, and must never be installed.

## Usage stats

Invocations are tracked by [skill-usage-tracker](skill-usage-tracker/) via a SessionStart hook. Query anytime with:

```bash
python3 skill-usage-tracker/scripts/query_usage.py --top 10
python3 skill-usage-tracker/scripts/query_usage.py --unused
```

### Top 10 most used (all time)

| # | Skill | Uses |
|---|-------|------|
| 1 | skill-creator | 149 |
| 2 | session-search | 80 |
| 3 | frontend-design | 49 |
| 4 | prompt-crafter | 41 |
| 5 | skill-researcher | 36 |
| 6 | homenetwork | 31 |
| 7 | artifact-design | 28 |
| 8 | frontend-design:frontend-design | 27 |
| 9 | handoff | 22 |
| 10 | svelte:svelte-core-bestpractices | 19 |

## Archive

Dead or superseded material moves to `_archive/<date>-<what>/` rather than being deleted outright.
