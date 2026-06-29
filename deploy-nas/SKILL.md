---
name: deploy-nas
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
| **LAN reverse proxy** | `etc/sites/<name>.caddy` (config only — nothing deployed to the NAS) | Reverse proxy to a host on the LAN (e.g. a Mac) | Quick Ref |

</deployment_types>

<preflight>

## Pre-flight: Check SMB Connection

Before deploying, mount (or verify) the NAS volume with the idempotent helper.
It skips if already mounted, picks a reachable address (`jongserve.local`, then
the IP), and confirms the right volume — aborting deploy if it can't:

```bash
"$(dirname "$0")/../scripts/mount-nas.sh" || exit 1
```

Credentials come from **onenv** (1Password), not the macOS Keychain. Store the
share password once (the script reads it on every mount):

```bash
onenv set nas SMB_PASSWORD     # the 'admin' share password
onenv set nas SMB_USER         # optional — defaults to 'admin'
```

The helper mounts via the macOS automounter (which creates `/Volumes/Container`
without sudo) using these creds, so no Finder/Keychain prompt is needed. Override
the namespace with `NAS_ONENV_NS=<ns>`. The NAS is `jongserve.local` — `nas.local`
does not resolve.

**No SMB mount? Use SSH.** The mount is a convenience, not a requirement. If
`mount-nas.sh` fails (e.g. `no SMB password in onenv`), every Caddy *config*
operation works over `ssh nas` instead — read with
`ssh nas 'cat /share/CACHEDEV1_DATA/Container/caddy/etc/sites/<name>.caddy'`,
write with `ssh nas 'cat > /share/CACHEDEV1_DATA/Container/caddy/etc/sites/<name>.caddy' <<'EOF' … EOF`,
then reload (see <caution>). Only the static-site *file* copies still need the
mount (or `rsync` over SSH).

</preflight>

<caution>

## Caution

- **`rsync --delete` overwrites.** `www/` already holds live sites (e.g. `demo`,
  `hello-world`). Never deploy under a name that exists unless you mean to replace
  it — check `ls /Volumes/Container/caddy/www/` first. `deploy-frontend.sh` refuses
  to clobber an existing site unless run with `--force`.
- **`apply_from_mac.sh` validates before reloading** (a malformed `.caddy` in any
  site aborts the reload, leaving the live config untouched). To check by hand:
  `ssh nas '/share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker exec caddy-porkbun caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile'`
- **Reloading Caddy over SSH needs `--address localhost:2019`** — without it the
  admin API returns `HTTP 403: client is not allowed to access from origin`:
  `ssh nas '/share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker exec caddy-porkbun caddy reload --config /etc/caddy/Caddyfile --address localhost:2019'`.
  (`apply_from_mac.sh` already passes this — you only need it for a manual reload.)
- **The SMB share has no Trash**, so macOS `rm`/Finder-delete fails on the mount.
  To remove a retired site, delete it NAS-side: `ssh nas 'rm -rf /share/CACHEDEV1_DATA/Container/caddy/www/<site>'`, then re-run `apply_from_mac.sh`.

</caution>

<quick_ref>

## Quick Reference

### Static Frontend
```bash
# Build and copy to www directory (refuses to clobber an existing site)
./deploy-frontend.sh

# ...or by hand — confirm the name is free first:
ls /Volumes/Container/caddy/www/ | grep myapp || \
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

### LAN reverse proxy
Proxy a subdomain to a host on the LAN (no files deployed to the NAS). Write the
site block into `etc/sites/<name>.caddy` (suffix-stripped, like app proxies):
```bash
# Over the SMB mount...
cat > /Volumes/Container/caddy/etc/sites/myapp.caddy <<'EOF'
myapp.jurrejan.com {
    import site_10mb
    reverse_proxy <lan-ip>:<port>
}
EOF

# ...or SSH-only (no mount needed):
ssh nas 'cat > /share/CACHEDEV1_DATA/Container/caddy/etc/sites/myapp.caddy' <<'EOF'
myapp.jurrejan.com {
    import site_10mb
    reverse_proxy <lan-ip>:<port>
}
EOF

# Apply (regenerates imports, validates, reloads — or reload via SSH, see Caution)
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

</quick_ref>

<directory_structure>

```
/Volumes/Container/caddy/
├── etc/
│   ├── Caddyfile              # Main Caddyfile: imports Caddyfile.imports + sites/*.caddy
│   ├── Caddyfile.imports      # Auto-generated: one `import /var/www/<site>/*.caddy` per static site
│   ├── sites/                 # App reverse-proxy configs (copied here from each app's app.caddy)
│   ├── snippets/common.caddy  # Shared snippets: default_site, security_headers, site_10mb, …
│   └── apply_from_mac.sh      # Regenerates Caddyfile.imports & reloads Caddy via SSH
├── www/                       # Static sites (mounted at /var/www inside the Caddy container)
│   └── ${SUBDOMAIN}.jurrejan.com/
│       ├── index.html
│       └── ${SUBDOMAIN}.caddy # site block; root points at /var/www/${SUBDOMAIN}.jurrejan.com
└── apps/                      # Node.js apps (run by PM2 on the NAS host, not in a container)
    └── ${SUBDOMAIN}.jurrejan.com/
        ├── build/             # SvelteKit build output (or server.js for plain Node)
        ├── ecosystem.config.js # PM2 configuration
        └── app.caddy          # Reverse proxy; deploy-app.sh copies it to etc/sites/<name>.caddy
```

Static sites are NOT imported from `www/*/*.caddy` directly — `apply_from_mac.sh`
scans `www/` and regenerates `etc/Caddyfile.imports`. App proxy configs are not
imported from `apps/` either — `deploy-app.sh` copies each `app.caddy` into
`etc/sites/<name>.caddy` (the `.jurrejan.com` suffix is stripped).

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

- `scripts/mount-nas.sh` - Idempotent SMB mount helper (run from the preflight)
- `templates/frontend-caddy.caddy` - Caddy config for static sites
- `templates/node-caddy.caddy` - Caddy reverse proxy config for Node apps
- `templates/ecosystem.config.js` - PM2 config template
- `templates/deploy-frontend.sh` - Frontend deployment script (renders config, refuses to clobber)
- `templates/deploy-node.sh` - Node.js deployment script

The `deploy-*.sh` and `*.caddy` templates carry `{{PLACEHOLDER}}` tokens
(`{{SUBDOMAIN}}`, `{{SOURCE_DIR}}`, `{{PORT}}`, `{{APP_NAME}}`). Render them
before running — copy the template into the project and substitute, e.g.:

```bash
sed -e 's/{{SUBDOMAIN}}/myapp/' -e 's#{{SOURCE_DIR}}#dist#' \
  templates/deploy-frontend.sh > deploy-frontend.sh && chmod +x deploy-frontend.sh
```

Prefer rendering and running the script over re-implementing its rsync +
Caddy-write steps inline.

</templates>
