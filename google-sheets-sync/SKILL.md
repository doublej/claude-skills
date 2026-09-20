---
name: google-sheets-sync
description: "Bidirectional JSON-to-Google Sheets sync for client-editable CMS workflows"
---

# Google Sheets Content Sync

Bidirectional sync between local JSON files and Google Sheets. Clients edit in Sheets, devs pull changes. Technical fields stay hidden via blacklist.

## When to Use

- Client needs to edit copy/content without touching code
- Multiple JSON files with mixed structures (flat key-value, nested arrays)
- Need to hide technical fields (IDs, paths, config) from editors

## Setup

### 1. Google Cloud Console

1. Create project at console.cloud.google.com
2. Enable Google Sheets API
3. Create Service Account (IAM & Admin → Service Accounts)
4. Generate JSON key → save as `google-credentials.json` (gitignored)
5. Share target spreadsheet with service account email (Editor access)

### 2. Environment

```bash
# .env.local
GOOGLE_SHEETS_ID=<spreadsheet-id-from-url>
GOOGLE_CREDENTIALS_PATH=./google-credentials.json
```

### 3. Install

```bash
bun add googleapis commander
```

### 4. Scaffold

Copy templates from `assets/` to `tools/sync-content/`:

```
tools/sync-content/
├── index.ts              # CLI entry
├── config.ts             # File mappings
├── blacklist.config.ts   # Fields to hide
└── lib/
    ├── sheets.ts         # Google API wrapper
    ├── parser.ts         # Sheet ↔ JSON conversion
    ├── merger.ts         # Diff + merge with blacklist
    ├── path-matcher.ts   # Blacklist pattern matching
    ├── types.ts          # Type definitions
    ├── validator.ts      # Content validation (customize)
    └── writer.ts         # JSON file I/O
```

### 5. Configure

**config.ts** - Map JSON files to sheet types:

```typescript
export const config = {
  spreadsheetId: process.env.GOOGLE_SHEETS_ID || '',
  credentialsPath: process.env.GOOGLE_CREDENTIALS_PATH || './google-credentials.json',
  dataDir: 'public/data',  // or 'src/data', etc.

  files: {
    'settings': { type: 'keyvalue' },                              // flat key-value
    'products': { type: 'array', arrayPath: 'data.items' },        // nested array
  } satisfies Record<string, FileConfig>,
} as const;
```

**blacklist.config.ts** - Hide technical fields:

```typescript
export const blacklistConfig: Record<string, string[]> = {
  '*': ['**.id', 'metaData'],           // apply to all files
  'products': ['data.items[*].sku'],    // file-specific
};
```

Patterns:
- `**` matches any nested path
- `[*]` matches any array index

### 6. Add Scripts

```json
// package.json
{
  "scripts": {
    "sync-content": "bun tools/sync-content/index.ts"
  }
}
```

## Usage

| Command | Description |
|---------|-------------|
| `bun run sync-content pull` | Pull from Sheets → update local JSON |
| `bun run sync-content pull --dry-run` | Preview changes without writing |
| `bun run sync-content pull -f settings` | Pull single file |
| `bun run sync-content push` | Push local JSON → Sheets (creates sheets if missing) |
| `bun run sync-content diff` | Show differences |
| `bun run sync-content blacklist` | Show hidden fields |

## File Types

### Key-Value (`type: 'keyvalue'`)

Sheet format:
| Key Path | Value |
|----------|-------|
| site.title | My Site |
| site.description | Welcome |
| contact.email | hi@example.com |

JSON result:
```json
{
  "site": { "title": "My Site", "description": "Welcome" },
  "contact": { "email": "hi@example.com" }
}
```

### Array (`type: 'array'`)

Sheet format (headers = field paths):
| name | price | category.name |
|------|-------|---------------|
| Widget | 9.99 | Tools |
| Gadget | 19.99 | Electronics |

JSON result (at `arrayPath`):
```json
[
  { "name": "Widget", "price": 9.99, "category": { "name": "Tools" } },
  { "name": "Gadget", "price": 19.99, "category": { "name": "Electronics" } }
]
```

## Workflow

1. **Initial setup**: `push` creates sheets with current JSON structure
2. **Client edits**: Make changes in Google Sheets
3. **Developer syncs**: `pull --dry-run` to preview, then `pull` to apply
4. **Commit**: Review diff, commit JSON changes

Blacklisted fields are preserved during pull — they won't be overwritten by empty sheet cells.

## Customization

### Validation (`lib/validator.ts`)

Add project-specific validation rules:

```typescript
// Example: validate image paths start with /images/
if (key === 'image' && !value.startsWith('/images/')) {
  errors.push({ path, value, reason: 'must start with /images/' });
}
```

### Value Parsing (`lib/parser.ts`)

Default parsing: `true`/`false` → boolean, numbers → number, rest → string.

Extend `parseValue()` for custom types (dates, JSON arrays in cells, etc.).
