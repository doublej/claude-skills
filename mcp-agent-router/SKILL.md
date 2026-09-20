---
name: mcp-agent-router
description: "Route MCP servers to dedicated agents to reduce token bloat in main context"
---

# MCP Agent Router

Offload MCP servers from primary session to dedicated agents. Each agent owns specific MCP servers and handles tasks on behalf of the main session.

## Why

Each MCP server adds 1k-10k+ tokens of tool descriptions to every turn. Loading gmail, notion, github, etc. directly wastes context when you only need them occasionally. Instead: create a project-level agent per MCP domain that the primary session delegates to via Task tool.

## Architecture

```
Primary Session (lean, no MCP bloat)
  ├── delegates "send email" → gmail-agent (has mcp__gmail tools)
  ├── delegates "update docs" → notion-agent (has mcp__notion tools)
  └── delegates "create PR"  → github-agent (has mcp__github tools)
```

**Key mechanism:** The `tools` field in agent frontmatter acts as an allowlist. When an agent specifies `tools: Read, Bash, mcp__gmail`, it signals which tools it needs. The `.mcp.json` provides the server config at project scope so agents can connect.

## Quick Start (mcpick-plus)

Use `mcpick-plus agent` to scaffold agent + MCP config in one command:

```bash
# List available MCP servers from catalog
bunx mcpick-plus init --list

# Create agent with specific servers (non-interactive)
bunx mcpick-plus agent --name "docs-helper" --servers "context7" --model haiku

# Create agent with multiple servers + custom description
bunx mcpick-plus agent --name "comms" --servers "notion,consult-user-mcp" --model sonnet --description "Handle Notion docs and user queries"

# Interactive wizard
bunx mcpick-plus agent

# List existing agents in project
bunx mcpick-plus agent --list
```

This generates:
- `.claude/agents/<name>.md` with `tools:` allowlist scoped to selected MCP servers
- `.mcp.json` with server configs from the catalog

## After mcpick-plus: Add delegation hint

Append a routing table to the project's `CLAUDE.md` so the primary session knows to delegate:

```markdown
## MCP Agent Routing

Delegate tasks to these agents instead of using MCP tools directly:

| Task Domain | Agent | Trigger |
|------------|-------|---------|
| Documentation | docs-helper | docs lookup, API reference, library usage |
| Communications | comms | notion pages, user questions |
```

## Manual Setup (when server isn't in catalog)

For MCP servers not in the mcpick-plus catalog, create files manually:

### Agent file: `<project>/.claude/agents/<name>.md`

```markdown
---
name: <name>
description: <What tasks to delegate here>. Use when <trigger phrases>.
model: sonnet
tools: Read, Write, Edit, Bash, Glob, Grep, mcp__<server-name>
---

You handle all <domain> tasks via MCP tools.

## When invoked
1. Read the task from your briefing
2. Use mcp__<server-name>__* tools to complete it
3. Return a concise result summary
```

### MCP config: `<project>/.mcp.json`

Merge the server entry into existing `.mcp.json` or create it:

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "<stdio|http|sse>",
      "command": "<command>",
      "args": ["<args>"],
      "env": { "<KEY>": "${<ENV_VAR>}" }
    }
  }
}
```

## Multi-server agents

Combine related MCP servers into one agent:

```bash
bunx mcpick-plus agent --name "comms" --servers "notion,consult-user-mcp" --model sonnet
```

## Removing a route

1. Delete `<project>/.claude/agents/<name>.md`
2. Remove server entry from `.mcp.json` (if no other agents need it)
3. Remove routing table row from `CLAUDE.md`
