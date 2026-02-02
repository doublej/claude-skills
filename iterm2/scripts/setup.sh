#!/bin/bash
# Setup venv for iTerm2 Python API scripts
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/pip" install -q iterm2
  echo "iTerm2 venv created at $VENV_DIR"
else
  echo "iTerm2 venv already exists"
fi
