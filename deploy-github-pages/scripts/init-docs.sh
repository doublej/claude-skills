#!/bin/bash
# Scaffold an flt-quality GitHub Pages docs site from the bundled templates.
#
# Usage:   init-docs.sh [PROJECT_ROOT]
# Override any field via environment variables:
#   REPO_NAME PROJECT_NAME WORDMARK REPO_SLUG REPO_URL PROJECT_TITLE
#   PROJECT_DESCRIPTION FIRST_LETTER
#
# Copies assets/scaffold/ -> docs/, strips the .tmpl suffix, substitutes
# {{PLACEHOLDERS}}, and installs the deploy workflow. After running, fill the
# real content into docs/src/routes/+page.svelte and the features page.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCAFFOLD="$SKILL_DIR/assets/scaffold"
WORKFLOW_TMPL="$SKILL_DIR/assets/deploy-docs.template.yml"

PROJECT_ROOT="${1:-.}"
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"

# --- Derive defaults --------------------------------------------------------
REPO_NAME="${REPO_NAME:-$(basename "$PROJECT_ROOT")}"
PROJECT_NAME="${PROJECT_NAME:-$REPO_NAME}"
WORDMARK="${WORDMARK:-$REPO_NAME}"

# REPO_SLUG (owner/repo) from the git remote when available.
if [ -z "${REPO_SLUG:-}" ]; then
  origin="$(git -C "$PROJECT_ROOT" remote get-url origin 2>/dev/null || true)"
  REPO_SLUG="$(printf '%s' "$origin" | sed -E 's#^.*github.com[:/]##; s#\.git$##')"
  [ -z "$REPO_SLUG" ] && REPO_SLUG="OWNER/$REPO_NAME"
fi
REPO_URL="${REPO_URL:-https://github.com/$REPO_SLUG}"
PROJECT_TITLE="${PROJECT_TITLE:-$REPO_NAME}"
PROJECT_DESCRIPTION="${PROJECT_DESCRIPTION:-}"
FIRST_LETTER="${FIRST_LETTER:-$(printf '%s' "$REPO_NAME" | cut -c1 | tr '[:lower:]' '[:upper:]')}"

echo "Scaffolding docs for: $REPO_NAME"
echo "  base path : /$REPO_NAME"
echo "  repo      : $REPO_URL"

# --- Copy scaffold ----------------------------------------------------------
DOCS="$PROJECT_ROOT/docs"
mkdir -p "$DOCS"
cp -R "$SCAFFOLD/." "$DOCS/"

mkdir -p "$PROJECT_ROOT/.github/workflows"
cp "$WORKFLOW_TMPL" "$PROJECT_ROOT/.github/workflows/deploy-docs.yml"

# --- Strip .tmpl suffix and substitute placeholders -------------------------
subst() {
  sed -e "s|{{REPO_NAME}}|$REPO_NAME|g" \
      -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
      -e "s|{{WORDMARK}}|$WORDMARK|g" \
      -e "s|{{REPO_SLUG}}|$REPO_SLUG|g" \
      -e "s|{{REPO_URL}}|$REPO_URL|g" \
      -e "s|{{PROJECT_TITLE}}|$PROJECT_TITLE|g" \
      -e "s|{{PROJECT_DESCRIPTION}}|$PROJECT_DESCRIPTION|g" \
      -e "s|{{FIRST_LETTER}}|$FIRST_LETTER|g"
}

find "$DOCS" -name '*.tmpl' | while read -r tmpl; do
  out="${tmpl%.tmpl}"
  subst < "$tmpl" > "$out"
  rm "$tmpl"
done

echo ""
echo "Scaffold ready. Next:"
echo "  cd $DOCS && bun install && bun run dev"
echo ""
echo "Then fill real content into:"
echo "  docs/src/routes/+page.svelte          (demo steps, features, commands)"
echo "  docs/src/routes/features/+page.svelte (feature deep-dives)"
echo "  docs/src/lib/components/Nav.svelte     (nav links)"
echo "  docs/src/app.html                      (replace YOUR_WEBSITE_ID with the Umami id)"
