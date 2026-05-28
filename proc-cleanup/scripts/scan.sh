#!/bin/bash
# Scan for Claude, MCP server, and dev server processes on macOS
# Usage: scan.sh [--json] [--ports]
set -euo pipefail

JSON=false
PORTS=false
for arg in "$@"; do
  case "$arg" in
    --json) JSON=true ;;
    --ports) PORTS=true ;;
  esac
done

# --- Claude Code processes ---
claude_procs() {
  ps aux | grep -E '[c]laude|[C]laude' | grep -v 'Claude\.app' | grep -v 'grep' | grep -v 'scan\.sh' || true
}

# --- MCP servers ---
orphan_mcps() {
  ps aux | grep -E '[m]cp-server|[m]cp_server|mcp-server\.cjs' | grep -v 'grep' || true
}

# --- Dev servers ---
dev_servers() {
  ps aux | grep -E '[n]ode.*dev|[v]ite|[n]ext.*dev|[n]uxt|[u]vicorn|[f]astapi|[g]unicorn|[f]lask.*run|python.*[h]ttp\.server|[l]ive-server|[w]ebpack.*dev|[t]urbo.*dev|[b]un.*dev|[d]eno.*serve' | grep -v 'grep' || true
}

# --- Port listeners (common dev ports) ---
port_listeners() {
  local ports="3000 3001 4173 5173 5174 8000 8080 8888 9000 4200 4321"
  for port in $ports; do
    lsof -iTCP:"$port" -sTCP:LISTEN -P -n 2>/dev/null || true
  done | sort -u
}

# --- Top resource hogs (macOS ps has no --sort, use sort command) ---
resource_hogs() {
  ps aux | sort -k3 -rn | head -10
}

if $JSON; then
  # Structured output for programmatic use
  echo '{'

  echo '"claude": ['
  claude_procs | awk '{printf "{\"pid\":%s,\"cpu\":\"%s\",\"mem\":\"%s\",\"cmd\":\"%s\"},\n", $2, $3, $4, substr($0,index($0,$11))}' | sed '$ s/,$//'
  echo '],'

  echo '"mcp_servers": ['
  orphan_mcps | awk '{printf "{\"pid\":%s,\"cpu\":\"%s\",\"mem\":\"%s\",\"cmd\":\"%s\"},\n", $2, $3, $4, substr($0,index($0,$11))}' | sed '$ s/,$//'
  echo '],'

  echo '"dev_servers": ['
  dev_servers | awk '{printf "{\"pid\":%s,\"cpu\":\"%s\",\"mem\":\"%s\",\"cmd\":\"%s\"},\n", $2, $3, $4, substr($0,index($0,$11))}' | sed '$ s/,$//'
  echo ']'

  echo '}'
else
  echo "=== Claude Code Processes ==="
  result=$(claude_procs)
  if [ -n "$result" ]; then
    echo "$result" | awk '{printf "  PID %-7s CPU: %5s%%  MEM: %5s%%  %s\n", $2, $3, $4, substr($0,index($0,$11))}'
  else
    echo "  (none)"
  fi

  echo ""
  echo "=== MCP Servers ==="
  result=$(orphan_mcps)
  if [ -n "$result" ]; then
    echo "$result" | awk '{printf "  PID %-7s CPU: %5s%%  MEM: %5s%%  %s\n", $2, $3, $4, substr($0,index($0,$11))}'
  else
    echo "  (none)"
  fi

  echo ""
  echo "=== Dev Servers ==="
  result=$(dev_servers)
  if [ -n "$result" ]; then
    echo "$result" | awk '{printf "  PID %-7s CPU: %5s%%  MEM: %5s%%  %s\n", $2, $3, $4, substr($0,index($0,$11))}'
  else
    echo "  (none)"
  fi

  if $PORTS; then
    echo ""
    echo "=== Port Listeners (dev ports) ==="
    result=$(port_listeners)
    if [ -n "$result" ]; then
      echo "$result" | awk '{printf "  PID %-7s %s → %s\n", $2, $9, $1}'
    else
      echo "  (none)"
    fi
  fi

  echo ""
  echo "=== Top CPU Hogs ==="
  resource_hogs | awk '{printf "  PID %-7s CPU: %5s%%  MEM: %5s%%  %s\n", $2, $3, $4, substr($0,index($0,$11))}'
fi
