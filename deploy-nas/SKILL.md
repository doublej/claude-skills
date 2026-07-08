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

File transfers go over SSH (`rsync ... nas:...` — delta transfer, much faster
than the SMB mount, which rewrites whole files). Node deploys need no mount at
all; frontend deploys need it only for the final `apply_from_mac.sh` step.

When the mount is needed, mount (or verify) it with the idempotent helper.
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

- **Never rsync into a live directory.** Stage to `.staging-<site>` (www) or
  `build.staging` (apps) and switch with NAS-side renames — see Quick Reference.
  `www/` already holds live sites (e.g. `demo`, `hello-world`); never deploy
  under a name that exists unless you mean to replace it — check
  `ssh nas 'ls /share/CACHEDEV1_DATA/Container/caddy/www/'` first.
  `deploy-frontend.sh` refuses to clobber an existing site unless run with `--force`.
- **Strip `*.caddy` from a kept `<site>.old`.** The previous release is kept
  for rollback, but a duplicate `.caddy` for the same domain fails validation
  on the next apply — the swap removes it (see guides/frontend.md). The staging
  dir is dot-prefixed precisely so the `www/*/` scan never sees it either.
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

**Zero-downtime rules: never rsync into a live directory, and transfer over
SSH, not the SMB mount.** Stage beside the live dir, then switch with NAS-side
renames at the end. Writing in place leaves the site/app serving a half-copied
tree for the whole transfer, and rsync onto the mount rewrites whole files
(delta transfer disabled). Both `deploy-*.sh` templates implement this; the
manual steps are in the guides.

### Static Frontend
```bash
# Stage over SSH + rename-switch + apply (refuses to clobber w/o --force)
./deploy-frontend.sh

# By hand: stage to a dot-dir (invisible to apply_from_mac.sh), then swap,
# keeping the previous release as .old with its .caddy stripped (rollback!)
rsync -a --delete dist/ nas:/share/CACHEDEV1_DATA/Container/caddy/www/.staging-myapp.jurrejan.com/
# ...write myapp.caddy into the staging dir, then (see guides/frontend.md):
ssh nas "cd /share/CACHEDEV1_DATA/Container/caddy/www \
  && rm -rf myapp.jurrejan.com.old \
  && { [ ! -d myapp.jurrejan.com ] || { mv myapp.jurrejan.com myapp.jurrejan.com.old \
       && rm -f myapp.jurrejan.com.old/*.caddy; }; } \
  && mv .staging-myapp.jurrejan.com myapp.jurrejan.com"

# Apply Caddy config (graceful reload; the only step needing the SMB mount)
cd /Volumes/Container/caddy/etc && ./apply_from_mac.sh
```

### Node.js App
```bash
# Full flow, no mount needed: stage over SSH, switch, restart, health-check
# with auto-rollback to build.old on failure (see guides/node.md)
./deploy-node.sh

# By hand: stage the new build beside the live one (app keeps running)
rsync -a --delete build/ nas:/share/CACHEDEV1_DATA/Container/caddy/apps/myapp.jurrejan.com/build.staging/

# Switch + restart via SSH — downtime = PM2 restart only
ssh nas "cd /share/CACHEDEV1_DATA/Container/caddy/apps/myapp.jurrejan.com \
  && rm -rf build.old \
  && { [ ! -d build ] || mv build build.old; } \
  && mv build.staging build \
  && /share/CACHEDEV1_DATA/Container/caddy/apps/deploy-app.sh myapp.jurrejan.com"
# ...then health-check the port and either rm build.old or roll back to it
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
- `templates/deploy-frontend.sh` - Frontend deploy: stage over SSH → rename-switch (keeps rollback `.old`) → apply (refuses to clobber w/o --force)
- `templates/deploy-node.sh` - Node.js deploy, mount-free: stage over SSH → rename-switch → PM2 restart → health check with auto-rollback to `build.old`

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
