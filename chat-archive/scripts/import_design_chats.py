#!/usr/bin/env python3
"""Import Claude.ai design/artifact chat exports (design_chats/*.json) into the chat-archive SQLite FTS5 database.

Each design_chats export file is a single chat (schema: title/messages/role/content),
unlike conversations.json (array of chats with chat_messages/sender/text). This adapts
one file per chat into the shape import_claude() expects and reuses it unchanged.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from import_conversations import init_db, import_claude  # noqa: E402


def extract_text(msg: dict) -> str:
    content = msg.get("content", {})
    text = (content.get("content") or "").strip()
    for att in content.get("attachments", []) or []:
        att_text = att.get("content", "")
        if isinstance(att_text, str) and att_text:
            text = f"{text}\n{att_text}" if text else att_text
    return text.strip()


def to_conversation(data: dict) -> dict:
    messages = []
    for m in data.get("messages", []):
        text = extract_text(m)
        if not text:
            continue
        content = m.get("content", {})
        messages.append({
            "uuid": m.get("uuid"),
            "sender": content.get("role", "unknown"),
            "text": text,
            "created_at": m.get("created_at"),
        })
    return {
        "uuid": data.get("uuid"),
        "name": f"[Design] {data.get('title', 'Untitled')}",
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "chat_messages": messages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Import design_chats export into chat-archive SQLite FTS5 DB")
    parser.add_argument("dir", help="Path to extracted design_chats/ directory (one JSON file per chat)")
    parser.add_argument("--db", default="~/.chat-archive/conversations.db")
    args = parser.parse_args()

    src_dir = Path(args.dir).expanduser().resolve()
    files = sorted(src_dir.glob("*.json"))
    if not files:
        print(json.dumps({"error": f"No JSON files found in {src_dir}"}))
        sys.exit(1)

    db_path = Path(args.db).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = init_db(str(db_path))

    conv_count = 0
    total_messages = 0
    for fp in files:
        data = json.loads(fp.read_text(encoding="utf-8"))
        conv = to_conversation(data)
        count = import_claude(conv, conn)
        if count > 0:
            conv_count += 1
            total_messages += count

    conn.commit()
    stats = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()
    total_msgs = conn.execute("SELECT COUNT(*) FROM messages").fetchone()
    conn.close()

    print(json.dumps({
        "imported": conv_count, "total_conversations": stats[0], "total_messages": total_msgs[0],
    }))


if __name__ == "__main__":
    main()
