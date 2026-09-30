#!/usr/bin/env bash
set -euo pipefail

PROMPT="${1:?Usage: launch_cli.sh <prompt> [codex flags...]}"
shift
CODEX_BIN="$(command -v codex)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-interactive.XXXXXX")"
COMMAND_FILE="$RUN_DIR/codex.command"
{
  printf '#!/usr/bin/env bash\nset -euo pipefail\n'
  printf 'cd %q\n' "$PWD"
  printf 'exec %q ' "$CODEX_BIN"
  printf '%q ' "$@" -- "$PROMPT"
  printf '\n'
} > "$COMMAND_FILE"
chmod 700 "$COMMAND_FILE"
SESSION_ID="$(bash "$SCRIPT_DIR/launch_iterm.sh" "$COMMAND_FILE" "Codex: $(basename "$PWD")")"
printf 'Interactive Codex launched in iTerm2 session %s: %s\n' "$SESSION_ID" "$COMMAND_FILE"
