#!/usr/bin/env bash
# Enable workremotely mode for a directory scope.
# Usage: enable.sh [host] [--at <path>]
#   host     Remote SSH host alias. Default: nas
#   --at     Directory to scope this to. Default: current working directory.
set -euo pipefail

HOST="nas"
SCOPE="$PWD"

while [ $# -gt 0 ]; do
  case "$1" in
    --at)
      SCOPE="${2:?--at requires a path}"
      shift 2
      ;;
    --at=*)
      SCOPE="${1#--at=}"
      shift
      ;;
    -h|--help)
      echo "Usage: enable.sh [host] [--at <path>]"
      exit 0
      ;;
    *)
      HOST="$1"
      shift
      ;;
  esac
done

if [ ! -d "$SCOPE" ]; then
  echo "error: scope directory does not exist: $SCOPE" >&2
  exit 1
fi

SCOPE="$(cd "$SCOPE" && pwd)"
MARKER="$SCOPE/.workremotely"

printf 'host=%s\n' "$HOST" > "$MARKER"
printf 'enabled_at=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$MARKER"

echo "workremotely ENABLED"
echo "  host:  $HOST"
echo "  scope: $SCOPE"
echo "  marker: $MARKER"
