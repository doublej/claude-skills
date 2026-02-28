---
name: sheet-cms
description: Set up bidirectional Google Sheets ↔ JSON sync for content management. Use when adding sheet-cms to a project, configuring content files, or setting up Google Cloud credentials.
---

# sheet-cms

Sync content bidirectionally between Google Sheets and local JSON files. Use Google Sheets as a CMS for client-editable content.

## Setup workflow

### 1. Add dependency

```bash
bun add sheet-cms
```

### 2. Run setup wizard

```bash
bunx sheet-cms setup
```

Wizard handles:
- Google Cloud project + Sheets API enable
- Service account creation + JSON key download
- `.env` file with `GOOGLE_CREDENTIALS_PATH` and `SHEET_CMS_SPREADSHEET_ID`
- Shares sheet with service account email

### 3. Create config

Create `sheet-cms.config.ts` in project root:

```ts
import { defineConfig } from 'sheet-cms'

export default defineConfig({
  spreadsheetId: process.env.SHEET_CMS_SPREADSHEET_ID!,
  dataDir: 'src/lib/data/content',  // adjust to project
  files: {
    // keyvalue: flat key-path/value pairs → nested JSON
    global: { type: 'keyvalue' },

    // array: header row + data rows → JSON array at arrayPath
    products: { type: 'array', arrayPath: 'items' },

    // stringPaths: force these paths to stay strings (not auto-parse numbers)
    stats: { type: 'keyvalue', stringPaths: ['stats[*].value'] },
  },
  blacklist: {
    // protect paths from being overwritten on pull or exported on push
    '*': ['**.href', '**.src'],  // global: all hrefs and image sources
    products: ['[*].internalId'],
  },
  validation: [
    // checked on push
    { match: 'global:url.*', rule: { startsWith: 'https://' }, message: 'URLs must use https' },
  ],
})
```

### 4. Initial push (creates sheets from JSON)

```bash
bunx sheet-cms push
```

### 5. Share sheet with client

Share the Google Sheet (Editor access) with whoever should edit content.

## CLI commands

| Command | Purpose |
|---------|---------|
| `bunx sheet-cms setup` | Interactive setup wizard |
| `bunx sheet-cms pull` | Pull sheet → local JSON |
| `bunx sheet-cms pull --dry-run` | Preview changes |
| `bunx sheet-cms pull -f <name>` | Pull single file |
| `bunx sheet-cms push` | Push local JSON → sheet |
| `bunx sheet-cms push -f <name>` | Push single file |
| `bunx sheet-cms diff` | Show differences |
| `bunx sheet-cms blacklist` | Show protected paths |
| `bunx sheet-cms serve` | Start HTTP API (port 3000) |

All commands accept `-c/--config <path>` for custom config location.

## File types

### keyvalue

Sheet layout:
```
path.to.field    | Hello world
path.to.nested   | Some value
array[0].name    | First item
```

Produces: `{ "path": { "to": { "field": "Hello world", "nested": "Some value" } }, "array": [{ "name": "First item" }] }`

### array

Sheet layout:
```
name   | price | active
Widget | 9.99  | true
Gadget | 19.99 | false
```

Produces (at arrayPath): `[{ "name": "Widget", "price": "9.99", "active": "true" }, ...]`

## Config reference

| Field | Type | Description |
|-------|------|-------------|
| `spreadsheetId` | string | From Google Sheets URL (between /d/ and /edit) |
| `credentialsPath` | string | Service account JSON key (default: `./google-credentials.json`) |
| `dataDir` | string | JSON files directory (default: `public/data`) |
| `files` | Record | `{ "filename": { type, arrayPath?, stringPaths? } }` |
| `blacklist` | Record | `{ "filename": ["glob.pattern.**"] }` — use `*` for all files |
| `validation` | array | `{ match, rule, message }` — checked on push |

### Blacklist glob patterns

- `*` — single segment (`items[*].id`)
- `**` — any depth (`**.href`)
- Combine: `form.fields[*].type`

### Validation rules

- `startsWith: string`
- `pattern: RegExp`
- `oneOf: string[]`
- `custom: (value: string) => boolean`

## Environment variables

| Variable | Purpose |
|----------|---------|
| `GOOGLE_CREDENTIALS_PATH` | Path to service account JSON |
| `SHEET_CMS_SPREADSHEET_ID` | Google Spreadsheet ID |
| `PORT` | HTTP server port (default: 3000) |
| `HOST` | HTTP server host (default: 0.0.0.0) |

## Analyzing project for config

When setting up sheet-cms for an existing project:

1. Find content JSON files: `find src -name "*.json" | grep -E "(content|data)"`
2. For each file, determine type:
   - Flat key-value pairs → `keyvalue`
   - Array of objects → `array` with `arrayPath`
3. Identify paths to protect (blacklist):
   - Image paths (`**.src`, `**.image`)
   - URLs/hrefs (`**.href`, `**.url`)
   - Internal IDs (`**.id`, `**.slug`)
   - Form field configs
4. Identify paths that should stay strings even if numeric (`stringPaths`)

## HTTP API (serve mode)

```bash
bunx sheet-cms serve
```

Endpoints:
- `POST /pull` — body: `{ dryRun?: boolean, file?: string }`
- `POST /push` — body: `{ file?: string }`
- `POST /diff` — body: `{ file?: string }`
- `GET /files` — list configured files
- `GET /blacklist` — all patterns
- `GET /blacklist/:file` — patterns for file
- `GET /health` — health check

Swagger docs at `/swagger` when running.

## Library API

```ts
import { loadConfig, createSheetsClient, pull, push, diff } from 'sheet-cms'

const config = await loadConfig()
const sheets = createSheetsClient(config)

await pull(config, sheets, { dryRun: false })
await push(config, sheets, { file: 'content' })
const changes = await diff(config, sheets)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Sheet not found" | Run `push` first to create sheets from JSON |
| "Permission denied" | Share sheet with service account email (Editor) |
| "Credentials not found" | Check `GOOGLE_CREDENTIALS_PATH` env var |
| Values parsed as numbers | Add path to `stringPaths` config |
| Field overwritten on pull | Add to `blacklist` |
