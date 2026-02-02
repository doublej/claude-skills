#!/usr/bin/env python3
"""Extract Claude Code session history for the current project."""

import json
import os
import sys
from pathlib import Path
from typing import Iterator

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
CHARS_PER_TOKEN = 4
BOX_WIDTH = 60  # inner width (between vertical bars)


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
    """Center a title in the box."""
    return f"║  {title:^{BOX_WIDTH - 4}}  ║"


def box_empty() -> str:
    return f"║{' ' * BOX_WIDTH}║"


def encode_project_path(cwd: str) -> str:
    """Encode project path to Claude's folder naming convention."""
    return cwd.replace("/", "-").replace("_", "-")


def find_project_dir(cwd: str) -> Path | None:
    """Find the Claude project directory for given working directory."""
    encoded = encode_project_path(cwd)
    project_dir = PROJECTS_DIR / encoded

    if project_dir.exists():
        return project_dir

    # Fuzzy match
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


def extract_messages(session_file: Path) -> list[dict]:
    """Extract messages with source references, including speak MCP interactions."""
    messages = []
    speak_questions = {}  # tool_id -> question text

    with open(session_file) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("type") not in ("user", "assistant"):
                    continue

                msg_content = entry.get("message", {}).get("content", "")

                # Handle list content (tool calls/results)
                if isinstance(msg_content, list):
                    for block in msg_content:
                        if not isinstance(block, dict):
                            continue

                        # Capture speak MCP questions from assistant
                        if block.get("type") == "tool_use" and "speak" in block.get("name", ""):
                            tool_id = block.get("id", "")
                            inp = block.get("input", {})
                            question = inp.get("prompt") or inp.get("message", "")
                            if tool_id and question:
                                speak_questions[tool_id] = question

                        # Capture speak MCP responses from user
                        if block.get("type") == "tool_result":
                            tool_id = block.get("tool_use_id", "")
                            if tool_id in speak_questions:
                                result_content = block.get("content", "")
                                if isinstance(result_content, list):
                                    for rc in result_content:
                                        if isinstance(rc, dict) and rc.get("type") == "text":
                                            try:
                                                resp = json.loads(rc.get("text", "{}"))
                                                # Handle pure confirmation dialogs
                                                if resp.get("cancelled") and len(resp) <= 2:
                                                    answer = "[Cancelled]"
                                                elif resp.get("confirmed") and len(resp) <= 2:
                                                    answer = "[Confirmed]"
                                                else:
                                                    if resp.get("cancelled"):
                                                        continue
                                                    # Flexible: grab first non-meta string value
                                                    skip_keys = {"cancelled", "confirmed", "success", "error"}
                                                    answer = ""
                                                    for k, v in resp.items():
                                                        if k not in skip_keys and isinstance(v, str) and v:
                                                            answer = v
                                                            break
                                                        if k not in skip_keys and isinstance(v, list):
                                                            answer = ", ".join(str(x) for x in v)
                                                            break
                                                if answer:
                                                    messages.append({
                                                        "type": "user",
                                                        "uuid": entry.get("uuid", ""),
                                                        "timestamp": entry.get("timestamp", ""),
                                                        "content": f"[Dialog] Q: {speak_questions[tool_id]}\nA: {answer}",
                                                        "session_id": entry.get("sessionId", session_file.stem),
                                                        "source_file": str(session_file),
                                                        "source_line": line_num,
                                                        "is_speak_mcp": True,
                                                    })
                                            except json.JSONDecodeError:
                                                pass

                    # Also extract regular text from list content
                    text_parts = [p.get("text", "") for p in msg_content if isinstance(p, dict) and p.get("type") == "text"]
                    msg_content = "\n".join(text_parts)

                if not isinstance(msg_content, str) or not msg_content.strip():
                    continue

                messages.append({
                    "type": entry["type"],
                    "uuid": entry.get("uuid", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "content": msg_content,
                    "session_id": entry.get("sessionId", session_file.stem),
                    "source_file": str(session_file),
                    "source_line": line_num,
                })
            except json.JSONDecodeError:
                continue
    return messages


def is_system_noise(content: str) -> bool:
    """Check if message is system-generated noise."""
    if not content:
        return True
    if content.startswith("<local-command-stdout>"):
        return True
    if content.startswith("<command-name>/"):
        return True
    if "Caveat: The messages below were generated" in content:
        return True
    if content.startswith("<system-reminder>"):
        return True
    if content.strip().startswith("[Request interrupted"):
        return True
    return False


def filter_user_messages(messages: list[dict]) -> list[dict]:
    """Filter to meaningful user messages only."""
    return [m for m in messages if m["type"] == "user" and not is_system_noise(m["content"])]


def estimate_tokens(messages: list[dict]) -> int:
    """Estimate token count."""
    return sum(len(m["content"]) for m in messages) // CHARS_PER_TOKEN


def scan_project(cwd: str) -> dict:
    """Scan project history and return statistics."""
    project_dir = find_project_dir(cwd)
    if not project_dir:
        return {"error": f"No history found for {cwd}"}

    all_messages = []
    session_count = 0

    for session_file in iter_project_sessions(project_dir):
        session_count += 1
        messages = extract_messages(session_file)
        all_messages.extend(messages)

    all_messages.sort(key=lambda m: m.get("timestamp", ""))
    user_messages = filter_user_messages(all_messages)

    return {
        "project": cwd,
        "project_dir": str(project_dir),
        "session_count": session_count,
        "total_messages": len(all_messages),
        "user_messages": len(user_messages),
        "estimated_tokens": estimate_tokens(all_messages),
        "user_tokens": estimate_tokens(user_messages),
        "oldest": all_messages[0]["timestamp"][:10] if all_messages else None,
        "newest": all_messages[-1]["timestamp"][:10] if all_messages else None,
    }


def extract_recent(cwd: str, message_limit: int, output_dir: Path) -> dict:
    """Extract most recent N user messages for project."""
    project_dir = find_project_dir(cwd)
    if not project_dir:
        return {"error": f"No history found for {cwd}"}

    all_messages = []
    for session_file in iter_project_sessions(project_dir):
        messages = extract_messages(session_file)
        all_messages.extend(messages)

    # Filter to user messages FIRST, then take most recent N
    all_messages.sort(key=lambda m: m.get("timestamp", ""), reverse=True)
    all_user_messages = filter_user_messages(all_messages)
    user_messages = all_user_messages[:message_limit]
    user_messages.reverse()  # chronological order

    # Create index with source refs
    index = [{
        "timestamp": m["timestamp"],
        "session_id": m["session_id"],
        "uuid": m["uuid"],
        "source_file": m["source_file"],
        "source_line": m["source_line"],
        "preview": m["content"][:100].replace("\n", " "),
        "char_count": len(m["content"]),
    } for m in user_messages]

    output_dir.mkdir(parents=True, exist_ok=True)

    index_file = output_dir / "message_index.json"
    with open(index_file, "w") as f:
        json.dump(index, f, indent=2)

    messages_file = output_dir / "user_messages.json"
    with open(messages_file, "w") as f:
        json.dump(user_messages, f, indent=2)

    return {
        "project": cwd,
        "message_count": len(user_messages),
        "estimated_tokens": estimate_tokens(user_messages),
        "index_file": str(index_file),
        "messages_file": str(messages_file),
        "time_range": f"{user_messages[0]['timestamp'][:10]} to {user_messages[-1]['timestamp'][:10]}" if user_messages else None,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Claude Code Session Analyzer")
    parser.add_argument("command", choices=["scan", "extract"])
    parser.add_argument("-p", "--project", type=str, default=os.getcwd(),
                       help="Project directory (default: current)")
    parser.add_argument("-n", "--limit", type=int, default=100,
                       help="Number of recent user messages")
    parser.add_argument("-o", "--output", type=str, default=".history-analysis")
    args = parser.parse_args()

    if args.command == "scan":
        stats = scan_project(args.project)
        if "error" in stats:
            print(f"Error: {stats['error']}")
            sys.exit(1)

        date_range = f"{stats['oldest'] or 'N/A'} to {stats['newest'] or 'N/A'}"
        print()
        print(box_top())
        print(box_title("PROJECT HISTORY SCAN"))
        print(box_sep())
        print(box_empty())
        print(box_line("Project:", Path(stats['project']).name))
        print(box_line("Sessions:", str(stats['session_count'])))
        print(box_line("Total msgs:", str(stats['total_messages'])))
        print(box_line("User msgs:", str(stats['user_messages'])))
        print(box_empty())
        print(box_line("Date range:", date_range))
        print(box_line("Est. tokens:", str(stats['user_tokens'])))
        print(box_empty())
        print(box_bottom())
        print()
        print(json.dumps(stats))

    elif args.command == "extract":
        result = extract_recent(args.project, args.limit, Path(args.output))
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print()
        print(box_top())
        print(box_title("EXTRACTION COMPLETE"))
        print(box_sep())
        print(box_empty())
        print(box_line("Messages:", str(result['message_count'])))
        print(box_line("Est. tokens:", str(result['estimated_tokens'])))
        print(box_line("Time range:", result['time_range'] or 'N/A'))
        print(box_empty())
        print(box_bottom())
        print()
        print(json.dumps(result))


if __name__ == "__main__":
    main()
