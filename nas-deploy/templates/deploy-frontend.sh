#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (static frontend)
# Deploys to NAS Caddy via mounted volume

set -e

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
TARGET_DIR="/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com"
SOURCE_DIR="{{SOURCE_DIR}}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Deploying ${SUBDOMAIN}.jurrejan.com...${NC}"

# Check mount
if [ ! -d "/Volumes/Container/caddy/www" ]; then
    echo -e "${RED}Error: Caddy volume not mounted${NC}"
    open smb://nas.local/Container
    echo "Please authenticate and retry."
    exit 1
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy files
echo -e "${YELLOW}Copying files...${NC}"
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    "$SOURCE_DIR/" "$TARGET_DIR/"

# Copy Caddy config
cp "${SUBDOMAIN}.caddy" "$TARGET_DIR/"

# Apply
echo -e "${YELLOW}Applying Caddy config...${NC}"
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh

echo -e "${GREEN}Deployed to https://${SUBDOMAIN}.jurrejan.com${NC}"
