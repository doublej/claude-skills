---
name: mcpick-plus
description: Manage MCP integrations across Claude Code configuration layers. Use when enabling/disabling MCP servers, creating agents with MCP capabilities, managing profiles, or inspecting layer configs.
---

# mcpick-plus

CLI tool for managing MCP integrations in Claude Code. Reduces startup time and token usage by selectively enabling only the MCP servers you need.

## Quick Reference

```bash
# Interactive menu (all features)
bunx mcpick-plus

# List available integrations from catalog
bunx mcpick-plus integrations catalog

# Enable integrations (comma-separated)
bunx mcpick-plus integrations enable "docs-context7,ui-consult-user" --layer project

# Disable integrations
bunx mcpick-plus integrations disable "docs-context7" --layer local

# Show what's installed (all layers or filtered)
bunx mcpick-plus integrations list
bunx mcpick-plus integrations list --layer project

# Describe an integration and its tools
bunx mcpick-plus integrations describe docs-context7
```

## Layers

| Layer | Flag | Config file | Scope |
|-------|------|-------------|-------|
| **project** | `--layer project` | `.mcp.json` | Shared via git |
| **local** | `--layer local` | `.claude/settings.local.json` | Machine-specific |
| **user** | `--layer user` | `~/.claude.json` | Global |

Default layer is `project`. Use `local` for personal overrides, `user` for system-wide tools.

```bash
# See all config paths
bunx mcpick-plus layers paths

# Show merged config with source attribution
bunx mcpick-plus layers effective
```

## Agents

Create dedicated agents with pre-configured MCP integrations:

```bash
# Create agent with specific integrations
bunx mcpick-plus agents create my-researcher --integrations "docs-context7" --layer project --description "Research agent"

# List / show / remove
bunx mcpick-plus agents list
bunx mcpick-plus agents show my-researcher
bunx mcpick-plus agents remove my-researcher
```

Agents are markdown files with YAML frontmatter saved to `.claude/agents/` (project) or `~/.claude/agents/` (user). Agent names must be lowercase alphanumeric with hyphens only.

## Profiles

Save and restore entire MCP configurations:

```bash
bunx mcpick-plus profiles save my-setup
bunx mcpick-plus profiles load my-setup
bunx mcpick-plus profiles list
```

## Other Commands

```bash
# System overview / cost dashboard
bunx mcpick-plus overview
bunx mcpick-plus dashboard

# Backup and restore
bunx mcpick-plus backup
bunx mcpick-plus restore

# Test MCP tools directly
bunx mcpick-plus mcp tools docs-context7
bunx mcpick-plus mcp call docs-context7 resolve-library-id --arg libraryName=react
```

## Global Flags

All commands accept: `--layer <layer>`, `--format json|table`, `--cwd <path>`, `--quiet`, `--verbose`.

## Built-in Catalog

| Name | Description |
|------|-------------|
| `docs-context7` | Up-to-date library docs and code examples |
| `ui-consult-user` | Ask user questions via native macOS dialogs |
| `notes-notion` | Read/update Notion workspaces |
| `storage-dropbox` | Search/browse Dropbox files |
| `ui-consult-user-sketch` | Interactive grid layout editor for wireframes |

Custom integrations can be added via the interactive menu or registered in `~/.claude/mcpick/servers.json`.

## Gotchas

- Only stdio servers supported for `mcp call` — HTTP/SSE configs can be stored but not invoked at runtime
- Catalog entries take precedence over user registry entries on name collision
- The `mcpick-plus-index` MCP server is auto-prepended to configs when enabling integrations (enables agent discovery)
- Plugin state tracked separately in `~/.claude/mcpick/plugin-state.json` — disabling doesn't modify plugin files
