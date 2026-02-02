---
name: nas-deploy
description: Deploy static sites and Node.js apps to NAS Caddy via mounted volume at /Volumes/Container/caddy
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# NAS Deploy Skill

Deploy applications to a QNAP NAS running Caddy.

## When to Use

- Deploying static frontend sites to NAS
- Deploying Node.js/SvelteKit apps to NAS
- Configuring Caddy for new sites

## Deployment Types

| Type | Location | Caddy Role | Guide |
|------|----------|------------|-------|
| **Frontend (Static)** | `/Volumes/Container/caddy/www` | File server | [Frontend Guide](guides/frontend.md) |
| **Node.js Apps** | `/Volumes/Container/caddy/apps` | Reverse proxy | [Node Guide](guides/node.md) |

## Pre-flight: Check SMB Connection

Before deploying, verify the NAS volume is mounted:

```bash
if [ ! -d "/Volumes/Container/caddy" ]; then
    open smb://nas.local/Container
    echo "SMB share not mounted. Opening connection dialog..."
    echo "Please authenticate and retry deployment."
    exit 1
fi
```

## Quick Reference

### Static Frontend
```bash
# Build and copy to www directory
rsync -av --delete dist/ /Volumes/Container/caddy/www/myapp.jurrejan.com/

# Apply Caddy config
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

### Node.js App
```bash
# Copy app to apps directory
rsync -av --delete build/ /Volumes/Container/caddy/apps/myapp.jurrejan.com/build/

# Deploy via SSH (starts/restarts PM2)
ssh nas "/share/CACHEDEV1_DATA/Container/caddy/apps/deploy-app.sh myapp.jurrejan.com"
```

## Directory Structure

```
/Volumes/Container/caddy/
├── etc/
│   ├── Caddyfile              # Main Caddyfile (imports from www/*/*.caddy and apps/*/*.caddy)
│   └── apply_from_mac.sh      # Regenerates imports & reloads Caddy via SSH
├── www/                       # Static sites
│   └── ${SUBDOMAIN}.jurrejan.com/
│       ├── index.html
│       └── ${SUBDOMAIN}.caddy
└── apps/                      # Node.js apps
    └── ${SUBDOMAIN}.jurrejan.com/
        ├── build/             # SvelteKit build output (or server.js for plain Node)
        ├── ecosystem.config.js # PM2 configuration
        └── app.caddy          # Caddy reverse proxy config
```

## Domain & Naming

| Item | Format | Example |
|------|--------|---------|
| Site/app directory | `${SUBDOMAIN}.jurrejan.com` | `myapp.jurrejan.com` |
| Domain | `${SUBDOMAIN}.jurrejan.com` | `https://myapp.jurrejan.com` |

## Guides

- **[Frontend Guide](guides/frontend.md)** - Static sites (HTML, Vite, etc.)
- **[Node Guide](guides/node.md)** - Node.js apps with PM2

## Templates

- `templates/frontend-caddy.caddy` - Caddy config for static sites
- `templates/node-caddy.caddy` - Caddy reverse proxy config for Node apps
- `templates/ecosystem.config.js` - PM2 config template
- `templates/deploy-frontend.sh` - Frontend deployment script
