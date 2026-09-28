#!/usr/bin/env python3
"""Self-check for scan_logging.py: bare print counts only beside a real logger, on any line."""

import tempfile
from pathlib import Path

from scan_logging import scan_file

with tempfile.TemporaryDirectory() as tmp:
    cli = Path(tmp) / "cli.py"
    cli.write_text("import sys\n\n\ndef main():\n    print('done')\n")
    service = Path(tmp) / "service.py"
    service.write_text("import logging\nlog = logging.getLogger(__name__)\n\n\ndef run():\n    print('here')\n")

    assert scan_file(cli).calls == [], "a script's print is its output"
    lines = [c.line for c in scan_file(service).calls]
    assert lines == [6], f"stray print beside a logger is found past line 1: {lines}"

print("scan_logging self-check: ok")
