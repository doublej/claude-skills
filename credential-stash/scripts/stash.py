#!/usr/bin/env python3
"""Find credentials that surfaced in Claude Code session transcripts and file them in 1Password.

scan   — walk recent transcripts for the cwd project, print masked findings, write full values to a findings file
stash  — push one finding into 1Password via `op item create` (JSON template on stdin, secret never on argv)
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"

# ponytail: regex list, not a secret-scanning engine. Extend the table when a real credential slips through.
PATTERNS = [
    ("url-with-creds", re.compile(r"\b[a-z][a-z0-9+.-]*://([^/\s:@]+):([^@\s]+)@([^\s\"'<>]+)")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("openai-key", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}\b")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("stripe-key", re.compile(r"\b[sp]k_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    ("assignment", re.compile(
        r"(?i)\b([A-Z0-9_]*(?:api[_-]?key|secret|token|password|passwd|pwd|client[_-]?secret)[A-Z0-9_]*)"
        r"\s*[:=]\s*[\"']?([^\s\"',;]{8,})")),
    ("labelled", re.compile(r"(?i)\b(password|passphrase|pin|api key|token)\b\s*(?:is|:)\s*[`\"']?([^\s`\"',;]{6,})")),
    # `demo@site.nl / demo-pass-2026` login lines in READMEs and seed output
    ("email-slash-pass", re.compile(r"`?([A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[a-z]{2,})`?\s*/\s*`?([^\s`\"',;]{6,})`?")),
    # string literal shortly after a password-ish word: hashPassword("x"), password: await hash("x")
    ("password-literal", re.compile(r"(?i)\b(\w*(?:password|passwd|secret)\w*)\b[^\n\"'`]{0,60}[\"'`]([^\"'`\s]{6,})[\"'`]")),
]
PLACEHOLDER = re.compile(r"(?i)^(?:<.*>|\$\{?[A-Z_]+\}?|op://.*|\*+|x{4,}|your[_-]|changeme|example|placeholder|redacted|\.\.\.|none|null|true|false|undefined|\[.*\])")
URL = re.compile(r"https?://[^\s\"'<>)\]]+")
USER = re.compile(r"(?i)\b(?:user(?:name)?|login|email)\s*[:=]\s*[\"']?([^\s\"',;]{2,})")


def walk_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from walk_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_strings(v)


def project_dir(cwd):
    return PROJECTS / re.sub(r"[^A-Za-z0-9]", "-", cwd)


def transcripts(cwd, session, since_hours):
    d = project_dir(cwd)
    if session:
        return [d / f"{session}.jsonl"]
    cutoff = time.time() - since_hours * 3600
    return sorted((p for p in d.glob("*.jsonl") if p.stat().st_mtime >= cutoff), key=lambda p: p.stat().st_mtime)


def mask(v):
    v = v.strip()
    return v if len(v) <= 8 else f"{v[:4]}…{v[-3:]} ({len(v)} chars)"


def scan(args):
    findings, seen = [], {}
    for path in transcripts(args.cwd, args.session, args.since):
        if not path.exists():
            continue
        for line in path.open(encoding="utf-8", errors="replace"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") not in ("user", "assistant"):
                continue
            for text in walk_strings(obj.get("message", {}).get("content")):
                for kind, rx in PATTERNS:
                    for m in rx.finditer(text):
                        if kind == "url-with-creds":
                            username, secret, host = m.group(1), m.group(2), m.group(3)
                            label = host.split("/")[0]
                        elif kind == "email-slash-pass":
                            username, secret, label = m.group(1), m.group(2), "login"
                        elif kind in ("assignment", "labelled", "password-literal"):
                            label, secret, username = m.group(1), m.group(2), None
                        else:
                            label, secret, username = kind, m.group(0), None
                        if PLACEHOLDER.match(secret) or secret in seen:
                            continue
                        ctx = text[max(0, m.start() - 300): m.end() + 300]
                        urls = [u for u in URL.findall(ctx) if secret not in u]
                        um = USER.search(ctx)
                        fid = f"c{len(findings) + 1}"
                        seen[secret] = fid
                        findings.append({
                            "id": fid, "kind": kind, "label": label, "secret": secret,
                            "username": username or (um.group(1) if um else None),
                            "url": urls[0] if urls else None,
                            "session": path.stem, "timestamp": obj.get("timestamp"),
                            "role": obj["type"],
                            "snippet": text[max(0, m.start() - 80): m.end() + 80],
                        })
    for f in findings:  # mask every known secret in every snippet, not just the one that produced it
        for s in seen:
            f["snippet"] = f["snippet"].replace(s, mask(s))
    out = Path(args.out)
    out.write_text(json.dumps(findings, indent=2))
    out.chmod(0o600)
    public = [{k: (mask(v) if k == "secret" else v) for k, v in f.items()} for f in findings]
    print(json.dumps({"findings": public, "findings_file": str(out)}, indent=2))


def stash(args):
    if args.id == "-":
        f = {"secret": sys.stdin.read().rstrip("\n")}
    else:
        f = {f["id"]: f for f in json.loads(Path(args.findings).read_text())}[args.id]
    if args.onenv:
        ns, key = args.onenv
        subprocess.run(["onenv", "set", ns, key, "--value-stdin"], input=f["secret"], text=True, check=True)
        print(json.dumps({"stored": "onenv", "namespace": ns, "key": key}))
        return
    category = args.category or ("Login" if f.get("username") or f.get("url") else "API Credential")
    fields = [{"id": "password" if category == "Login" else "credential",
               "type": "CONCEALED", "purpose": "PASSWORD" if category == "Login" else "",
               "label": "password" if category == "Login" else "credential", "value": f["secret"]}]
    username = args.username or f.get("username")
    if username:
        fields.insert(0, {"id": "username", "type": "STRING", "purpose": "USERNAME", "label": "username", "value": username})
    if args.notes:
        fields.append({"id": "notesPlain", "type": "STRING", "purpose": "NOTES", "label": "notesPlain", "value": args.notes})
    item = {"title": args.title, "category": category.upper().replace(" ", "_"), "fields": fields,
            "tags": ["credential-stash"]}
    url = args.url or f.get("url")
    if url:
        item["urls"] = [{"label": "website", "primary": True, "href": url}]
    cmd = ["op", "item", "create", "--vault", args.vault, "--format", "json"]
    if args.account:
        cmd += ["--account", args.account]
    r = subprocess.run(cmd, input=json.dumps(item), text=True, capture_output=True)
    if r.returncode:
        sys.exit(r.stderr.strip())
    created = json.loads(r.stdout)
    print(json.dumps({"stored": "1password", "id": created["id"], "title": created["title"],
                      "vault": created["vault"]["name"], "category": created["category"],
                      "url": url, "username": username}))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="find credentials in recent transcripts for cwd")
    s.add_argument("cwd", nargs="?", default=os.getcwd(), help="project root (default: cwd)")
    s.add_argument("--session", default=os.environ.get("CLAUDE_CODE_SESSION_ID"), help="single session id (default: $CLAUDE_CODE_SESSION_ID)")
    s.add_argument("--all-recent", action="store_true", help="ignore --session, scan every transcript within --since")
    s.add_argument("--since", type=float, default=24, help="hours back when scanning all recent (default 24)")
    s.add_argument("--out", default=os.environ.get("TMPDIR", "/tmp") + "/credential-stash.json", help="findings file with full values (chmod 600)")
    s.set_defaults(fn=scan)
    t = sub.add_parser("stash", help="store one finding in 1Password (or onenv)")
    t.add_argument("id", help="finding id from scan, e.g. c1 — or `-` to read the secret from stdin")
    t.add_argument("--findings", default=os.environ.get("TMPDIR", "/tmp") + "/credential-stash.json")
    t.add_argument("--title", required=True)
    t.add_argument("--vault", default="Private")
    t.add_argument("--account", help="op account shorthand/url, e.g. pimpelmees.1password.com")
    t.add_argument("--category", choices=["Login", "API Credential", "Password"])
    t.add_argument("--url", help="website URL so 1Password autofill triggers there")
    t.add_argument("--username")
    t.add_argument("--notes")
    t.add_argument("--onenv", nargs=2, metavar=("NAMESPACE", "KEY"), help="store as onenv env var instead of a 1Password item")
    t.set_defaults(fn=stash)
    args = p.parse_args()
    if args.cmd == "scan" and args.all_recent:
        args.session = None
    args.fn(args)


if __name__ == "__main__":
    main()
