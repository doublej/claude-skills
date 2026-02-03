---
name: skill-usage-tracker
description: Internal skill usage tracking system for claude-skills project. Automatically logs skill invocations via PostToolUse hook and displays usage statistics at session start via SessionStart hook. Use for analyzing skill usage patterns and identifying archival candidates.
metadata:
  internal: true
  version: "1.0.0"
---

# Skill Usage Tracker

Automatically tracks skill invocations within the claude-skills project for usage analysis and optimization.

## Features

- 📊 Real-time tracking via PostToolUse hook
- 👋 Welcome statistics via SessionStart hook
- 🔍 Query tools for detailed analysis
- 💡 Actionable suggestions for skill management

## Database

**Location**: `.claude/skill-usage.db` (SQLite with WAL mode)

**Schema**:
```sql
CREATE TABLE skill_usage (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER NOT NULL,     -- Unix timestamp (ms)
    skill_name TEXT NOT NULL,
    session_id TEXT NOT NULL,
    args TEXT,
    success INTEGER DEFAULT 1,
    error_message TEXT
);
```

## Usage

### View Comprehensive Statistics

```bash
python3 skill-usage-tracker/scripts/generate_stats.py
```

Shows: total invocations, unique skills, usage by skill with percentages, trends, session analysis, success rates.

### Query Usage Data

```bash
# Top 10 skills
python3 skill-usage-tracker/scripts/query_usage.py --top 10

# Recent usage (last 7 days)
python3 skill-usage-tracker/scripts/query_usage.py --recent 7

# Skills with < 3 uses
python3 skill-usage-tracker/scripts/query_usage.py --below-threshold 3

# Export to JSONL
python3 skill-usage-tracker/scripts/query_usage.py --export output.jsonl

# Top 5 skills from last 30 days
python3 skill-usage-tracker/scripts/query_usage.py --top 5 --days 30
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

-- Usage by day
SELECT DATE(timestamp/1000, 'unixepoch') as day, COUNT(*) as uses
FROM skill_usage
GROUP BY day
ORDER BY day DESC;
```

## Configuration

### Disable Welcome Message

```bash
export SKILL_STATS_ENABLED=0
```

### Hook Registration

The hooks are registered in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "python3 skill-usage-tracker/hooks/track_usage.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 skill-usage-tracker/hooks/welcome_stats.py"
          }
        ]
      }
    ]
  }
}
```

## Maintenance

### Initialize Database

```bash
python3 skill-usage-tracker/scripts/init_db.py
```

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

Errors are logged to `.claude/skill-usage.log`:

```bash
tail -f .claude/skill-usage.log
```

## How It Works

1. **Invocation**: User invokes skill via Claude Code
2. **PostToolUse Hook**: `track_usage.py` captures invocation → writes to SQLite
3. **SessionStart Hook**: `welcome_stats.py` reads DB → displays statistics
4. **Analysis**: User runs scripts to query/analyze usage patterns

## Welcome Message Format

```
👋 Welcome back! Here are your skill usage statistics:

📊 Overall: 127 invocations across 42 skills (last 30 days)

🔥 Top 5 Most Used:
   1. swift-app-ui          38 uses  (29.9%)
   2. message-rewriter      21 uses  (16.5%)
   ...

💤 Bottom 5 Least Used:
   1. theatre-js             0 uses
   2. sam-audio              1 use
   ...

💡 Suggestions:
   → Consider archiving 8 skills with < 3 total uses
```

## Performance

- Hook overhead: ~10-50ms per invocation
- SQLite write: ~5-20ms (WAL mode)
- Welcome message: ~50-100ms (once per session)
- Total impact: Negligible

## Error Handling

- Hook failures logged to `.claude/skill-usage.log`
- Never blocks skill execution (always exits 0)
- Database locked: 5-second timeout, then skip write
- Auto-creates database on first use

## Dependencies

Python 3.7+ standard library only:
- json
- sqlite3
- pathlib
- datetime
- argparse

No external packages required
