#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (static frontend)
# Zero-downtime: stages the full site over SSH (delta rsync — much faster than
# SMB), then swaps it in with two NAS-side renames. The previous release is
# kept as <site>.old (its .caddy stripped, so validation can't trip on it):
# rollback is one rename away.
# Usage: ./deploy-frontend.sh [--force]   (--force overwrites an existing site)

set -euo pipefail

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
SOURCE_DIR="{{SOURCE_DIR}}"
SITE="${SUBDOMAIN}.jurrejan.com"
WWW_NAS="/share/CACHEDEV1_DATA/Container/caddy/www"
ETC_MAC="/Volumes/Container/caddy/etc"
MOUNT_HELPER="$HOME/.claude/skills/deploy-nas/scripts/mount-nas.sh"

FORCE=0
if [ "${1:-}" = "--force" ]; then FORCE=1; fi

# Colors
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${YELLOW}Deploying ${SITE}...${NC}"

# Guard: never clobber an existing live site unless --force (checked over SSH)
if ssh nas "[ -d '${WWW_NAS}/${SITE}' ]" && [ "$FORCE" -eq 0 ]; then
    echo -e "${RED}Refusing to overwrite existing site: ${SITE}${NC}"
    echo "Re-run with --force if you really mean to replace it."
    exit 1
fi

# Stage over SSH: delta transfer, live site untouched. Dot-prefixed so
# apply_from_mac.sh's www/*/ scan never imports a half-staged site.
echo -e "${YELLOW}Staging files over SSH (live site keeps serving)...${NC}"
ssh nas "rm -rf '${WWW_NAS}/.staging-${SITE}'"
rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    "$SOURCE_DIR/" "nas:${WWW_NAS}/.staging-${SITE}/"

# Generate the site's Caddy config into staging (root inside the container is /var/www/<site>)
ssh nas "cat > '${WWW_NAS}/.staging-${SITE}/${SUBDOMAIN}.caddy'" <<EOF
${SITE} {
    import default_site
    root * /var/www/${SITE}
}
EOF

# Switch: two renames on the NAS — effectively instant. The previous release
# stays as <site>.old with its .caddy removed (a duplicate .caddy would fail
# validation on the next apply). Rollback:
#   ssh nas "cd ${WWW_NAS} && mv ${SITE} ${SITE}.bad && mv ${SITE}.old ${SITE} \
#            && cp ${SITE}.bad/${SUBDOMAIN}.caddy ${SITE}/"
echo -e "${YELLOW}Switching to new version...${NC}"
ssh nas "cd '${WWW_NAS}' \
    && rm -rf '${SITE}.old' \
    && { [ ! -d '${SITE}' ] || { mv '${SITE}' '${SITE}.old' && rm -f '${SITE}.old/'*.caddy; }; } \
    && mv '.staging-${SITE}' '${SITE}'"

# Apply (regenerates imports, validates, reloads — Caddy reloads are graceful).
# This is the only step that needs the SMB mount; mount it idempotently.
echo -e "${YELLOW}Applying Caddy config...${NC}"
if [ ! -d "$ETC_MAC" ]; then
    if [ -x "$MOUNT_HELPER" ]; then
        "$MOUNT_HELPER"
    else
        echo -e "${RED}Error: Caddy volume not mounted and mount helper missing${NC}"
        open "smb://jongserve.local/Container"   # NOT nas.local — that name does not resolve
        echo "Please authenticate and retry."
        exit 1
    fi
fi
cd "$ETC_MAC" && ./apply_from_mac.sh

echo -e "${GREEN}Deployed to https://${SITE}${NC}"
