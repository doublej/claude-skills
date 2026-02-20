#!/usr/bin/env python3
"""Unified Claude Code session history: search, scan, extract with multi-project support."""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
CHARS_PER_TOKEN = 4
BOX_WIDTH = 60
TIMELINE_WIDTH = 80


# ── Box Drawing ──────────────────────────────────────────────

def box_line(label: str, value: str, label_width: int = 14) -> str:
    content = f"{label:<{label_width}} {value}"
    if len(content) > BOX_WIDTH - 4:
        content = content[: BOX_WIDTH - 7] + "..."
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


# ── Project Discovery ────────────────────────────────────────

def encode_project_path(cwd: str) -> str:
    return cwd.replace("/", "-").replace("_", "-")


def find_project_dir(cwd: str) -> Path | None:
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
    for session_file in project_dir.glob("*.jsonl"):
        if not session_file.name.startswith("agent-"):
            yield session_file


def discover_projects(
    folder: str | None = None,
    since_minutes: int | None = None,
) -> list[dict]:
    """Discover projects using sessions-index.json for fast filtering.

    Returns list of {project_dir, project_path, session_entries}.
    """
    now_ms = datetime.now().timestamp() * 1000
    cutoff_ms = (now_ms - since_minutes * 60 * 1000) if since_minutes else None
    results = []

    for index_file in PROJECTS_DIR.glob("*/sessions-index.json"):
        project_dir = index_file.parent
        # skip archive dirs
        if "_archive" in project_dir.parts:
            continue
        try:
            data = json.loads(index_file.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        entries = data.get("entries", [])
        if not entries:
            continue

        project_path = entries[0].get("projectPath", "")

        # folder filter: projectPath must start with the given folder
        if folder:
            norm_folder = str(Path(folder).resolve())
            if not project_path.startswith(norm_folder):
                continue

        # time filter: keep only entries modified after cutoff
        if cutoff_ms:
            entries = [e for e in entries if e.get("fileMtime", 0) >= cutoff_ms]
            if not entries:
                continue

        results.append({
            "project_dir": project_dir,
            "project_path": project_path,
            "session_entries": entries,
        })

    results.sort(key=lambda r: r["project_path"])
    return results


def resolve_projects(args) -> list[dict]:
    """Resolve project scope from CLI args into a list of project dicts."""
    if args.all_projects:
        return discover_projects(
            since_minutes=getattr(args, "since", None),
        )
    if args.folder:
        return discover_projects(
            folder=args.folder,
            since_minutes=getattr(args, "since", None),
        )
    # single project
    project_dir = find_project_dir(args.project)
    if not project_dir:
        return []
    return [{"project_dir": project_dir, "project_path": args.project, "session_entries": None}]


def iter_sessions_for_project(proj: dict, since_minutes: int | None = None) -> Iterator[Path]:
    """Yield session files for a project dict, optionally time-filtered."""
    if proj["session_entries"] is not None:
        cutoff_ms = None
        if since_minutes:
            cutoff_ms = datetime.now().timestamp() * 1000 - since_minutes * 60 * 1000
        for entry in proj["session_entries"]:
            if cutoff_ms and entry.get("fileMtime", 0) < cutoff_ms:
                continue
            p = Path(entry["fullPath"])
            if p.exists():
                yield p
    else:
        for sf in iter_project_sessions(proj["project_dir"]):
            if since_minutes:
                cutoff = datetime.now().timestamp() - since_minutes * 60
                if sf.stat().st_mtime < cutoff:
                    continue
            yield sf


# ── Message Extraction ───────────────────────────────────────

def extract_messages(session_file: Path) -> list[dict]:
    """Extract messages with source refs, including speak MCP interactions."""
    messages = []
    speak_questions = {}

    with open(session_file) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") not in ("user", "assistant"):
                continue

            msg_content = entry.get("message", {}).get("content", "")
            session_id = entry.get("sessionId", session_file.stem)
            timestamp = entry.get("timestamp", "")
            uuid = entry.get("uuid", "")

            if isinstance(msg_content, list):
                for block in msg_content:
                    if not isinstance(block, dict):
                        continue
                    # speak MCP questions from assistant
                    if block.get("type") == "tool_use" and "speak" in block.get("name", ""):
                        tool_id = block.get("id", "")
                        inp = block.get("input", {})
                        question = inp.get("prompt") or inp.get("message", "")
                        if tool_id and question:
                            speak_questions[tool_id] = question
                    # speak MCP responses from user
                    if block.get("type") == "tool_result":
                        tool_id = block.get("tool_use_id", "")
                        if tool_id in speak_questions:
                            answer = _parse_speak_answer(block)
                            if answer:
                                messages.append({
                                    "type": "user",
                                    "uuid": uuid,
                                    "timestamp": timestamp,
                                    "content": f"[Dialog] Q: {speak_questions[tool_id]}\nA: {answer}",
                                    "session_id": session_id,
                                    "source_file": str(session_file),
                                    "source_line": line_num,
                                    "is_speak_mcp": True,
                                })

                text_parts = [
                    p.get("text", "")
                    for p in msg_content
                    if isinstance(p, dict) and p.get("type") == "text"
                ]
                msg_content = "\n".join(text_parts)

            if not isinstance(msg_content, str) or not msg_content.strip():
                continue

            messages.append({
                "type": entry["type"],
                "uuid": uuid,
                "timestamp": timestamp,
                "content": msg_content,
                "session_id": session_id,
                "source_file": str(session_file),
                "source_line": line_num,
            })
    return messages


def _parse_speak_answer(block: dict) -> str | None:
    result_content = block.get("content", "")
    if not isinstance(result_content, list):
        return None
    for rc in result_content:
        if not isinstance(rc, dict) or rc.get("type") != "text":
            continue
        try:
            resp = json.loads(rc.get("text", "{}"))
        except json.JSONDecodeError:
            continue
        if resp.get("cancelled") and len(resp) <= 2:
            return "[Cancelled]"
        if resp.get("confirmed") and len(resp) <= 2:
            return "[Confirmed]"
        if resp.get("cancelled"):
            continue
        skip_keys = {"cancelled", "confirmed", "success", "error"}
        for k, v in resp.items():
            if k in skip_keys:
                continue
            if isinstance(v, str) and v:
                return v
            if isinstance(v, list):
                return ", ".join(str(x) for x in v)
    return None


def is_system_noise(content: str) -> bool:
    if not content:
        return True
    prefixes = ("<local-command-stdout>", "<command-name>/", "<system-reminder>")
    if any(content.startswith(p) for p in prefixes):
        return True
    if "Caveat: The messages below were generated" in content:
        return True
    if content.strip().startswith("[Request interrupted"):
        return True
    return False


def filter_user_messages(messages: list[dict]) -> list[dict]:
    return [m for m in messages if m["type"] == "user" and not is_system_noise(m["content"])]


def estimate_tokens(messages: list[dict]) -> int:
    return sum(len(m["content"]) for m in messages) // CHARS_PER_TOKEN


def parse_timestamp(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


# ── Search & Time Windowing ──────────────────────────────────

def search_messages(messages: list[dict], query: str) -> list[dict]:
    regex = re.compile(re.escape(query), re.IGNORECASE)
    return [m for m in messages if regex.search(m["content"])]


def build_time_windows(
    matches: list[dict],
    margin_minutes: int = 5,
    gap_minutes: int = 10,
) -> list[tuple[datetime, datetime]]:
    timestamps = sorted(filter(None, (parse_timestamp(m["timestamp"]) for m in matches)))
    if not timestamps:
        return []

    margin = timedelta(minutes=margin_minutes)
    gap = timedelta(minutes=gap_minutes)
    windows = []
    start = timestamps[0] - margin
    end = timestamps[0] + margin

    for ts in timestamps[1:]:
        ws, we = ts - margin, ts + margin
        if ws <= end + gap:
            end = max(end, we)
        else:
            windows.append((start, end))
            start, end = ws, we

    windows.append((start, end))
    return windows


def extract_window_messages(
    messages: list[dict],
    windows: list[tuple[datetime, datetime]],
) -> list[dict]:
    result = []
    for msg in messages:
        ts = parse_timestamp(msg["timestamp"])
        if not ts:
            continue
        for s, e in windows:
            if s <= ts <= e:
                result.append(msg)
                break
    return result


# ── Timeline Generation ──────────────────────────────────────

def generate_timeline(matches: list[dict], windows: list[dict], query: str, project_label: str | None = None) -> str:
    if not matches:
        return "No matches to display."

    by_date: dict[str, list[dict]] = {}
    for m in matches:
        ts = m.get("timestamp", "")
        if not ts:
            continue
        date_str = ts[:10]
        by_date.setdefault(date_str, []).append(m)

    window_by_date: dict[str, list[dict]] = {}
    for w in windows:
        date_str = w["start"][:10]
        window_by_date.setdefault(date_str, []).append(w)

    lines = []
    w = TIMELINE_WIDTH
    dates = sorted(by_date.keys())
    date_range = f"{dates[0]} - {dates[-1]}" if len(dates) > 1 else dates[0]

    lines.append(f"╔{'═' * w}╗")
    title = f'TIMELINE: "{query}"'
    if project_label:
        title = f"{project_label} | {title}"
    lines.append(f"║{title:^{w}}║")
    lines.append(f"║{date_range:^{w}}║")
    lines.append(f"╠{'═' * w}╣")
    lines.append("")

    for date_str in dates:
        day_matches = by_date[date_str]
        day_windows = window_by_date.get(date_str, [])

        try:
            date_label = datetime.fromisoformat(date_str).strftime("%b %d")
        except ValueError:
            date_label = date_str

        lines.append(f"  {date_label}   ●{'━' * (w - 12)}●")

        for window in sorted(day_windows, key=lambda x: x["start"]):
            time_str = window["start"][11:16]
            dur = f"{window['duration_minutes']:.0f}m"
            lines.append(f"  {time_str}   │ {dur} session")

            ws = datetime.fromisoformat(window["start"].replace("Z", "+00:00"))
            we = datetime.fromisoformat(window["end"].replace("Z", "+00:00"))
            for activity in _extract_activities(day_matches, ws, we)[:4]:
                truncated = activity[: w - 14]
                if len(activity) > w - 14:
                    truncated += "..."
                lines.append(f"          │ • {truncated}")
            lines.append(f"          └{'─' * (w - 11)}")
        lines.append("")

    lines.append(f"╚{'═' * w}╝")
    return "\n".join(lines)


def _extract_activities(matches: list[dict], start: datetime, end: datetime) -> list[str]:
    activities = []
    seen: set[str] = set()
    for m in matches:
        ts = parse_timestamp(m.get("timestamp", ""))
        if not ts or not (start <= ts <= end):
            continue
        preview = m.get("preview", m.get("content", ""))[:100].replace("\n", " ").strip()
        activity = _infer_activity(preview, m.get("type", ""))
        if activity and activity not in seen:
            seen.add(activity)
            activities.append(activity)
    return activities


def _infer_activity(preview: str, msg_type: str) -> str | None:
    preview_lower = preview.lower()
    preview_clean = preview.replace("\n", " ").strip()

    skip = [
        "let me", "i'll ", "i will", "now let", "base directory",
        "launching skill", "skill is running", "<bash-stdout>",
        "i'm going to", "i need to",
    ]
    if any(p in preview_lower for p in skip):
        return None

    if msg_type == "user" and len(preview_clean) > 10:
        if preview_clean.startswith(("<", "```", "{")):
            return None
        clean = preview_clean[:70]
        return clean + "..." if len(preview_clean) > 70 else clean

    if msg_type == "assistant":
        patterns = [
            (r"created.*skill", "Created skill"),
            (r"installed.*skill", "Installed skill"),
            (r"skill.*created", "Skill created"),
            (r"skill.*installed", "Skill installed"),
            (r"done\.", "Task completed"),
            (r"fixed", "Fixed issue"),
            (r"updated", "Updated"),
        ]
        for pattern, label in patterns:
            if re.search(pattern, preview_lower):
                first_sentence = preview_clean.split(".")[0][:60]
                return first_sentence if len(first_sentence) > 15 else label

    return None


# ── Subcommand: search ───────────────────────────────────────

def cmd_search(args):
    query = " ".join(args.query)
    projects = resolve_projects(args)
    if not projects:
        print(f"Error: No projects found for scope")
        sys.exit(1)

    output_dir = Path(args.output) if args.output else None
    all_results = []

    for proj in projects:
        all_messages = []
        for sf in iter_sessions_for_project(proj, getattr(args, "since", None)):
            all_messages.extend(extract_messages(sf))
        all_messages.sort(key=lambda m: m.get("timestamp", ""))

        matches = search_messages(all_messages, query)
        if not matches:
            continue

        windows = build_time_windows(matches, args.margin, args.gap)
        context_messages = extract_window_messages(all_messages, windows)

        result = {
            "project": proj["project_path"],
            "query": query,
            "match_count": len(matches),
            "window_count": len(windows),
            "context_messages": len(context_messages),
            "windows": [
                {
                    "start": w[0].isoformat(),
                    "end": w[1].isoformat(),
                    "duration_minutes": (w[1] - w[0]).total_seconds() / 60,
                }
                for w in windows
            ],
            "matches_data": matches,
            "context_data": context_messages,
        }
        all_results.append(result)

    if not all_results:
        print()
        print(box_top())
        print(box_title("SESSION SEARCH RESULTS"))
        print(box_sep())
        print(box_empty())
        print(box_line("Query:", f'"{query}"'))
        print(box_line("Matches:", "0"))
        print(box_empty())
        print(box_bottom())
        print()
        sys.exit(0)

    # Print summary
    total_matches = sum(r["match_count"] for r in all_results)
    total_windows = sum(r["window_count"] for r in all_results)
    total_ctx = sum(r["context_messages"] for r in all_results)

    print()
    print(box_top())
    print(box_title("SESSION SEARCH RESULTS"))
    print(box_sep())
    print(box_empty())
    print(box_line("Query:", f'"{query}"'))
    print(box_line("Projects:", str(len(all_results))))
    print(box_line("Matches:", str(total_matches)))
    print(box_line("Time windows:", str(total_windows)))
    print(box_line("Context msgs:", str(total_ctx)))
    print(box_empty())

    for r in all_results:
        print(box_sep())
        proj_name = Path(r["project"]).name or r["project"]
        print(box_title(proj_name))
        print(box_sep())
        print(box_line("Matches:", str(r["match_count"])))
        print(box_line("Windows:", str(r["window_count"])))
        for i, w in enumerate(r["windows"][:3], 1):
            start = w["start"][:16].replace("T", " ")
            dur = f"{w['duration_minutes']:.0f}m"
            print(box_line(f"  Window {i}:", f"{start} ({dur})"))
        if len(r["windows"]) > 3:
            print(box_line("", f"... +{len(r['windows']) - 3} more"))
        print(box_empty())

    print(box_bottom())
    print()

    # Save output
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build serialisable results (strip raw data)
        serialisable = []
        for r in all_results:
            sr = {k: v for k, v in r.items() if k not in ("matches_data", "context_data")}
            sr["matches"] = [
                {
                    "timestamp": m["timestamp"],
                    "type": m["type"],
                    "session_id": m["session_id"],
                    "preview": m["content"][:100].replace("\n", " "),
                }
                for m in r["matches_data"]
            ]
            serialisable.append(sr)

        with open(output_dir / "search_index.json", "w") as f:
            json.dump({"query": query, "projects": serialisable}, f, indent=2)

        # Collect all context messages
        all_ctx = []
        for r in all_results:
            for m in r["context_data"]:
                m_copy = {k: v for k, v in m.items()}
                m_copy["project"] = r["project"]
                all_ctx.append(m_copy)
        all_ctx.sort(key=lambda m: m.get("timestamp", ""))

        with open(output_dir / "context_messages.json", "w") as f:
            json.dump(all_ctx, f, indent=2)

        print(f"Results saved to: {output_dir}/")

    # Timeline
    if args.timeline and output_dir:
        timeline_parts = []
        for r in all_results:
            proj_label = Path(r["project"]).name if len(all_results) > 1 else None
            match_previews = [
                {
                    "timestamp": m["timestamp"],
                    "type": m["type"],
                    "preview": m["content"][:100].replace("\n", " "),
                }
                for m in r["matches_data"]
            ]
            tl = generate_timeline(match_previews, r["windows"], query, proj_label)
            timeline_parts.append(tl)

        timeline = "\n\n".join(timeline_parts)
        with open(output_dir / "timeline.txt", "w") as f:
            f.write(timeline)

        print()
        print(timeline)
        print()
        print(f"Timeline saved to: {output_dir / 'timeline.txt'}")

    # JSON output
    output = {
        "query": query,
        "total_matches": total_matches,
        "total_windows": total_windows,
        "total_context_messages": total_ctx,
        "project_count": len(all_results),
        "projects": [
            {k: v for k, v in r.items() if k not in ("matches_data", "context_data")}
            for r in all_results
        ],
    }
    print(json.dumps(output, indent=2))


# ── Subcommand: scan ─────────────────────────────────────────

def cmd_scan(args):
    projects = resolve_projects(args)
    if not projects:
        print("Error: No projects found for scope")
        sys.exit(1)

    all_stats = []
    for proj in projects:
        all_messages = []
        session_count = 0
        for sf in iter_sessions_for_project(proj, getattr(args, "since", None)):
            session_count += 1
            all_messages.extend(extract_messages(sf))

        all_messages.sort(key=lambda m: m.get("timestamp", ""))
        user_messages = filter_user_messages(all_messages)

        stats = {
            "project": proj["project_path"],
            "project_dir": str(proj["project_dir"]),
            "session_count": session_count,
            "total_messages": len(all_messages),
            "user_messages": len(user_messages),
            "estimated_tokens": estimate_tokens(all_messages),
            "user_tokens": estimate_tokens(user_messages),
            "oldest": all_messages[0]["timestamp"][:10] if all_messages else None,
            "newest": all_messages[-1]["timestamp"][:10] if all_messages else None,
        }
        all_stats.append(stats)

    # Display
    for stats in all_stats:
        proj_name = Path(stats["project"]).name or stats["project"]
        date_range = f"{stats['oldest'] or 'N/A'} to {stats['newest'] or 'N/A'}"
        print()
        print(box_top())
        print(box_title("PROJECT HISTORY SCAN"))
        print(box_sep())
        print(box_empty())
        print(box_line("Project:", proj_name))
        print(box_line("Sessions:", str(stats["session_count"])))
        print(box_line("Total msgs:", str(stats["total_messages"])))
        print(box_line("User msgs:", str(stats["user_messages"])))
        print(box_empty())
        print(box_line("Date range:", date_range))
        print(box_line("Est. tokens:", str(stats["user_tokens"])))
        print(box_empty())
        print(box_bottom())

    print()
    if len(all_stats) > 1:
        total_sessions = sum(s["session_count"] for s in all_stats)
        total_msgs = sum(s["total_messages"] for s in all_stats)
        total_user = sum(s["user_messages"] for s in all_stats)
        total_tokens = sum(s["user_tokens"] for s in all_stats)
        print(box_top())
        print(box_title("TOTALS"))
        print(box_sep())
        print(box_empty())
        print(box_line("Projects:", str(len(all_stats))))
        print(box_line("Sessions:", str(total_sessions)))
        print(box_line("Total msgs:", str(total_msgs)))
        print(box_line("User msgs:", str(total_user)))
        print(box_line("Est. tokens:", str(total_tokens)))
        print(box_empty())
        print(box_bottom())
        print()

    print(json.dumps(all_stats if len(all_stats) > 1 else all_stats[0], indent=2))


# ── Subcommand: extract ──────────────────────────────────────

def cmd_extract(args):
    projects = resolve_projects(args)
    if not projects:
        print("Error: No projects found for scope")
        sys.exit(1)

    output_dir = Path(args.output)
    all_results = []

    for proj in projects:
        all_messages = []
        for sf in iter_sessions_for_project(proj, getattr(args, "since", None)):
            all_messages.extend(extract_messages(sf))

        all_messages.sort(key=lambda m: m.get("timestamp", ""), reverse=True)
        user_messages = filter_user_messages(all_messages)[: args.limit]
        user_messages.reverse()

        if not user_messages:
            continue

        # Per-project subdirectory when multi-project
        if len(projects) > 1:
            proj_name = Path(proj["project_path"]).name or "unknown"
            proj_output = output_dir / proj_name
        else:
            proj_output = output_dir

        proj_output.mkdir(parents=True, exist_ok=True)

        index = [
            {
                "timestamp": m["timestamp"],
                "session_id": m["session_id"],
                "uuid": m["uuid"],
                "source_file": m["source_file"],
                "source_line": m["source_line"],
                "preview": m["content"][:100].replace("\n", " "),
                "char_count": len(m["content"]),
            }
            for m in user_messages
        ]

        with open(proj_output / "message_index.json", "w") as f:
            json.dump(index, f, indent=2)
        with open(proj_output / "user_messages.json", "w") as f:
            json.dump(user_messages, f, indent=2)

        result = {
            "project": proj["project_path"],
            "message_count": len(user_messages),
            "estimated_tokens": estimate_tokens(user_messages),
            "index_file": str(proj_output / "message_index.json"),
            "messages_file": str(proj_output / "user_messages.json"),
            "time_range": (
                f"{user_messages[0]['timestamp'][:10]} to {user_messages[-1]['timestamp'][:10]}"
                if user_messages
                else None
            ),
        }
        all_results.append(result)

    if not all_results:
        print("Error: No messages found")
        sys.exit(1)

    for result in all_results:
        proj_name = Path(result["project"]).name or result["project"]
        print()
        print(box_top())
        print(box_title("EXTRACTION COMPLETE"))
        print(box_sep())
        print(box_empty())
        print(box_line("Project:", proj_name))
        print(box_line("Messages:", str(result["message_count"])))
        print(box_line("Est. tokens:", str(result["estimated_tokens"])))
        print(box_line("Time range:", result["time_range"] or "N/A"))
        print(box_empty())
        print(box_bottom())

    print()
    print(json.dumps(all_results if len(all_results) > 1 else all_results[0], indent=2))


# ── CLI ──────────────────────────────────────────────────────

def add_scope_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-p", "--project", type=str, default=os.getcwd(),
        help="Project directory (default: cwd)",
    )
    parser.add_argument(
        "--all-projects", action="store_true",
        help="Search all projects under ~/.claude/projects/",
    )
    parser.add_argument(
        "--folder", type=str, default=None,
        help="All projects whose projectPath starts with PATH",
    )
    parser.add_argument(
        "--since", type=int, default=None,
        help="Only sessions modified in past N minutes",
    )
    parser.add_argument(
        "-o", "--output", type=str, default=".session-search",
        help="Output directory (default: .session-search)",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Session History Tool",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    sp_search = sub.add_parser("search", help="Search for a phrase in session history")
    sp_search.add_argument("query", nargs="+", help="Search phrase")
    sp_search.add_argument("-m", "--margin", type=int, default=5, help="Context margin minutes")
    sp_search.add_argument("-g", "--gap", type=int, default=10, help="Merge gap minutes")
    sp_search.add_argument("-t", "--timeline", action="store_true", help="Generate timeline")
    add_scope_args(sp_search)

    # scan
    sp_scan = sub.add_parser("scan", help="Scan project history stats")
    add_scope_args(sp_scan)

    # extract
    sp_extract = sub.add_parser("extract", help="Extract recent user messages")
    sp_extract.add_argument("-n", "--limit", type=int, default=100, help="Message count limit")
    add_scope_args(sp_extract)

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "scan":
        cmd_scan(args)
    elif args.command == "extract":
        cmd_extract(args)


if __name__ == "__main__":
    main()
