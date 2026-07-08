#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (static frontend)
# Zero-downtime: stages the full site next to the live dir, then swaps it in
# with two NAS-side renames. The site is only "in between" for the rename
# instant, not for the whole rsync.
# Usage: ./deploy-frontend.sh [--force]   (--force overwrites an existing site)

set -euo pipefail

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
SOURCE_DIR="{{SOURCE_DIR}}"
SITE="${SUBDOMAIN}.jurrejan.com"
WWW_MAC="/Volumes/Container/caddy/www"
WWW_NAS="/share/CACHEDEV1_DATA/Container/caddy/www"
TARGET_DIR="${WWW_MAC}/${SITE}"
# Dot-prefixed so apply_from_mac.sh's www/*/ scan never imports a half-staged site
STAGING=".staging-${SITE}"

FORCE=0
if [ "${1:-}" = "--force" ]; then FORCE=1; fi

# Colors
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${YELLOW}Deploying ${SITE}...${NC}"

# Check mount
if [ ! -d "$WWW_MAC" ]; then
    echo -e "${RED}Error: Caddy volume not mounted${NC}"
    open "smb://jongserve.local/Container"   # NOT nas.local — that name does not resolve
    echo "Please authenticate and retry."
    exit 1
fi

# Guard: never clobber an existing live site unless --force
if [ -d "$TARGET_DIR" ] && [ "$FORCE" -eq 0 ]; then
    echo -e "${RED}Refusing to overwrite existing site: ${SITE}${NC}"
    echo "Re-run with --force if you really mean to replace it."
    exit 1
fi

# Stage: build the complete new site beside the live one (live site untouched)
echo -e "${YELLOW}Staging files (live site keeps serving)...${NC}"
ssh nas "rm -rf '${WWW_NAS}/${STAGING}'"   # SMB rm is unreliable; clean NAS-side
mkdir -p "${WWW_MAC}/${STAGING}"
rsync -av \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    "$SOURCE_DIR/" "${WWW_MAC}/${STAGING}/"

# Generate the site's Caddy config into staging (root inside the container is /var/www/<site>)
cat > "${WWW_MAC}/${STAGING}/${SUBDOMAIN}.caddy" <<EOF
${SITE} {
    import default_site
    root * /var/www/${SITE}
}
EOF

# Switch: two renames on the NAS — effectively instant.
# The old tree is deleted afterwards; it must not linger, or its duplicate
# .caddy would fail validation on the next apply.
echo -e "${YELLOW}Switching to new version...${NC}"
ssh nas "cd '${WWW_NAS}' \
    && rm -rf '${SITE}.old' \
    && { [ ! -d '${SITE}' ] || mv '${SITE}' '${SITE}.old'; } \
    && mv '${STAGING}' '${SITE}' \
    && rm -rf '${SITE}.old'"

# Apply (regenerates imports, validates, reloads — Caddy reloads are graceful)
echo -e "${YELLOW}Applying Caddy config...${NC}"
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh

echo -e "${GREEN}Deployed to https://${SITE}${NC}"
