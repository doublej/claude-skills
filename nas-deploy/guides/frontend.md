# Frontend (Static) Deployment Guide

Deploy static frontend sites to NAS Caddy.

## Target

- **Volume**: `/Volumes/Container/caddy/www`
- **Caddy Role**: File server (serves files directly)
- **Domain**: `${SUBDOMAIN}.jurrejan.com`

## Directory Structure

```
/Volumes/Container/caddy/www/
└── ${SUBDOMAIN}.jurrejan.com/
    ├── index.html
    ├── assets/
    │   ├── app.js
    │   └── style.css
    └── ${SUBDOMAIN}.caddy  # Site Caddy config
```

## Workflow

### 1. Build Your Project

```bash
# Vite/SvelteKit static
bun run build

# Or any static site generator
```

### 2. Create Site Directory

```bash
SUBDOMAIN="myapp"
mkdir -p "/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com"
```

### 3. Copy Built Files

```bash
rsync -av --delete \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    dist/ "/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com/"
```

### 4. Create Caddy Config

Create `${SUBDOMAIN}.caddy` **inside the site directory**:

```caddy
myapp.jurrejan.com {
    import default_site
    root * /var/www/myapp.jurrejan.com
}
```

The `default_site` snippet (defined in `etc/snippets/common.caddy`) includes:
- Security headers (HSTS, XSS protection, etc.)
- 5MB request body limit
- file_server directive

### 5. Apply Changes

```bash
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

This script:
- Scans `www/*/` for `*.caddy` files
- Regenerates import statements in main Caddyfile
- Triggers Caddy reload via SSH

## SPA Routing

For single-page apps with client-side routing, add `try_files` fallback:

```caddy
myapp.jurrejan.com {
    import default_site
    root * /var/www/myapp.jurrejan.com
    try_files {path} /index.html
}
```

## Complete Example

```bash
#!/bin/bash
set -e

SUBDOMAIN="myapp"
TARGET_DIR="/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com"

# Check mount
if [ ! -d "/Volumes/Container/caddy/www" ]; then
    open smb://nas.local/Container
    echo "Mount volume and retry"
    exit 1
fi

# Build
bun run build

# Deploy
mkdir -p "$TARGET_DIR"
rsync -av --delete --exclude='.DS_Store' dist/ "$TARGET_DIR/"

# Copy Caddy config
cp "${SUBDOMAIN}.caddy" "$TARGET_DIR/"

# Apply
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh

echo "Deployed to https://${SUBDOMAIN}.jurrejan.com"
```
