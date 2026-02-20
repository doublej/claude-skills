#!/bin/bash

# Interactive skill installer for Codex CLI
# Presents skills in categories and allows multi-select installation

set -e

CODEX_SKILLS_DIR="$HOME/.codex/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Codex CLI Skill Installer ===${NC}\n"
echo "Available skills organized by category:"
echo ""

# Development Tools
echo -e "${YELLOW}Development & Code Tools:${NC}"
echo "  1. codex-cli               - OpenAI Codex CLI usage guide"
echo "  2. claude-code-cli         - Claude Code CLI workflows"
echo "  3. claude-agent-sdk        - Build AI agents with Claude SDK"
echo "  4. dev-refactor            - Codebase architecture analysis"
echo "  5. repomap-analyzer        - Find deprecated patterns/dead code"
echo "  6. modularize              - Split oversized files into modules"
echo "  7. version-manager         - Version bumping and releases"
echo "  8. rename-project          - Safely rename projects"
echo ""

# Documentation & Writing
echo -e "${YELLOW}Documentation & Writing:${NC}"
echo "  9. blog-writer             - Authentic blog posts"
echo " 10. claude-md-optimizer     - Optimize CLAUDE.md files"
echo " 11. github-pages-generator  - Generate docs with SvelteKit"
echo " 12. message-rewriter        - Platform-native messages"
echo " 13. social-promotion        - Social media content"
echo ""

# Design & Creative
echo -e "${YELLOW}Design & Creative:${NC}"
echo " 14. frontend-design         - Production-grade UI"
echo " 15. logo-creator            - SVG logo generation"
echo " 16. creative-director-unhinged - Bold visual design"
echo " 17. screenshot-pipeline     - Polished promo screenshots"
echo " 18. infographic-brief       - Infographic content briefs"
echo ""

# Automation & DevOps
echo -e "${YELLOW}Automation & DevOps:${NC}"
echo " 19. browser-automation      - Puppeteer/Playwright automation"
echo " 20. process-cleanup         - Clean up dev processes"
echo " 21. process-monitor         - Monitor system resources"
echo " 22. nas-deploy              - Deploy to NAS Caddy"
echo ""

# Data & APIs
echo -e "${YELLOW}Data & APIs:${NC}"
echo " 23. pydantic-v2             - Data validation with Pydantic"
echo " 24. shopify-api             - Shopify integrations"
echo " 25. twilio-api              - Twilio SMS/voice integrations"
echo " 26. telegram                - Telegram bot development"
echo " 27. porkbun-api             - Domain/DNS management"
echo ""

# Graphics & Media
echo -e "${YELLOW}Graphics & Media:${NC}"
echo " 28. pixijs-dev              - PixiJS 2D graphics"
echo " 29. pixijs-perf             - PixiJS performance optimization"
echo " 30. threejs                 - Three.js 3D graphics"
echo " 31. theatre-js              - Motion design & animation"
echo " 32. animation-easing        - Animation timing guides"
echo " 33. blender                 - Blender 4.x scripting"
echo ""

# Specialized Tools
echo -e "${YELLOW}Specialized Tools:${NC}"
echo " 34. mermaid-graphs          - Create Mermaid diagrams"
echo " 35. ghostscript             - PDF/PostScript manipulation"
echo " 36. reportlab-pdf           - PDF generation in Python"
echo " 37. icc-color-pdf           - ICC profiles for PDFs"
echo " 38. erdantic                - ERD from data models"
echo " 39. epc-qr                  - SEPA payment QR codes"
echo ""

# Platform-Specific
echo -e "${YELLOW}Platform-Specific:${NC}"
echo " 40. swift-app-ui            - iOS/macOS UI design"
echo " 41. swift-app-arch          - Swift app architecture"
echo " 42. raycast-extensions      - Raycast extensions"
echo " 43. raycast-scripts         - Raycast script commands"
echo " 44. raycast-snippets        - Raycast snippets"
echo " 45. kirby-cms               - Kirby CMS development"
echo ""

# Utilities
echo -e "${YELLOW}Utilities & Meta:${NC}"
echo " 46. skill-creator           - Create new skills"
echo " 47. skill-overview          - List available skills"
echo " 48. context-cascade         - Visualize CLAUDE.md hierarchy"
echo " 49. session-history-analyzer - Analyze session history"
echo " 50. session-search          - Search session history"
echo " 51. chat-archive            - Search ChatGPT/Claude exports"
echo " 52. obsidian                - Manage Obsidian vaults"
echo " 53. tmux                    - Control tmux sessions"
echo " 54. iterm2                  - iTerm2 Python API"
echo ""

echo -e "${BLUE}Installation Options:${NC}"
echo "  all        - Install all 73 skills"
echo "  dev        - Development tools (1-8)"
echo "  docs       - Documentation (9-13)"
echo "  design     - Design & creative (14-18)"
echo "  auto       - Automation (19-22)"
echo "  api        - Data & APIs (23-27)"
echo "  graphics   - Graphics & media (28-33)"
echo "  special    - Specialized tools (34-39)"
echo "  platform   - Platform-specific (40-45)"
echo "  util       - Utilities (46-54)"
echo "  <numbers>  - Specific skills (e.g., '1 5 10' or '1-8')"
echo ""

read -p "What would you like to install? " selection

mkdir -p "$CODEX_SKILLS_DIR"

install_skill() {
    local skill_name="$1"
    local source="$SCRIPT_DIR/$skill_name"
    local target="$CODEX_SKILLS_DIR/$skill_name"

    if [ ! -d "$source" ]; then
        echo -e "${YELLOW}⚠${NC} $skill_name not found, skipping"
        return
    fi

    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        rm -rf "$target"
    fi

    ln -s "$source" "$target"
    echo -e "${GREEN}✓${NC} $skill_name"
}

case "$selection" in
    all)
        echo -e "${YELLOW}Installing all 73 skills...${NC}"
        for dir in "$SCRIPT_DIR"/*/; do
            if [ -f "$dir/SKILL.md" ]; then
                install_skill "$(basename "$dir")"
            fi
        done
        ;;
    dev)
        for skill in codex-cli claude-code-cli claude-agent-sdk dev-refactor repomap-analyzer modularize version-manager rename-project; do
            install_skill "$skill"
        done
        ;;
    docs)
        for skill in blog-writer claude-md-optimizer github-pages-generator message-rewriter social-promotion; do
            install_skill "$skill"
        done
        ;;
    design)
        for skill in frontend-design logo-creator creative-director-unhinged screenshot-pipeline infographic-brief; do
            install_skill "$skill"
        done
        ;;
    auto)
        for skill in browser-automation process-cleanup process-monitor nas-deploy; do
            install_skill "$skill"
        done
        ;;
    api)
        for skill in pydantic-v2 shopify-api twilio-api telegram porkbun-api; do
            install_skill "$skill"
        done
        ;;
    graphics)
        for skill in pixijs-dev pixijs-perf threejs theatre-js animation-easing blender; do
            install_skill "$skill"
        done
        ;;
    special)
        for skill in mermaid-graphs ghostscript reportlab-pdf icc-color-pdf erdantic epc-qr; do
            install_skill "$skill"
        done
        ;;
    platform)
        for skill in swift-app-ui swift-app-arch raycast-extensions raycast-scripts raycast-snippets kirby-cms; do
            install_skill "$skill"
        done
        ;;
    util)
        for skill in skill-creator skill-overview context-cascade session-history-analyzer session-search chat-archive obsidian tmux iterm2; do
            install_skill "$skill"
        done
        ;;
    *)
        # Parse number ranges and individual numbers
        skills=(
            codex-cli claude-code-cli claude-agent-sdk dev-refactor repomap-analyzer
            modularize version-manager rename-project blog-writer claude-md-optimizer
            github-pages-generator message-rewriter social-promotion frontend-design logo-creator
            creative-director-unhinged screenshot-pipeline infographic-brief browser-automation process-cleanup
            process-monitor nas-deploy pydantic-v2 shopify-api twilio-api
            telegram porkbun-api pixijs-dev pixijs-perf threejs
            theatre-js animation-easing blender mermaid-graphs ghostscript
            reportlab-pdf icc-color-pdf erdantic epc-qr swift-app-ui
            swift-app-arch raycast-extensions raycast-scripts raycast-snippets kirby-cms
            skill-creator skill-overview context-cascade session-history-analyzer session-search
            chat-archive obsidian tmux iterm2
        )

        for item in $selection; do
            if [[ "$item" =~ ^([0-9]+)-([0-9]+)$ ]]; then
                # Range like 1-8
                start=${BASH_REMATCH[1]}
                end=${BASH_REMATCH[2]}
                for ((i=start; i<=end; i++)); do
                    idx=$((i-1))
                    if [ $idx -lt ${#skills[@]} ]; then
                        install_skill "${skills[$idx]}"
                    fi
                done
            elif [[ "$item" =~ ^[0-9]+$ ]]; then
                # Single number
                idx=$((item-1))
                if [ $idx -lt ${#skills[@]} ]; then
                    install_skill "${skills[$idx]}"
                fi
            fi
        done
        ;;
esac

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}Restart Codex CLI to load the new skills${NC}"
echo ""
echo "Verify installation:"
echo "  ls -la ~/.codex/skills/"
