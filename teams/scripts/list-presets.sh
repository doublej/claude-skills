#!/usr/bin/env bash
# list-presets.sh — show bundled + user presets with descriptions.
set -euo pipefail

SKILL_DIR="${TEAMS_SKILL_DIR:-$HOME/.claude/skills/teams}"
BUNDLED="$SKILL_DIR/presets"
USER_DIR="$HOME/.claude/team-presets"

printf "%-28s %-10s %s\n" "preset" "source" "description"
printf "%-28s %-10s %s\n" "------" "------" "-----------"

declare -A SEEN

print_preset() {
  local file="$1"
  local source="$2"
  local name; name="$(basename "$file" .yaml)"
  [[ "$name" == "_schema" ]] && return
  local desc
  desc=$(awk '/^description:/{sub(/^description:[ \t]*/, ""); gsub(/\\n/, " "); print; exit}' "$file" 2>/dev/null)
  # Handle YAML folded scalars on next line
  if [[ -z "$desc" ]]; then
    desc=$(awk 'BEGIN{f=0} /^description:/{f=1;next} f&&/^[ \t]+[^ ]/{sub(/^[ \t]+/, ""); print; exit}' "$file")
  fi
  printf "%-28s %-10s %s\n" "$name" "$source" "${desc:-"(no description)"}"
  SEEN["$name"]=1
}

# User overrides first (they win).
if [[ -d "$USER_DIR" ]]; then
  for f in "$USER_DIR"/*.yaml; do
    [[ -f "$f" ]] || continue
    print_preset "$f" "(user)"
  done
fi

# Bundled — skip if user override already printed that name.
if [[ -d "$BUNDLED" ]]; then
  for f in "$BUNDLED"/*.yaml; do
    [[ -f "$f" ]] || continue
    name="$(basename "$f" .yaml)"
    [[ -n "${SEEN[$name]:-}" ]] && continue
    print_preset "$f" "(bundled)"
  done
fi
