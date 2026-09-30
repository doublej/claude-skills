#!/usr/bin/env bash
set -euo pipefail

PROMPT="${1:?Usage: generate.sh <brief> [dest_dir] [input_image...]}"
DEST_DIR="${2:-$(pwd)/tmp}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
command -v codex >/dev/null
command -v python3 >/dev/null
mkdir -p "$DEST_DIR"
WORKDIR="$(mktemp -d)"
LAST_MSG="$WORKDIR/result.json"
trap 'rm -rf "$WORKDIR"' EXIT

CODEX_ARGS=(-C "$WORKDIR" -s read-only --skip-git-repo-check --json
  --output-schema "$SCRIPT_DIR/../assets/image-result.schema.json" -o "$LAST_MSG")
[ -z "${CODEX_MODEL:-}" ] || CODEX_ARGS+=(-m "$CODEX_MODEL")
if [ "$#" -gt 2 ]; then
  shift 2
  for INPUT_IMAGE in "$@"; do
    [ -f "$INPUT_IMAGE" ] || { printf 'Input image missing: %s\n' "$INPUT_IMAGE" >&2; exit 1; }
    CODEX_ARGS+=(-i "$(cd "$(dirname "$INPUT_IMAGE")" && pwd -P)/$(basename "$INPUT_IMAGE")")
  done
fi

INSTRUCTION="Create or edit one image according to this visual brief:
$PROMPT

Use only the built-in image generation tool. Attached images have the roles
specified in the brief; inspect local edit targets before editing. Follow the
actual tool schema. Do not silently substitute API calls, models, or drawings.
Do not run git or create, move, or modify files through shell tools. Leave the
image where the built-in tool saves it. Report the exact generated file path.
Return JSON matching the output schema: image_path is the absolute path and
error is null on success. If blocked, image_path is null and error explains why."

bash "$SCRIPT_DIR/../../codex-launch/scripts/run_monitored.sh" "Codex image" \
  codex exec "${CODEX_ARGS[@]}" -- "$INSTRUCTION" >&2
[ -s "$LAST_MSG" ] || { printf 'Codex returned no structured image result.\n' >&2; exit 1; }
python3 "$SCRIPT_DIR/copy_result.py" "$LAST_MSG" "$DEST_DIR"
