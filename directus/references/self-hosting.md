# Self-Hosting

Docker Compose is the canonical way to run Directus (matches the user's `haist-cms/docker-compose.yml` setup).

## Minimal `docker-compose.yml`

```yaml
services:
  directus:
    image: directus/directus:latest
    ports:
      - '8055:8055'
    volumes:
      - ./database:/directus/database     # if using SQLite
      - ./uploads:/directus/uploads
      - ./extensions:/directus/extensions
      - ./snapshots:/directus/snapshots   # schema YAML + seed data
    environment:
      KEY: '<random-uuid-v4>'             # openssl rand -hex 32
      SECRET: '<random-uuid-v4>'          # openssl rand -hex 32
      ADMIN_EMAIL: 'admin@example.com'
      ADMIN_PASSWORD: '<strong-password>'
      PUBLIC_URL: 'http://localhost:8055'

      DB_CLIENT: 'pg'
      DB_HOST: 'database'
      DB_PORT: '5432'
      DB_DATABASE: 'directus'
      DB_USER: 'directus'
      DB_PASSWORD: 'directus'

      CACHE_ENABLED: 'true'
      CACHE_STORE: 'redis'
      REDIS: 'redis://cache:6379'

      WEBSOCKETS_ENABLED: 'true'
    depends_on:
      - database
      - cache

  database:
    image: postgis/postgis:15-master
    volumes:
      - ./pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: 'directus'
      POSTGRES_USER: 'directus'
      POSTGRES_PASSWORD: 'directus'

  cache:
    image: redis:7-alpine
```

Generate `KEY` and `SECRET`:

```bash
openssl rand -hex 32
```

## Required env vars

| Var | Purpose |
|---|---|
| `KEY` | Unique identifier for this instance; used for signing |
| `SECRET` | JWT signing secret |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Initial admin (first boot only) |
| `PUBLIC_URL` | Canonical URL; used in emails, password resets, assets |
| `DB_CLIENT` | `pg`, `mysql`, `sqlite3`, `mssql`, `oracledb` |
| `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USER`, `DB_PASSWORD` | Connection |

## Optional but useful

### Storage

```yaml
STORAGE_LOCATIONS: 'local,s3'

STORAGE_LOCAL_DRIVER: 'local'
STORAGE_LOCAL_ROOT: './uploads'

STORAGE_S3_DRIVER: 's3'
STORAGE_S3_BUCKET: 'my-bucket'
STORAGE_S3_REGION: 'eu-west-1'
STORAGE_S3_KEY: '<aws-key>'
STORAGE_S3_SECRET: '<aws-secret>'
STORAGE_S3_ENDPOINT: 'https://s3.eu-west-1.amazonaws.com'    # omit for AWS
STORAGE_S3_FORCE_PATH_STYLE: 'true'                          # for MinIO / R2
```

### Email

```yaml
EMAIL_TRANSPORT: 'smtp'
EMAIL_FROM: 'noreply@example.com'
EMAIL_SMTP_HOST: 'smtp.example.com'
EMAIL_SMTP_PORT: '587'
EMAIL_SMTP_USER: '<user>'
EMAIL_SMTP_PASSWORD: '<pass>'
EMAIL_SMTP_SECURE: 'false'
```

### Cache

```yaml
CACHE_ENABLED: 'true'
CACHE_AUTO_PURGE: 'true'              # bust on item changes
CACHE_STORE: 'redis'                  # or 'memory'
REDIS: 'redis://cache:6379'
CACHE_TTL: '5m'
```

### Rate limiting

```yaml
RATE_LIMITER_ENABLED: 'true'
RATE_LIMITER_POINTS: '50'             # requests per duration
RATE_LIMITER_DURATION: '1'            # seconds
RATE_LIMITER_STORE: 'redis'
```

### Websockets

```yaml
WEBSOCKETS_ENABLED: 'true'
WEBSOCKETS_REST_ENABLED: 'true'
WEBSOCKETS_GRAPHQL_ENABLED: 'true'
WEBSOCKETS_HEARTBEAT_ENABLED: 'true'
WEBSOCKETS_HEARTBEAT_FREQUENCY: '30'  # seconds
```

### Auth providers

```yaml
AUTH_PROVIDERS: 'google,github'

AUTH_GOOGLE_DRIVER: 'openid'
AUTH_GOOGLE_CLIENT_ID: '<id>'
AUTH_GOOGLE_CLIENT_SECRET: '<secret>'
AUTH_GOOGLE_ISSUER_URL: 'https://accounts.google.com'
AUTH_GOOGLE_IDENTIFIER_KEY: 'email'
AUTH_GOOGLE_ALLOW_PUBLIC_REGISTRATION: 'false'
```

### Extensions auto-reload (dev only)

```yaml
EXTENSIONS_AUTO_RELOAD: 'true'
```

## Common operations

### Start / stop

```bash
docker compose up -d
docker compose logs -f directus
docker compose down
```

### Run the Directus CLI inside the container

```bash
docker compose exec directus npx directus --help

# Schema snapshot / apply
docker compose exec directus npx directus schema snapshot --yes ./snapshots/schema.yaml
docker compose exec directus npx directus schema apply        ./snapshots/schema.yaml

# Create / reset admin user
docker compose exec directus npx directus users create --email new@example.com --password <pwd> --role <role-id>
docker compose exec directus npx directus users passwd --email admin@example.com --password <new>

# Bootstrap (idempotent first-boot; useful in CI)
docker compose exec directus npx directus bootstrap

# Count items in a collection
docker compose exec directus npx directus count <collection>
```

### Upgrade

1. Read the [changelog](https://github.com/directus/directus/releases) for breaking changes
2. Back up: `docker compose exec database pg_dump -U directus directus > backup.sql`
3. Bump image tag: `directus/directus:11.x.x` → `directus/directus:11.y.z`
4. `docker compose pull && docker compose up -d`
5. Directus auto-runs migrations on start — watch logs

### Backup

Postgres:
```bash
docker compose exec database pg_dump -U directus directus | gzip > backup-$(date +%F).sql.gz
```

Uploads:
```bash
tar -czf uploads-$(date +%F).tar.gz ./uploads
```

Restore:
```bash
gunzip -c backup.sql.gz | docker compose exec -T database psql -U directus directus
```

## Behind a reverse proxy (Caddy / Traefik / nginx)

Set `PUBLIC_URL` to the external URL with `https://`. Directus respects `X-Forwarded-Proto` when `IP_TRUST_PROXY=true`:

```yaml
IP_TRUST_PROXY: 'true'
```

Caddy example:

```caddyfile
cms.example.com {
  reverse_proxy directus:8055
}
```

Nginx: forward `Host`, `X-Forwarded-Proto`, `X-Forwarded-For`, and `Upgrade`/`Connection` headers (for websockets).

## Performance tuning

| Var | Default | When to change |
|---|---|---|
| `CACHE_ENABLED` | `false` | Always turn on in production |
| `CACHE_AUTO_PURGE` | `false` | Turn on so item writes bust cached reads |
| `DB_POOL_MIN` / `DB_POOL_MAX` | 0/10 | Raise `MAX` for high-concurrency sites |
| `PRESSURE_LIMITER_ENABLED` | `true` | Keep on; rejects requests when event loop lag spikes |
| `ASSETS_CACHE_TTL` | `30d` | Assets are immutable by id; long TTL is safe |
| `LOG_LEVEL` | `info` | `warn` in prod to reduce noise |

## Hardening

- Rotate `KEY` and `SECRET` → **invalidates all existing tokens**
- Disable public role signup: `AUTH_DISABLE_DEFAULT: 'false'` + no `ALLOW_PUBLIC_REGISTRATION`
- Set `ASSETS_TRANSFORM_MAX_CONCURRENT` and `ASSETS_TRANSFORM_MAX_OPERATIONS` to prevent DoS via transform URLs
- Use **named storage presets** (`?key=thumb`) instead of raw transform params; configure in Settings → Project Settings → Storage Assets
- Turn off the GraphQL introspection/playground in prod via `EXTENSIONS_CACHE_TTL` + reverse-proxy allow-list if exposed to the internet
- Run the container as non-root (the official image already does)

## Directus Cloud vs self-hosted

This skill assumes self-hosted. Directus Cloud uses the same SDK, same API, same extensions — the differences are: no env vars to manage, auto-scaling, and the "Cloud Exclusive" toolbar. Everything in `sdk-cookbook.md`, `filter-rules.md`, and `schema-builder.md` applies equally.
