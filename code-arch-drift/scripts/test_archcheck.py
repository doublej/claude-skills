#!/usr/bin/env python3
"""Self-check: a repo with no blueprint must still say so, on stdout, in JSON."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).with_name("archcheck.py"))


def test_no_blueprint_is_not_silent() -> None:
    with tempfile.TemporaryDirectory() as root:
        r = subprocess.run([sys.executable, SCRIPT, "--root", root, "--json"],
                           capture_output=True, text=True)
    assert r.returncode == 2, r.returncode
    payload = json.loads(r.stdout)
    assert payload["status"] == "no_blueprint", payload
    assert payload["count"] == 0, payload
    assert r.stderr.strip(), "no_blueprint must also explain itself on stderr"


if __name__ == "__main__":
    test_no_blueprint_is_not_silent()
    print("ok")
