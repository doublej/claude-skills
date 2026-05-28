#!/usr/bin/env bash
# Setup RepoMapper venv within the skill directory
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPOMAP_DIR="$SCRIPT_DIR/repomap"
VENV_DIR="$REPOMAP_DIR/.venv"

if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" ]; then
  echo "RepoMapper venv already exists at $VENV_DIR"
  exit 0
fi

echo "Creating venv at $VENV_DIR..."
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet -r "$REPOMAP_DIR/requirements.txt"
echo "RepoMapper setup complete."
