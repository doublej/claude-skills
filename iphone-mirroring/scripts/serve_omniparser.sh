#!/usr/bin/env bash
# serve_omniparser.sh — start the FastAPI wrapper around OmniParser v2.
# Defaults: bind 127.0.0.1:8765, install root $HOME/.local/omniparser
set -euo pipefail

HOST="${OMNI_HOST:-127.0.0.1}"
PORT="${OMNI_PORT:-8765}"
ROOT="${OMNI_ROOT:-$HOME/.local/omniparser}"
REPO="$ROOT/repo"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$REPO" ]; then
  echo "OmniParser repo not found at $REPO" >&2
  echo "See references/omniparser-setup.md for one-time install." >&2
  exit 2
fi

if [ ! -d "$REPO/.venv" ]; then
  echo "Python venv not found at $REPO/.venv" >&2
  echo "See references/omniparser-setup.md for one-time install." >&2
  exit 2
fi

# Already running?
if curl -fsS --max-time 1 "http://$HOST:$PORT/health" >/dev/null 2>&1; then
  echo "OmniParser already up at http://$HOST:$PORT"
  exit 0
fi

cd "$REPO"
# shellcheck disable=SC1091
source .venv/bin/activate

# The server file lives in this skill's scripts/ dir.
exec python "$SCRIPT_DIR/serve_omniparser.py" --host "$HOST" --port "$PORT"
