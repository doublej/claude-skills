#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (static frontend)
# Deploys to NAS Caddy via mounted volume.
# Usage: ./deploy-frontend.sh [--force]   (--force overwrites an existing site)

set -euo pipefail

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
SOURCE_DIR="{{SOURCE_DIR}}"
TARGET_DIR="/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com"

FORCE=0
if [ "${1:-}" = "--force" ]; then FORCE=1; fi

# Colors
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${YELLOW}Deploying ${SUBDOMAIN}.jurrejan.com...${NC}"

# Check mount
if [ ! -d "/Volumes/Container/caddy/www" ]; then
    echo -e "${RED}Error: Caddy volume not mounted${NC}"
    open "smb://jongserve.local/Container"   # NOT nas.local — that name does not resolve
    echo "Please authenticate and retry."
    exit 1
fi

# Guard: never clobber an existing live site unless --force
if [ -d "$TARGET_DIR" ] && [ "$FORCE" -eq 0 ]; then
    echo -e "${RED}Refusing to overwrite existing site: ${SUBDOMAIN}.jurrejan.com${NC}"
    echo "Re-run with --force if you really mean to replace it."
    exit 1
fi

# Copy files
echo -e "${YELLOW}Copying files...${NC}"
mkdir -p "$TARGET_DIR"
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    "$SOURCE_DIR/" "$TARGET_DIR/"

# Generate the site's Caddy config (root inside the container is /var/www/<site>)
echo -e "${YELLOW}Writing Caddy config...${NC}"
cat > "${TARGET_DIR}/${SUBDOMAIN}.caddy" <<EOF
${SUBDOMAIN}.jurrejan.com {
    import default_site
    root * /var/www/${SUBDOMAIN}.jurrejan.com
}
EOF

# Apply (regenerates imports, validates, reloads)
echo -e "${YELLOW}Applying Caddy config...${NC}"
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh

echo -e "${GREEN}Deployed to https://${SUBDOMAIN}.jurrejan.com${NC}"
