#!/usr/bin/env bash
# Run RepoMapper from the bundled source
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPOMAP_DIR="$SCRIPT_DIR/repomap"
VENV_PYTHON="$REPOMAP_DIR/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
  echo "RepoMapper venv not found. Running setup..." >&2
  bash "$SCRIPT_DIR/setup.sh"
fi

export PYTHONPATH="$REPOMAP_DIR:${PYTHONPATH:-}"
exec "$VENV_PYTHON" "$REPOMAP_DIR/repomap.py" "$@"
