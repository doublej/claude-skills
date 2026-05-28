# Directus Content MCP Server

`@directus/content-mcp` — the official Directus team's MCP server. Source: https://github.com/directus/mcp.

Use for **runtime data ops** from an LLM (read/write items, files, fields, flows). Use this skill for authoring patterns (SDK, schema builder, extensions).

## Install

### Claude Desktop / Claude Code / Cursor

```json
{
  "mcpServers": {
    "directus": {
      "command": "npx",
      "args": ["@directus/content-mcp@latest"],
      "env": {
        "DIRECTUS_URL": "https://your-directus-url.com",
        "DIRECTUS_TOKEN": "<static token>"
      }
    }
  }
}
```

Email/password alternative:

```json
"env": {
  "DIRECTUS_URL": "https://your-directus-url.com",
  "DIRECTUS_USER_EMAIL": "user@example.com",
  "DIRECTUS_USER_PASSWORD": "your-password"
}
```

### Claude Code CLI

```bash
claude mcp add directus \
  --env DIRECTUS_URL=https://your-directus-url.com \
  --env DIRECTUS_TOKEN=<static-token> \
  -- npx @directus/content-mcp@latest
```

### Get a static token

1. Login to Directus
2. User Directory → your user → scroll to **Token** field
3. Generate → copy → **Save the user** (easy to forget — missing this causes "Invalid token")

## Tools exposed

### System / user

| Tool | Purpose |
|---|---|
| `system-prompt` | Provides context to the LLM about its role in this Directus instance |
| `users-me` | Get current user info (permissions, role, language) |

### Collections / schema (read-only)

| Tool | Purpose |
|---|---|
| `read-collections` | Schema of all collections — **call first** to discover structure |
| `read-fields` | Fields of a specific collection |
| `read-field` | Single field config |

### Items

| Tool | Purpose |
|---|---|
| `read-items` | Query items with filter/sort/fields/limit |
| `create-item` | Insert a new item |
| `update-item` | Modify an existing item |
| `delete-item` | Remove an item |

### Fields (schema writes — limited)

| Tool | Purpose |
|---|---|
| `create-field` | Add a field to an existing collection |
| `update-field` | Modify field config |

(No `delete-field` or `delete-collection` — intentional data-loss guardrail.)

### Files

| Tool | Purpose |
|---|---|
| `read-files` | List or get file metadata/content |
| `import-file` | Upload from a URL |
| `update-files` | Update file metadata |

### Flows

| Tool | Purpose |
|---|---|
| `read-flows` | List automation flows |
| `trigger-flow` | Execute a manual-trigger flow |

### Comments

| Tool | Purpose |
|---|---|
| `read-comments` | View comments on items |
| `upsert-comment` | Add or update a comment |

### Prompts (dynamic, optional)

| Tool | Purpose |
|---|---|
| `get-prompts` | List prompt templates from a Directus collection |
| `get-prompt` | Execute a stored prompt |

### Misc

| Tool | Purpose |
|---|---|
| `markdown-tool` | Convert between markdown and HTML (for WYSIWYG fields) |

## Env vars reference

| Var | Required | Purpose |
|---|---|---|
| `DIRECTUS_URL` | Yes | Instance URL |
| `DIRECTUS_TOKEN` | Either | Static access token |
| `DIRECTUS_USER_EMAIL` + `DIRECTUS_USER_PASSWORD` | Either | Login credentials |
| `DISABLE_TOOLS` | No | Comma-separated tool names to hide (e.g. `delete-item,update-field`) |
| `MCP_SYSTEM_PROMPT_ENABLED` | No | `false` to disable the default system prompt |
| `MCP_SYSTEM_PROMPT` | No | Override the default system prompt text |
| `DIRECTUS_PROMPTS_COLLECTION_ENABLED` | No | `true` to enable prompt templates from a collection |
| `DIRECTUS_PROMPTS_COLLECTION` | No | Collection name holding prompts (default: `prompts`) |
| `DIRECTUS_PROMPTS_NAME_FIELD` | No | Field for prompt name (default: `name`) |
| `DIRECTUS_PROMPTS_DESCRIPTION_FIELD` | No | Field for description (default: `description`) |
| `DIRECTUS_PROMPTS_SYSTEM_PROMPT_FIELD` | No | Field for system text (default: `system_prompt`) |
| `DIRECTUS_PROMPTS_MESSAGES_FIELD` | No | Field for messages array (default: `messages`) |

## Dynamic prompts (advanced)

The MCP can expose prompts stored as rows in a Directus collection. Each row = one prompt template with name, description, system prompt, and messages (mustache templating supported via `{{ variable }}`).

1. Create a `prompts` collection with fields: `name`, `description`, `system_prompt` (text), `messages` (json)
2. Set `DIRECTUS_PROMPTS_COLLECTION_ENABLED=true`
3. LLM clients that support MCP prompts (Claude Desktop does) will see them as slash-commands

## Safety model

The MCP intentionally **blocks destructive schema ops**:
- No `delete-collection` tool
- No `delete-field` tool
- `delete-item` exists but is scoped per-role

For additional safety in untrusted contexts, disable specific tools:

```json
"env": {
  "DIRECTUS_URL": "...",
  "DIRECTUS_TOKEN": "...",
  "DISABLE_TOOLS": "delete-item,update-field,create-field"
}
```

For dev environments, run from source (`node dist/index.js` pointing at a cloned repo) — future releases may ship a dev-oriented package with destructive tools unlocked.

## When to use the MCP vs this skill

| Task | Use |
|---|---|
| "Show me all drafts by X" | MCP `read-items` |
| "Add a new blog post" | MCP `create-item` |
| "Trigger the publish flow" | MCP `trigger-flow` |
| "Write a TypeScript migration script" | Skill (`schema-builder.md`) |
| "Build an interface extension" | Skill (`extensions.md`) |
| "Set up docker compose" | Skill (`self-hosting.md`) |
| "Debug a filter rule" | Skill (`filter-rules.md`) |

The MCP operates on a **live instance**; the skill helps you **write code** that runs against Directus later.
