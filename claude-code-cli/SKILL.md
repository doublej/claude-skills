---
name: claude-code-cli
description: Automates workflows with the Claude Code CLI. Covers interactive mode, print mode for scripting, conversation management, MCP configuration, multi-agent patterns, and JSON output schemas. Use when building automation scripts, configuring MCP servers, creating multi-agent workflows, or integrating Claude Code into CI/CD pipelines.
---

# Claude Code CLI

The Claude Code CLI (`claude`) provides three operating modes: interactive conversations, print mode for scripting, and session management for continuing work.

## Quick Start

```bash
# Interactive conversation
claude

# One-shot query (print mode)
claude -p "explain this codebase"

# Process file content
cat file.py | claude -p "review this code"

# Continue last conversation
claude -c
```

## Quick Command Reference

| Task | Command |
|------|---------|
| Interactive chat | `claude` |
| Start with prompt | `claude "initial question"` |
| One-shot query | `claude -p "query"` |
| Process file | `cat file \| claude -p "analyze"` |
| Continue chat | `claude -c` |
| Resume session | `claude -r "session-id"` |
| Use Opus model | `claude --model opus "query"` |
| JSON output | `claude -p --output-format json "query"` |
| Skip permissions | `claude -p --dangerously-skip-permissions "task"` |
| Limit turns | `claude -p --max-turns 5 "task"` |
| Custom agent | `claude --agent code-reviewer "review PR"` |

## Essential Flags

| Flag | Description |
|------|-------------|
| `-p, --print` | Print mode - outputs response and exits |
| `-c, --continue` | Continue most recent conversation |
| `-r, --resume <id>` | Resume specific session by ID |
| `--model <name>` | Model: `sonnet`, `opus`, `haiku` |
| `--output-format <fmt>` | Output: `text`, `json`, `stream-json` |
| `--system-prompt <text>` | Replace entire system prompt |
| `--append-system-prompt` | Add to default system prompt |
| `--tools <list>` | Available tools (e.g., `"Read,Bash"`) |
| `--max-turns <n>` | Limit agentic turns |
| `--mcp-config <path>` | Load MCP servers from JSON |
| `--agents <json>` | Define custom subagents |

## Three Operating Modes

### Interactive Mode (default)

Multi-turn conversations with human-in-the-loop:

```bash
claude                    # Start fresh
claude "explain this"     # Start with initial prompt
```

Use when: exploring code, iterative tasks, need human decisions.

### Print Mode (`-p`)

Single response, then exits. Perfect for scripting:

```bash
claude -p "what does main.py do"
cat error.log | claude -p "explain this error"
```

Use when: automation, scripts, CI/CD pipelines, one-shot queries.

### Continue/Resume

Pick up where you left off:

```bash
claude -c                      # Continue most recent
claude -c -p "add tests"       # Continue in print mode
claude -r "abc123" "query"     # Resume specific session
```

## Common Scripting Patterns

### Process File Content

```bash
# Code review
cat src/app.py | claude -p "review for bugs and improvements"

# Explain complex code
cat algorithm.py | claude -p "explain step by step"

# Generate tests
cat utils.py | claude -p "generate pytest tests"
```

### Git Integration

```bash
# Commit message from diff
git diff --cached | claude -p "write a commit message"

# PR description
git log main..HEAD --oneline | claude -p "summarize for PR description"

# Review changes
git diff | claude -p "review these changes"
```

### Capture Output

```bash
# To variable
RESULT=$(claude -p "query")

# To file
claude -p "query" > output.txt

# JSON parsing with jq
claude -p --output-format json "query" | jq '.result'
```

### Batch Processing

```bash
# Process multiple files
for f in src/*.py; do
    claude -p "review: $(cat $f)" > "reviews/$(basename $f).md"
done
```

**See [scripting-patterns.md](references/scripting-patterns.md) for comprehensive automation patterns.**

## Configuration Overview

### Model Selection

```bash
claude --model sonnet "query"  # Default, balanced
claude --model opus "query"    # Most capable
claude --model haiku "query"   # Fastest, cheapest
```

### System Prompts

```bash
# Replace entirely
claude -p --system-prompt "You are a code reviewer" "review this"

# Append to default
claude -p --append-system-prompt "Always use TypeScript" "write a function"
```

### Tool Control

```bash
# Specific tools only
claude -p --tools "Read,Grep" "find all TODOs"

# Disable all tools
claude -p --tools "" "just answer"

# Default (all tools)
claude -p --tools "default" "task"
```

### MCP Servers

```bash
# Configure MCP servers
claude mcp add filesystem /path/to/allowed

# Use MCP config file
claude --mcp-config ./mcp-servers.json "task"
```

**See [configuration.md](references/configuration.md) for full configuration details.**

## Advanced Features

### JSON Output

```bash
# Full JSON response
claude -p --output-format json "query"

# Stream JSON events
claude -p --output-format stream-json --include-partial-messages "query"
```

### JSON Schema Validation

Extract structured data with guaranteed schema:

```bash
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "summary": {"type": "string"},
    "issues": {"type": "array", "items": {"type": "string"}}
  }
}' "analyze this code for issues"
```

### Multi-Agent with `--agents`

Define specialized subagents:

```bash
claude --agents '{
  "reviewer": {
    "description": "Code review specialist",
    "prompt": "Focus on security and performance",
    "tools": ["Read", "Grep"],
    "model": "sonnet"
  }
}' "review the authentication module"
```

### Agentic Loop Control

Limit autonomous turns for safety:

```bash
claude -p --max-turns 3 "refactor this module"
```

**See [advanced-workflows.md](references/advanced-workflows.md) for SDK patterns and CI/CD integration.**

## Decision Guide

```
What do you need?
│
├─ Interactive conversation?
│  └─ claude "start question"
│
├─ Single query, capture output?
│  └─ claude -p "query"
│
├─ Process file content?
│  └─ cat file | claude -p "analyze"
│
├─ Continue previous work?
│  └─ claude -c
│
├─ Automated script/pipeline?
│  └─ claude -p --output-format json "query"
│
├─ Structured data extraction?
│  └─ claude -p --json-schema '{...}' "query"
│
├─ Limit autonomous actions?
│  └─ claude -p --max-turns N "task"
│
└─ Multi-agent workflow?
   └─ claude --agents '{...}' "task"
```

## Reference Files

- **[scripting-patterns.md](references/scripting-patterns.md)** - Comprehensive automation, CI/CD, git integration
- **[configuration.md](references/configuration.md)** - Models, prompts, tools, MCP, settings
- **[advanced-workflows.md](references/advanced-workflows.md)** - JSON schemas, multi-agent, SDK integration
