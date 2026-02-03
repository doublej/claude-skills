#!/usr/bin/env python3
"""PostToolUse hook to track skill invocations."""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def log_error(message: str, log_path: Path) -> None:
    """Log errors to file without disrupting workflow."""
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass  # Silently fail - never disrupt workflow


def track_usage() -> None:
    """Track skill usage from PostToolUse hook."""
    try:
        # Read hook data from stdin
        hook_data = json.load(sys.stdin)

        # Only track Skill tool invocations
        if hook_data.get("tool_name") != "Skill":
            sys.exit(0)

        # Extract data
        tool_input = hook_data.get("tool_input", {})
        skill_name = tool_input.get("skill", "unknown")
        args = tool_input.get("args", "")
        session_id = hook_data.get("session_id", "unknown")
        cwd = hook_data.get("cwd", "")
        exit_code = hook_data.get("tool_exit_code", 0)
        success = 1 if exit_code == 0 else 0
        error_message = hook_data.get("error_message")

        # Find project root
        project_root = Path(cwd) if cwd else Path.cwd()
        while not (project_root / ".claude").exists() and project_root != project_root.parent:
            project_root = project_root.parent

        db_path = project_root / ".claude" / "skill-usage.db"
        log_path = project_root / ".claude" / "skill-usage.log"

        # Ensure database exists
        if not db_path.exists():
            db_path.parent.mkdir(parents=True, exist_ok=True)
            conn_init = sqlite3.connect(str(db_path))
            conn_init.execute("PRAGMA journal_mode=WAL")
            conn_init.execute("""
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
            conn_init.execute("CREATE INDEX IF NOT EXISTS idx_skill_name ON skill_usage(skill_name)")
            conn_init.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON skill_usage(timestamp)")
            conn_init.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON skill_usage(session_id)")
            conn_init.commit()
            conn_init.close()

        # Insert record
        conn = sqlite3.connect(str(db_path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")

        timestamp = int(datetime.now().timestamp() * 1000)

        conn.execute("""
            INSERT INTO skill_usage (timestamp, skill_name, session_id, args, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, skill_name, session_id, args or None, success, error_message))

        conn.commit()
        conn.close()

    except Exception as e:
        # Log error but never fail
        try:
            project_root = Path.cwd()
            while not (project_root / ".claude").exists() and project_root != project_root.parent:
                project_root = project_root.parent
            log_path = project_root / ".claude" / "skill-usage.log"
            log_error(f"track_usage error: {e}", log_path)
        except Exception:
            pass

    sys.exit(0)


if __name__ == "__main__":
    track_usage()
