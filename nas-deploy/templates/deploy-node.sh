#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (Node.js app)
# Deploys to NAS Caddy via mounted volume + PM2

set -e

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
TARGET_DIR="/Volumes/Container/caddy/apps/${SUBDOMAIN}.jurrejan.com"
SOURCE_DIR="{{SOURCE_DIR}}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Deploying ${SUBDOMAIN}.jurrejan.com (Node.js)...${NC}"

# Check mount
if [ ! -d "/Volumes/Container/caddy/apps" ]; then
    echo -e "${RED}Error: Caddy volume not mounted${NC}"
    open smb://nas.local/Container
    echo "Please authenticate and retry."
    exit 1
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy build files
echo -e "${YELLOW}Copying files...${NC}"
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    "$SOURCE_DIR/" "$TARGET_DIR/build/"

# Copy config files
cp ecosystem.config.js app.caddy "$TARGET_DIR/"

# Deploy on NAS
echo -e "${YELLOW}Starting app on NAS...${NC}"
ssh nas "/share/CACHEDEV1_DATA/Container/caddy/apps/deploy-app.sh ${SUBDOMAIN}.jurrejan.com"

echo -e "${GREEN}Deployed to https://${SUBDOMAIN}.jurrejan.com${NC}"
