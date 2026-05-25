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

### 3. Copy Files

For SvelteKit:
```bash
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    build/ "/Volumes/Container/caddy/apps/${SUBDOMAIN}.jurrejan.com/build/"
```

For plain Node:
```bash
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    server.js package.json "/Volumes/Container/caddy/apps/${SUBDOMAIN}.jurrejan.com/"
```

### 4. Copy Config Files

```bash
cp ecosystem.config.js app.caddy "/Volumes/Container/caddy/apps/${SUBDOMAIN}.jurrejan.com/"
```

### 5. Deploy via SSH

```bash
ssh nas "/share/CACHEDEV1_DATA/Container/caddy/apps/deploy-app.sh myapp.jurrejan.com"
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

```bash
#!/bin/bash
set -e

SUBDOMAIN="myapp"
TARGET_DIR="/Volumes/Container/caddy/apps/${SUBDOMAIN}.jurrejan.com"

# Check mount (or run scripts/mount-nas.sh for an idempotent mount)
if [ ! -d "/Volumes/Container/caddy/apps" ]; then
    open "smb://jongserve.local/Container"   # NOT nas.local — that name does not resolve
    echo "Mount volume and retry"
    exit 1
fi

# Build
bun run build

# Deploy files
mkdir -p "$TARGET_DIR"
rsync -av --delete --exclude='.DS_Store' build/ "$TARGET_DIR/build/"
cp ecosystem.config.js app.caddy "$TARGET_DIR/"

# Start/restart on NAS
ssh nas "/share/CACHEDEV1_DATA/Container/caddy/apps/deploy-app.sh ${SUBDOMAIN}.jurrejan.com"

echo "Deployed to https://${SUBDOMAIN}.jurrejan.com"
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
