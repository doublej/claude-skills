#!/usr/bin/env bash
# scan-fonts.sh — Scan project for font-family declarations, output Mermaid LR flowchart
# Usage: scan-fonts.sh [project-dir]
set -euo pipefail

DIR="${1:-.}"
DIR="$(cd "$DIR" && pwd)"

DECLS=$(mktemp)
trap 'rm -f "$DECLS"' EXIT

rel() { echo "${1#"$DIR"/}"; }

# --- CSS/SCSS parser: tracks selector context across { } blocks ---
parse_css() {
  local file="$1" line_offset="${2:-0}"
  awk -v file="$file" -v offset="$line_offset" '
    BEGIN { depth=0; selector=""; buf=""; in_comment=0 }
    {
      line = $0
      # Handle multi-line comments
      if (in_comment) {
        if (line ~ /\*\//) { sub(/.*\*\//, "", line); in_comment=0 }
        else next
      }
      # Strip inline comments /* ... */
      gsub(/\/\*.*\*\//, "", line)
      # Start of multi-line comment
      if (line ~ /\/\*/) { sub(/\/\*.*/, "", line); in_comment=1 }
      # Skip blank lines
      if (line ~ /^[[:space:]]*$/) next
      # Skip @font-face, @import, @keyframes blocks
      if (line ~ /^[[:space:]]*@(font-face|import|keyframes|media)/) { skip=1 }
      if (skip && line ~ /\}/) { skip=0; next }
      if (skip) next

      # Track selector: accumulate text before {
      if (line ~ /\{/) {
        # Everything before { on this line + buffered text = selector
        split(line, parts, "{")
        candidate = buf parts[1]
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", candidate)
        gsub(/[[:space:]]+/, " ", candidate)
        # Skip empty or comment remnants
        if (candidate != "" && candidate !~ /^[=*\/]/) {
          if (depth == 0) selector = candidate
          else selector = selector " " candidate
        }
        buf = ""
        depth++
      }

      # Check for font-family declaration
      if (line ~ /font-family[[:space:]]*:/ && line !~ /--font-family/) {
        val = line
        sub(/.*font-family[[:space:]]*:[[:space:]]*/, "", val)
        sub(/[[:space:]]*;.*/, "", val)
        sub(/[[:space:]]*!important/, "", val)
        sub(/[[:space:]]*\}.*/, "", val)
        gsub(/[[:space:]]+/, " ", val)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", val)
        lnum = NR + offset
        if (selector != "") print selector "|" val "|" file ":" lnum
      }

      if (line ~ /\}/) {
        depth--
        if (depth <= 0) { selector = ""; depth = 0 }
        buf = ""
      }

      # Buffer non-block lines as potential selector text
      if (line !~ /[{}]/ && depth == 0) {
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
        if (line != "") buf = buf " " line
      }
    }
  '
}

# Scan .css and .scss/.sass files
find "$DIR" -type f \( -name '*.css' -o -name '*.scss' -o -name '*.sass' \) \
  ! -path '*/node_modules/*' ! -path '*/.svelte-kit/*' ! -path '*/dist/*' \
  ! -path '*/.git/*' ! -path '*/vendor/*' ! -path '*/build/*' ! -path '*/.claude/*' \
  2>/dev/null | sort | while read -r f; do
  parse_css "$(rel "$f")" 0 < "$f" >> "$DECLS"
done

# Scan .svelte files — extract <style> blocks, preserve line numbers
find "$DIR" -type f -name '*.svelte' \
  ! -path '*/node_modules/*' ! -path '*/.svelte-kit/*' ! -path '*/dist/*' \
  ! -path '*/.git/*' ! -path '*/build/*' ! -path '*/.claude/*' \
  2>/dev/null | sort | while read -r f; do
  rf="$(rel "$f")"
  # Extract style block with line offset
  awk '
    /<style[^>]*>/ { inside=1; start=NR; next }
    /<\/style>/ { inside=0; next }
    inside { print }
  ' "$f" 2>/dev/null | parse_css "$rf" 0 >> "$DECLS"
done

# Scan Tailwind config
for tw in "$DIR"/tailwind.config.{js,ts,mjs,cjs}; do
  [ -f "$tw" ] || continue
  rf="$(rel "$tw")"
  command -v node &>/dev/null || continue
  node -e "
    const fs = require('fs');
    const src = fs.readFileSync('$tw', 'utf8');
    const m = src.match(/fontFamily[^{]*\{([^}]+)\}/s);
    if (!m) process.exit(0);
    const entries = [...m[1].matchAll(/(\w+)\s*:\s*\[([^\]]+)\]/g)];
    const lines = src.split('\n');
    for (const e of entries) {
      const key = e[1];
      const fonts = e[2].replace(/[\"']/g, '').split(',').map(s => s.trim()).join(', ');
      const ln = lines.findIndex(l => l.includes(key) && l.includes('[')) + 1;
      console.log('tw:' + key + '|' + fonts + '|$rf:' + ln);
    }
  " 2>/dev/null >> "$DECLS"
done

# --- Build Mermaid output ---
if [ ! -s "$DECLS" ]; then
  echo "No font-family declarations found in: $DIR"
  exit 0
fi

# Deterministic: sort and deduplicate
sort -t'|' -k1,1 -k3,3 "$DECLS" | uniq > "${DECLS}.sorted"
mv "${DECLS}.sorted" "$DECLS"

# Escape for Mermaid node labels
esc() { printf '%s' "$1" | sed 's/"/\&quot;/g'; }

# Find body/html/:root declarations (roots)
BODY_LINE=$(grep -iE '^(body|html|:root)\b' "$DECLS" | head -1 || true)

echo '```mermaid'
echo 'flowchart LR'

if [ -n "$BODY_LINE" ]; then
  sel=$(echo "$BODY_LINE" | cut -d'|' -f1)
  fonts=$(echo "$BODY_LINE" | cut -d'|' -f2)
  loc=$(echo "$BODY_LINE" | cut -d'|' -f3)
  echo "  root[\"$(esc "$sel") → $(esc "$fonts")<br/><small>$(esc "$loc")</small>\"]"
else
  echo '  root["body → (not set)"]'
fi

N=1
grep -ivE '^(body|html|:root)\b' "$DECLS" | while IFS='|' read -r selector fonts loc; do
  [ -z "$selector" ] && continue
  echo "  n${N}[\"$(esc "$selector") → $(esc "$fonts")<br/><small>$(esc "$loc")</small>\"]"
  echo "  root --> n${N}"
  N=$((N + 1))
done

echo '```'
