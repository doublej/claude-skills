#!/bin/bash

# Deployment script for {{SUBDOMAIN}}.jurrejan.com (Node.js app)
# Zero-downtime, mount-free: stages the new build over SSH (delta rsync),
# swaps it in with NAS-side renames, restarts PM2, then health-checks the app.
# A failed health check rolls back to the previous build automatically.
# Downtime is just the PM2 restart (~1s), not the transfer.

set -euo pipefail

# Configuration
SUBDOMAIN="{{SUBDOMAIN}}"
SOURCE_DIR="{{SOURCE_DIR}}"
PORT="{{PORT}}"
SITE="${SUBDOMAIN}.jurrejan.com"
APPS_NAS="/share/CACHEDEV1_DATA/Container/caddy/apps"
APP_NAS="${APPS_NAS}/${SITE}"

# Colors
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${YELLOW}Deploying ${SITE} (Node.js)...${NC}"

# Stage over SSH: delta transfer, running app untouched
echo -e "${YELLOW}Staging build over SSH (app keeps running)...${NC}"
ssh nas "mkdir -p '${APP_NAS}' && rm -rf '${APP_NAS}/build.staging'"
rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    "$SOURCE_DIR/" "nas:${APP_NAS}/build.staging/"
rsync -a ecosystem.config.js app.caddy "nas:${APP_NAS}/"

# Switch: rename swap (the running process keeps its open files from the old
# dir), then restart via deploy-app.sh. build.old stays until health check passes.
echo -e "${YELLOW}Switching build and restarting app...${NC}"
ssh nas "cd '${APP_NAS}' \
    && rm -rf build.old \
    && { [ ! -d build ] || mv build build.old; } \
    && mv build.staging build \
    && '${APPS_NAS}/deploy-app.sh' '${SITE}'"

# Health check: up to 10s for the app to answer on its port (any 2xx/3xx).
# If your app's / route legitimately returns 4xx/5xx, drop the -f flag.
echo -e "${YELLOW}Health-checking http://172.29.20.1:${PORT} ...${NC}"
if ssh nas "for i in 1 2 3 4 5 6 7 8 9 10; do \
        curl -fsS -o /dev/null --max-time 3 'http://172.29.20.1:${PORT}' && exit 0; \
        sleep 1; done; exit 1"; then
    ssh nas "rm -rf '${APP_NAS}/build.old'"
    echo -e "${GREEN}Deployed to https://${SITE}${NC}"
else
    if ssh nas "[ -d '${APP_NAS}/build.old' ]"; then
        echo -e "${RED}Health check failed — rolling back to previous build${NC}"
        ssh nas "cd '${APP_NAS}' \
            && rm -rf build.failed && mv build build.failed && mv build.old build \
            && '${APPS_NAS}/deploy-app.sh' '${SITE}'"
        echo -e "${YELLOW}Rolled back. Bad build kept at ${APP_NAS}/build.failed${NC}"
        echo "Inspect logs: ssh nas \"PM2_HOME=/share/CACHEDEV1_DATA/pm2 /opt/bin/pm2 logs {{APP_NAME}} --lines 50\""
    else
        echo -e "${RED}Health check failed on first deploy (nothing to roll back to)${NC}"
        echo "Inspect logs: ssh nas \"PM2_HOME=/share/CACHEDEV1_DATA/pm2 /opt/bin/pm2 logs {{APP_NAME}} --lines 50\""
    fi
    exit 1
fi
