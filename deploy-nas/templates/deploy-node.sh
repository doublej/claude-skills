#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (Node.js app)
# Zero-downtime: stages the new build beside the live one, swaps it in with
# NAS-side renames, then restarts PM2. The app keeps serving the old build
# during the whole rsync; downtime is just the PM2 restart (~1s).

set -euo pipefail

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
SOURCE_DIR="{{SOURCE_DIR}}"
SITE="${SUBDOMAIN}.jurrejan.com"
APPS_MAC="/Volumes/Container/caddy/apps"
APPS_NAS="/share/CACHEDEV1_DATA/Container/caddy/apps"
TARGET_DIR="${APPS_MAC}/${SITE}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Deploying ${SITE} (Node.js)...${NC}"

# Check mount
if [ ! -d "$APPS_MAC" ]; then
    echo -e "${RED}Error: Caddy volume not mounted${NC}"
    open "smb://jongserve.local/Container"
    echo "Please authenticate and retry."
    exit 1
fi

mkdir -p "$TARGET_DIR"

# Stage: copy the new build beside the live one (running app untouched)
echo -e "${YELLOW}Staging build (app keeps running)...${NC}"
ssh nas "rm -rf '${APPS_NAS}/${SITE}/build.staging'"   # SMB rm is unreliable; clean NAS-side
rsync -av \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    "$SOURCE_DIR/" "${TARGET_DIR}/build.staging/"

# Config files are tiny — safe to copy in place
cp ecosystem.config.js app.caddy "$TARGET_DIR/"

# Switch: rename swap on the NAS (the running process keeps its open files
# from the old dir until PM2 restarts it), then restart via deploy-app.sh
echo -e "${YELLOW}Switching build and restarting app...${NC}"
ssh nas "cd '${APPS_NAS}/${SITE}' \
    && rm -rf build.old \
    && { [ ! -d build ] || mv build build.old; } \
    && mv build.staging build \
    && '${APPS_NAS}/deploy-app.sh' '${SITE}' \
    && rm -rf build.old"

echo -e "${GREEN}Deployed to https://${SITE}${NC}"
