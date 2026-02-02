---
name: obsidian
description: Manage Obsidian vaults via MCP - read, write, search, tag, and organize notes. Use when user asks to interact with Obsidian notes, create/update vault content, search knowledge base, or manage note metadata. Checks MCP availability and guides setup if missing.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Obsidian Vault Management

Interact with Obsidian vaults through the Obsidian MCP server (cyanheads/obsidian-mcp-server).

## Pre-flight: Check MCP Availability

**Always run this first** before any Obsidian operation:

```bash
bash ~/.claude/skills/obsidian/scripts/check-obsidian-mcp.sh
```

If status is `NOT_REACHABLE`, guide the user through setup:

1. Open Obsidian
2. Install "Local REST API" community plugin (Settings > Community plugins > Browse)
3. Enable plugin, copy the API key from its settings
4. Install the MCP server:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_API_KEY": "<api-key>",
        "OBSIDIAN_BASE_URL": "http://127.0.0.1:27123"
      }
    }
  }
}
```

5. Restart Claude Code to pick up the MCP config

If status is `REACHABLE` but `MCP_CONFIGURED: false`, warn the user that the REST API is running but the MCP bridge is not configured.

## MCP Tools Reference

Once the MCP server is available, these tools are exposed:

| Tool | Purpose | Key Args |
|------|---------|----------|
| `obsidian_list_notes` | List files in vault folder | `path`, `extension_filter` |
| `obsidian_read_note` | Read note content + metadata | `path`, `format` (markdown/json) |
| `obsidian_update_note` | Append/prepend/overwrite note | `path`, `content`, `mode` |
| `obsidian_search_replace` | Find and replace in a note | `path`, `search`, `replace` |
| `obsidian_global_search` | Search across entire vault | `query`, `path_filter`, `regex` |
| `obsidian_manage_frontmatter` | Get/set/delete YAML keys | `path`, `action`, `key`, `value` |
| `obsidian_manage_tags` | Add/remove/list tags | `path`, `action`, `tag` |
| `obsidian_delete_note` | Delete a note | `path` |

## Common Workflows

### Create a new note
```
obsidian_update_note(path="Inbox/my-note.md", content="# Title\n\nContent here", mode="overwrite", create_if_missing=true)
```

### Search vault
```
obsidian_global_search(query="project deadline", path_filter="Projects/")
```

### Add tags to a note
```
obsidian_manage_tags(path="Projects/launch.md", action="add", tag="priority/high")
```

### Update frontmatter
```
obsidian_manage_frontmatter(path="Projects/launch.md", action="set", key="status", value="in-progress")
```

## Alternative: Direct Filesystem Access

If MCP setup is not desired, Obsidian vaults are plain Markdown on disk. Locate the vault:

```bash
find ~/Documents -name ".obsidian" -type d -maxdepth 3 2>/dev/null | sed 's/\/.obsidian$//'
```

Then use standard file tools (Read, Write, Edit, Grep, Glob) to interact with `.md` files directly. This bypasses frontmatter-aware tooling and search indexing but works without any plugins.

## Tips

- Obsidian vaults are just folders of `.md` files with a `.obsidian/` config dir
- The REST API runs on `http://127.0.0.1:27123` by default (HTTPS on 27124)
- Vault cache refreshes every 10 minutes; force refresh by restarting the MCP server
- Use `format: "json"` with `obsidian_read_note` to get structured frontmatter separately
