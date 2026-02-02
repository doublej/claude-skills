# Configuration

Complete reference for configuring Codex CLI: config files, providers, history, and AGENTS.md.

## Table of Contents

- [Config File](#config-file)
- [Provider Setup](#provider-setup)
- [History Settings](#history-settings)
- [AGENTS.md Deep Dive](#agentsmd-deep-dive)
- [Environment Variables](#environment-variables)

## Config File

Location: `~/.codex/config.yaml` or `~/.codex/config.json`

### Full Configuration Example

```yaml
# Model selection
model: o4-mini

# Approval mode: suggest | auto-edit | full-auto
approvalMode: suggest

# Desktop notifications
notify: true

# Error handling in full-auto mode
fullAutoErrorMode: ask-user  # or: ignore-and-continue

# History settings
history:
  maxSize: 1000
  saveHistory: true
  sensitivePatterns:
    - "password"
    - "api_key"
    - "secret"
    - "token"

# Custom providers
providers:
  - name: ollama
    baseURL: http://localhost:11434/v1
    envKey: OLLAMA_API_KEY
  - name: azure
    baseURL: https://myresource.openai.azure.com
    envKey: AZURE_OPENAI_API_KEY
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | string | `o4-mini` | Default model |
| `approvalMode` | string | `suggest` | Default autonomy level |
| `notify` | boolean | `false` | Desktop notifications |
| `fullAutoErrorMode` | string | `ask-user` | Error handling in full-auto |

## Provider Setup

### Built-in Providers

| Provider | Models | Setup Required |
|----------|--------|----------------|
| OpenAI | o4-mini, gpt-4o, etc. | `OPENAI_API_KEY` |
| OpenRouter | Various | `OPENROUTER_API_KEY` |
| Azure | Azure-deployed models | Custom config |
| Gemini | Gemini models | `GEMINI_API_KEY` |
| Ollama | Local models | Local server |
| Mistral | Mistral models | `MISTRAL_API_KEY` |
| DeepSeek | DeepSeek models | `DEEPSEEK_API_KEY` |
| xAI | Grok models | `XAI_API_KEY` |
| Groq | Fast inference | `GROQ_API_KEY` |
| ArceeAI | Arcee models | `ARCEEAI_API_KEY` |

### OpenAI (Default)

```bash
export OPENAI_API_KEY="sk-..."
codex "task"
```

### Ollama (Local)

Start Ollama server, then:

```bash
codex --provider ollama -m llama3 "task"
codex --provider ollama -m codellama "task"
```

### Azure OpenAI

Config in `~/.codex/config.yaml`:

```yaml
providers:
  - name: azure
    baseURL: https://<resource>.openai.azure.com
    envKey: AZURE_OPENAI_API_KEY
```

```bash
export AZURE_OPENAI_API_KEY="..."
codex --provider azure -m gpt-4o "task"
```

### OpenRouter

```bash
export OPENROUTER_API_KEY="..."
codex --provider openrouter -m anthropic/claude-3-opus "task"
```

### Custom OpenAI-Compatible API

```yaml
providers:
  - name: myapi
    baseURL: https://api.myservice.com/v1
    envKey: MYAPI_KEY
```

```bash
export MYAPI_KEY="..."
codex --provider myapi -m custom-model "task"
```

## History Settings

### Configuration

```yaml
history:
  maxSize: 1000           # Max stored sessions
  saveHistory: true       # Enable/disable history
  sensitivePatterns:      # Patterns to redact
    - "password"
    - "api_key"
    - "secret"
    - "bearer"
    - "token"
```

### Session Storage

Sessions stored in `~/.codex/sessions/`:

```
~/.codex/sessions/
├── 7f9f9a2e-1b3c-4c7a-9b0e-123456789abc.json
├── 8a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d.json
└── ...
```

### Session Management

```bash
# List all sessions (picker UI)
codex resume

# Resume most recent
codex resume --last

# Resume specific session
codex resume 7f9f9a2e-1b3c-4c7a-9b0e-123456789abc
```

## AGENTS.md Deep Dive

### File Hierarchy

Codex merges `AGENTS.md` files from multiple locations:

```
~/.codex/AGENTS.md              # Global (lowest priority)
    ↓
<repo-root>/AGENTS.md           # Repository level
    ↓
<parent-dir>/AGENTS.md          # Parent directories
    ↓
<current-dir>/AGENTS.md         # Current directory (highest priority)
```

### Override Files

Use `AGENTS.override.md` for local customizations (gitignored):

```
project/
├── AGENTS.md              # Shared, committed
└── AGENTS.override.md     # Local, gitignored
```

### Example AGENTS.md Files

**Global (`~/.codex/AGENTS.md`):**

```markdown
# Global Preferences

- Always explain changes before making them
- Use conventional commit messages
- Prefer TypeScript over JavaScript
```

**Repository (`<repo>/AGENTS.md`):**

```markdown
# Project: MyApp

## Stack
- Framework: Next.js 14
- Database: PostgreSQL with Prisma
- Testing: Jest + React Testing Library

## Conventions
- Use server components by default
- API routes in app/api/
- Run `pnpm test` before completing tasks

## File Patterns
- Components: PascalCase
- Utils: camelCase
- Tests: *.test.ts
```

**Directory-specific (`src/components/AGENTS.md`):**

```markdown
# Component Guidelines

- Use functional components with hooks
- Export default from index.ts
- Include unit tests in __tests__/
```

### Disabling AGENTS.md

```bash
# Skip all AGENTS.md files
codex --no-project-doc "task"

# Via environment
CODEX_DISABLE_PROJECT_DOC=1 codex "task"
```

## Environment Variables

### Authentication

| Variable | Provider |
|----------|----------|
| `OPENAI_API_KEY` | OpenAI (default) |
| `OPENROUTER_API_KEY` | OpenRouter |
| `AZURE_OPENAI_API_KEY` | Azure |
| `GEMINI_API_KEY` | Google Gemini |
| `MISTRAL_API_KEY` | Mistral |
| `DEEPSEEK_API_KEY` | DeepSeek |
| `XAI_API_KEY` | xAI |
| `GROQ_API_KEY` | Groq |
| `ARCEEAI_API_KEY` | ArceeAI |

### Custom Provider Variables

For custom providers defined in config:

```yaml
providers:
  - name: myservice
    baseURL: https://api.myservice.com/v1
    envKey: MYSERVICE_API_KEY
```

Set: `export MYSERVICE_API_KEY="..."`

### Behavior Variables

| Variable | Effect |
|----------|--------|
| `DEBUG=true` | Verbose logging |
| `CODEX_QUIET_MODE=1` | Force quiet mode |
| `CODEX_DISABLE_PROJECT_DOC=1` | Skip AGENTS.md |

### Example .env Setup

```bash
# .env.codex
export OPENAI_API_KEY="sk-..."
export CODEX_QUIET_MODE=0

# Source before use
source .env.codex && codex "task"
```

### Shell RC Integration

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Codex CLI
export OPENAI_API_KEY="sk-..."

# Completions
eval "$(codex completion zsh)"
```
