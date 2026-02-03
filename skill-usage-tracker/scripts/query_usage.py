#!/usr/bin/env python3
"""Query skill usage data from the database."""

import argparse
import json
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


def query_top(conn: sqlite3.Connection, limit: int = 10, days: int | None = None) -> None:
    """Show top N most used skills."""
    cursor = conn.cursor()

    if days:
        cutoff = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        cursor.execute("""
            SELECT skill_name, COUNT(*) as count
            FROM skill_usage
            WHERE timestamp >= ?
            GROUP BY skill_name
            ORDER BY count DESC
            LIMIT ?
        """, (cutoff, limit))
        print(f"Top {limit} skills (last {days} days):")
    else:
        cursor.execute("""
            SELECT skill_name, COUNT(*) as count
            FROM skill_usage
            GROUP BY skill_name
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        print(f"Top {limit} skills (all time):")

    for i, (skill, count) in enumerate(cursor.fetchall(), 1):
        print(f"{i:>3}. {skill:<30} {count:>5} uses")


def query_recent(conn: sqlite3.Connection, days: int = 7) -> None:
    """Show recent usage."""
    cursor = conn.cursor()
    cutoff = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)

    cursor.execute("""
        SELECT timestamp, skill_name, args, success
        FROM skill_usage
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (cutoff,))

    print(f"Recent usage (last {days} days):")
    for row in cursor.fetchall():
        ts_ms, skill, args, success = row
        dt = datetime.fromtimestamp(ts_ms / 1000)
        status = "✓" if success else "✗"
        args_str = f" ({args})" if args else ""
        print(f"{status} {dt.strftime('%Y-%m-%d %H:%M:%S')} {skill}{args_str}")


def query_unused(conn: sqlite3.Connection) -> None:
    """Show skills that have never been used."""
    # This requires knowledge of all available skills
    # For now, just show skills with 0 uses in the database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT skill_name, COUNT(*) as count
        FROM skill_usage
        GROUP BY skill_name
        HAVING count = 0
    """)

    results = cursor.fetchall()
    if results:
        print("Unused skills:")
        for skill, _ in results:
            print(f"  - {skill}")
    else:
        print("No unused skills found in database")


def query_below_threshold(conn: sqlite3.Connection, threshold: int = 3) -> None:
    """Show skills below usage threshold."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT skill_name, COUNT(*) as count
        FROM skill_usage
        GROUP BY skill_name
        HAVING count < ?
        ORDER BY count ASC
    """, (threshold,))

    results = cursor.fetchall()
    if results:
        print(f"Skills with < {threshold} uses:")
        for skill, count in results:
            use_text = "use" if count == 1 else "uses"
            print(f"  - {skill:<30} {count} {use_text}")
    else:
        print(f"No skills found with < {threshold} uses")


def export_data(conn: sqlite3.Connection, output_path: Path) -> None:
    """Export all data to JSONL."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill_usage ORDER BY timestamp")

    columns = [desc[0] for desc in cursor.description]
    count = 0

    with open(output_path, "w") as f:
        for row in cursor.fetchall():
            record = dict(zip(columns, row))
            f.write(json.dumps(record) + "\n")
            count += 1

    print(f"Exported {count} records to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Query skill usage data")
    parser.add_argument("--top", type=int, metavar="N", help="Show top N skills")
    parser.add_argument("--recent", type=int, metavar="DAYS", help="Show usage from last N days")
    parser.add_argument("--unused", action="store_true", help="Show unused skills")
    parser.add_argument("--below-threshold", type=int, metavar="N", help="Show skills with < N uses")
    parser.add_argument("--export", type=str, metavar="FILE", help="Export data to JSONL file")
    parser.add_argument("--days", type=int, help="Filter to last N days (for --top)")

    args = parser.parse_args()

    # Require at least one action
    if not any([args.top, args.recent, args.unused, args.below_threshold, args.export]):
        parser.print_help()
        sys.exit(1)

    db_path = find_db_path()
    conn = sqlite3.connect(str(db_path))

    try:
        if args.top:
            query_top(conn, args.top, args.days)
        if args.recent:
            query_recent(conn, args.recent)
        if args.unused:
            query_unused(conn)
        if args.below_threshold:
            query_below_threshold(conn, args.below_threshold)
        if args.export:
            export_data(conn, Path(args.export))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
