#!/bin/bash
# Launch Codex desktop app with prompt copied to clipboard so user can paste.
# Usage: launch_app.sh "<prompt text>"

set -e

PROMPT="${1:?prompt required}"

printf '%s' "$PROMPT" | pbcopy

open -a "Codex" || {
  echo "Codex.app not found at /Applications/Codex.app" >&2
  exit 1
}

osascript -e 'display notification "Prompt copied — paste into Codex (⌘V)" with title "codex-launch:app" sound name "Tink"' >/dev/null 2>&1 || true

echo "✓ Codex app opened. Prompt is on the clipboard — user pastes with ⌘V."
