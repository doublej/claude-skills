#!/usr/bin/env python3
"""Digest recent Claude Code sessions: goal, where each left off, and git state per project.

Reuses session-search for discovery, parsing and noise filtering. Writes the full
digest to <out>/catchup.json and prints one row per session (or the JSON with --json).
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/session-search/scripts"))
import session_search as ss  # noqa: E402


def clip(text: str, limit: int) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[:limit] + " …"


def run_git(repo: str, *args: str) -> str | None:
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def git_state(repo: str) -> dict | None:
    if not Path(repo).is_dir() or run_git(repo, "rev-parse", "--git-dir") is None:
        return None
    porcelain = run_git(repo, "status", "--porcelain") or ""
    unpushed = run_git(repo, "rev-list", "--count", "@{u}..HEAD")
    return {
        "branch": run_git(repo, "branch", "--show-current"),
        "dirty_files": len(porcelain.splitlines()),
        "unpushed": int(unpushed) if unpushed is not None else None,  # None = no upstream
        "last_commit": run_git(repo, "log", "-1", "--format=%cr · %s"),
    }


def digest_session(sf: Path, project: str, tail: int, clip_at: int) -> dict | None:
    msgs = [m for m in ss.extract_messages(sf) if m.get("timestamp")]
    real = [m for m in msgs if not (m["type"] == "user" and ss.is_system_noise(m["content"]))]
    user = [m for m in real if m["type"] == "user"]
    if not user:
        return None
    return {
        "session_id": sf.stem,
        "project": str(Path(project).resolve()),  # ~/Documents/development symlink → ~/dev realpath
        "cwd": project,
        "first": msgs[0]["timestamp"],
        "last": msgs[-1]["timestamp"],
        "age_min": int((datetime.now(timezone.utc) - ss.parse_timestamp(msgs[-1]["timestamp"])).total_seconds() // 60),
        "user_messages": len(user),
        "ended_on": real[-1]["type"],  # "user" = last prompt never got a text reply
        "goal": clip(user[0]["content"], clip_at),
        "tail": [{"type": m["type"], "timestamp": m["timestamp"], "content": clip(m["content"], clip_at)} for m in real[-tail:]],
        "resume": f"cd {project} && claude --resume {sf.stem}",  # --resume looks up the original cwd
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    ss.add_scope_args(p)
    p.add_argument(
        "--min-user-msgs", type=int, default=2, help="drop sessions with fewer real prompts (default 2; drops claude -p one-shots)"
    )
    p.add_argument("--tail", type=int, default=6, help="last N real messages kept per session (default 6)")
    p.add_argument("--clip", type=int, default=700, help="max chars per message (default 700)")
    p.add_argument("--exclude", action="append", default=[], help="session id to skip (the running session); repeatable")
    p.add_argument("--json", action="store_true", help="print the digest JSON instead of the table")
    p.set_defaults(since=2880, output=str(Path.home() / "dev/_data/session-catchup"))
    args = p.parse_args()

    projects = ss.resolve_projects(args)
    if not projects:
        sys.exit("Error: No projects found for scope")

    cutoff = datetime.now(timezone.utc).timestamp() - args.since * 60
    sessions = []
    for proj in projects:
        for sf in ss.iter_sessions_for_project(proj, args.since):
            if sf.stem in args.exclude:
                continue
            d = digest_session(sf, proj["project_path"], args.tail, args.clip)
            # --since is file mtime; also require the last message itself to be in the window
            if d and d["user_messages"] >= args.min_user_msgs and ss.parse_timestamp(d["last"]).timestamp() >= cutoff:
                sessions.append(d)
    sessions.sort(key=lambda s: s["last"], reverse=True)

    repos = {s["project"]: git_state(s["project"]) for s in sessions}
    digest = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "since_minutes": args.since,
        "session_count": len(sessions),
        "projects": repos,
        "sessions": sessions,
    }
    out = Path(args.output).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    (out / "catchup.json").write_text(json.dumps(digest, indent=2))

    if args.json:
        print(json.dumps(digest, indent=2))
        return
    print(f"{len(sessions)} session(s) in {len(repos)} project(s) → {out / 'catchup.json'}")
    for s in sessions:
        g = repos[s["project"]]
        git = (
            "no git" if g is None else f"{g['branch']} dirty:{g['dirty_files']} unpushed:{'—' if g['unpushed'] is None else g['unpushed']}"
        )
        last = s["last"][:16].replace("T", " ")
        print(f"{last}  {s['session_id'][:8]}  {s['user_messages']:>4}p  end:{s['ended_on']:<9}  {s['project']}  [{git}]")


if __name__ == "__main__":
    main()
