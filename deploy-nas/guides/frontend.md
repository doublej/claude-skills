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

Never rsync into the live directory — the site would serve a half-copied tree
for the whole transfer. Stage beside it over SSH (delta rsync — much faster
than the SMB mount, which disables delta transfer), dot-prefixed so
`apply_from_mac.sh`'s `www/*/` scan can't import the half-staged site:

```bash
WWW_NAS="/share/CACHEDEV1_DATA/Container/caddy/www"
SITE="${SUBDOMAIN}.jurrejan.com"
ssh nas "rm -rf '${WWW_NAS}/.staging-${SITE}'"
rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='._*' \
    --exclude='.git' \
    dist/ "nas:${WWW_NAS}/.staging-${SITE}/"
```

### 4. Create Caddy Config

Write `${SUBDOMAIN}.caddy` **into the staging directory** (over SSH):

```bash
ssh nas "cat > '${WWW_NAS}/.staging-${SITE}/${SUBDOMAIN}.caddy'" <<EOF
${SITE} {
    import default_site
    root * /var/www/${SITE}
}
EOF
```

The `default_site` snippet (defined in `etc/snippets/common.caddy`) includes:
- Security headers (HSTS, XSS protection, etc.)
- 5MB request body limit
- file_server directive

### 5. Switch (near-atomic)

Two renames on the NAS — the site is only "in between" for the rename instant.
The previous release is kept as `<site>.old` with its `.caddy` stripped (a
duplicate `.caddy` would fail validation on the next apply):

```bash
ssh nas "cd '${WWW_NAS}' \
    && rm -rf '${SITE}.old' \
    && { [ ! -d '${SITE}' ] || { mv '${SITE}' '${SITE}.old' && rm -f '${SITE}.old/'*.caddy; }; } \
    && mv '.staging-${SITE}' '${SITE}'"
```

Rollback (one rename, restoring the config from the bad release):

```bash
ssh nas "cd '${WWW_NAS}' \
    && mv '${SITE}' '${SITE}.bad' && mv '${SITE}.old' '${SITE}' \
    && cp '${SITE}.bad/${SUBDOMAIN}.caddy' '${SITE}/'"
```

### 6. Apply Changes

The only step that needs the SMB mount (run `scripts/mount-nas.sh` first if
`/Volumes/Container` is absent):

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
WWW_NAS="/share/CACHEDEV1_DATA/Container/caddy/www"

# Build
bun run build

# Stage over SSH (live site keeps serving the old version)
ssh nas "rm -rf '${WWW_NAS}/.staging-${SITE}'"
rsync -a --delete --exclude='.DS_Store' dist/ "nas:${WWW_NAS}/.staging-${SITE}/"
ssh nas "cat > '${WWW_NAS}/.staging-${SITE}/${SUBDOMAIN}.caddy'" < "${SUBDOMAIN}.caddy"

# Switch (two renames — effectively instant; previous release kept as .old)
ssh nas "cd '${WWW_NAS}' \
    && rm -rf '${SITE}.old' \
    && { [ ! -d '${SITE}' ] || { mv '${SITE}' '${SITE}.old' && rm -f '${SITE}.old/'*.caddy; }; } \
    && mv '.staging-${SITE}' '${SITE}'"

# Apply — the only step needing the SMB mount
[ -d /Volumes/Container/caddy/etc ] || "$HOME/.claude/skills/deploy-nas/scripts/mount-nas.sh"
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh

echo "Deployed to https://${SITE}"
```
