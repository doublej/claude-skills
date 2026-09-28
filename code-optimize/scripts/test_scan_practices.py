#!/usr/bin/env python3
"""Self-check for scan_practices.py file rules on a throwaway repo (no atlas calls)."""

import subprocess
import tempfile
from pathlib import Path

from scan_practices import scan

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    files = {
        ".env": "TOKEN=x\n",
        ".env.example": "TOKEN=\n",
        "bun.lock": "",
        "package-lock.json": "{}",
        "Justfile": "test:\n    npm run test\n    bun run lint\n",
        "notes.md": f"see {Path.home()}/dev/web/foo\nand {Path.home()}/dev/web/bar\n",
        ".orchestrate/brief.md": f"{Path.home()}/dev/x\n",
        "ui/node_modules/pkg/index.js": "",
        "README.md": "uv pip install -e .\n",
    }
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-f", "."], cwd=root, check=True)

    result = scan(root.resolve(), use_atlas=False)
    rules = result["rule_counts"]

    assert rules["secrets.dotenv"] == 1, ".env flagged, .env.example allowed"
    assert rules["pm.lockfiles"] == 1, "bun.lock + package-lock.json is mixed"
    assert rules["pm.commands"] == 1, "npm in a bun repo; bun run is fine"
    assert rules["paths.devtree"] == 1, "one finding per file, agent scratch skipped"
    assert rules["vendored.tracked"] == 1, "tracked node_modules"
    assert result["count"] == sum(rules.values())
    assert result["skipped"] == [{"rules": "atlas.*", "reason": "--no-atlas"}]

print("scan_practices self-check: ok")
