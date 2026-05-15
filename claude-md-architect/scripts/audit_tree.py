#!/usr/bin/env python3
"""
audit_tree.py — Inventory candidate folders for CLAUDE.md files.

Walks a repo tree, scores each folder for "context value" using simple
heuristics, marks which folders already have a CLAUDE.md, and prints a
ranked proposal of where to add (or audit) context packets.

This is a starting point, not a final answer. Human judgment overrides
the score. The point is to surface candidates, not to mass-generate files.

Usage:
    python3 audit_tree.py <repo-root> [--min-files N] [--limit N] [--json]

Examples:
    python3 audit_tree.py ~/code/my-saas
    python3 audit_tree.py . --limit 20
    python3 audit_tree.py . --json > audit.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Folders we never recurse into.
SKIP_DIRS = {
    ".git", ".hg", ".svn",
    "node_modules", "bower_components",
    ".venv", "venv", "env", ".env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "dist", "build", "out", "target", ".next", ".nuxt", ".svelte-kit",
    "coverage", ".coverage", ".nyc_output",
    "tmp", ".tmp", ".cache", ".turbo",
    ".idea", ".vscode", ".DS_Store",
    "vendor", "third_party",
}

# Folder-name fragments that strongly signal a context-worthy domain.
# Score boost when the folder name (lowercased) contains any of these.
HIGH_VALUE_NAMES = {
    # Money / commerce
    "billing": 4, "payment": 4, "payments": 4, "invoice": 3, "checkout": 3,
    "subscription": 4, "subscriptions": 4, "stripe": 3, "adyen": 3,
    "pricing": 3, "tax": 3,
    # Identity / security
    "auth": 4, "authentication": 4, "authorization": 3, "rbac": 3,
    "permissions": 3, "security": 4, "session": 3, "sessions": 3,
    "oauth": 3, "saml": 3, "sso": 3, "tokens": 3, "passwords": 3,
    # Data
    "db": 4, "database": 4, "schema": 4, "migrations": 4, "migrate": 3,
    "prisma": 3, "drizzle": 3, "models": 2,
    # API / contracts
    "api": 3, "openapi": 3, "graphql": 3, "webhooks": 4, "webhook": 4,
    "contracts": 3,
    # AI / ML
    "ai": 3, "ml": 3, "llm": 4, "prompts": 3, "agents": 3, "rag": 3,
    "embeddings": 3,
    # UI domains (qualify only with secondary signal)
    "components": 2, "charts": 3, "forms": 3, "design-system": 4,
    "ui": 2, "tokens": 2,
    # Infra / ops
    "workers": 3, "worker": 3, "queue": 3, "jobs": 3, "cron": 3,
    "deploy": 2, "infra": 2, "terraform": 2,
}

# File extensions that count as "source files" for the volume heuristic.
SOURCE_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".rs", ".go", ".java", ".kt", ".swift",
    ".rb", ".php", ".cs", ".cpp", ".c", ".h", ".hpp",
    ".sql", ".graphql", ".prisma",
    ".svelte", ".vue", ".astro",
}

# Distinctive marker files: their presence is a strong "this is a domain" signal.
MARKER_FILES = {
    "schema.prisma": 4, "drizzle.config.ts": 3, "drizzle.config.js": 3,
    "openapi.yaml": 4, "openapi.yml": 4, "openapi.json": 4,
    "schema.graphql": 4, "schema.gql": 4,
    "package.json": 2,  # standalone workspace
    "pyproject.toml": 2, "Cargo.toml": 2, "go.mod": 2,
    "wrangler.toml": 3,
}

# Folder names that almost always shouldn't get a CLAUDE.md even if scored high.
NEVER_NAMES = {
    "tests", "test", "__tests__", "spec", "specs", "e2e", "fixtures",
    "mocks", "__mocks__", "stories", "examples", "docs", "scripts",
    "public", "static", "assets", "images", "img", "fonts",
    "generated", "__generated__", "types-generated", "auto-generated",
}


@dataclass
class FolderAudit:
    path: Path
    rel: str
    source_files: int = 0
    total_files: int = 0
    subfolders: int = 0
    has_claude_md: bool = False
    claude_md_location: str | None = None
    claude_md_lines: int = 0
    marker_score: int = 0
    name_score: int = 0
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    children_with_packet: int = 0
    verdict: str = ""

    def to_dict(self) -> dict:
        return {
            "rel": self.rel,
            "score": self.score,
            "verdict": self.verdict,
            "has_claude_md": self.has_claude_md,
            "claude_md_location": self.claude_md_location,
            "claude_md_lines": self.claude_md_lines,
            "source_files": self.source_files,
            "subfolders": self.subfolders,
            "reasons": self.reasons,
        }


def find_claude_md(folder: Path) -> tuple[Path | None, int]:
    """Return (path, line_count) of the folder's CLAUDE.md if present."""
    for candidate in (folder / "CLAUDE.md", folder / ".claude" / "CLAUDE.md"):
        if candidate.is_file():
            try:
                lines = sum(1 for _ in candidate.open(encoding="utf-8", errors="ignore"))
            except OSError:
                lines = 0
            return candidate, lines
    return None, 0


def scan_folder(folder: Path, root: Path) -> FolderAudit:
    rel = str(folder.relative_to(root)) or "."
    audit = FolderAudit(path=folder, rel=rel)

    try:
        entries = list(folder.iterdir())
    except (PermissionError, OSError):
        return audit

    for entry in entries:
        if entry.is_dir():
            if entry.name in SKIP_DIRS:
                continue
            audit.subfolders += 1
        elif entry.is_file():
            audit.total_files += 1
            if entry.suffix.lower() in SOURCE_EXTS:
                audit.source_files += 1
            if entry.name in MARKER_FILES:
                bonus = MARKER_FILES[entry.name]
                audit.marker_score += bonus
                audit.reasons.append(f"marker file: {entry.name} (+{bonus})")

    claude_md_path, claude_md_lines = find_claude_md(folder)
    audit.has_claude_md = claude_md_path is not None
    if claude_md_path is not None:
        audit.claude_md_location = str(claude_md_path.relative_to(root))
        audit.claude_md_lines = claude_md_lines

    return audit


def score_folder(audit: FolderAudit) -> None:
    folder_name = audit.path.name.lower()
    score = 0

    if folder_name in NEVER_NAMES or audit.rel == ".":
        # Root is scored separately; never-names are tagged.
        if folder_name in NEVER_NAMES:
            audit.reasons.append(f"name in skip-list ({folder_name})")
        score = 0
    else:
        for fragment, bonus in HIGH_VALUE_NAMES.items():
            if fragment == folder_name or f"-{fragment}" in folder_name or f"{fragment}-" in folder_name:
                audit.name_score = max(audit.name_score, bonus)
        if audit.name_score:
            score += audit.name_score
            audit.reasons.append(f"name suggests domain (+{audit.name_score})")

        score += audit.marker_score

        if 5 <= audit.source_files <= 60:
            score += 2
            audit.reasons.append(f"healthy source-file count ({audit.source_files}, +2)")
        elif audit.source_files > 60:
            score += 1
            audit.reasons.append(f"large folder ({audit.source_files} src files, +1)")

        if audit.subfolders >= 4:
            score += 1
            audit.reasons.append(f"hub folder ({audit.subfolders} subfolders, +1)")

    audit.score = score


def classify(audit: FolderAudit) -> None:
    is_root = audit.rel == "."
    if audit.has_claude_md:
        if audit.claude_md_lines > 200:
            audit.verdict = "REVIEW (existing CLAUDE.md > 200 lines)"
        elif audit.claude_md_lines < 5:
            audit.verdict = "REVIEW (existing CLAUDE.md < 5 lines — likely delete)"
        elif is_root or audit.score >= 3:
            audit.verdict = "KEEP (existing, healthy)"
        else:
            audit.verdict = "REVIEW (existing CLAUDE.md but score low — maybe redundant)"
    else:
        if is_root:
            audit.verdict = "STRONG candidate (root)"
        elif audit.score >= 5:
            audit.verdict = "STRONG candidate"
        elif audit.score >= 3:
            audit.verdict = "candidate"
        else:
            audit.verdict = "skip"


def walk(root: Path, min_files: int) -> list[FolderAudit]:
    audits: list[FolderAudit] = []
    queue: list[Path] = [root]
    while queue:
        folder = queue.pop()
        audit = scan_folder(folder, root)
        # Always include root.
        if folder == root or audit.source_files >= min_files or audit.subfolders >= 2 or audit.has_claude_md:
            score_folder(audit)
            classify(audit)
            audits.append(audit)
        try:
            for entry in folder.iterdir():
                if entry.is_dir() and entry.name not in SKIP_DIRS:
                    queue.append(entry)
        except (PermissionError, OSError):
            continue
    return audits


def render_text(audits: list[FolderAudit], limit: int) -> str:
    lines: list[str] = []
    lines.append("CLAUDE.md tree audit")
    lines.append("=" * 60)

    root = next((a for a in audits if a.rel == "."), None)
    if root is not None:
        if root.has_claude_md:
            lines.append(f"ROOT: CLAUDE.md present ({root.claude_md_lines} lines) at {root.claude_md_location}")
        else:
            lines.append("ROOT: NO CLAUDE.md — write one first (see references/examples/root-claude-md.md)")
        lines.append("")

    strong = [a for a in audits if a.verdict.startswith("STRONG candidate")]
    cand = [a for a in audits if a.verdict == "candidate"]
    existing_review = [a for a in audits if a.verdict.startswith("REVIEW")]
    keep = [a for a in audits if a.verdict == "KEEP (existing, healthy)"]

    def section(title: str, items: list[FolderAudit]) -> None:
        if not items:
            return
        lines.append(f"## {title} ({len(items)})")
        lines.append("")
        items_sorted = sorted(items, key=lambda a: (-a.score, a.rel))[:limit]
        for a in items_sorted:
            head = f"  [{a.score:>2}] {a.rel}"
            if a.has_claude_md:
                head += f"   (existing: {a.claude_md_lines} lines)"
            lines.append(head)
            for r in a.reasons[:4]:
                lines.append(f"        - {r}")
        lines.append("")

    section("Strong candidates — add CLAUDE.md here", strong)
    section("Weaker candidates — consider, only if you have domain context to write", cand)
    section("Existing CLAUDE.md to review", existing_review)
    section("Existing CLAUDE.md that look healthy", keep)

    lines.append("=" * 60)
    lines.append("Next steps:")
    lines.append("  1. Confirm the proposed file list with the user before writing packets.")
    lines.append("  2. Write or audit root CLAUDE.md first.")
    lines.append("  3. For each chosen folder, use references/context-packet-template.md.")
    lines.append("  4. Lift cross-cutting rules into .claude/rules/ with paths: frontmatter.")
    lines.append("  5. Verify with /memory and /context in a fresh Claude Code session.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Repo root to audit")
    parser.add_argument("--min-files", type=int, default=3, help="Min source files to consider a folder")
    parser.add_argument("--limit", type=int, default=40, help="Max items per section in text output")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")
    args = parser.parse_args()

    root: Path = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2

    audits = walk(root, args.min_files)

    if args.json:
        print(json.dumps([a.to_dict() for a in audits], indent=2))
    else:
        print(render_text(audits, args.limit))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
