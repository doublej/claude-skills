# Ollama + Gemma Agent Quick Reference

> One-pager for AI agents to interact with local Ollama/Gemma models

## Endpoint

```
POST {baseURL}/chat/completions
```

Default: `http://192.168.178.197:11434/v1/chat/completions`

## Minimal Request

```typescript
const response = await fetch(`${baseURL}/chat/completions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'gemma4-64k:latest',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Summarize this text: ...' }
    ]
  })
})

const data = await response.json()
const content = data.choices[0].message.content
```

## Full Config

```typescript
type OllamaConfig = {
  baseURL: string        // e.g. 'http://192.168.178.197:11434/v1'
  model: string          // e.g. 'gemma4-64k:latest'
  timeout?: number       // ms, default 300000 (5 min)
  temperature?: number   // default 1.0
  top_p?: number         // default 0.95
  top_k?: number         // default 64
  think?: boolean        // enable reasoning mode, default false
}
```

## Reusable Client

```typescript
import { createOllamaClient } from './ollama.js'

const client = createOllamaClient({
  baseURL: 'http://192.168.178.197:11434/v1',
  model: 'gemma4-64k:latest',
  temperature: 1.0,
  top_p: 0.95,
  top_k: 64,
})

const response = await client.chat([
  { role: 'system', content: 'Extract key points.' },
  { role: 'user', content: transcriptText }
])
```

## Message Format

```typescript
type ChatMessage = {
  role: 'system' | 'user' | 'assistant'
  content: string
}
```

Pattern: system prompt defines behavior, user message provides input.

## Response Format

```typescript
type ChatResponse = {
  choices: [{ message: { content: string } }]
}
```

Access: `data.choices[0].message.content`

## Error Handling

```typescript
if (!response.ok) {
  const text = await response.text()
  throw new Error(`Ollama error ${response.status}: ${text}`)
}
```

Common errors:
- Connection refused: Ollama not running
- 404: Wrong endpoint path
- Timeout: Model still loading or prompt too large

## Timeout with AbortController

```typescript
const controller = new AbortController()
const timeout = setTimeout(() => controller.abort(), 300_000)

try {
  const response = await fetch(url, {
    // ...
    signal: controller.signal
  })
} finally {
  clearTimeout(timeout)
}
```

## Prompt Pattern Example

System prompt with structured output:

```typescript
const SYSTEM = `Extract action items.

Rules:
- Max 10 items
- Format: "- [ ] action"
- Drop completed items

Output only the list.`

const USER = `=== TRANSCRIPT ===
${transcript}

=== PRIOR CONTEXT ===
${priorContext ?? 'None'}`
```

## Defaults Reference

| Param | Default | Notes |
|-------|---------|-------|
| model | `gemma4-64k:latest` | 64k context window |
| temperature | 1.0 | Higher = more creative |
| top_p | 0.95 | Nucleus sampling |
| top_k | 64 | Vocab filtering |
| timeout | 300000ms | 5 minutes |
| think | false | Reasoning mode |

## Quick Checklist

1. Ollama running? (`curl http://host:11434/v1/models`)
2. Model pulled? (`ollama pull gemma4-64k`)
3. Using `/v1/chat/completions` path? (OpenAI-compatible)
4. Timeout sufficient for context size?
5. Handling abort/timeout?
