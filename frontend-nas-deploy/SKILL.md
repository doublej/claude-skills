---
name: frontend-nas-deploy
description: Deploy static frontend sites to NAS Caddy via mounted volume at /Volumes/Container/caddy/www
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Frontend NAS Deploy Skill

Deploy static frontend sites to a NAS running Caddy via mounted volume.

## When to Use

- Deploying static frontend sites to NAS
- Configuring Caddy for new sites
- Setting up local development with NAS deployment

## Target

- **Volume**: `/Volumes/Container/caddy/www`
- **Server**: NAS running Caddy
- **Domain**: `${SUBDOMAIN}.jurrejan.com`

## Directory Structure

```
/Volumes/Container/caddy/
├── etc/
│   ├── Caddyfile              # Main Caddyfile (imports from www/*/*.caddy)
│   └── apply_from_mac.sh      # Regenerates imports & reloads Caddy via SSH
└── www/
    └── ${SUBDOMAIN}.jurrejan.com/
        ├── index.html
        ├── ...                 # Site files
        └── ${SUBDOMAIN}.jurrejan.com.caddy  # Site Caddy config (auto-imported)
```

## Workflow

### 1. Pre-flight: Check SMB Connection

Before deploying, verify the NAS volume is mounted:

```bash
if [ ! -d "/Volumes/Container/caddy/www" ]; then
    open smb://nas.local/Container
    echo "SMB share not mounted. Opening connection dialog..."
    echo "Please authenticate and retry deployment."
    exit 1
fi
```

### 2. Deploy Steps

1. Build frontend project
2. Create site directory: `/Volumes/Container/caddy/www/${SUBDOMAIN}.jurrejan.com/`
3. Copy built files to site directory
4. Copy Caddy config as `${SUBDOMAIN}.jurrejan.com.caddy` **inside the site directory**
5. Run apply script to reload Caddy

### 3. Apply Changes

The `apply_from_mac.sh` script:
- Scans `www/*/` for `*.caddy` files
- Regenerates import statements in main Caddyfile
- Triggers Caddy reload via SSH

```bash
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

## Naming Conventions

| Item | Format | Example |
|------|--------|---------|
| Site directory | `${SUBDOMAIN}.jurrejan.com` | `myapp.jurrejan.com` |
| Caddy config file | `${SUBDOMAIN}.jurrejan.com.caddy` | `myapp.jurrejan.com.caddy` |
| Caddy config location | Inside site directory | `www/myapp.jurrejan.com/myapp.jurrejan.com.caddy` |

## Files

- `caddy-template.caddy` - Caddy config template (uses `{{SUBDOMAIN}}` placeholder)
- `deploy-template.sh` - Deployment script template
