#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
SOURCE="$SCRIPT_DIR/../assets/codex-live-monitor.md"
TARGET="$HOME/.claude/rules/codex-live-monitor.md"
mkdir -p "$(dirname "$TARGET")"
if [ -e "$TARGET" ] && [ ! -L "$TARGET" ]; then
  printf 'Refusing to replace existing rule: %s\n' "$TARGET" >&2
  exit 1
fi
ln -sfn "$SOURCE" "$TARGET"
printf 'Installed global Claude rule: %s\n' "$TARGET"
