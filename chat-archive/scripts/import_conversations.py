#!/usr/bin/env python3
"""Import ChatGPT and Claude.ai conversation exports into SQLite FTS5 database."""

import argparse
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            title TEXT,
            created_at TEXT,
            updated_at TEXT,
            message_count INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            timestamp TEXT,
            model TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
            content, conversation_id UNINDEXED, message_id UNINDEXED
        );
        CREATE TABLE IF NOT EXISTS import_meta (
            file_path TEXT PRIMARY KEY,
            file_hash TEXT NOT NULL,
            imported_at TEXT NOT NULL,
            record_count INTEGER
        );
        CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
    """)
    # Sync triggers for FTS
    conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
            INSERT INTO messages_fts(content, conversation_id, message_id)
            VALUES (NEW.content, NEW.conversation_id, NEW.id);
        END;
        CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
            DELETE FROM messages_fts WHERE message_id = OLD.id;
        END;
    """)
    return conn


def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_platform(data) -> str:
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Expected a JSON array of conversations")
    sample = data[0]
    if "mapping" in sample:
        return "chatgpt"
    if "chat_messages" in sample:
        return "claude"
    raise ValueError("Cannot detect platform — use --platform flag")


def ts_to_iso(ts) -> str | None:
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    return str(ts)


def import_chatgpt(conv: dict, conn: sqlite3.Connection) -> int:
    conv_id = conv.get("id") or conv.get("conversation_id") or hashlib.md5(
        (conv.get("title", "") + str(conv.get("create_time", ""))).encode()
    ).hexdigest()
    title = conv.get("title", "Untitled")
    created = ts_to_iso(conv.get("create_time"))
    updated = ts_to_iso(conv.get("update_time"))
    mapping = conv.get("mapping", {})

    # Walk tree from current_node to root, then reverse
    node_id = conv.get("current_node")
    chain = []
    while node_id and node_id in mapping:
        chain.append(mapping[node_id])
        node_id = mapping[node_id].get("parent")
    chain.reverse()

    messages = []
    for node in chain:
        msg = node.get("message")
        if not msg or not msg.get("content"):
            continue
        parts = msg["content"].get("parts", [])
        text = "\n".join(str(p) for p in parts if isinstance(p, str)).strip()
        if not text:
            continue
        role = msg.get("author", {}).get("role", "unknown")
        if role == "system":
            continue
        msg_id = msg.get("id", node.get("id", ""))
        messages.append((
            msg_id, conv_id, role, text,
            ts_to_iso(msg.get("create_time")),
            (msg.get("metadata") or {}).get("model_slug"),
        ))

    if not messages:
        return 0

    conn.execute(
        "INSERT OR REPLACE INTO conversations VALUES (?,?,?,?,?,?)",
        (conv_id, "chatgpt", title, created, updated, len(messages)),
    )
    conn.executemany("INSERT OR REPLACE INTO messages VALUES (?,?,?,?,?,?)", messages)
    return len(messages)


def import_claude(conv: dict, conn: sqlite3.Connection) -> int:
    conv_id = conv.get("uuid") or conv.get("id") or hashlib.md5(
        (conv.get("name", "") + str(conv.get("created_at", ""))).encode()
    ).hexdigest()
    title = conv.get("name", "Untitled")
    created = conv.get("created_at")
    updated = conv.get("updated_at")
    chat_messages = conv.get("chat_messages", [])

    messages = []
    for i, msg in enumerate(chat_messages):
        role = msg.get("sender", "unknown")
        text = ""
        # Handle different content formats
        if "text" in msg:
            text = msg["text"]
        elif "content" in msg:
            content = msg["content"]
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = "\n".join(
                    p.get("text", "") for p in content
                    if isinstance(p, dict) and p.get("type") == "text"
                )
        text = text.strip()
        if not text:
            continue
        msg_id = msg.get("uuid") or f"{conv_id}_{i}"
        messages.append((
            msg_id, conv_id, role, text,
            msg.get("created_at"), None,
        ))

    if not messages:
        return 0

    conn.execute(
        "INSERT OR REPLACE INTO conversations VALUES (?,?,?,?,?,?)",
        (conv_id, "claude", title, created, updated, len(messages)),
    )
    conn.executemany("INSERT OR REPLACE INTO messages VALUES (?,?,?,?,?,?)", messages)
    return len(messages)


def main():
    parser = argparse.ArgumentParser(description="Import conversations into SQLite FTS5")
    parser.add_argument("file", help="Path to export JSON file")
    parser.add_argument("--platform", choices=["auto", "chatgpt", "claude"], default="auto")
    parser.add_argument("--db", default="~/.chat-archive/conversations.db")
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        print(json.dumps({"error": f"File not found: {file_path}"}))
        sys.exit(1)

    db_path = Path(args.db).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    fhash = file_hash(str(file_path))
    conn = init_db(str(db_path))

    # Check if already imported with same hash
    existing = conn.execute(
        "SELECT file_hash FROM import_meta WHERE file_path = ?", (str(file_path),)
    ).fetchone()
    if existing and existing[0] == fhash:
        stats = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()
        total_msgs = conn.execute("SELECT COUNT(*) FROM messages").fetchone()
        print(json.dumps({
            "imported": 0, "skipped": 1,
            "total_conversations": stats[0], "total_messages": total_msgs[0],
            "reason": "File unchanged since last import",
        }))
        conn.close()
        return

    data = json.loads(file_path.read_text(encoding="utf-8"))
    platform = args.platform if args.platform != "auto" else detect_platform(data)
    importer = import_chatgpt if platform == "chatgpt" else import_claude

    total_messages = 0
    conv_count = 0
    for conv in data:
        count = importer(conv, conn)
        if count > 0:
            conv_count += 1
            total_messages += count

    conn.execute(
        "INSERT OR REPLACE INTO import_meta VALUES (?,?,?,?)",
        (str(file_path), fhash, datetime.now(timezone.utc).isoformat(), conv_count),
    )
    conn.commit()

    stats = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()
    total_msgs = conn.execute("SELECT COUNT(*) FROM messages").fetchone()
    conn.close()

    print(json.dumps({
        "imported": conv_count, "skipped": 0,
        "total_conversations": stats[0], "total_messages": total_msgs[0],
    }))


if __name__ == "__main__":
    main()
