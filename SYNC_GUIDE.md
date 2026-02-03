# Skill Sync Guide

Sync Claude Code skills to Codex CLI using `sync-skills.py`.

## Quick Start

```bash
# View all skills and their sync status
python3 sync-skills.py list

# Show summary statistics
python3 sync-skills.py status

# Sync specific skill to Codex
python3 sync-skills.py sync <skill-name>

# Sync all skills (with confirmation)
python3 sync-skills.py sync --all

# Dry-run (see what would happen)
python3 sync-skills.py sync --all --dry-run

# Fix broken symlinks
python3 sync-skills.py fix

# Validate all skills
python3 sync-skills.py validate
```

## Commands

### `list` - List all skills with sync status
- `--filter all` - Show all skills (default)
- `--filter claude-only` - Skills only in Claude
- `--filter codex-only` - Skills only in Codex
- `--filter synced` - Skills in both
- `--filter issues` - Skills with problems

### `status` - Show summary statistics
Displays total skills, sync counts, and warnings.

### `sync` - Sync skills to Codex
- `sync <skill>` - Sync single skill
- `sync --all` - Sync all Claude skills
- `sync --all --validated-only` - Only sync skills with valid descriptions (<500 chars)
- `--dry-run` - Preview without making changes

### `fix` - Fix broken symlinks
Removes invalid/broken symlinks from `~/.codex/skills/`.

### `validate` - Validate skills
Checks for:
- Description length (>500 chars warning)
- Invalid symlinks
- Missing descriptions

## Paths

- **Source**: `/Users/jurrejan/Documents/development/_management/claude-skills/<skill-name>/`
- **Claude**: `~/.claude/skills/`
- **Codex**: `~/.codex/skills/`

## Notes

- Restart Codex CLI after syncing to load new skills
- Skills need `SKILL.md` with YAML frontmatter
- Descriptions >500 chars will trigger warnings but can still sync
