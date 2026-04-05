# Wrangler Config Reference

## Bindings

Add bindings to wrangler.toml or wrangler.jsonc to connect Cloudflare services.

### D1 (SQL database)

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "<uuid>"
migrations_dir = "migrations"
```

### KV (key-value store)

```toml
[[kv_namespaces]]
binding = "CACHE"
id = "<namespace-id>"
```

### R2 (object storage)

```toml
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"
```

### Durable Objects

```toml
[durable_objects]
bindings = [
  { name = "SESSION", class_name = "SessionDO" }
]

[[migrations]]
tag = "v1"
new_sqlite_classes = ["SessionDO"]
```

### Static Assets (Worker with dashboard)

```toml
[assets]
directory = "build"
binding = "ASSETS"
html_handling = "drop-trailing-slash"
not_found_handling = "single-page-application"
```

### AI

```toml
[ai]
binding = "AI"
```

### Queues

```toml
[[queues.producers]]
binding = "QUEUE"
queue = "my-queue"
```

### Hyperdrive (Postgres)

```toml
[[hyperdrive]]
binding = "HYPERDRIVE"
id = "<config-id>"
```

## Environment Variables

### Plain vars (non-secret)

```toml
[vars]
ENVIRONMENT = "production"
API_VERSION = "v2"
```

### Secrets (set via CLI, never in config)

```bash
wrangler secret put API_KEY
wrangler secret put DATABASE_URL
wrangler secret list
```

## Environment Overrides

Use `[env.production]` and `[env.preview]` for Pages, or named environments for Workers.

### Pages environments

```toml
name = "my-app"
pages_build_output_dir = "dist"
compatibility_date = "2025-01-01"

[env.production]
vars = { API_URL = "https://api.example.com" }

[env.preview]
vars = { API_URL = "https://staging-api.example.com" }
```

### Worker environments

```toml
name = "my-worker"
main = "src/index.ts"

[env.staging]
vars = { ENVIRONMENT = "staging" }

[env.production]
vars = { ENVIRONMENT = "production" }
```

Non-inheritable keys (bindings) must be fully specified in each environment.

## Build Configuration

```toml
[build]
command = "bun run build"
```

## Dev Configuration

```toml
[dev]
port = 8787
```

## Placement

```toml
[placement]
mode = "smart"
```

## Cron Triggers (Workers only)

```toml
[triggers]
crons = [
  "*/5 * * * *",
  "0 12 * * 1-5"
]
```

## JSONC Format

Same structure but JSON with comments. Include schema for editor autocomplete:

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  // or remote:
  // "$schema": "https://raw.githubusercontent.com/cloudflare/workers-sdk/main/packages/wrangler/config-schema.json",
  "name": "my-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],

  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-db",
      "database_id": "<uuid>",
      "migrations_dir": "migrations"
    }
  ]
}
```

## Pages Limits

- Max 20,000 files per deployment
- Max 25 MiB per file
- Functions directory auto-deploys when present

## Setup Recipes (for Justfile)

```just
[group('setup')]
# Create D1 database and R2 bucket for the project
cf-setup name:
    wrangler d1 create {{name}}
    wrangler r2 bucket create {{name}}-assets
    @echo "Update wrangler config with the database_id from above"

[group('setup')]
# Set a secret in Cloudflare
cf-secret name:
    wrangler secret put {{name}}
```
