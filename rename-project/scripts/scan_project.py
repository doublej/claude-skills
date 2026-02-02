#!/usr/bin/env python3
"""Scan a project and produce a rename action plan.

Usage:
    python3 scan_project.py /path/to/project new-name        # human summary
    python3 scan_project.py /path/to/project new-name --json  # structured JSON
"""

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def to_snake(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def git_remote_url(project: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project, capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def parse_github_remote(url: str) -> tuple[str, str] | None:
    """Return (org, repo) from a GitHub remote URL."""
    patterns = [
        r"github\.com[:/]([^/]+)/([^/.]+?)(?:\.git)?$",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1), m.group(2)
    return None


def scan_folder(project: Path, old_slug: str, new_slug: str) -> dict | None:
    if old_slug == new_slug:
        return None
    return {
        "type": "rename_folder",
        "description": f"Rename folder '{old_slug}' → '{new_slug}'",
        "old": str(project),
        "new": str(project.parent / new_slug),
    }


def scan_github(project: Path, new_slug: str) -> list[dict]:
    actions = []
    url = git_remote_url(project)
    if not url:
        return actions
    parsed = parse_github_remote(url)
    if not parsed:
        return actions
    org, repo = parsed
    if repo == new_slug:
        return actions
    new_url = url.replace(f"{org}/{repo}", f"{org}/{new_slug}")
    actions.append({
        "type": "rename_github_repo",
        "description": f"Rename GitHub repo '{org}/{repo}' → '{org}/{new_slug}'",
        "org": org,
        "old_repo": repo,
        "new_repo": new_slug,
    })
    actions.append({
        "type": "update_git_remote",
        "description": f"Update origin remote URL",
        "old_url": url,
        "new_url": new_url,
    })
    return actions


def scan_pyproject(project: Path, new_slug: str, new_snake: str) -> list[dict]:
    actions = []
    path = project / "pyproject.toml"
    if not path.exists():
        return actions
    with open(path, "rb") as f:
        data = tomllib.load(f)
    name = data.get("project", {}).get("name")
    if name and name != new_slug:
        actions.append({
            "type": "update_manifest",
            "description": f"pyproject.toml: update project.name '{name}' → '{new_slug}'",
            "file": "pyproject.toml",
            "field": "project.name",
            "old": name,
            "new": new_slug,
        })
    # Check src/<pkg>/ dirs
    src = project / "src"
    if src.is_dir():
        for d in sorted(src.iterdir()):
            if d.is_dir() and (d / "__init__.py").exists():
                pkg = d.name
                if pkg != new_snake and pkg == to_snake(name or ""):
                    actions.append({
                        "type": "rename_package_dir",
                        "description": f"Rename src/{pkg}/ → src/{new_snake}/",
                        "old": f"src/{pkg}",
                        "new": f"src/{new_snake}",
                    })
    return actions


def scan_package_json(project: Path, new_slug: str) -> list[dict]:
    actions = []
    path = project / "package.json"
    if not path.exists():
        return actions
    with open(path) as f:
        data = json.load(f)
    name = data.get("name", "")
    if name and name != new_slug and not name.startswith("@"):
        actions.append({
            "type": "update_manifest",
            "description": f"package.json: update name '{name}' → '{new_slug}'",
            "file": "package.json",
            "field": "name",
            "old": name,
            "new": new_slug,
        })
    elif name and name.startswith("@"):
        scope = name.split("/")[0]
        old_pkg = name.split("/")[1] if "/" in name else ""
        if old_pkg and old_pkg != new_slug:
            new_name = f"{scope}/{new_slug}"
            actions.append({
                "type": "update_manifest",
                "description": f"package.json: update name '{name}' → '{new_name}'",
                "file": "package.json",
                "field": "name",
                "old": name,
                "new": new_name,
            })
    return actions


def scan_cargo_toml(project: Path, new_slug: str) -> list[dict]:
    actions = []
    path = project / "Cargo.toml"
    if not path.exists():
        return actions
    text = path.read_text()
    m = re.search(r'^\s*name\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if m and m.group(1) != new_slug:
        actions.append({
            "type": "update_manifest",
            "description": f"Cargo.toml: update name '{m.group(1)}' → '{new_slug}'",
            "file": "Cargo.toml",
            "field": "package.name",
            "old": m.group(1),
            "new": new_slug,
        })
    return actions


def scan_go_mod(project: Path, new_slug: str) -> list[dict]:
    actions = []
    path = project / "go.mod"
    if not path.exists():
        return actions
    text = path.read_text()
    m = re.match(r"module\s+(\S+)", text)
    if not m:
        return actions
    mod = m.group(1)
    parts = mod.rsplit("/", 1)
    if len(parts) == 2 and parts[1] != new_slug:
        new_mod = f"{parts[0]}/{new_slug}"
        actions.append({
            "type": "update_manifest",
            "description": f"go.mod: update module '{mod}' → '{new_mod}'",
            "file": "go.mod",
            "field": "module",
            "old": mod,
            "new": new_mod,
        })
    return actions


def scan_python_imports(project: Path, old_snake: str, new_snake: str) -> list[dict]:
    if old_snake == new_snake:
        return []
    hits = []
    for py in project.rglob("*.py"):
        if ".venv" in py.parts or "node_modules" in py.parts:
            continue
        try:
            text = py.read_text()
        except (OSError, UnicodeDecodeError):
            continue
        pat = rf"\b(?:import\s+{re.escape(old_snake)}|from\s+{re.escape(old_snake)})\b"
        if re.search(pat, text):
            hits.append(str(py.relative_to(project)))
    if not hits:
        return []
    return [{
        "type": "fix_python_imports",
        "description": f"Update Python imports '{old_snake}' → '{new_snake}' in {len(hits)} file(s)",
        "old_import": old_snake,
        "new_import": new_snake,
        "files": hits,
    }]


def scan_lock_files(project: Path) -> list[dict]:
    locks = ["uv.lock", "bun.lock", "package-lock.json", "Cargo.lock", "go.sum"]
    found = [lf for lf in locks if (project / lf).exists()]
    if not found:
        return []
    return [{
        "type": "regenerate_lock_files",
        "description": f"Regenerate lock file(s): {', '.join(found)}",
        "files": found,
    }]


def scan_venv(project: Path) -> list[dict]:
    if (project / ".venv").is_dir():
        return [{
            "type": "recreate_venv",
            "description": "Recreate .venv (rm + uv venv + uv sync)",
        }]
    return []


def scan_docs(project: Path, old_slug: str, old_snake: str) -> list[dict]:
    doc_globs = ["README.md", "CLAUDE.md", "AGENTS.md", "docs/**/*.md"]
    hits = []
    for pattern in doc_globs:
        for md in project.glob(pattern):
            try:
                text = md.read_text()
            except (OSError, UnicodeDecodeError):
                continue
            if old_slug in text or old_snake in text:
                hits.append(str(md.relative_to(project)))
    if not hits:
        return []
    return [{
        "type": "update_docs",
        "description": f"Update references in {len(hits)} doc(s): {', '.join(hits)}",
        "old_slug": old_slug,
        "old_snake": old_snake,
        "files": hits,
    }]


def scan(project_path: str, new_name: str) -> dict:
    project = Path(project_path).resolve()
    if not project.is_dir():
        return {"error": f"Not a directory: {project}"}

    old_slug = project.name
    new_slug = slugify(new_name)
    old_snake = to_snake(old_slug)
    new_snake = to_snake(new_slug)

    actions = []

    # Order: github first, then manifests, imports, docs, locks, venv, folder last
    actions.extend(scan_github(project, new_slug))
    actions.extend(scan_pyproject(project, new_slug, new_snake))
    actions.extend(scan_package_json(project, new_slug))
    actions.extend(scan_cargo_toml(project, new_slug))
    actions.extend(scan_go_mod(project, new_slug))
    actions.extend(scan_python_imports(project, old_snake, new_snake))
    actions.extend(scan_docs(project, old_slug, old_snake))
    actions.extend(scan_lock_files(project))
    actions.extend(scan_venv(project))

    folder_action = scan_folder(project, old_slug, new_slug)
    if folder_action:
        actions.append(folder_action)

    return {
        "project": str(project),
        "old_slug": old_slug,
        "new_slug": new_slug,
        "old_snake": old_snake,
        "new_snake": new_snake,
        "action_count": len(actions),
        "actions": actions,
    }


def print_human(result: dict):
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Project:   {result['project']}")
    print(f"Rename:    {result['old_slug']} → {result['new_slug']}")
    if result["old_snake"] != result["old_slug"]:
        print(f"Snake:     {result['old_snake']} → {result['new_snake']}")
    print(f"Actions:   {result['action_count']}")
    print()

    if not result["actions"]:
        print("No rename actions needed.")
        return

    for i, action in enumerate(result["actions"], 1):
        print(f"  {i}. [{action['type']}] {action['description']}")
    print()


def main():
    if len(sys.argv) < 3:
        print("Usage: scan_project.py <project-path> <new-name> [--json]", file=sys.stderr)
        sys.exit(1)

    project_path = sys.argv[1]
    new_name = sys.argv[2]
    use_json = "--json" in sys.argv

    result = scan(project_path, new_name)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
