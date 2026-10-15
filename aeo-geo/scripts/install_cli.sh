#!/usr/bin/env bash
# Install the geo-optimizer-skill CLI (required) and searchstack-aeo (optional).
# Idempotent — safe to rerun.
set -euo pipefail

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
ok()   { printf "✓ %s\n" "$*"; }
warn() { printf "⚠ %s\n" "$*" >&2; }

bold "aeo-geo: tool install"

# Required: uv
if ! command -v uv >/dev/null 2>&1; then
  warn "uv not found. Install it first: brew install uv"
  exit 1
fi

# 1. geo-optimizer-skill (required)
if command -v geo >/dev/null 2>&1; then
  ok "geo CLI already installed: $(geo --version 2>/dev/null || echo unknown)"
else
  bold "Installing geo-optimizer-skill..."
  uv tool install geo-optimizer-skill
  ok "geo CLI installed"
fi

# 2. searchstack-aeo (optional citation monitoring)
read -r -p "Install searchstack-aeo for citation monitoring? [y/N] " ans
case "${ans:-n}" in
  y|Y|yes)
    if command -v searchstack >/dev/null 2>&1; then
      ok "searchstack already installed"
    else
      uv tool install searchstack
      ok "searchstack installed — run 'searchstack init' to configure API keys"
    fi
    ;;
  *)
    ok "skipped searchstack (optional)"
    ;;
esac

# 3. Optional: lychee for dead-link checking
if ! command -v lychee >/dev/null 2>&1; then
  warn "lychee (dead-link checker) not installed — 'cargo install lychee' or 'brew install lychee' if you want it"
fi

bold "Done. Try: geo audit --url https://example.com"
