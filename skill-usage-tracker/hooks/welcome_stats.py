#!/usr/bin/env python3
"""SessionStart hook to display skill usage statistics."""

import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_stats(db_path: Path, days: int = 30) -> dict | None:
    """Query database for usage statistics."""
    if not db_path.exists():
        return None

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Calculate date range
    cutoff = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)

    # Total invocations
    cursor.execute("SELECT COUNT(*) FROM skill_usage WHERE timestamp >= ?", (cutoff,))
    total_uses = cursor.fetchone()[0]

    # Skill counts
    cursor.execute("""
        SELECT skill_name, COUNT(*) as count
        FROM skill_usage
        WHERE timestamp >= ?
        GROUP BY skill_name
        ORDER BY count DESC
    """, (cutoff,))
    skill_counts = cursor.fetchall()

    conn.close()

    return {
        "total_uses": total_uses,
        "skill_counts": skill_counts,
        "days": days
    }


def generate_suggestions(skill_counts: list, threshold: int = 3) -> list:
    """Generate actionable suggestions based on usage patterns."""
    suggestions = []

    # Convert skill_counts to dict
    usage_dict = {skill: count for skill, count in skill_counts}

    # Find unused or rarely used skills
    low_usage = [skill for skill, count in usage_dict.items() if count < threshold]

    if low_usage:
        suggestions.append(f"→ Consider archiving {len(low_usage)} skills with < {threshold} total uses")

    return suggestions


def display_welcome_stats() -> None:
    """Display welcome statistics on session start."""
    # Check if disabled
    if os.environ.get("SKILL_STATS_ENABLED") == "0":
        sys.exit(0)

    try:
        # Find project root
        project_root = Path.cwd()
        while not (project_root / ".claude").exists() and project_root != project_root.parent:
            project_root = project_root.parent

        db_path = project_root / ".claude" / "skill-usage.db"

        if not db_path.exists():
            # No data yet
            sys.exit(0)

        stats = get_stats(db_path)
        if not stats or stats["total_uses"] == 0:
            sys.exit(0)

        skill_counts = stats["skill_counts"]
        total_uses = stats["total_uses"]
        days = stats["days"]

        # Build output
        output = [
            "👋 Welcome back! Here are your skill usage statistics:",
            "",
            f"📊 Overall: {total_uses} invocations across {len(skill_counts)} skills (last {days} days)",
            ""
        ]

        # Top 5
        top_5 = skill_counts[:5]
        if top_5:
            output.append("🔥 Top 5 Most Used:")
            for i, (skill, count) in enumerate(top_5, 1):
                pct = (count / total_uses) * 100
                output.append(f"   {i}. {skill:<25} {count:>3} uses  ({pct:>5.1f}%)")
            output.append("")

        # Bottom 5
        bottom_5 = sorted(skill_counts, key=lambda x: x[1])[:5]
        if len(skill_counts) > 5 and bottom_5:
            output.append("💤 Bottom 5 Least Used:")
            for i, (skill, count) in enumerate(bottom_5, 1):
                use_text = "use" if count == 1 else "uses"
                output.append(f"   {i}. {skill:<25} {count} {use_text}")
            output.append("")

        # Suggestions
        suggestions = generate_suggestions(skill_counts)
        if suggestions:
            output.append("💡 Suggestions:")
            for suggestion in suggestions:
                output.append(f"   {suggestion}")
            output.append("")

        # Footer
        output.append("Type 'python3 skill-usage-tracker/scripts/query_usage.py' for detailed analysis")

        print("\n".join(output))

    except Exception:
        # Silently fail - never disrupt workflow
        pass

    sys.exit(0)


if __name__ == "__main__":
    display_welcome_stats()
