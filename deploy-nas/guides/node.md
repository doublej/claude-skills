# Node.js Deployment Guide

Deploy Node.js apps (including SvelteKit) to NAS with PM2 process management.

## Target

- **Volume**: `/Volumes/Container/caddy/apps`
- **NAS Path**: `/share/CACHEDEV1_DATA/Container/caddy/apps`
- **Caddy Role**: Reverse proxy to Node process
- **Process Manager**: PM2
- **Domain**: `${SUBDOMAIN}.jurrejan.com`

## Directory Structure

```
/Volumes/Container/caddy/apps/
└── ${SUBDOMAIN}.jurrejan.com/
    ├── build/                  # SvelteKit build output
    │   └── index.js
    ├── ecosystem.config.js     # PM2 configuration (required)
    └── app.caddy              # Caddy reverse proxy config
```

For plain Node.js (non-SvelteKit):
```
└── ${SUBDOMAIN}.jurrejan.com/
    ├── server.js              # Entry point
    ├── ecosystem.config.js
    └── app.caddy
```

## Port Allocation

Each app's port lives in its `ecosystem.config.js`. Don't trust a hardcoded
table — query PM2 on the NAS for what's actually in use, then pick the next free
port (existing apps cluster in the 31xx range):

```bash
ssh nas "PM2_HOME=/share/CACHEDEV1_DATA/pm2 /opt/bin/pm2 list"
```

## Required Files

### 1. ecosystem.config.js (PM2 Config)

```javascript
module.exports = {
  apps: [{
    name: 'myapp',
    script: 'build/index.js',  // or 'server.js' for plain Node
    interpreter: '/opt/bin/node',
    cwd: '/share/CACHEDEV1_DATA/Container/caddy/apps/myapp.jurrejan.com',
    env: {
      NODE_ENV: 'production',
      PORT: 3102  // Use next available port
    }
  }]
}
```

### 2. app.caddy (Reverse Proxy)

```caddy
myapp.jurrejan.com {
    import security_headers
    reverse_proxy 172.29.20.1:3102
}
```

The IP `172.29.20.1` is the Docker bridge network IP for the NAS host.

## Workflow

### 1. Build Your Project

```bash
# SvelteKit
bun run build

# Or plain Node - no build needed
```

### 2. Create App Directory

```bash
SUBDOMAIN="myapp"
mkdir -p "/Volumes/Container/caddy/apps/${SUBDOMAIN}.jurrejan.com"
```

### 3. Stage Files

Never rsync `--delete` into the live `build/` — the running app serves a
half-copied tree for the whole (slow, SMB) transfer. Stage beside it:

```bash
SITE="${SUBDOMAIN}.jurrejan.com"
APPS_NAS="/share/CACHEDEV1_DATA/Container/caddy/apps"
ssh nas "rm -rf '${APPS_NAS}/${SITE}/build.staging'"

# SvelteKit
rsync -av \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    build/ "/Volumes/Container/caddy/apps/${SITE}/build.staging/"

# Plain Node
rsync -av \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    server.js package.json "/Volumes/Container/caddy/apps/${SITE}/build.staging/"
```

### 4. Copy Config Files

Tiny files — safe to copy in place:

```bash
cp ecosystem.config.js app.caddy "/Volumes/Container/caddy/apps/${SITE}/"
```

### 5. Switch and Restart via SSH

Swap the build with renames (the running process keeps its open files from
the old dir), then restart. Downtime is just the PM2 restart (~1s), not the
rsync. `build.old` is kept until the restart succeeds, so a failed deploy
leaves a rollback: `ssh nas "cd ${APPS_NAS}/${SITE} && mv build.old build"`.

```bash
ssh nas "cd '${APPS_NAS}/${SITE}' \
    && rm -rf build.old \
    && { [ ! -d build ] || mv build build.old; } \
    && mv build.staging build \
    && '${APPS_NAS}/deploy-app.sh' '${SITE}' \
    && rm -rf build.old"
```

This script:
- Installs dependencies (if `package.json` exists and there's no prebuilt `build/`)
- Starts/restarts the app with PM2 (`PM2_HOME=/share/CACHEDEV1_DATA/pm2`)
- Copies `app.caddy` → `etc/sites/${SUBDOMAIN}.caddy` (the `.jurrejan.com` suffix is stripped)
- Validates the Caddy config, then reloads only if valid

Note: retiring or renaming an app leaves its `etc/sites/<name>.caddy` behind —
delete it by hand on the NAS, or the old proxy route lingers.

## PM2 Commands

```bash
# List all apps
ssh nas "/opt/bin/pm2 list"

# View logs
ssh nas "/opt/bin/pm2 logs myapp"

# Restart app
ssh nas "/opt/bin/pm2 restart myapp"

# Stop app
ssh nas "/opt/bin/pm2 stop myapp"

# Delete app from PM2
ssh nas "/opt/bin/pm2 delete myapp"
```

## Complete Example

Prefer rendering `templates/deploy-node.sh` — it implements this
stage-then-switch flow. By hand:

```bash
#!/bin/bash
set -euo pipefail

SUBDOMAIN="myapp"
SITE="${SUBDOMAIN}.jurrejan.com"
APPS_MAC="/Volumes/Container/caddy/apps"
APPS_NAS="/share/CACHEDEV1_DATA/Container/caddy/apps"
TARGET_DIR="${APPS_MAC}/${SITE}"

# Check mount (or run scripts/mount-nas.sh for an idempotent mount)
if [ ! -d "$APPS_MAC" ]; then
    open "smb://jongserve.local/Container"   # NOT nas.local — that name does not resolve
    echo "Mount volume and retry"
    exit 1
fi

# Build
bun run build

# Stage (app keeps running the old build)
mkdir -p "$TARGET_DIR"
ssh nas "rm -rf '${APPS_NAS}/${SITE}/build.staging'"
rsync -av --exclude='.DS_Store' build/ "$TARGET_DIR/build.staging/"
cp ecosystem.config.js app.caddy "$TARGET_DIR/"

# Switch + restart on NAS (downtime = PM2 restart only)
ssh nas "cd '${APPS_NAS}/${SITE}' \
    && rm -rf build.old \
    && { [ ! -d build ] || mv build build.old; } \
    && mv build.staging build \
    && '${APPS_NAS}/deploy-app.sh' '${SITE}' \
    && rm -rf build.old"

echo "Deployed to https://${SITE}"
```

## Troubleshooting

### App not starting
```bash
# Check PM2 logs
ssh nas "/opt/bin/pm2 logs myapp --lines 50"

# Check if port is in use
ssh nas "netstat -tlnp | grep 3102"
```

### Caddy not proxying
```bash
# Test local connection on NAS
ssh nas "curl -I http://172.29.20.1:3102"

# Reload Caddy
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

### Permission issues
```bash
# Files should be readable by the user running PM2
ssh nas "ls -la /share/CACHEDEV1_DATA/Container/caddy/apps/myapp.jurrejan.com/"
```
