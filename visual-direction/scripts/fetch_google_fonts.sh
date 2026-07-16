#!/usr/bin/env bash
set -euo pipefail
# Fetch Google Fonts TTFs into the user fontconfig dir so rsvg-convert can render them.
# Usage: fetch_google_fonts.sh "Family Name:400,600,700" ["Second Family:400,500"] ...
# Weights are optional (default 400,700). Prints the fontconfig match per family so the
# caller can verify the face actually resolves before rendering.

FONT_DIR="${HOME}/.local/share/fonts/visual-direction"
mkdir -p "$FONT_DIR"

for spec in "$@"; do
  family="${spec%%:*}"
  weights="400,700"
  if [[ "$spec" == *:* ]]; then weights="${spec#*:}"; fi
  css_url="https://fonts.googleapis.com/css2?family=${family// /+}:wght@${weights//,/;}"
  css="$(curl -fsS "$css_url")" # default curl UA -> Google serves TTF urls
  i=0
  while IFS= read -r url; do
    i=$((i + 1))
    curl -fsS -o "${FONT_DIR}/${family// /-}-${i}.ttf" "$url"
  done < <(grep -oE 'https://[^) ]+\.ttf' <<<"$css" | sort -u)
  echo "fetched ${i} file(s) for ${family}"
done

fc-cache -f "$FONT_DIR" >/dev/null
for spec in "$@"; do
  family="${spec%%:*}"
  echo "fc-match ${family}: $(fc-match "$family")"
done
