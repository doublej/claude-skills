#!/usr/bin/env python3
"""Initialize the skill usage tracking database."""

import sqlite3
import sys
from pathlib import Path


def init_database(db_path: Path) -> None:
    """Create the skill usage database with schema."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")

    cursor = conn.cursor()

    # Create main table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            session_id TEXT NOT NULL,
            args TEXT,
            success INTEGER NOT NULL DEFAULT 1,
            error_message TEXT
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_skill_name ON skill_usage(skill_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON skill_usage(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON skill_usage(session_id)")

    conn.commit()
    conn.close()

    print(f"Database initialized at {db_path}")


if __name__ == "__main__":
    # Default to .claude/skill-usage.db in project root
    project_root = Path.cwd()
    while not (project_root / ".claude").exists() and project_root != project_root.parent:
        project_root = project_root.parent

    db_path = project_root / ".claude" / "skill-usage.db"

    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])

    init_database(db_path)
