#!/usr/bin/env python3
"""Search conversations in SQLite FTS5 database."""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def get_db(db_path: str) -> sqlite3.Connection:
    path = Path(db_path).expanduser().resolve()
    if not path.exists():
        print(json.dumps({"error": "Database not found. Run import first."}))
        sys.exit(1)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def show_stats(conn: sqlite3.Connection):
    total_convs = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    total_msgs = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    platforms = conn.execute(
        "SELECT platform, COUNT(*) as count FROM conversations GROUP BY platform"
    ).fetchall()
    print(json.dumps({
        "total_conversations": total_convs,
        "total_messages": total_msgs,
        "platforms": {r["platform"]: r["count"] for r in platforms},
    }))


def _truncate(text: str | None, limit: int) -> str:
    if not text:
        return ""
    return text[:limit] + "..." if len(text) > limit else text


def show_conversation(conn: sqlite3.Connection, conv_id: str,
                      max_msgs: int, trunc: int, around: int | None):
    conv = conn.execute(
        "SELECT * FROM conversations WHERE id = ?", (conv_id,)
    ).fetchone()
    if not conv:
        print(json.dumps({"error": f"Conversation {conv_id} not found"}))
        sys.exit(1)
    all_msgs = conn.execute(
        "SELECT role, content, timestamp, model FROM messages "
        "WHERE conversation_id = ? ORDER BY timestamp, rowid", (conv_id,)
    ).fetchall()
    total = len(all_msgs)

    if around is not None:
        half = max_msgs // 2
        start = max(0, around - half)
        end = min(total, start + max_msgs)
        window = all_msgs[start:end]
        window_start = start
    else:
        window = all_msgs[:max_msgs]
        window_start = 0

    messages = [
        {"index": window_start + i, "role": r["role"],
         "content": _truncate(r["content"], trunc),
         "timestamp": r["timestamp"], "model": r["model"]}
        for i, r in enumerate(window)
    ]
    print(json.dumps({
        "conversation": {
            "id": conv["id"], "platform": conv["platform"],
            "title": conv["title"], "created_at": conv["created_at"],
            "message_count": conv["message_count"],
        },
        "total_messages": total,
        "showing": len(messages),
        "window_start": window_start,
        "truncated_at": trunc,
        "messages": messages,
    }))


def _fetch_context(conn: sqlite3.Connection, msg_id: str, conv_id: str) -> str | None:
    """Fetch the previous message in the same conversation as context."""
    row = conn.execute(
        "SELECT content FROM messages "
        "WHERE conversation_id = ? AND rowid < (SELECT rowid FROM messages WHERE id = ?) "
        "ORDER BY rowid DESC LIMIT 1",
        (conv_id, msg_id),
    ).fetchone()
    if not row or not row["content"]:
        return None
    text = row["content"]
    return text[:120] + "..." if len(text) > 120 else text


def _recency_factor(created_at: str | None) -> float:
    """Compute recency boost: 1/(1 + days_old/365). Returns 0.0 on parse failure."""
    if not created_at:
        return 0.0
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        days_old = max(0, (datetime.now(dt.tzinfo) - dt).days)
        return 1.0 / (1.0 + days_old / 365.0)
    except (ValueError, TypeError):
        return 0.0


def search(conn: sqlite3.Connection, query: str, platform: str | None,
           after: str | None, before: str | None, title: str | None,
           limit: int, group: bool):
    sql = """
        SELECT
            c.id, c.platform, c.title, c.created_at, c.message_count,
            snippet(messages_fts, 0, '>>>', '<<<', '...', 40) as snippet,
            m.role, m.timestamp, m.id as msg_id, rank
        FROM messages_fts f
        JOIN messages m ON m.id = f.message_id
        JOIN conversations c ON c.id = f.conversation_id
        WHERE messages_fts MATCH ?
    """
    params: list = [query]

    if platform:
        sql += " AND c.platform = ?"
        params.append(platform)
    if after:
        sql += " AND c.created_at >= ?"
        params.append(after)
    if before:
        sql += " AND c.created_at <= ?"
        params.append(before)
    if title:
        sql += " AND c.title LIKE ?"
        params.append(f"%{title}%")

    sql += " ORDER BY rank LIMIT ?"
    params.append(limit * 10 if group else limit)

    rows = conn.execute(sql, params).fetchall()

    if not group:
        results = []
        for r in rows:
            score = -r["rank"] * (1 + 0.3 * _recency_factor(r["created_at"]))
            ctx = _fetch_context(conn, r["msg_id"], r["id"])
            results.append({
                "conversation_id": r["id"], "platform": r["platform"],
                "title": r["title"], "created_at": r["created_at"],
                "snippet": r["snippet"], "role": r["role"],
                "timestamp": r["timestamp"], "context": ctx, "score": score,
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:limit]
        print(json.dumps({"query": query, "count": len(results), "results": results}))
        return

    groups: dict[str, dict] = {}
    for r in rows:
        score = -r["rank"] * (1 + 0.3 * _recency_factor(r["created_at"]))
        cid = r["id"]
        if cid not in groups:
            groups[cid] = {
                "conversation_id": cid, "platform": r["platform"],
                "title": r["title"], "created_at": r["created_at"],
                "match_count": 0, "best_score": 0.0, "snippets": [],
            }
        g = groups[cid]
        g["match_count"] += 1
        g["best_score"] = max(g["best_score"], score)
        if len(g["snippets"]) < 3:
            ctx = _fetch_context(conn, r["msg_id"], cid)
            g["snippets"].append({
                "snippet": r["snippet"], "role": r["role"],
                "timestamp": r["timestamp"], "context": ctx,
            })

    sorted_groups = sorted(groups.values(), key=lambda x: x["best_score"], reverse=True)[:limit]
    for g in sorted_groups:
        del g["best_score"]
    print(json.dumps({"query": query, "count": len(sorted_groups), "results": sorted_groups}))


def main():
    parser = argparse.ArgumentParser(description="Search conversation archive")
    parser.add_argument("query", nargs="?", help="Search query (FTS5 syntax)")
    parser.add_argument("--platform", choices=["chatgpt", "claude"])
    parser.add_argument("--after", help="Filter after date (YYYY-MM-DD)")
    parser.add_argument("--before", help="Filter before date (YYYY-MM-DD)")
    parser.add_argument("--title", help="Filter by conversation title")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--db", default="~/.chat-archive/conversations.db")
    parser.add_argument("--no-group", action="store_true",
                        help="Flat results instead of conversation grouping")
    parser.add_argument("--stats", action="store_true", help="Show database stats")
    parser.add_argument("--conversation", help="Show messages for a conversation ID")
    parser.add_argument("--max-messages", type=int, default=40,
                        help="Max messages to return (default 40)")
    parser.add_argument("--truncate", type=int, default=300,
                        help="Truncate message content to N chars (default 300)")
    parser.add_argument("--around", type=int, default=None,
                        help="Center window around message index")
    args = parser.parse_args()

    conn = get_db(args.db)

    if args.stats:
        show_stats(conn)
    elif args.conversation:
        show_conversation(conn, args.conversation, args.max_messages,
                          args.truncate, args.around)
    elif args.query:
        search(conn, args.query, args.platform, args.after, args.before,
               args.title, args.limit, group=not args.no_group)
    else:
        print(json.dumps({"error": "Provide a search query, --stats, or --conversation"}))
        sys.exit(1)

    conn.close()


if __name__ == "__main__":
    main()
