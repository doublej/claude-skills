# Payload CMS MCP Server Setup

Connect Claude/AI assistants to a live Payload CMS instance via MCP.

## Option 1: ohnicholas93/payload-mcp-server (Python, REST bridge)

Best for: live instance CRUD, content management workflows.

### Install
```bash
git clone https://github.com/ohnicholas93/payload-mcp-server.git
cd payload-mcp-server
pip install -r requirements.txt
```

### Configure (claude_desktop_config.json or .claude/settings.json)
```json
{
  "mcpServers": {
    "payload-cms": {
      "command": "python",
      "args": ["path/to/payload-mcp-server/server.py"],
      "env": {
        "PAYLOAD_URL": "http://localhost:3000",
        "PAYLOAD_EMAIL": "admin@example.com",
        "PAYLOAD_PASSWORD": "your-password"
      }
    }
  }
}
```

### Available Tools
- `create_object` - Create documents in any collection
- `search_objects` - Query with where filters, pagination, sorting
- `update_object` - Update document by ID
- `get_global` / `update_global` - Read/write globals

### Available Resources
- `payload://server/info` - Server metadata
- `payload://collections/{collection}` - List/query collection
- `payload://collections/{collection}/{id}` - Single document
- `payload://globals/{slug}` - Global document

## Option 2: Govcraft/payload-mcp (TypeScript, type-aware code gen)

Best for: generating correct Payload 3.0 code from current type definitions.

### Install
```bash
git clone https://github.com/Govcraft/payload-mcp.git
cd payload-mcp
pnpm install
pnpm generate-tools  # parses Payload's .d.ts files
pnpm dev
```

### Available Tools (auto-generated)
- `createCollection` - Generate collection config
- `createGlobal` - Generate global config
- `createField` - Generate field config
- `createAuth` - Generate auth config
- `createConfig` - Generate main Payload config

## Option 3: Custom MCP server (recommended for production)

Build a lightweight MCP server wrapping Payload's REST API for your specific needs.

### Minimal implementation pattern
```ts
// payload-mcp/index.ts
import { McpServer } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'

const PAYLOAD_URL = process.env.PAYLOAD_URL || 'http://localhost:3000'
let token: string | null = null

async function auth() {
  const res = await fetch(`${PAYLOAD_URL}/api/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: process.env.PAYLOAD_EMAIL,
      password: process.env.PAYLOAD_PASSWORD,
    }),
  })
  const data = await res.json()
  token = data.token
}

async function payloadFetch(path: string, options: RequestInit = {}) {
  if (!token) await auth()
  return fetch(`${PAYLOAD_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `JWT ${token}`,
      ...options.headers,
    },
  })
}

const server = new McpServer({ name: 'payload-cms', version: '1.0.0' })

server.tool('find', { collection: z.string(), limit: z.number().optional() },
  async ({ collection, limit }) => {
    const res = await payloadFetch(`/api/${collection}?limit=${limit || 10}`)
    const data = await res.json()
    return { content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] }
  }
)

server.tool('create', { collection: z.string(), data: z.record(z.any()) },
  async ({ collection, data }) => {
    const res = await payloadFetch(`/api/${collection}`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    const result = await res.json()
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] }
  }
)

// Add more tools as needed...

const transport = new StdioServerTransport()
await server.connect(transport)
```

### MCP config for custom server
```json
{
  "mcpServers": {
    "payload-cms": {
      "command": "node",
      "args": ["--import=tsx/esm", "payload-mcp/index.ts"],
      "env": {
        "PAYLOAD_URL": "http://localhost:3000",
        "PAYLOAD_EMAIL": "admin@example.com",
        "PAYLOAD_PASSWORD": "your-password"
      }
    }
  }
}
```
