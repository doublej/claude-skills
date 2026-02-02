# Configuration

Complete reference for configuring Claude Code CLI: models, prompts, tools, MCP servers, and settings.

## Table of Contents

- [Model Selection](#model-selection)
- [System Prompts](#system-prompts)
- [Tool Configuration](#tool-configuration)
- [MCP Server Configuration](#mcp-server-configuration)
- [Settings Files](#settings-files)
- [Environment Variables](#environment-variables)

## Model Selection

### Available Models

| Model | Alias | Best For | Speed | Cost |
|-------|-------|----------|-------|------|
| Claude Sonnet | `sonnet` | General tasks, balanced | Fast | Medium |
| Claude Opus | `opus` | Complex reasoning, difficult tasks | Slower | Higher |
| Claude Haiku | `haiku` | Simple tasks, high volume | Fastest | Lowest |

### Usage

```bash
# Use alias
claude --model sonnet "query"
claude --model opus "complex analysis"
claude --model haiku "simple task"

# Full model name also works
claude --model claude-sonnet-4-20250514 "query"
```

### Fallback Models

For print mode, specify a fallback when primary model is overloaded:

```bash
claude -p --model opus --fallback-model sonnet "query"
```

### Model Selection Guide

```
Task complexity?
├─ Simple (formatting, basic Q&A)
│  └─ haiku - fastest, cheapest
├─ Standard (code review, explanations)
│  └─ sonnet - balanced default
└─ Complex (architecture, multi-step reasoning)
   └─ opus - most capable
```

## System Prompts

### Replace Default Prompt

Completely override the built-in system prompt:

```bash
# Inline
claude -p --system-prompt "You are a security auditor. Focus only on vulnerabilities." "review this code"

# From file (print mode only)
claude -p --system-prompt-file ./prompts/reviewer.txt "review"
```

### Append to Default

Add instructions while keeping Claude Code's default capabilities:

```bash
# Add constraints
claude -p --append-system-prompt "Always use TypeScript. Never use any." "write a utility"

# Add persona
claude -p --append-system-prompt "Respond in a friendly, casual tone." "explain this"

# Add format requirements
claude -p --append-system-prompt "Always output valid JSON." "analyze"
```

### Comparison

| Flag | Behavior | Default Tools | Use Case |
|------|----------|---------------|----------|
| `--system-prompt` | Replace all | Lost unless specified | Complete control |
| `--system-prompt-file` | Replace from file | Lost unless specified | Reproducible setups |
| `--append-system-prompt` | Add to default | Preserved | Add constraints |

### Common Prompt Patterns

```bash
# Code style enforcement
--append-system-prompt "Follow Google style guide. Use descriptive names."

# Output format
--append-system-prompt "Output only code, no explanations."

# Language preference
--append-system-prompt "Write all code in Rust."

# Security focus
--append-system-prompt "Prioritize security. Flag any potential vulnerabilities."
```

## Tool Configuration

### Available Tools

Core tools Claude Code can use:

- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit files
- `Bash` - Execute shell commands
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `Task` - Spawn sub-agents
- `WebFetch` - Fetch URLs
- `WebSearch` - Search the web

### Restrict Tools

```bash
# Specific tools only
claude -p --tools "Read,Grep,Glob" "find all TODO comments"

# Read-only mode
claude -p --tools "Read,Grep" "analyze this codebase"

# Disable all tools (pure conversation)
claude -p --tools "" "explain recursion"

# All tools (explicit default)
claude -p --tools "default" "full task"
```

### Tool Permissions

Control which tools need approval:

```bash
# Allow specific tools without prompting
claude --allowedTools "Read,Grep"

# Disallow specific tools
claude --disallowedTools "Bash,Write"
```

### Dangerous Permissions

Skip all permission prompts (use with caution):

```bash
# Only in controlled environments
claude -p --dangerously-skip-permissions "automated task"
```

**Warning**: Only use in trusted automation scenarios. Never with untrusted input.

## MCP Server Configuration

### Managing MCP Servers

```bash
# List configured servers
claude mcp list

# Add a server
claude mcp add <name> <command> [args...]

# Remove a server
claude mcp remove <name>
```

### Common MCP Servers

```bash
# Filesystem access
claude mcp add filesystem npx @anthropic/mcp-filesystem /allowed/path

# Git operations
claude mcp add git npx @anthropic/mcp-git

# Database access
claude mcp add postgres npx @anthropic/mcp-postgres "connection-string"
```

### MCP Config File

Create `mcp-servers.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic/mcp-filesystem", "/project"],
      "env": {}
    },
    "database": {
      "command": "npx",
      "args": ["@anthropic/mcp-postgres"],
      "env": {
        "DATABASE_URL": "postgres://..."
      }
    }
  }
}
```

Use with:

```bash
claude --mcp-config ./mcp-servers.json "query database"
```

### Strict MCP Mode

Only use servers from config file, ignore global settings:

```bash
claude --strict-mcp-config --mcp-config ./project-mcp.json "task"
```

## Settings Files

### Settings Hierarchy

1. **User settings** - `~/.claude/settings.json` (global defaults)
2. **Project settings** - `.claude/settings.json` (project-specific)
3. **Local settings** - `.claude/settings.local.json` (gitignored overrides)

### Settings File Format

```json
{
  "model": "sonnet",
  "customInstructions": "Always use TypeScript",
  "allowedTools": ["Read", "Grep", "Glob"],
  "disallowedTools": ["Bash"],
  "mcpServers": {
    "myserver": {
      "command": "node",
      "args": ["./server.js"]
    }
  }
}
```

### Control Settings Sources

```bash
# Load only user settings
claude --setting-sources "user"

# Load only project settings
claude --setting-sources "project"

# Combine specific sources
claude --setting-sources "user,project"

# Override with inline JSON
claude --settings '{"model": "opus"}' "query"

# Override with file
claude --settings ./custom-settings.json "query"
```

### CLAUDE.md Files

Project instructions via markdown files:

- `~/.claude/CLAUDE.md` - Global instructions
- `./CLAUDE.md` - Project root instructions
- `./.claude/CLAUDE.md` - Alternative project location

These are loaded as context, not as settings.

## Environment Variables

### API Configuration

```bash
# API key (required for API key auth)
export ANTHROPIC_API_KEY="sk-ant-..."

# API base URL (for proxies)
export ANTHROPIC_BASE_URL="https://custom-proxy.com"
```

### Authentication

```bash
# Force console-based auth (no browser)
export CLAUDE_CODE_SKIP_BROWSER=1
```

### Debugging

```bash
# Enable debug output
claude --debug "api,hooks"

# Verbose mode
claude --verbose "query"

# Debug categories
claude --debug "api"      # API calls
claude --debug "hooks"    # Hook execution
claude --debug "mcp"      # MCP servers
claude --debug "!statsig" # Exclude statsig
```

### Example .env Setup

```bash
# .env.claude
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_CODE_SKIP_BROWSER=1

# Source before use
source .env.claude && claude "query"
```
