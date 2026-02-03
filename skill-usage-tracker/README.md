# Skill Usage Tracker

Internal tracking system for skill usage analytics in the claude-skills project.

## Quick Start

The system is already configured and running. Skill invocations are automatically tracked via PostToolUse hooks, and usage statistics are displayed at the start of each session.

### View Statistics

```bash
# Comprehensive report
python3 skill-usage-tracker/scripts/generate_stats.py

# Top 10 skills
python3 skill-usage-tracker/scripts/query_usage.py --top 10

# Skills with < 3 uses (archival candidates)
python3 skill-usage-tracker/scripts/query_usage.py --below-threshold 3
```

## Components

### Hooks

- **`hooks/track_usage.py`** - PostToolUse hook that logs skill invocations
- **`hooks/welcome_stats.py`** - SessionStart hook that displays usage statistics

### Scripts

- **`scripts/init_db.py`** - Initialize the SQLite database
- **`scripts/query_usage.py`** - Query usage data with various filters
- **`scripts/generate_stats.py`** - Generate comprehensive statistics report

### Configuration

- **`.claude/settings.json`** - Hook registration
- **`.claude/skill-usage.db`** - SQLite database with usage data
- **`.claude/skill-usage.log`** - Error log (created on first error)

## Database Schema

```sql
CREATE TABLE skill_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,       -- Unix timestamp (ms)
    skill_name TEXT NOT NULL,
    session_id TEXT NOT NULL,
    args TEXT,
    success INTEGER NOT NULL DEFAULT 1,
    error_message TEXT
);
```

## Configuration

### Disable Welcome Message

```bash
export SKILL_STATS_ENABLED=0
```

### Direct SQL Access

```bash
sqlite3 .claude/skill-usage.db
```

Example queries:
```sql
-- Most used skills
SELECT skill_name, COUNT(*) as uses
FROM skill_usage
GROUP BY skill_name
ORDER BY uses DESC;

-- Recent activity
SELECT
    datetime(timestamp/1000, 'unixepoch', 'localtime') as time,
    skill_name,
    args
FROM skill_usage
ORDER BY timestamp DESC
LIMIT 20;
```

## Maintenance

### Backup

```bash
cp .claude/skill-usage.db .claude/skill-usage-backup-$(date +%Y%m%d).db
```

### Reset

```bash
rm .claude/skill-usage.db
python3 skill-usage-tracker/scripts/init_db.py
```

### View Logs

```bash
tail -f .claude/skill-usage.log
```

## Performance

- Hook overhead: ~10-50ms per invocation
- SQLite write: ~5-20ms (WAL mode)
- Welcome message: ~50-100ms (once per session)
- Total impact: Negligible

## Dependencies

Python 3.7+ standard library only (no external packages).

## Troubleshooting

### Database locked errors

The database uses WAL mode with 5-second timeouts. If you see locked errors in the log, they're automatically handled and won't affect skill execution.

### Hooks not running

Check that `.claude/settings.json` exists and contains the hook configuration. Verify hook scripts have correct paths.

### Missing statistics

If the welcome message doesn't appear, check:
1. Database exists at `.claude/skill-usage.db`
2. Database contains records
3. `SKILL_STATS_ENABLED` is not set to `0`
