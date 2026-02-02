#!/usr/bin/env bash
# Check if Obsidian MCP server is reachable and configured.
# Exit 0 = ready, Exit 1 = not available (prints setup guidance).

set -euo pipefail

BASE_URL="${OBSIDIAN_BASE_URL:-http://127.0.0.1:27123}"
API_KEY="${OBSIDIAN_API_KEY:-}"

# 1. Check if Obsidian REST API is reachable
if ! curl -sf --max-time 2 -o /dev/null "$BASE_URL"; then
  echo "STATUS: NOT_REACHABLE"
  echo ""
  echo "Obsidian Local REST API is not responding at $BASE_URL."
  echo ""
  echo "Setup steps:"
  echo "  1. Open Obsidian"
  echo "  2. Settings > Community plugins > Browse"
  echo "  3. Search 'Local REST API' and install it"
  echo "  4. Enable the plugin and copy the API key"
  echo "  5. The API runs on http://127.0.0.1:27123 by default"
  exit 1
fi

# 2. Check if MCP server is configured in Claude settings
MCP_CONFIGURED=false
for cfg in \
  "$HOME/.claude/settings.json" \
  "$HOME/.claude.json" \
  "$HOME/Library/Application Support/Claude/claude_desktop_config.json"; do
  if [ -f "$cfg" ] && grep -qi "obsidian" "$cfg" 2>/dev/null; then
    MCP_CONFIGURED=true
    break
  fi
done

# 3. Check if npx obsidian-mcp-server is available
NPX_AVAILABLE=false
if command -v npx &>/dev/null && npx --yes obsidian-mcp-server --help &>/dev/null 2>&1; then
  NPX_AVAILABLE=true
fi

echo "STATUS: REACHABLE"
echo "BASE_URL: $BASE_URL"
echo "MCP_CONFIGURED: $MCP_CONFIGURED"
echo "NPX_AVAILABLE: $NPX_AVAILABLE"

if [ "$MCP_CONFIGURED" = false ]; then
  echo ""
  echo "WARNING: No Obsidian MCP server found in Claude config."
  echo ""
  echo "To add it, put this in your Claude MCP settings:"
  echo '  {'
  echo '    "mcpServers": {'
  echo '      "obsidian": {'
  echo '        "command": "npx",'
  echo '        "args": ["obsidian-mcp-server"],'
  echo '        "env": {'
  echo '          "OBSIDIAN_API_KEY": "<your-api-key>",'
  echo '          "OBSIDIAN_BASE_URL": "http://127.0.0.1:27123"'
  echo '        }'
  echo '      }'
  echo '    }'
  echo '  }'
fi

exit 0
