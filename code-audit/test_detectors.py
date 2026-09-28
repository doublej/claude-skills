#!/usr/bin/env python3
"""Self-check for the regex detectors: real dead code is caught, known false positives are not."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from detectors.conventions import check_import_order
from detectors.deadcode import find_commented_code, find_unused_imports
from detectors.duplicates import find_similar_functions

FILES = {
    "App.svelte": "<script>\nimport type { Q } from './q'\nlet q: Q\n</script>\n{#if q}\n{/if}\n",
    "flow.ts": "// policy === 'trunk': ours\n// const old = compute(x);\nconst y = 1 // note = here;\n",
    "mod.py": "from __future__ import annotations\nimport os\nimport xml.etree.ElementTree as ET\n# def gone(x):\n# for each file we scan\nprint(ET)\n",
    "View.swift": "import SwiftUI\nstruct V {}\n",
    "lib.c": "#if DEBUG\nint x;\n#endif\n",
}

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for name, text in FILES.items():
        (root / name).write_text(text)

    commented = {(f["file"], f["line"]) for f in find_commented_code(root)}
    assert commented == {("flow.ts", 2), ("mod.py", 4)}, commented

    unused = {(f["file"], f["message"]) for f in find_unused_imports(root)}
    assert unused == {("mod.py", "Unused import: os")}, unused

    assert check_import_order(root / "mod.py") == [], "__future__ and os are stdlib"

    (root / "twin.ts").write_text(  # indented and braced: both body patterns match it
        "  async function addGlossaryFor(dir: string, claudeId: string | null): Promise<void> {\n"
        "    const g = await glossaryIn(dir)\n"
        "    if (g) await addNode(g, 'glossary', claudeId)\n"
        "  }\n"
    )
    assert find_similar_functions(root) == [], "one function is not its own duplicate"

print("detectors self-check: ok")
