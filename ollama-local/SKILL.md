---
name: ollama-local
description: Use local network Ollama (Gemma) for LLM tasks like summarization, extraction, analysis. Trigger when offloading work to local model makes sense.
---

# Ollama Local

<description>
Interact with local network Ollama instance running Gemma models.
</description>

<endpoint>

## Endpoint

```
POST http://192.168.178.197:11434/v1/chat/completions
```

Verify: `curl http://192.168.178.197:11434/v1/models`

</endpoint>

<minimal_request>

## Minimal Request

```bash
curl -X POST http://192.168.178.197:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4-64k:latest",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Summarize: ..."}
    ]
  }'
```

Response: `data.choices[0].message.content`

</minimal_request>

<parameters>

## Parameters

| Param | Default | Notes |
|-------|---------|-------|
| model | `gemma4-64k:latest` | 64k context |
| temperature | 1.0 | Higher = creative |
| top_p | 0.95 | Nucleus sampling |
| top_k | 64 | Vocab filtering |
| think | false | Reasoning mode |

</parameters>

<typescript_client>

## TypeScript Client

For repeated calls, use or create reusable client:

```typescript
const response = await fetch('http://192.168.178.197:11434/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  signal: AbortSignal.timeout(300_000), // 5 min
  body: JSON.stringify({
    model: 'gemma4-64k:latest',
    messages: [
      { role: 'system', content: 'Extract key points.' },
      { role: 'user', content: inputText }
    ]
  })
})
const { choices } = await response.json()
return choices[0].message.content
```

</typescript_client>

<error_handling>

## Error Handling

- Connection refused → Ollama not running
- 404 → Wrong endpoint (must use `/v1/chat/completions`)
- Timeout → Model loading or prompt too large

</error_handling>

<when_to_use>

## When to Use

- Summarization of large text
- Data extraction/structuring
- Analysis that doesn't need Claude's capabilities
- Batch processing to save API costs

Full reference: `references/ollama-agent-guide.md`

</when_to_use>
