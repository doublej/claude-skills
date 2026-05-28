#!/usr/bin/env python3
"""Check the age of the skill's best practices information."""

import json
from datetime import datetime, timedelta
from pathlib import Path

def check_age():
    """Check age and warn if information is stale."""
    skill_dir = Path(__file__).parent.parent
    metadata_file = skill_dir / "METADATA.json"

    if not metadata_file.exists():
        return "⚠️  Metadata file not found"

    with open(metadata_file) as f:
        metadata = json.load(f)

    # Freshness is measured from when the best practices were last authored,
    # not the immutable creation date — otherwise an updated skill reads as stale.
    anchor = metadata.get("best_practices_date", metadata["created_date"])
    anchor_date = datetime.fromisoformat(anchor)
    today = datetime.now()
    age_days = (today - anchor_date).days

    # Format age
    if age_days == 0:
        age_str = "today"
    elif age_days == 1:
        age_str = "1 day old"
    elif age_days < 7:
        age_str = f"{age_days} days old"
    elif age_days < 30:
        weeks = age_days // 7
        age_str = f"{weeks} week{'s' if weeks != 1 else ''} old"
    else:
        months = age_days // 30
        age_str = f"{months} month{'s' if months != 1 else ''} old"

    # Warning if > 6 weeks (42 days)
    warning = ""
    if age_days > 42:
        warning = "\n\n⚠️  WARNING: This information is more than 6 weeks old. Consider updating with latest best practices."

    return f"""📅 Best Practices Information Age: {age_str}
📝 Last authored: {anchor}
🤖 Model Context: {metadata['model_context']}
🧠 Knowledge Base: {metadata['knowledge_cutoff']}{warning}"""

if __name__ == "__main__":
    print(check_age())
