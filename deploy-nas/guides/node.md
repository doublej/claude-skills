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

### 2. Stage Files (over SSH — no mount needed)

Never rsync `--delete` into the live `build/` — the running app would serve a
half-copied tree for the whole transfer. Stage beside it over SSH (delta
rsync — much faster than the SMB mount, which disables delta transfer):

```bash
SUBDOMAIN="myapp"
SITE="${SUBDOMAIN}.jurrejan.com"
APPS_NAS="/share/CACHEDEV1_DATA/Container/caddy/apps"
ssh nas "mkdir -p '${APPS_NAS}/${SITE}' && rm -rf '${APPS_NAS}/${SITE}/build.staging'"

# SvelteKit
rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    build/ "nas:${APPS_NAS}/${SITE}/build.staging/"

# Plain Node
rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    server.js package.json "nas:${APPS_NAS}/${SITE}/build.staging/"
```

### 3. Copy Config Files

Tiny files — safe to copy in place:

```bash
rsync -a ecosystem.config.js app.caddy "nas:${APPS_NAS}/${SITE}/"
```

### 4. Switch and Restart via SSH

Swap the build with renames (the running process keeps its open files from
the old dir), then restart. Downtime is just the PM2 restart (~1s), not the
rsync. `build.old` stays until the health check passes.

```bash
ssh nas "cd '${APPS_NAS}/${SITE}' \
    && rm -rf build.old \
    && { [ ! -d build ] || mv build build.old; } \
    && mv build.staging build \
    && '${APPS_NAS}/deploy-app.sh' '${SITE}'"
```

### 5. Health Check (auto-rollback)

Probe the app's port (from `ecosystem.config.js`) for up to 10s; on failure,
roll back to `build.old` and restart. Drop curl's `-f` if your app's `/`
route legitimately returns 4xx/5xx.

```bash
PORT=3102
if ssh nas "for i in 1 2 3 4 5 6 7 8 9 10; do \
        curl -fsS -o /dev/null --max-time 3 'http://172.29.20.1:${PORT}' && exit 0; \
        sleep 1; done; exit 1"; then
    ssh nas "rm -rf '${APPS_NAS}/${SITE}/build.old'"
else
    ssh nas "cd '${APPS_NAS}/${SITE}' \
        && rm -rf build.failed && mv build build.failed && mv build.old build \
        && '${APPS_NAS}/deploy-app.sh' '${SITE}'"
    echo "Rolled back; bad build kept at ${APPS_NAS}/${SITE}/build.failed"
    exit 1
fi
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

Prefer rendering `templates/deploy-node.sh` — it implements this whole flow
(stage over SSH → switch → restart → health check → auto-rollback) with no
SMB mount needed. By hand, run steps 2–5 above in order after `bun run build`.

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
