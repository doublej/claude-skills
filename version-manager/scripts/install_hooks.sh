#!/bin/bash
# Install git hooks for version management

set -e

# Get script directory (skill/scripts)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
HOOKS_SOURCE="$SKILL_DIR/hooks"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "✗ Not a git repository"
    exit 1
fi

HOOKS_DEST=".git/hooks"

echo "Installing git hooks..."
echo "Source: $HOOKS_SOURCE"
echo "Dest: $HOOKS_DEST"
echo ""

# Install each hook
for hook in "$HOOKS_SOURCE"/*; do
    if [ -f "$hook" ]; then
        hook_name=$(basename "$hook")
        dest_path="$HOOKS_DEST/$hook_name"

        # Copy hook
        cp "$hook" "$dest_path"
        chmod +x "$dest_path"

        echo "✓ Installed $hook_name"
    fi
done

echo ""
echo "✅ Git hooks installed successfully"
echo ""
echo "Hooks installed:"
echo "  pre-commit  - Validate version consistency"
echo "  commit-msg  - Enforce conventional commits (opt-in, create .conventional-commits file to enable)"
echo "  pre-push    - Validate tag format"
