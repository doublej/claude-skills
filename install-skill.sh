#!/bin/bash

# Install a skill to Claude Code
# Usage: ./install-skill.sh <skill-folder-name>

set -e

SKILL_NAME="$1"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CURRENT_DIR="$(pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-folder-name>"
    exit 1
fi

if [ ! -d "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill folder '$SKILL_NAME' not found in current directory${NC}"
    exit 1
fi

if [ ! -f "$SKILL_NAME/SKILL.md" ]; then
    echo -e "${RED}Error: SKILL.md not found in $SKILL_NAME/${NC}"
    echo "A valid skill must contain a SKILL.md file"
    exit 1
fi

echo -e "${YELLOW}Installing skill: $SKILL_NAME${NC}"

mkdir -p "$CLAUDE_SKILLS_DIR"

TARGET="$CLAUDE_SKILLS_DIR/$SKILL_NAME"

if [ -L "$TARGET" ]; then
    echo -e "${YELLOW}Removing existing symlink...${NC}"
    rm "$TARGET"
elif [ -d "$TARGET" ]; then
    echo -e "${RED}Error: Directory already exists at $TARGET${NC}"
    echo "Remove it first or use a different skill name"
    exit 1
fi

ln -s "$CURRENT_DIR/$SKILL_NAME" "$TARGET"

echo -e "${GREEN}✓ Skill installed successfully!${NC}"
echo -e "${GREEN}✓ Symlinked: $TARGET -> $CURRENT_DIR/$SKILL_NAME${NC}"
echo -e "${YELLOW}Restart Claude Code to load the skill${NC}"
