#!/usr/bin/env bash

# Install skills to Claude Code and/or Codex CLI as symlinks
# Usage: ./install-skill.sh <skill-name>           Install to Claude (default)
#        ./install-skill.sh --codex <skill-name>   Install to Codex
#        ./install-skill.sh --both <skill-name>    Install to both
#        ./install-skill.sh --all                  Install all to Claude
#        ./install-skill.sh --codex --all          Install all to Codex
#        ./install-skill.sh --both --all           Install all to both
#        ./install-skill.sh --validate --all       Check descriptions
#        ./install-skill.sh --budget               Check aggregate token budget
#        ./install-skill.sh --list                 List available skills

set -euo pipefail

CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CODEX_SKILLS_DIR="$HOME/.codex/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLIGNORE_FILE="$SCRIPT_DIR/.skillignore"

CODEX_MODE=false
BOTH_MODE=false
VALIDATE_MODE=false

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Returns 0 if the dir name is listed in .skillignore (one name per line, # comments)
is_ignored() {
    local skill_name="$1"
    [ -f "$SKILLIGNORE_FILE" ] || return 1
    local line
    while IFS= read -r line; do
        # Strip trailing whitespace; skip blanks and comments
        line="${line%"${line##*[![:space:]]}"}"
        case "$line" in
            ''|'#'*) continue ;;
        esac
        if [ "$line" == "$skill_name" ]; then
            return 0
        fi
    done < "$SKILLIGNORE_FILE"
    return 1
}

validate_description() {
    local skill_path="$1"
    local skill_name="$2"
    local skill_file="$skill_path/SKILL.md"

    # Extract description from YAML frontmatter
    local desc=$(sed -n '/^---$/,/^---$/p' "$skill_file" | grep -E '^description:' | sed 's/^description:[[:space:]]*//')
    local len=${#desc}

    if [ "$len" -gt 500 ]; then
        echo -e "${YELLOW}⚠${NC} $skill_name: description is $len chars (Codex limit: 500)"
        return 1
    fi
    return 0
}

install_to_target() {
    local skill_name="$1"
    local target_dir="$2"
    local target_name="$3"
    local source="$SCRIPT_DIR/$skill_name"
    local target="$target_dir/$skill_name"

    # Remove existing (symlink or directory)
    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        rm -rf "$target"
    fi

    ln -s "$source" "$target"
    echo -e "${GREEN}✓${NC} $skill_name → $target_name"
}

install_skill() {
    local skill_name="$1"
    local source="$SCRIPT_DIR/$skill_name"

    if is_ignored "$skill_name"; then
        echo -e "${YELLOW}⚠${NC} $skill_name is listed in .skillignore — skipping"
        return 1
    fi

    if [ ! -d "$source" ]; then
        echo -e "${RED}Error: Skill folder '$skill_name' not found${NC}"
        return 1
    fi

    if [ ! -f "$source/SKILL.md" ]; then
        echo -e "${RED}Error: SKILL.md not found in $skill_name/${NC}"
        return 1
    fi

    # Validate for Codex targets
    if $CODEX_MODE || $BOTH_MODE; then
        validate_description "$source" "$skill_name" || true
    fi

    # Install to appropriate targets
    if $BOTH_MODE; then
        install_to_target "$skill_name" "$CLAUDE_SKILLS_DIR" "Claude"
        install_to_target "$skill_name" "$CODEX_SKILLS_DIR" "Codex"
    elif $CODEX_MODE; then
        install_to_target "$skill_name" "$CODEX_SKILLS_DIR" "Codex"
    else
        install_to_target "$skill_name" "$CLAUDE_SKILLS_DIR" "Claude"
    fi
}

list_skills() {
    echo "Available skills:"
    for dir in "$SCRIPT_DIR"/*/; do
        if [ -f "$dir/SKILL.md" ]; then
            name=$(basename "$dir")
            echo "  $name"
        fi
    done
}

validate_all() {
    echo -e "${YELLOW}Validating descriptions for Codex compatibility...${NC}"
    local warnings=0
    for dir in "$SCRIPT_DIR"/*/; do
        if [ -f "$dir/SKILL.md" ]; then
            name=$(basename "$dir")
            validate_description "$dir" "$name" || warnings=$((warnings + 1))
        fi
    done
    if [ "$warnings" -eq 0 ]; then
        echo -e "${GREEN}All descriptions within 500-char limit${NC}"
    else
        echo -e "${YELLOW}$warnings skill(s) exceed 500-char limit${NC}"
    fi
}

get_target_message() {
    if $BOTH_MODE; then
        echo "Claude Code and Codex CLI"
    elif $CODEX_MODE; then
        echo "Codex CLI"
    else
        echo "Claude Code"
    fi
}

# Dispatch --budget before the generic flag parser (passes remaining args through)
if [ "${1:-}" == "--budget" ]; then
    shift
    exec python3 "$SCRIPT_DIR/validate-context-budget.py" "$@"
fi

# Parse flags
while [[ "${1:-}" == --* ]]; do
    case "$1" in
        --codex)
            CODEX_MODE=true
            shift
            ;;
        --both)
            BOTH_MODE=true
            shift
            ;;
        --validate)
            VALIDATE_MODE=true
            shift
            ;;
        --all|--list)
            break
            ;;
        *)
            echo -e "${RED}Unknown flag: $1${NC}"
            exit 1
            ;;
    esac
done

# Create target directories
mkdir -p "$CLAUDE_SKILLS_DIR"
if $CODEX_MODE || $BOTH_MODE; then
    mkdir -p "$CODEX_SKILLS_DIR"
fi

# Handle validate-only mode
if $VALIDATE_MODE; then
    if [ "${1:-}" == "--all" ]; then
        validate_all
        exit 0
    else
        echo -e "${RED}--validate requires --all${NC}"
        exit 1
    fi
fi

case "${1:-}" in
    --all)
        echo -e "${YELLOW}Installing all skills to $(get_target_message)...${NC}"
        count=0
        for dir in "$SCRIPT_DIR"/*/; do
            if [ -f "$dir/SKILL.md" ]; then
                name=$(basename "$dir")
                if is_ignored "$name"; then
                    continue
                fi
                install_skill "$name" && count=$((count + 1)) || true
            fi
        done
        echo -e "${GREEN}Installed $count skills${NC}"
        echo -e "${YELLOW}Restart $(get_target_message) to load skills${NC}"
        ;;
    --list)
        list_skills
        ;;
    "")
        echo "Usage: $0 [--codex|--both] [--validate] <skill-name>|--all|--list"
        exit 1
        ;;
    *)
        install_skill "$1"
        echo -e "${YELLOW}Restart $(get_target_message) to load the skill${NC}"
        ;;
esac
