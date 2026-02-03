#!/usr/bin/env python3
"""Generate comprehensive skill usage statistics."""

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_db_path() -> Path:
    """Find the skill-usage.db in project .claude directory."""
    project_root = Path.cwd()
    while not (project_root / ".claude").exists() and project_root != project_root.parent:
        project_root = project_root.parent

    db_path = project_root / ".claude" / "skill-usage.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    return db_path


def generate_statistics(conn: sqlite3.Connection) -> None:
    """Generate comprehensive statistics report."""
    cursor = conn.cursor()

    # Overall statistics
    cursor.execute("SELECT COUNT(*) FROM skill_usage")
    total_invocations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT skill_name) FROM skill_usage")
    unique_skills = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM skill_usage")
    min_ts, max_ts = cursor.fetchone()

    if min_ts and max_ts:
        min_date = datetime.fromtimestamp(min_ts / 1000)
        max_date = datetime.fromtimestamp(max_ts / 1000)
        date_range = f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
    else:
        date_range = "N/A"

    # Success rate
    cursor.execute("SELECT COUNT(*) FROM skill_usage WHERE success = 1")
    successful = cursor.fetchone()[0]
    success_rate = (successful / total_invocations * 100) if total_invocations > 0 else 0

    print("=" * 60)
    print("SKILL USAGE STATISTICS")
    print("=" * 60)
    print()
    print(f"Total Invocations:  {total_invocations}")
    print(f"Unique Skills:      {unique_skills}")
    print(f"Date Range:         {date_range}")
    print(f"Success Rate:       {success_rate:.1f}%")
    print()

    # Usage by skill
    cursor.execute("""
        SELECT skill_name, COUNT(*) as count
        FROM skill_usage
        GROUP BY skill_name
        ORDER BY count DESC
    """)

    print("=" * 60)
    print("USAGE BY SKILL")
    print("=" * 60)
    print()
    print(f"{'Skill':<35} {'Uses':>8} {'%':>8}")
    print("-" * 60)

    for skill, count in cursor.fetchall():
        pct = (count / total_invocations * 100) if total_invocations > 0 else 0
        print(f"{skill:<35} {count:>8} {pct:>7.1f}%")

    print()

    # Last 7 days trend
    cutoff_7d = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
    cursor.execute("SELECT COUNT(*) FROM skill_usage WHERE timestamp >= ?", (cutoff_7d,))
    last_7d = cursor.fetchone()[0]

    # Last 30 days trend
    cutoff_30d = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
    cursor.execute("SELECT COUNT(*) FROM skill_usage WHERE timestamp >= ?", (cutoff_30d,))
    last_30d = cursor.fetchone()[0]

    print("=" * 60)
    print("USAGE TRENDS")
    print("=" * 60)
    print()
    print(f"Last 7 days:   {last_7d} invocations ({last_7d/7:.1f}/day)")
    print(f"Last 30 days:  {last_30d} invocations ({last_30d/30:.1f}/day)")
    print()

    # Session analysis
    cursor.execute("SELECT COUNT(DISTINCT session_id) FROM skill_usage")
    total_sessions = cursor.fetchone()[0]

    if total_sessions > 0:
        avg_per_session = total_invocations / total_sessions
        print("=" * 60)
        print("SESSION ANALYSIS")
        print("=" * 60)
        print()
        print(f"Total Sessions:            {total_sessions}")
        print(f"Avg Skills per Session:    {avg_per_session:.1f}")
        print()

    # Success rate by skill
    cursor.execute("""
        SELECT skill_name,
               COUNT(*) as total,
               SUM(success) as successful
        FROM skill_usage
        GROUP BY skill_name
        HAVING total > 1
        ORDER BY (CAST(successful AS FLOAT) / total) ASC
        LIMIT 5
    """)

    low_success = cursor.fetchall()
    if low_success:
        print("=" * 60)
        print("SKILLS WITH LOWER SUCCESS RATES")
        print("=" * 60)
        print()
        print(f"{'Skill':<35} {'Success Rate':>15}")
        print("-" * 60)

        for skill, total, successful in low_success:
            rate = (successful / total * 100) if total > 0 else 0
            print(f"{skill:<35} {rate:>14.1f}%")

        print()

    print("=" * 60)


def main():
    db_path = find_db_path()
    conn = sqlite3.connect(str(db_path))

    try:
        generate_statistics(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
