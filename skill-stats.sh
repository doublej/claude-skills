#!/bin/bash

# Show statistics for skills
# Usage: ./skill-stats.sh [skill-name]   Stats for one skill
#        ./skill-stats.sh                Stats for all skills

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

EXCLUDE="-not -path '*/.venv/*' -not -path '*/node_modules/*' -not -path '*/.idea/*' -not -path '*/.git/*' -not -path '*/__pycache__/*'"

skill_stats() {
    local skill="$1"
    local dir="$SCRIPT_DIR/$skill"

    if [ ! -d "$dir" ] || [ ! -f "$dir/SKILL.md" ]; then
        return 1
    fi

    # Count files (excluding hidden and vendor dirs)
    local files=$(eval "find '$dir' -type f ! -name '.*' $EXCLUDE" | wc -l | tr -d ' ')

    # Count lines in SKILL.md
    local skill_lines=$(wc -l < "$dir/SKILL.md" | tr -d ' ')

    # Count total lines (all .md files)
    local md_lines=$(eval "find '$dir' -name '*.md' $EXCLUDE -exec cat {} +" 2>/dev/null | wc -l | tr -d ' ')

    # Count scripts
    local scripts=$(eval "find '$dir' -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' -o -name '*.ts' \) $EXCLUDE" 2>/dev/null | wc -l | tr -d ' ')

    # Check for references dir
    local refs=""
    [ -d "$dir/references" ] && refs="refs "
    [ -d "$dir/scripts" ] && refs="${refs}scripts "
    [ -d "$dir/examples" ] && refs="${refs}examples "

    printf "%-28s %4s files  %5s lines  %2s scripts  %s\n" "$skill" "$files" "$md_lines" "$scripts" "$refs"
}

if [ -n "$1" ]; then
    # Single skill
    skill_stats "$1" || echo "Skill '$1' not found"
else
    # All skills
    echo -e "${YELLOW}Skill Statistics${NC}"
    echo "───────────────────────────────────────────────────────────────────"
    printf "%-28s %5s       %6s       %3s\n" "SKILL" "FILES" "LINES" "SCR"
    echo "───────────────────────────────────────────────────────────────────"

    total_files=0
    total_lines=0
    total_scripts=0
    count=0

    for dir in "$SCRIPT_DIR"/*/; do
        name=$(basename "$dir")
        if [ -f "$dir/SKILL.md" ]; then
            skill_stats "$name"

            # Accumulate totals
            files=$(eval "find '$dir' -type f ! -name '.*' $EXCLUDE" | wc -l | tr -d ' ')
            lines=$(eval "find '$dir' -name '*.md' $EXCLUDE -exec cat {} +" 2>/dev/null | wc -l | tr -d ' ')
            scripts=$(eval "find '$dir' -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' -o -name '*.ts' \) $EXCLUDE" 2>/dev/null | wc -l | tr -d ' ')

            total_files=$((total_files + files))
            total_lines=$((total_lines + lines))
            total_scripts=$((total_scripts + scripts))
            ((count++))
        fi
    done

    echo "───────────────────────────────────────────────────────────────────"
    printf "${GREEN}%-28s %4s files  %5s lines  %2s scripts${NC}\n" "TOTAL ($count skills)" "$total_files" "$total_lines" "$total_scripts"
fi
