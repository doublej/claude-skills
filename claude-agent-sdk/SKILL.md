---
name: claude-agent-sdk
description: "Build AI agents: auth, query API, hooks, subagents, MCP, sessions"
---

# Claude Agent SDK

Build AI agents using the same tools and agent loop that power Claude Code, programmable in Python and TypeScript.

<installation>
```bash
# TypeScript (Node.js 18+)
npm install @anthropic-ai/claude-agent-sdk

# Python (3.10+)
pip install claude-agent-sdk
```
</installation>

<authentication>
Priority order:
1. `ANTHROPIC_API_KEY` env var (if set — **overrides everything**)
2. Claude Code keychain credentials (default — works if logged into `claude` CLI)

**IMPORTANT**: Do NOT create a `.env` with a placeholder API key — it overrides working keychain auth and causes "Invalid API key" errors. If authenticated via `claude` CLI, you likely don't need `ANTHROPIC_API_KEY` at all.

Third-party providers:
- **Amazon Bedrock**: `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials
- **Google Vertex AI**: `CLAUDE_CODE_USE_VERTEX=1` + Google Cloud credentials
- **Microsoft Azure**: `CLAUDE_CODE_USE_FOUNDRY=1` + Azure credentials

API keys: https://platform.claude.com/
</authentication>

<quickstart>

### TypeScript

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  if ("result" in message) console.log(message.result);
}
```

### Python

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```


### TypeScript

```typescript
query({
  prompt: "string" | AsyncIterable<SDKUserMessage>,  // string or iterator for multi-turn
  options: {
    cwd: process.cwd(),
    systemPrompt: "You are...",
    allowedTools: ["Read", "Edit", "Bash"],
    disallowedTools: ["Write"],
    permissionMode: "bypassPermissions",    // or "acceptEdits", "default"
    allowDangerouslySkipPermissions: true,  // required for bypassPermissions
    settingSources: ["user", "project"],
    maxTurns: 10,
    resume: sessionId,
    mcpServers: { ... },
    hooks: { ... },
    agents: { ... },
  }
})
```

### Python

```python
ClaudeAgentOptions(
    cwd="/path/to/project",
    system_prompt="You are...",
    allowed_tools=["Read", "Edit", "Bash"],
    disallowed_tools=["Write"],
    permission_mode="bypassPermissions",
    allow_dangerously_skip_permissions=True,
    setting_sources=["user", "project"],
    max_turns=10,
    resume=session_id,
    mcp_servers={ ... },
    hooks={ ... },
    agents={ ... },
)
```

### settingSources

- `"user"` — `~/.claude/settings.json` + **keychain credentials**
- `"project"` — `.claude/settings.json` + `CLAUDE.md`
- `"local"` — `.claude/settings.local.json`

Recommended: `["user", "project"]` — loads credentials AND project config.
</quickstart>

<built_in_tools>

| Tool | Description |
|------|-------------|
| Read | Read any file |
| Write | Create new files |
| Edit | Precise edits to existing files |
| Bash | Run terminal commands |
| Glob | Find files by pattern |
| Grep | Search file contents with regex |
| WebSearch | Search the web |
| WebFetch | Fetch and parse web pages |
| Agent | Spawn subagents |
| AskUserQuestion | Ask user clarifying questions |
</built_in_tools>

<message_types>

### TypeScript

```typescript
for await (const msg of query({ prompt, options })) {
  switch (msg.type) {
    case "system":    // init with session_id
      if (msg.subtype === "init") sessionId = msg.session_id;
      break;
    case "assistant": // Claude's response — msg.message.content is ContentBlock[]
      break;
    case "result":    // turn complete — msg.result has final text
      break;
  }
}
```

### Python

```python
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
    elif isinstance(message, ResultMessage):
        print(message.result)
```

### Error Types (Python)

```python
from claude_agent_sdk import (
    ClaudeSDKError,      # base
    CLINotFoundError,    # Claude Code CLI missing
    CLIConnectionError,  # connection issues
    ProcessError,        # process failed (.exit_code)
    CLIJSONDecodeError,  # JSON parsing
)
```
</message_types>

<advanced_features>
See `references/` for detailed patterns:
- **Hooks** — programmatic lifecycle hooks (PreToolUse, PostToolUse, Stop, etc.)
- **Subagents** — inline specialized agents via `agents` option
- **MCP** — external tool servers + Python in-process SDK MCP servers
- **Sessions** — resume/fork conversations
- **Multi-turn** — bidirectional conversations via async iterators (TS) or ClaudeSDKClient (Python)
</advanced_features>

<gotchas>
### Nested Session Prevention

When running SDK from within a Claude Code terminal, inherited env vars cause issues:
```typescript
// Top of entry file, before other imports
delete process.env.CLAUDECODE;
delete process.env.CLAUDE_CODE_ENTRYPOINT;
```
Or: `CLAUDECODE= CLAUDE_CODE_ENTRYPOINT= bun src/index.ts`

### Version Pinning

Pin your version — breaking changes occur between releases. TS SDK is on **0.2.x**, Python on **0.1.x**. Check changelogs before upgrading.

### Claude Code Features

With `settingSources: ["project"]`, agents get access to:
- Subagents (`.claude/agents/`), Skills (`.claude/skills/`), Hooks (`.claude/settings.json`)
- Slash Commands (`.claude/commands/`), Memory (`CLAUDE.md`), Plugins (via `plugins` option)
</gotchas>

<resources>
- **Docs**: https://platform.claude.com/docs/en/agent-sdk/overview
- **TS GitHub**: https://github.com/anthropics/claude-agent-sdk-typescript
- **Python GitHub**: https://github.com/anthropics/claude-agent-sdk-python
- **Examples**: https://github.com/anthropics/claude-agent-sdk-demos
</resources>
