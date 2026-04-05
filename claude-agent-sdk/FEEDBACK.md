# Claude Agent SDK Skill - Feedback (resolved 2026-03-31)

## Session Context
- **Date**: 2026-03-10
- **Project**: BYOC (Bring Your Own Claude) plugin - WebSocket server exposing Claude Agent SDK to websites
- **Time spent debugging**: ~2 hours
- **Root cause**: Misleading auth documentation + placeholder `.env` overriding keychain auth

---

## Critical Issues

### 1. Authentication Section is Misleading/Incomplete

**Current documentation says:**
```
Set ANTHROPIC_API_KEY environment variable
Get key from: https://platform.claude.com/api
```

**What actually happens:**
- The SDK uses Claude Code's **built-in keychain authentication** by default (stored in macOS Keychain under "claude")
- Setting `ANTHROPIC_API_KEY` in `.env` **overrides** this built-in auth
- A placeholder like `ANTHROPIC_API_KEY=your-key-here` will cause "Invalid API key" errors
- The SDK does NOT clearly indicate when it's using keychain vs env var auth

**Fix needed:**
Add a section explaining:
```markdown
## Authentication Priority

The SDK uses credentials in this order:
1. `ANTHROPIC_API_KEY` environment variable (if set)
2. Claude Code's keychain credentials (default - works if you're logged into Claude Code)

**IMPORTANT**: Do NOT create a `.env` file with a placeholder API key.
This will override the working keychain auth and cause "Invalid API key" errors.

If you're already authenticated with Claude Code (via `claude` CLI), you likely
don't need to set ANTHROPIC_API_KEY at all.
```

### 2. No Working Code Examples

The skill provides no actual runnable code. Compare to beads-kanban which has working patterns:

**Missing: Basic query() usage**
```typescript
import { query, type SDKMessage, type SDKUserMessage } from '@anthropic-ai/claude-agent-sdk'

// Simple single-turn query
const q = query({
  prompt: 'Say hello',
  options: {
    cwd: process.cwd(),
    permissionMode: 'bypassPermissions',
    allowDangerouslySkipPermissions: true,
    settingSources: ['user', 'project'], // Load user's Claude config
  },
})

for await (const msg of q) {
  console.log(msg.type, msg)
  if (msg.type === 'result') break
}
```

**Missing: Multi-turn with async iterator**
```typescript
import { query, type SDKUserMessage } from '@anthropic-ai/claude-agent-sdk'

// Input queue for multi-turn conversations
const inputQueue: SDKUserMessage[] = []
let inputResolver: ((msg: SDKUserMessage) => void) | undefined

async function* createInputIterator(): AsyncIterable<SDKUserMessage> {
  while (true) {
    if (inputQueue.length > 0) {
      yield inputQueue.shift()!
    } else {
      const msg = await new Promise<SDKUserMessage>((resolve) => {
        inputResolver = resolve
      })
      inputResolver = undefined
      yield msg
    }
  }
}

// Create user message
function createUserMessage(content: string, sessionId?: string): SDKUserMessage {
  return {
    type: 'user',
    session_id: sessionId || 'new',
    parent_tool_use_id: null,
    message: { role: 'user', content },
  }
}

// Start query with iterator
const agentQuery = query({
  prompt: createInputIterator(),
  options: {
    cwd: process.cwd(),
    permissionMode: 'bypassPermissions',
    allowDangerouslySkipPermissions: true,
    settingSources: ['user', 'project'],
  },
})
```

### 3. Missing: Nested Session Prevention

**Critical gotcha not documented:**
When running the SDK from within a Claude Code session (e.g., via `just dev` or `bun --watch`), the `CLAUDECODE=1` and `CLAUDE_CODE_ENTRYPOINT=cli` env vars are inherited and can cause issues.

**Add to skill:**
```markdown
## Running SDK From Within Claude Code

If you start your SDK server from within a Claude Code session (terminal),
clear these env vars to prevent nested session detection:

```typescript
// At the very top of your entry file (before imports)
delete process.env.CLAUDECODE
delete process.env.CLAUDE_CODE_ENTRYPOINT
```

Or when starting the server:
```bash
CLAUDECODE= CLAUDE_CODE_ENTRYPOINT= bun src/index.ts
```
```

### 4. SDKMessage Type Structure Not Documented

**Add message type reference:**
```markdown
## SDK Message Types

The SDK emits these message types:

- `system` - Init message with `session_id`, status updates
- `assistant` - Claude's response with `message.content` array
- `stream_event` - Streaming deltas (when `includePartialMessages: true`)
  - `event.type === 'content_block_delta'` contains `delta.text`
- `result` - Final result, indicates turn complete

### Extracting Text from Messages

```typescript
function extractText(msg: SDKMessage): string | null {
  // Streaming delta
  if (msg.type === 'stream_event') {
    const event = msg.event
    if (event?.type === 'content_block_delta' && event.delta?.type === 'text_delta') {
      return event.delta.text
    }
  }

  // Full assistant message
  if (msg.type === 'assistant' && msg.message?.content) {
    return msg.message.content
      .filter(b => b.type === 'text')
      .map(b => b.text)
      .join('')
  }

  return null
}
```
```

### 5. settingSources Explanation Incomplete

**Current:** Just mentions `['project']` for CLAUDE.md

**Should explain:**
```markdown
## settingSources Options

- `'user'` - Load from `~/.claude/settings.json` + **keychain credentials**
- `'project'` - Load from `.claude/settings.json` + `CLAUDE.md`
- `'local'` - Load from `.claude/settings.local.json`

**Recommended for most use cases:**
```typescript
settingSources: ['user', 'project']
```
This loads user's credentials from keychain AND project-level config.
```

### 6. Version Compatibility Warning

The SDK has breaking changes between versions. The skill should note:
```markdown
## Version Compatibility

SDK versions can have breaking changes. Pin your version:
```json
"@anthropic-ai/claude-agent-sdk": "0.1.77"
```

Major version differences (0.1.x vs 0.2.x) may have different APIs.
Check the changelog before upgrading.
```

---

## Minor Issues

### 7. Wrong Documentation URL
Current: `https://platform.claude.com/api`
Should be: `https://console.anthropic.com/` (for API keys)

### 8. No Bun-Specific Notes
The SDK works with both Node.js and Bun, but Bun has better native WebSocket support. Worth mentioning for server use cases.

### 9. No Error Handling Examples
The skill mentions "Production Essentials: Error handling" but provides no examples of catching SDK errors or handling connection failures.

---

## Suggested Skill Structure

1. **Quick Start** - Minimal working example (5 lines)
2. **Authentication** - Priority order, keychain vs env var, common pitfalls
3. **Message Types** - What the SDK emits, how to extract text
4. **Single-Turn vs Multi-Turn** - Code examples for both
5. **Options Reference** - All query() options with descriptions
6. **Common Gotchas** - Nested sessions, .env override, version compat
7. **Integration Patterns** - WebSocket server, REST API, CLI tool

---

## Summary

The current skill reads like marketing copy rather than practical documentation. It lists features but doesn't show how to use them. The authentication section actively caused confusion by implying `ANTHROPIC_API_KEY` is required when the SDK can use keychain auth.

**Time lost due to missing info:** ~2 hours debugging "Invalid API key" that was caused by a placeholder `.env` file.

**What would have helped:** A single sentence: "If you're authenticated with Claude Code, you don't need ANTHROPIC_API_KEY - the SDK uses your keychain credentials. Setting an invalid key in .env will override this."
