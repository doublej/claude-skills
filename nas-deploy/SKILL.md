---
name: nas-deploy
description: "Deploy static sites and Node.js apps to NAS Caddy via mounted volume"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# NAS Deploy Skill

<description>
Deploy applications to a QNAP NAS running Caddy.
</description>

<when_to_use>

- Deploying static frontend sites to NAS
- Deploying Node.js/SvelteKit apps to NAS
- Configuring Caddy for new sites

</when_to_use>

<deployment_types>

| Type | Location | Caddy Role | Guide |
|------|----------|------------|-------|
| **Frontend (Static)** | `/Volumes/Container/caddy/www` | File server | [Frontend Guide](guides/frontend.md) |
| **Node.js Apps** | `/Volumes/Container/caddy/apps` | Reverse proxy | [Node Guide](guides/node.md) |

</deployment_types>

<preflight>

## Pre-flight: Check SMB Connection

Before deploying, mount (or verify) the NAS volume with the idempotent helper.
It skips if already mounted, picks a reachable address (`jongserve.local`, then
the IP), and confirms the right volume — aborting deploy if it can't:

```bash
"$(dirname "$0")/../scripts/mount-nas.sh" || exit 1
```

First run needs the password saved once: in Finder press Cmd-K and connect to
`smb://jongserve.local/Container` (not `nas.local` — that name does not resolve),
authenticate as `admin`, and tick "Remember this password in my keychain".

</preflight>

<quick_ref>

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

</quick_ref>

<directory_structure>

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

</directory_structure>

<naming>

## Domain & Naming

| Item | Format | Example |
|------|--------|---------|
| Site/app directory | `${SUBDOMAIN}.jurrejan.com` | `myapp.jurrejan.com` |
| Domain | `${SUBDOMAIN}.jurrejan.com` | `https://myapp.jurrejan.com` |

</naming>

<guides>

- **[Frontend Guide](guides/frontend.md)** - Static sites (HTML, Vite, etc.)
- **[Node Guide](guides/node.md)** - Node.js apps with PM2

</guides>

<templates>

- `templates/frontend-caddy.caddy` - Caddy config for static sites
- `templates/node-caddy.caddy` - Caddy reverse proxy config for Node apps
- `templates/ecosystem.config.js` - PM2 config template
- `templates/deploy-frontend.sh` - Frontend deployment script

</templates>
