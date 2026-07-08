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
SITE="/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com"
# Guard: www/ holds live sites — do not overwrite one by accident
[ -d "$SITE" ] && { echo "$SUBDOMAIN already exists; pick another name"; exit 1; }
mkdir -p "$SITE"
```

### 3. Stage Built Files

Never rsync into the live directory — the site serves a half-copied tree for
the whole (slow, SMB) transfer. Stage beside it, dot-prefixed so
`apply_from_mac.sh`'s `www/*/` scan can't import the half-staged site:

```bash
WWW_NAS="/share/CACHEDEV1_DATA/Container/caddy/www"
ssh nas "rm -rf '${WWW_NAS}/.staging-${SUBDOMAIN}.jurrejan.com'"
rsync -av \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    dist/ "/Volumes/Container/caddy/www/.staging-${SUBDOMAIN}.jurrejan.com/"
```

### 4. Create Caddy Config

Create `${SUBDOMAIN}.caddy` **inside the staging directory**:

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

### 5. Switch (near-atomic)

Two renames on the NAS — the site is only "in between" for the rename instant.
Delete the `.old` tree right after: its duplicate `.caddy` would fail
validation on the next apply if it lingered.

```bash
SITE="${SUBDOMAIN}.jurrejan.com"
ssh nas "cd '${WWW_NAS}' \
    && rm -rf '${SITE}.old' \
    && { [ ! -d '${SITE}' ] || mv '${SITE}' '${SITE}.old'; } \
    && mv '.staging-${SITE}' '${SITE}' \
    && rm -rf '${SITE}.old'"
```

### 6. Apply Changes

```bash
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

Caddy reloads are graceful (no dropped connections). For a redeploy of an
existing site the config is unchanged, so this step is a no-op safety check.

This script:
- Scans `www/*/` for `*.caddy` files
- Regenerates `etc/Caddyfile.imports` (`import /var/www/<site>/*.caddy` per site)
- Validates the full config in the container, then triggers Caddy reload via SSH
  (a malformed `.caddy` in any site aborts the reload for all)

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

Prefer rendering `templates/deploy-frontend.sh` — it implements this
stage-then-switch flow. By hand:

```bash
#!/bin/bash
set -euo pipefail

SUBDOMAIN="myapp"
SITE="${SUBDOMAIN}.jurrejan.com"
WWW_MAC="/Volumes/Container/caddy/www"
WWW_NAS="/share/CACHEDEV1_DATA/Container/caddy/www"

# Check mount (or run scripts/mount-nas.sh for an idempotent mount)
if [ ! -d "$WWW_MAC" ]; then
    open "smb://jongserve.local/Container"   # NOT nas.local — that name does not resolve
    echo "Mount volume and retry"
    exit 1
fi

# Build
bun run build

# Stage (live site keeps serving the old version)
ssh nas "rm -rf '${WWW_NAS}/.staging-${SITE}'"
rsync -av --exclude='.DS_Store' dist/ "${WWW_MAC}/.staging-${SITE}/"
cp "${SUBDOMAIN}.caddy" "${WWW_MAC}/.staging-${SITE}/"

# Switch (two renames — effectively instant)
ssh nas "cd '${WWW_NAS}' \
    && rm -rf '${SITE}.old' \
    && { [ ! -d '${SITE}' ] || mv '${SITE}' '${SITE}.old'; } \
    && mv '.staging-${SITE}' '${SITE}' \
    && rm -rf '${SITE}.old'"

# Apply
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh

echo "Deployed to https://${SITE}"
```
