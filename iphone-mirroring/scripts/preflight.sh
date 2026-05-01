#!/usr/bin/env bash
# preflight.sh — verify the host is ready to drive iPhone Mirroring.
# Exits non-zero with a human-readable reason if anything is missing.
set -u

OK="✅"; FAIL="❌"; WARN="⚠️ "
status=0

say() { printf '%s %s\n' "$1" "$2"; }
fail() { say "$FAIL" "$1"; status=1; }

# 1. macOS version
ver=$(sw_vers -productVersion)
major=${ver%%.*}
if [ "$major" -ge 15 ]; then say "$OK" "macOS $ver"
else fail "macOS $ver — need 15+ (Sequoia) or 26+"
fi

# 2. iPhone Mirroring app present
if [ -d "/System/Applications/iPhone Mirroring.app" ]; then say "$OK" "iPhone Mirroring.app present"
else fail "iPhone Mirroring.app not found"
fi

# 3. Paired device
paired=$(defaults read com.apple.ScreenContinuity onenessPairedDeviceID 2>/dev/null || true)
if [ -n "$paired" ]; then say "$OK" "Paired device: $paired"
else say "$WARN" "No paired device. Open iPhone Mirroring once and accept on iPhone."
fi

# 4. cliclick
if command -v cliclick >/dev/null; then say "$OK" "cliclick: $(command -v cliclick)"
else fail "cliclick missing — brew install cliclick"
fi

# 5. uv
if command -v uv >/dev/null; then say "$OK" "uv: $(uv --version | head -1)"
else fail "uv missing — curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# 6. OmniParser server
if curl -fsS --max-time 1 http://127.0.0.1:8765/health >/dev/null 2>&1; then
  say "$OK" "OmniParser server up at :8765"
else
  say "$WARN" "OmniParser server down — bash scripts/serve_omniparser.sh"
fi

# 7. Permissions smoke tests
if cliclick p: >/dev/null 2>&1; then say "$OK" "Accessibility (cliclick can post events)"
else fail "Accessibility denied — System Settings → Privacy → Accessibility"
fi

tmp=$(mktemp -t perm).png
if screencapture -x "$tmp" 2>/dev/null && [ -s "$tmp" ]; then
  say "$OK" "Screen Recording (screencapture works)"
else
  fail "Screen Recording denied — System Settings → Privacy → Screen Recording"
fi
rm -f "$tmp"

if osascript -e 'tell application "System Events" to count processes' >/dev/null 2>&1; then
  say "$OK" "Automation → System Events"
else
  fail "Automation blocked — Privacy → Automation → terminal → System Events"
fi

# 8. Remote Ollama on Fractal (vision LLM lives off-box)
OLLAMA_URL="${OLLAMA_URL:-http://192.168.178.197:11434}"
GEMMA_MODEL="${GEMMA_MODEL:-gemma4-64k:latest}"

if curl -fsS --max-time 3 "$OLLAMA_URL/v1/models" >/dev/null 2>&1; then
  say "$OK" "Fractal Ollama reachable at $OLLAMA_URL"
  if curl -fsS --max-time 3 "$OLLAMA_URL/v1/models" | grep -q "\"$GEMMA_MODEL\""; then
    say "$OK" "Model present: $GEMMA_MODEL"
  else
    say "$WARN" "Model $GEMMA_MODEL not on Fractal. SSH in and: ollama pull $GEMMA_MODEL"
    say "$WARN" "Available models:"
    curl -fsS --max-time 3 "$OLLAMA_URL/v1/models" | python3 -c "import sys,json; [print('   - '+m['id']) for m in json.load(sys.stdin)['data']]" 2>/dev/null || true
  fi
else
  say "$WARN" "Fractal Ollama unreachable at $OLLAMA_URL — Claude vision will be the only backend"
  say "$WARN" "  is Fractal powered on? (homenetwork skill: ssh user@192.168.178.197)"
fi

exit "$status"
