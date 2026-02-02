---
name: codex-cli
description: Automates coding with the OpenAI Codex CLI. Covers interactive TUI, quiet mode for scripting, approval modes (suggest, auto-edit, full-auto), sandboxing, session management, and multi-provider support. Use when building Codex automation scripts, configuring approval modes, or integrating Codex into CI/CD pipelines.
---

# Codex CLI

OpenAI's Codex CLI (`codex`) is an AI coding agent with three autonomy levels, sandboxed execution, and multi-provider support.

## Quick Start

```bash
# Interactive TUI
codex

# Start with prompt
codex "fix all lint errors"

# Non-interactive (CI/scripts)
codex -q "explain utils.ts"

# Resume last session
codex resume --last
```

## Quick Command Reference

| Task | Command |
|------|---------|
| Interactive TUI | `codex` |
| Start with prompt | `codex "task"` |
| Quiet mode (scripting) | `codex -q "task"` |
| Exec mode | `codex exec "task"` |
| Resume last session | `codex resume --last` |
| Resume specific session | `codex resume <SESSION_ID>` |
| Session picker | `codex resume` |
| Suggest mode | `codex -a suggest "task"` |
| Auto-edit mode | `codex -a auto-edit "task"` |
| Full-auto mode | `codex -a full-auto "task"` |
| Use specific model | `codex -m o4-mini "task"` |
| Shell completions | `codex completion zsh` |

## Essential Flags

| Flag | Description |
|------|-------------|
| `-q, --quiet` | Non-interactive mode for scripts/CI |
| `-m, --model` | Specify model (default: `o4-mini`) |
| `-a, --approval-mode` | Autonomy: `suggest`, `auto-edit`, `full-auto` |
| `--provider` | AI provider (openai, azure, ollama, etc.) |
| `-C, --cd` | Set working directory root |
| `--add-dir` | Add writable directories (repeatable) |
| `-i, --image` | Attach images (comma-separated paths) |
| `--notify` | Enable desktop notifications |
| `--no-project-doc` | Disable AGENTS.md loading |
| `--json` | Output as JSON |

## Approval Modes

### Suggest (Default)

Most restrictive - read-only filesystem access:

```bash
codex -a suggest "analyze this codebase"
```

- Can read files
- Requires approval for all writes and shell commands
- Safe for exploration

### Auto-Edit

Balanced - can modify files autonomously:

```bash
codex -a auto-edit "refactor auth module"
```

- Can read and write files
- Requires approval for shell commands
- Good for refactoring tasks

### Full-Auto

Maximum autonomy with sandboxing:

```bash
codex -a full-auto "fix all tests and run them"
```

- Can read, write, and execute commands
- Network disabled by default
- Directory sandboxed
- No approval required

## Sandboxing

### macOS (12+)

Uses Apple Seatbelt (`sandbox-exec`):
- Restricts filesystem to working directory
- Blocks all outbound network

### Linux

Uses Docker with `iptables`:
- Read/write mounts at same paths
- Firewall denies all egress except OpenAI API
- Directory sandboxed

### Multi-Directory Access

```bash
# Main directory + additional writable dirs
codex --cd apps/frontend --add-dir ../backend --add-dir ../shared "update imports"
```

## Session Management

Sessions stored in `~/.codex/sessions/`:

```bash
# Show session picker UI
codex resume

# Resume most recent
codex resume --last

# Resume specific session
codex resume 7f9f9a2e-1b3c-4c7a-9b0e-123456789abc
```

## Interactive Features

### File Search

Type `@` to trigger fuzzy filename search, use arrow keys to select.

### Message Editing

Press `Esc` twice when composer is empty to edit previous messages. Press repeatedly to step through older messages.

## AGENTS.md Configuration

Codex merges guidance from multiple `AGENTS.md` files:

1. `~/.codex/AGENTS.md` - Global instructions
2. `<repo-root>/AGENTS.md` - Repository instructions
3. `<current-dir>/AGENTS.md` - Directory-specific instructions

Override files with `AGENTS.override.md` for local customization.

Example `AGENTS.md`:

```markdown
# Project Guidelines

- Use TypeScript for all new files
- Follow existing code style
- Run tests before completing tasks
- Prefer functional patterns
```

## Configuration Overview

Config file: `~/.codex/config.yaml` or `config.json`

```yaml
model: o4-mini
approvalMode: suggest
notify: true
fullAutoErrorMode: ask-user  # or ignore-and-continue
history:
  maxSize: 1000
  saveHistory: true
  sensitivePatterns:
    - "password"
    - "api_key"
```

**See [configuration.md](references/configuration.md) for full configuration and provider setup.**

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI API authentication |
| `<PROVIDER>_API_KEY` | Custom provider key |
| `<PROVIDER>_BASE_URL` | Custom provider endpoint |
| `DEBUG=true` | Verbose logging |
| `CODEX_QUIET_MODE=1` | Force quiet mode |
| `CODEX_DISABLE_PROJECT_DOC=1` | Skip AGENTS.md |

## Supported Providers

OpenAI, OpenRouter, Azure, Gemini, Ollama, Mistral, DeepSeek, xAI, Groq, ArceeAI, plus any OpenAI-compatible API.

```bash
# Use specific provider
codex --provider ollama -m llama3 "task"

# Use Azure
codex --provider azure -m gpt-4o "task"
```

**See [configuration.md](references/configuration.md) for custom provider setup.**

## Common Patterns

### Code Review

```bash
codex -a suggest "review this PR for security issues"
```

### Refactoring

```bash
codex -a auto-edit "extract common logic into utils module"
```

### Test Generation

```bash
codex -a full-auto "generate tests for auth.ts and run them"
```

### CI/CD Integration

```bash
# Non-interactive with JSON output
CODEX_QUIET_MODE=1 codex -q --json "analyze code quality" > report.json
```

**See [automation-patterns.md](references/automation-patterns.md) for comprehensive scripting patterns.**

## Decision Guide

```
What's your task?
│
├─ Exploration/analysis?
│  └─ codex -a suggest "query"
│
├─ Code changes (no shell)?
│  └─ codex -a auto-edit "task"
│
├─ Full automation (sandboxed)?
│  └─ codex -a full-auto "task"
│
├─ CI/CD pipeline?
│  └─ codex -q --json "task"
│
├─ Continue previous work?
│  └─ codex resume --last
│
└─ Multi-directory project?
   └─ codex --cd main --add-dir lib "task"
```

## Reference Files

- **[configuration.md](references/configuration.md)** - Full config, providers, history settings
- **[automation-patterns.md](references/automation-patterns.md)** - CI/CD, scripting, batch processing
