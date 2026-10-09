#!/usr/bin/env python3
"""Local web UI for reviewing skill usage and nominating skills for removal.

Serves a single-page dashboard on 127.0.0.1 only. Nominations are stored in
the same SQLite database used for usage tracking, in a `removal_nominations`
table. Nominating a skill never deletes or archives it -- it just records
that a human flagged it for review.
"""

import argparse
import json
import re
import sqlite3
import sys
import webbrowser
from datetime import datetime
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import tiktoken

DEFAULT_PORT = 8420
DB_PATH = Path.home() / ".claude" / "skill-usage.db"
REPO_ROOT = Path(__file__).resolve().parents[2]
WEB_DIR = Path(__file__).resolve().parent.parent / "web"
SKILLIGNORE_PATH = REPO_ROOT / ".skillignore"
CLAUDE_SKILLS_DIR = Path.home() / ".claude" / "skills"
NOMINATION_LEVELS = {"hide", "delete"}

# Same frontmatter parsing as validate-context-budget.py, kept in sync deliberately.
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
DESC_RE = re.compile(r"^description:\s*(.+?)(?=\n[a-z_-]+:|\Z)", re.MULTILINE | re.DOTALL)


@lru_cache(maxsize=1)
def _encoding():
    return tiktoken.get_encoding("cl100k_base")


def _read_skill_md(skill_name: str) -> str | None:
    try:
        return (REPO_ROOT / skill_name / "SKILL.md").read_text(errors="ignore")
    except OSError:
        return None


def count_skill_md_tokens(skill_name: str) -> int | None:
    """Token count of the skill's full SKILL.md, via tiktoken cl100k_base."""
    text = _read_skill_md(skill_name)
    if text is None:
        return None
    return len(_encoding().encode(text))


def count_description_tokens(skill_name: str) -> int | None:
    """Token count of just the frontmatter `description:` line -- the part that's
    always loaded into context for every skill, regardless of whether it's invoked."""
    text = _read_skill_md(skill_name)
    if text is None:
        return None
    fm = FRONTMATTER_RE.search(text)
    if not fm:
        return None
    desc = DESC_RE.search(fm.group(1))
    if not desc:
        return None
    return len(_encoding().encode(desc.group(1).strip().strip("\"'")))


def ensure_nominations_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS removal_nominations (
            skill_name TEXT PRIMARY KEY,
            note TEXT,
            nominated_at INTEGER NOT NULL,
            level TEXT NOT NULL DEFAULT 'delete'
        )
    """)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(removal_nominations)")}
    if "level" not in columns:
        conn.execute("ALTER TABLE removal_nominations ADD COLUMN level TEXT NOT NULL DEFAULT 'delete'")
    conn.commit()


def installed_skill_path(skill_name: str) -> Path:
    return CLAUDE_SKILLS_DIR / skill_name


def is_installed(skill_name: str) -> bool:
    """True if ~/.claude/skills/<name> is a symlink into this repo (i.e. its
    description loads into context). False if missing or hidden."""
    link = installed_skill_path(skill_name)
    return link.is_symlink() and link.resolve() == (REPO_ROOT / skill_name).resolve()


def apply_hide(skill_name: str) -> bool:
    """Remove the ~/.claude/skills symlink so the description stops loading.
    The repo folder itself is untouched. Returns False if nothing to remove
    or the symlink doesn't point into this repo (never touch unrelated links)."""
    link = installed_skill_path(skill_name)
    if not is_installed(skill_name):
        return False
    link.unlink()
    return True


def apply_unhide(skill_name: str) -> bool:
    """Recreate the ~/.claude/skills symlink. Returns False if already installed
    or the skill no longer exists in the repo."""
    source = REPO_ROOT / skill_name
    link = installed_skill_path(skill_name)
    if is_installed(skill_name) or not source.is_dir():
        return False
    if link.exists() or link.is_symlink():
        link.unlink()  # broken/stale symlink with the same name
    link.symlink_to(source)
    return True


def apply_hide_all() -> int:
    """Uninstall every currently-installed local skill. Returns count hidden."""
    return sum(apply_hide(name) for name in discover_local_skills())


def apply_unhide_all() -> int:
    """Reinstall every currently-hidden local skill. Returns count restored."""
    return sum(apply_unhide(name) for name in discover_local_skills())


def load_ignored_dirs() -> set:
    ignored = set()
    if SKILLIGNORE_PATH.exists():
        for line in SKILLIGNORE_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                ignored.add(line)
    return ignored


def discover_local_skills() -> set:
    """Top-level repo directories that contain a SKILL.md."""
    ignored = load_ignored_dirs()
    skills = set()
    for entry in REPO_ROOT.iterdir():
        if not entry.is_dir() or entry.name.startswith(".") or entry.name in ignored:
            continue
        if (entry / "SKILL.md").exists():
            skills.add(entry.name)
    return skills


def build_dataset(conn: sqlite3.Connection) -> dict:
    local_skills = discover_local_skills()
    cutoff_30d = int((datetime.now().timestamp() - 30 * 86400) * 1000)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT skill_name, COUNT(*) as total, MAX(timestamp) as last_used, MIN(timestamp) as first_seen
        FROM skill_usage
        GROUP BY skill_name
    """)
    usage_rows = {row[0]: row for row in cursor.fetchall()}

    cursor.execute("""
        SELECT skill_name, COUNT(*) FROM skill_usage
        WHERE timestamp >= ? GROUP BY skill_name
    """, (cutoff_30d,))
    uses_30d = dict(cursor.fetchall())

    cursor.execute("SELECT skill_name, note, nominated_at, level FROM removal_nominations")
    nominations = {
        row[0]: {"note": row[1], "nominated_at": row[2], "level": row[3]}
        for row in cursor.fetchall()
    }

    all_names = local_skills | set(usage_rows.keys()) | set(nominations.keys())

    skills = []
    for name in sorted(all_names):
        row = usage_rows.get(name)
        skills.append({
            "name": name,
            "in_repo": name in local_skills,
            "installed": is_installed(name) if name in local_skills else None,
            "total_uses": row[1] if row else 0,
            "uses_30d": uses_30d.get(name, 0),
            "last_used": row[2] if row else None,
            "first_seen": row[3] if row else None,
            "skill_md_tokens": count_skill_md_tokens(name) if name in local_skills else None,
            "description_tokens": count_description_tokens(name) if name in local_skills else None,
            "nomination": nominations.get(name),
        })

    return {"skills": skills, "generated_at": int(datetime.now().timestamp() * 1000)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # keep stdout quiet; errors still raise

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html = (WEB_DIR / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        if self.path == "/api/data":
            conn = sqlite3.connect(str(DB_PATH))
            try:
                ensure_nominations_table(conn)
                self._send_json(build_dataset(conn))
            finally:
                conn.close()
            return

        self.send_error(404)

    def do_POST(self):
        if self.path == "/api/nominate":
            data = self._read_json_body()
            skill = data.get("skill", "").strip()
            note = (data.get("note") or "").strip()
            level = data.get("level", "delete")
            if not skill:
                self._send_json({"error": "skill is required"}, status=400)
                return
            if level not in NOMINATION_LEVELS:
                self._send_json({"error": f"level must be one of {sorted(NOMINATION_LEVELS)}"}, status=400)
                return
            conn = sqlite3.connect(str(DB_PATH))
            try:
                ensure_nominations_table(conn)
                conn.execute("""
                    INSERT INTO removal_nominations (skill_name, note, nominated_at, level)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(skill_name) DO UPDATE SET note = excluded.note, level = excluded.level
                """, (skill, note, int(datetime.now().timestamp() * 1000), level))
                conn.commit()
            finally:
                conn.close()
            self._send_json({"ok": True})
            return

        if self.path == "/api/unnominate":
            data = self._read_json_body()
            skill = data.get("skill", "").strip()
            conn = sqlite3.connect(str(DB_PATH))
            try:
                ensure_nominations_table(conn)
                conn.execute("DELETE FROM removal_nominations WHERE skill_name = ?", (skill,))
                conn.commit()
            finally:
                conn.close()
            self._send_json({"ok": True})
            return

        if self.path == "/api/apply-hide":
            data = self._read_json_body()
            skill = data.get("skill", "").strip()
            if not skill or not (REPO_ROOT / skill).is_dir():
                self._send_json({"error": "unknown skill"}, status=400)
                return
            self._send_json({"ok": True, "installed": not apply_hide(skill)})
            return

        if self.path == "/api/apply-unhide":
            data = self._read_json_body()
            skill = data.get("skill", "").strip()
            if not skill or not (REPO_ROOT / skill).is_dir():
                self._send_json({"error": "unknown skill"}, status=400)
                return
            apply_unhide(skill)
            self._send_json({"ok": True, "installed": is_installed(skill)})
            return

        if self.path == "/api/apply-hide-all":
            self._send_json({"ok": True, "hidden": apply_hide_all()})
            return

        if self.path == "/api/apply-unhide-all":
            self._send_json({"ok": True, "restored": apply_unhide_all()})
            return

        self.send_error(404)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the skill usage web UI")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open a browser tab")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run init_db.py first.", file=sys.stderr)
        sys.exit(1)

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{args.port}/"
    print(f"Skill usage dashboard running at {url} (Ctrl+C to stop)")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
