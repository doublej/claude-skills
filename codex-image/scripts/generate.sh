#!/bin/bash
# Run codex exec to generate an image, then copy result to CWD/tmp/
set -euo pipefail

PROMPT="${1:?Usage: generate.sh \"<image prompt>\" [dest_dir] [input_image]}"
DEST_DIR="${2:-$(pwd)/tmp}"
INPUT_IMAGE="${3:-}"

mkdir -p "$DEST_DIR"

LAST_MSG=$(mktemp)
trap 'rm -f "$LAST_MSG"' EXIT

# Generate mode (text-to-image) or edit mode (image-to-image, when an input image is given)
CODEX_ARGS=(-s danger-full-access --skip-git-repo-check --ephemeral -o "$LAST_MSG")
if [ -n "$INPUT_IMAGE" ]; then
  [ -f "$INPUT_IMAGE" ] || { echo "ERROR: input image not found: $INPUT_IMAGE"; exit 1; }
  CODEX_ARGS+=(-i "$INPUT_IMAGE")
  INSTRUCTION="Edit the provided image with this instruction: $PROMPT"
  echo "▶ Launching Codex image edit..."
else
  INSTRUCTION="Generate an image with this prompt: $PROMPT"
  echo "▶ Launching Codex image generation..."
fi

codex exec "${CODEX_ARGS[@]}" \
  "$INSTRUCTION

After generating, print ONLY the absolute file path of the generated image on a single line prefixed with IMAGE_PATH: — nothing else after that line."

echo "▶ Codex finished. Extracting image path..."

IMAGE_PATH=""

# Try to extract path from last message
if [ -s "$LAST_MSG" ]; then
  IMAGE_PATH=$(grep -oE 'IMAGE_PATH: .+' "$LAST_MSG" | head -1 | sed 's/IMAGE_PATH: //')
fi

# Fallback: find most recent image in codex generated_images
if [ -z "$IMAGE_PATH" ] || [ ! -f "$IMAGE_PATH" ]; then
  CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
  IMAGE_PATH=$(find "$CODEX_HOME/generated_images" -type f \( -name "*.png" -o -name "*.webp" -o -name "*.jpg" \) -newer "$LAST_MSG" 2>/dev/null | sort | tail -1)

  # If no newer files, get the most recently modified
  if [ -z "$IMAGE_PATH" ] || [ ! -f "$IMAGE_PATH" ]; then
    IMAGE_PATH=$(find "$CODEX_HOME/generated_images" -type f \( -name "*.png" -o -name "*.webp" -o -name "*.jpg" \) -exec stat -f '%m %N' {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
  fi
fi

if [ -z "$IMAGE_PATH" ] || [ ! -f "$IMAGE_PATH" ]; then
  echo "ERROR: Could not locate generated image"
  exit 1
fi

FILENAME=$(basename "$IMAGE_PATH")
FINAL="$DEST_DIR/$FILENAME"
cp "$IMAGE_PATH" "$FINAL"

echo "IMAGE_RESULT: $FINAL"
