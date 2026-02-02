#!/usr/bin/env python3
"""Search Claude Code session history with smart time windowing."""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
BOX_WIDTH = 60
TIMELINE_WIDTH = 80


# === Box Drawing Framework ===

def box_line(label: str, value: str, label_width: int = 14) -> str:
    """Format a box line with fixed width, truncating/padding as needed."""
    content = f"{label:<{label_width}} {value}"
    if len(content) > BOX_WIDTH - 4:
        content = content[:BOX_WIDTH - 7] + "..."
    return f"║  {content:<{BOX_WIDTH - 4}}  ║"


def box_top() -> str:
    return f"╔{'═' * BOX_WIDTH}╗"


def box_sep() -> str:
    return f"╠{'═' * BOX_WIDTH}╣"


def box_bottom() -> str:
    return f"╚{'═' * BOX_WIDTH}╝"


def box_title(title: str) -> str:
    return f"║  {title:^{BOX_WIDTH - 4}}  ║"


def box_empty() -> str:
    return f"║{' ' * BOX_WIDTH}║"


# === Timeline Generation ===

def generate_timeline(matches: list[dict], windows: list[dict], query: str) -> str:
    """Generate ASCII timeline visualization from search results."""
    if not matches:
        return "No matches to display."

    # Group matches by date
    by_date: dict[str, list[dict]] = {}
    for m in matches:
        ts = m.get("timestamp", "")
        if not ts:
            continue
        date_str = ts[:10]  # YYYY-MM-DD
        if date_str not in by_date:
            by_date[date_str] = []
        by_date[date_str].append(m)

    # Build window lookup by date
    window_by_date: dict[str, list[dict]] = {}
    for w in windows:
        date_str = w["start"][:10]
        if date_str not in window_by_date:
            window_by_date[date_str] = []
        window_by_date[date_str].append(w)

    lines = []
    w = TIMELINE_WIDTH

    # Header
    date_range = f"{min(by_date.keys())} - {max(by_date.keys())}" if len(by_date) > 1 else list(by_date.keys())[0]

    lines.append(f"╔{'═' * w}╗")
    lines.append(f"║{f'TIMELINE: \"{query}\"':^{w}}║")
    lines.append(f"║{date_range:^{w}}║")
    lines.append(f"╠{'═' * w}╣")
    lines.append("")

    # Process each date
    for date_str in sorted(by_date.keys()):
        day_matches = by_date[date_str]
        day_windows = window_by_date.get(date_str, [])

        # Format date header
        try:
            dt = datetime.fromisoformat(date_str)
            date_label = dt.strftime("%b %d")
        except ValueError:
            date_label = date_str

        lines.append(f"  {date_label}   ●{'━' * (w - 12)}●")

        # Group by time window
        for window in sorted(day_windows, key=lambda x: x["start"]):
            time_str = window["start"][11:16]
            dur = f"{window['duration_minutes']:.0f}m"

            lines.append(f"  {time_str}   │ {dur} session")

            # Extract activities from matches in this window
            window_start = datetime.fromisoformat(window["start"].replace("Z", "+00:00"))
            window_end = datetime.fromisoformat(window["end"].replace("Z", "+00:00"))

            activities = extract_activities(day_matches, window_start, window_end)
            for activity in activities[:4]:  # Max 4 per window
                truncated = activity[:w - 14]
                if len(activity) > w - 14:
                    truncated += "..."
                lines.append(f"          │ • {truncated}")

            lines.append(f"          └{'─' * (w - 11)}")

        lines.append("")

    lines.append(f"╚{'═' * w}╝")

    return "\n".join(lines)


def extract_activities(matches: list[dict], start: datetime, end: datetime) -> list[str]:
    """Extract unique activities from matches within a time window."""
    activities = []
    seen = set()

    for m in matches:
        ts_str = m.get("timestamp", "")
        if not ts_str:
            continue
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        if not (start <= ts <= end):
            continue

        preview = m.get("preview", m.get("content", ""))[:100]
        preview = preview.replace("\n", " ").strip()

        # Extract meaningful activity description
        activity = infer_activity(preview, m.get("type", ""))
        if activity and activity not in seen:
            seen.add(activity)
            activities.append(activity)

    return activities


def infer_activity(preview: str, msg_type: str) -> str | None:
    """Infer activity from message preview."""
    preview_lower = preview.lower()
    preview_clean = preview.replace("\n", " ").strip()

    # Skip generic/boilerplate messages
    skip_patterns = [
        "let me", "i'll ", "i will", "now let", "base directory",
        "launching skill", "skill is running", "<bash-stdout>",
        "i'm going to", "i need to"
    ]
    if any(p in preview_lower for p in skip_patterns):
        return None

    # User requests - clean up and return
    if msg_type == "user" and len(preview_clean) > 10:
        # Skip system/technical content
        if preview_clean.startswith(("<", "```", "{")):
            return None
        # Clean and truncate user request
        clean = preview_clean[:70]
        if len(preview_clean) > 70:
            clean += "..."
        return clean

    # Assistant completion messages
    if msg_type == "assistant":
        # Look for completion patterns
        completion_patterns = [
            (r"created.*skill", "Created skill"),
            (r"installed.*skill", "Installed skill"),
            (r"skill.*created", "Skill created"),
            (r"skill.*installed", "Skill installed"),
            (r"done\.", "Task completed"),
            (r"fixed", "Fixed issue"),
            (r"updated", "Updated"),
        ]
        for pattern, label in completion_patterns:
            if re.search(pattern, preview_lower):
                # Try to extract what was created/fixed
                first_sentence = preview_clean.split(".")[0][:60]
                if len(first_sentence) > 15:
                    return first_sentence
                return label

    return None


# === Project Detection ===

def encode_project_path(cwd: str) -> str:
    """Encode project path to Claude's folder naming convention."""
    return cwd.replace("/", "-").replace("_", "-")


def find_project_dir(cwd: str) -> Path | None:
    """Find the Claude project directory for given working directory."""
    encoded = encode_project_path(cwd)
    project_dir = PROJECTS_DIR / encoded

    if project_dir.exists():
        return project_dir

    cwd_normalized = encoded.lower()
    for d in PROJECTS_DIR.iterdir():
        if not d.is_dir():
            continue
        if cwd_normalized == d.name.lower() or cwd_normalized in d.name.lower():
            return d
    return None


def iter_project_sessions(project_dir: Path) -> Iterator[Path]:
    """Iterate session files for a project."""
    for session_file in project_dir.glob("*.jsonl"):
        if not session_file.name.startswith("agent-"):
            yield session_file


# === Message Extraction ===

def extract_all_messages(session_file: Path) -> list[dict]:
    """Extract ALL messages (user + assistant) with source refs."""
    messages = []
    with open(session_file) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("type") not in ("user", "assistant"):
                    continue

                content = entry.get("message", {}).get("content", "")
                if isinstance(content, list):
                    text_parts = [p.get("text", "") for p in content if isinstance(p, dict)]
                    content = "\n".join(text_parts)
                if not isinstance(content, str):
                    continue

                messages.append({
                    "type": entry["type"],
                    "uuid": entry.get("uuid", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "content": content,
                    "session_id": entry.get("sessionId", session_file.stem),
                    "source_file": str(session_file),
                    "source_line": line_num,
                })
            except json.JSONDecodeError:
                continue
    return messages


def parse_timestamp(ts: str) -> datetime | None:
    """Parse ISO timestamp to datetime."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


# === Search & Time Windowing ===

def search_messages(messages: list[dict], query: str, case_insensitive: bool = True) -> list[dict]:
    """Find messages containing the exact query phrase."""
    flags = re.IGNORECASE if case_insensitive else 0
    pattern = re.escape(query)
    regex = re.compile(pattern, flags)

    matches = []
    for msg in messages:
        if regex.search(msg["content"]):
            matches.append(msg)
    return matches


def build_time_windows(
    matches: list[dict],
    margin_minutes: int = 5,
    gap_minutes: int = 10
) -> list[tuple[datetime, datetime]]:
    """Build time windows around matches, merging nearby ones."""
    if not matches:
        return []

    timestamps = []
    for m in matches:
        dt = parse_timestamp(m["timestamp"])
        if dt:
            timestamps.append(dt)

    if not timestamps:
        return []

    timestamps.sort()
    margin = timedelta(minutes=margin_minutes)
    gap = timedelta(minutes=gap_minutes)

    windows = []
    current_start = timestamps[0] - margin
    current_end = timestamps[0] + margin

    for ts in timestamps[1:]:
        window_start = ts - margin
        window_end = ts + margin

        if window_start <= current_end + gap:
            current_end = max(current_end, window_end)
        else:
            windows.append((current_start, current_end))
            current_start = window_start
            current_end = window_end

    windows.append((current_start, current_end))
    return windows


def extract_window_messages(
    messages: list[dict],
    windows: list[tuple[datetime, datetime]]
) -> list[dict]:
    """Extract all messages falling within any time window."""
    result = []
    for msg in messages:
        ts = parse_timestamp(msg["timestamp"])
        if not ts:
            continue
        for start, end in windows:
            if start <= ts <= end:
                result.append(msg)
                break
    return result


# === Main Search Function ===

def search_project(
    cwd: str,
    query: str,
    margin_minutes: int = 5,
    gap_minutes: int = 10,
    output_dir: Path | None = None
) -> dict:
    """Search project history and extract context around matches."""
    project_dir = find_project_dir(cwd)
    if not project_dir:
        return {"error": f"No history found for {cwd}"}

    all_messages = []
    for session_file in iter_project_sessions(project_dir):
        messages = extract_all_messages(session_file)
        all_messages.extend(messages)

    all_messages.sort(key=lambda m: m.get("timestamp", ""))

    matches = search_messages(all_messages, query)
    if not matches:
        return {
            "project": cwd,
            "query": query,
            "match_count": 0,
            "window_count": 0,
            "context_messages": 0,
            "windows": [],
        }

    windows = build_time_windows(matches, margin_minutes, gap_minutes)
    context_messages = extract_window_messages(all_messages, windows)

    result = {
        "project": cwd,
        "query": query,
        "match_count": len(matches),
        "window_count": len(windows),
        "context_messages": len(context_messages),
        "windows": [
            {
                "start": w[0].isoformat(),
                "end": w[1].isoformat(),
                "duration_minutes": (w[1] - w[0]).total_seconds() / 60
            }
            for w in windows
        ],
    }

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

        index_file = output_dir / "search_index.json"
        with open(index_file, "w") as f:
            json.dump({
                "query": query,
                "match_count": len(matches),
                "windows": result["windows"],
                "matches": [
                    {
                        "timestamp": m["timestamp"],
                        "type": m["type"],
                        "session_id": m["session_id"],
                        "preview": m["content"][:100].replace("\n", " "),
                    }
                    for m in matches
                ]
            }, f, indent=2)

        messages_file = output_dir / "context_messages.json"
        with open(messages_file, "w") as f:
            json.dump(context_messages, f, indent=2)

        result["index_file"] = str(index_file)
        result["messages_file"] = str(messages_file)

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Search Claude Code Session History",
        epilog="Example: search_session.py 'design skill' -t"
    )
    parser.add_argument("query", nargs="+", help="Search phrase (joined as exact match)")
    parser.add_argument("-p", "--project", type=str, default=os.getcwd(),
                       help="Project directory (default: current)")
    parser.add_argument("-m", "--margin", type=int, default=5,
                       help="Minutes of context before/after matches (default: 5)")
    parser.add_argument("-g", "--gap", type=int, default=10,
                       help="Max gap in minutes to merge windows (default: 10)")
    parser.add_argument("-o", "--output", type=str, default=None,
                       help="Output directory for results (optional)")
    parser.add_argument("-t", "--timeline", action="store_true",
                       help="Generate visual timeline")
    args = parser.parse_args()

    # Join query parts into single phrase for exact matching
    query = " ".join(args.query)

    output_dir = Path(args.output) if args.output else None
    result = search_project(
        args.project,
        query,
        args.margin,
        args.gap,
        output_dir
    )

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print()
    print(box_top())
    print(box_title("SESSION SEARCH RESULTS"))
    print(box_sep())
    print(box_empty())
    print(box_line("Query:", f'"{result["query"]}"'))
    print(box_line("Matches:", str(result["match_count"])))
    print(box_line("Time windows:", str(result["window_count"])))
    print(box_line("Context msgs:", str(result["context_messages"])))
    print(box_empty())

    if result["windows"]:
        print(box_sep())
        print(box_title("TIME WINDOWS"))
        print(box_sep())
        for i, w in enumerate(result["windows"][:5], 1):
            start = w["start"][:16].replace("T", " ")
            dur = f"{w['duration_minutes']:.0f}m"
            print(box_line(f"Window {i}:", f"{start} ({dur})"))
        if len(result["windows"]) > 5:
            print(box_line("", f"... +{len(result['windows']) - 5} more"))
        print(box_empty())

    print(box_bottom())
    print()

    if output_dir:
        print(f"Results saved to: {output_dir}/")

    # Generate timeline if requested
    if args.timeline and output_dir and result["match_count"] > 0:
        index_file = output_dir / "search_index.json"
        if index_file.exists():
            with open(index_file) as f:
                index_data = json.load(f)

            timeline = generate_timeline(
                index_data.get("matches", []),
                result["windows"],
                result["query"]
            )

            # Save timeline
            timeline_file = output_dir / "timeline.txt"
            with open(timeline_file, "w") as f:
                f.write(timeline)

            print()
            print(timeline)
            print()
            print(f"Timeline saved to: {timeline_file}")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
