#!/usr/bin/env bash
# Run Shopify theme-check linter on a theme directory
# Usage: theme-check.sh [theme-dir] [--auto-correct]
#
# Requires: shopify CLI (npm install -g @shopify/cli)
# Falls back to: theme-check gem if shopify CLI unavailable

set -euo pipefail

THEME_DIR="${1:-.}"
EXTRA_ARGS="${2:-}"

if ! [ -d "$THEME_DIR" ]; then
  echo "Error: Directory '$THEME_DIR' not found" >&2
  exit 1
fi

# Try shopify CLI first, then theme-check gem
if command -v shopify &>/dev/null; then
  echo "Running: shopify theme check (dir: $THEME_DIR)"
  shopify theme check --path "$THEME_DIR" $EXTRA_ARGS
elif command -v theme-check &>/dev/null; then
  echo "Running: theme-check (dir: $THEME_DIR)"
  theme-check "$THEME_DIR" $EXTRA_ARGS
else
  echo "Error: Neither 'shopify' CLI nor 'theme-check' gem found." >&2
  echo "Install: npm install -g @shopify/cli @shopify/theme" >&2
  echo "    or:  gem install theme-check" >&2
  exit 1
fi
