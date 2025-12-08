#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com
# Deploys to NAS Caddy via mounted volume

set -e

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
TARGET_DIR="/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com"
SOURCE_DIR="{{SOURCE_DIR}}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting deployment to ${SUBDOMAIN}.jurrejan.com...${NC}"

# Check if target directory is accessible
if [ ! -d "/Volumes/Container/caddy/www" ]; then
    echo -e "${RED}Error: Caddy volume not mounted at /Volumes/Container/caddy/www${NC}"
    echo -e "${RED}Please ensure the NAS volume is mounted before running this script.${NC}"
    exit 1
fi

# Create target directory if it doesn't exist
echo -e "${YELLOW}Creating target directory...${NC}"
mkdir -p "$TARGET_DIR"

# Copy static files
echo -e "${YELLOW}Copying files to $TARGET_DIR...${NC}"
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    --exclude='deploy.sh' \
    --exclude='*.caddy' \
    "$SOURCE_DIR/" "$TARGET_DIR/"

# Copy Caddyfile to target directory (must be named ${SUBDOMAIN}.jurrejan.com.caddy)
echo -e "${YELLOW}Copying Caddyfile...${NC}"
cp "${SUBDOMAIN}.jurrejan.com.caddy" "$TARGET_DIR/"

# Verify deployment
if [ -f "$TARGET_DIR/index.html" ]; then
    echo -e "${GREEN}✓ Files copied successfully!${NC}"
    echo -e "${GREEN}✓ Deployment completed to: $TARGET_DIR${NC}"

    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Run apply script: cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh"
    echo -e "  2. Access site at: https://${SUBDOMAIN}.jurrejan.com"

    echo -e "${YELLOW}Deployed files:${NC}"
    ls -la "$TARGET_DIR"
else
    echo -e "${RED}✗ Deployment failed - index.html not found in target directory${NC}"
    exit 1
fi
