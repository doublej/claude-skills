# Advanced Patterns

## Programmatic Hooks

Run custom code at lifecycle points: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`.

### TypeScript

```typescript
import { query, HookCallback } from "@anthropic-ai/claude-agent-sdk";
import { appendFile } from "fs/promises";

const logEdits: HookCallback = async (input) => {
  const filePath = (input as any).tool_input?.file_path ?? "unknown";
  await appendFile("./audit.log", `${new Date().toISOString()}: modified ${filePath}\n`);
  return {};
};

for await (const message of query({
  prompt: "Refactor utils.py",
  options: {
    permissionMode: "acceptEdits",
    hooks: {
      PostToolUse: [{ matcher: "Edit|Write", hooks: [logEdits] }]
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

### Python

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def block_dangerous(input_data, tool_use_id, context):
    cmd = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf" in cmd:
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Blocked dangerous command"
        }}
    return {}

async def main():
    async for message in query(
        prompt="Clean up temp files",
        options=ClaudeAgentOptions(
            allowed_tools=["Bash"],
            hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[block_dangerous])]}
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)
```

## Programmatic Subagents

Define specialized agents inline. Include `Agent` in `allowedTools`.

### TypeScript

```typescript
for await (const message of query({
  prompt: "Use the reviewer agent to review this codebase",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Agent"],
    agents: {
      "reviewer": {
        description: "Code reviewer for quality and security.",
        prompt: "Analyze code quality and suggest improvements.",
        tools: ["Read", "Glob", "Grep"]
      }
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

### Python

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Agent"],
    agents={
        "reviewer": AgentDefinition(
            description="Code reviewer for quality and security.",
            prompt="Analyze code quality and suggest improvements.",
            tools=["Read", "Glob", "Grep"],
        )
    },
)
```

Messages from subagents include `parent_tool_use_id` for tracking.

## MCP Integration

### External MCP servers (both languages)

```typescript
// TypeScript
for await (const message of query({
  prompt: "Open example.com and describe what you see",
  options: {
    mcpServers: {
      playwright: { command: "npx", args: ["@playwright/mcp@latest"] }
    }
  }
})) { ... }
```

```python
# Python
options = ClaudeAgentOptions(
    mcp_servers={
        "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
    }
)
```

### Python SDK MCP servers (in-process)

Eliminates subprocess overhead — tools run in the same process:

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("greet", "Greet a user", {"name": str})
async def greet_user(args):
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}

server = create_sdk_mcp_server(name="my-tools", version="1.0.0", tools=[greet_user])

options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__greet"]
)
```

## Sessions

Capture session ID from init message, resume later with full context:

### TypeScript

```typescript
let sessionId: string | undefined;

// First query — capture session
for await (const msg of query({
  prompt: "Read the auth module",
  options: { allowedTools: ["Read", "Glob"] }
})) {
  if (msg.type === "system" && msg.subtype === "init") {
    sessionId = msg.session_id;
  }
}

// Resume with full context
for await (const msg of query({
  prompt: "Now find all places that call it",
  options: { resume: sessionId }
})) {
  if ("result" in msg) console.log(msg.result);
}
```

### Python

```python
session_id = None

async for message in query(
    prompt="Read the auth module",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"]),
):
    if hasattr(message, "subtype") and message.subtype == "init":
        session_id = message.session_id

async for message in query(
    prompt="Now find all places that call it",
    options=ClaudeAgentOptions(resume=session_id),
):
    if hasattr(message, "result"):
        print(message.result)
```

## Multi-Turn Conversations

### TypeScript — Async Iterator

```typescript
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

const inputQueue: SDKUserMessage[] = [];
let inputResolver: ((msg: SDKUserMessage) => void) | undefined;

async function* createInputIterator(): AsyncIterable<SDKUserMessage> {
  while (true) {
    if (inputQueue.length > 0) {
      yield inputQueue.shift()!;
    } else {
      yield await new Promise<SDKUserMessage>(r => { inputResolver = r; });
      inputResolver = undefined;
    }
  }
}

function sendMessage(content: string, sessionId?: string): void {
  const msg: SDKUserMessage = {
    type: "user",
    session_id: sessionId || "new",
    parent_tool_use_id: null,
    message: { role: "user", content },
  };
  inputResolver ? inputResolver(msg) : inputQueue.push(msg);
}

const q = query({
  prompt: createInputIterator(),
  options: {
    permissionMode: "bypassPermissions",
    allowDangerouslySkipPermissions: true,
    settingSources: ["user", "project"],
  },
});
```

### Python — ClaudeSDKClient

Bidirectional interactive client:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(allowed_tools=["Read", "Bash"])

async with ClaudeSDKClient(options=options) as client:
    await client.query("What files are here?")
    async for msg in client.receive_response():
        print(msg)

    # Continue the conversation
    await client.query("Now show me the largest file")
    async for msg in client.receive_response():
        print(msg)
```
