---
name: cloudflare
description: "Pages/Workers with Wrangler: D1/KV/R2 bindings, wrangler.toml"
---

# Cloudflare

Set up, configure, and deploy Cloudflare Pages and Workers projects using the Wrangler CLI.

Always use `bunx` instead of `npx` for running wrangler commands.

Default Cloudflare account: `jurrejan@gmail.com` (Account ID: `e26bfba81a629fb8b4dcd538b1f73781`). Dashboard: https://dash.cloudflare.com/e26bfba81a629fb8b4dcd538b1f73781

<accounts>
Other available accounts:
- `Jrs@haist.one` — `ed64021ce50096c7eb065bb773a34be8`
- `Jurrejan@poolsuite.net` — `015478e13d7ca9d81172aafcf5f199b6`
</accounts>

<workflow>

1. Detect project type (SvelteKit, Astro, Next.js, static, Worker)
2. Create or update wrangler config
3. Add Justfile deploy recipes
4. Verify with `wrangler whoami` and `just --list`

## Project Types

### Pages (static / SvelteKit / Astro)
Serves static assets + optional server-side functions (SSR).

```bash
# Create project
bunx wrangler pages project create <project-name> --production-branch production

# Deploy
bunx wrangler pages deploy <output-dir> --project-name <project-name>

# Preview branch deploy
bunx wrangler pages deploy <output-dir> --project-name <project-name> --branch <branch>
```

### Workers (API / full app)
Runs on the edge with bindings (D1, KV, R2, DO, etc.).

```bash
# Deploy
wrangler deploy

# Dev
wrangler dev

# Dry-run (validate without deploying)
wrangler deploy --dry-run
```

## Wrangler Config

Prefer `wrangler.toml` for simple projects, `wrangler.jsonc` when comments or JSON tooling is needed.

### Pages (SvelteKit) — wrangler.toml

```toml
name = "<project-name>"
pages_build_output_dir = ".svelte-kit/cloudflare"
compatibility_date = "2025-01-01"
compatibility_flags = ["nodejs_compat"]
```

### Pages (Astro / Vite) — wrangler.toml

```toml
name = "<project-name>"
pages_build_output_dir = "dist"
compatibility_date = "2025-01-01"
compatibility_flags = ["nodejs_compat"]
```

### Worker — wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "<project-name>",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"]
}
```

See `references/wrangler-config.md` for bindings, environments, and advanced config.
</workflow>

<justfile_recipes>
## Justfile Deploy Recipes

Add to the project's Justfile. Detect which pattern applies:

### Pages deploy (SvelteKit / bun)

```just
# Build output directory for Cloudflare Pages
_cf_output := ".svelte-kit/cloudflare"
_cf_project := "<project-name>"

[group('deploy')]
# Deploy to Cloudflare Pages (production)
cf-deploy: build
    bunx wrangler pages deploy {{_cf_output}} --project-name {{_cf_project}} --branch production

[group('deploy')]
# Deploy preview branch to Cloudflare Pages
cf-deploy-preview branch="preview": build
    bunx wrangler pages deploy {{_cf_output}} --project-name {{_cf_project}} --branch {{branch}}
```

### Worker deploy

```just
[group('deploy')]
# Deploy Worker to Cloudflare
cf-deploy:
    wrangler deploy

[group('deploy')]
# Validate Worker build without deploying
cf-deploy-check:
    wrangler deploy --dry-run
```

### Combined (Worker + Pages client)

```just
[group('deploy')]
# Deploy Worker
cf-deploy-worker:
    cd worker && bunx wrangler deploy

[group('deploy')]
# Build and deploy client to Cloudflare Pages
cf-deploy-client: build
    bunx wrangler pages deploy <output-dir> --project-name <project-name> --branch production

[group('deploy')]
# Deploy everything
cf-deploy: cf-deploy-worker cf-deploy-client
```
</justfile_recipes>

<commands>

| Command | Purpose |
|---------|---------|
| `wrangler login` | Authenticate with Cloudflare |
| `wrangler whoami` | Check current account |
| `wrangler pages project create <name>` | Create Pages project |
| `wrangler pages project list` | List Pages projects |
| `wrangler pages deploy <dir>` | Deploy to Pages |
| `wrangler deploy` | Deploy Worker |
| `wrangler dev` | Local dev server |
| `wrangler secret put <NAME>` | Set encrypted secret |
| `wrangler d1 create <name>` | Create D1 database |
| `wrangler d1 migrations apply <db> --local` | Run D1 migrations locally |
| `wrangler d1 migrations apply <db> --remote` | Run D1 migrations in prod |
| `wrangler r2 bucket create <name>` | Create R2 bucket |
| `wrangler kv namespace create <name>` | Create KV namespace |
| `wrangler tail` | Stream live Worker logs |
</commands>

<framework_dirs>

| Framework | Output Directory |
|-----------|-----------------|
| SvelteKit | `.svelte-kit/cloudflare` |
| Astro | `dist` |
| Vite / React | `dist` |
| Next.js (on Pages) | `.vercel/output/static` |
| Hugo | `public` |
| Static (no build) | `.` or `public` |
</framework_dirs>

<setup_checklist>

When setting up a new project:

1. `wrangler login` (if not authenticated)
2. Create wrangler config matching project type
3. Test locally with `wrangler dev` or `wrangler pages dev <dir>`
4. Create Pages project: `wrangler pages project create <name>`
5. First deploy: `wrangler pages deploy <dir> --project-name <name>`
6. Add `cf-deploy` recipe to Justfile
7. Verify: `just cf-deploy`
</setup_checklist>

<mcp_servers>

Cloudflare provides remote MCP servers for deeper integration. Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "cloudflare-docs": {
      "command": "bunx",
      "args": ["mcp-remote", "https://docs.mcp.cloudflare.com/mcp"]
    },
    "cloudflare-bindings": {
      "command": "bunx",
      "args": ["mcp-remote", "https://bindings.mcp.cloudflare.com/mcp"]
    }
  }
}
```

Available servers: docs, bindings, builds, observability, radar, containers, browser-rendering, logpush, ai-gateway, autorag, audit-logs, dns-analytics, graphql.
</mcp_servers>
