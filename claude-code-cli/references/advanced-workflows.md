# Advanced Workflows

Advanced patterns for JSON output, multi-agent configurations, SDK integration, and production workflows.

## Table of Contents

- [JSON Output Modes](#json-output-modes)
- [JSON Schema Validation](#json-schema-validation)
- [Multi-Agent Patterns](#multi-agent-patterns)
- [SDK Integration](#sdk-integration)
- [Agentic Loop Control](#agentic-loop-control)
- [Production Patterns](#production-patterns)

## JSON Output Modes

### Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Text | `--output-format text` | Human readable (default) |
| JSON | `--output-format json` | Structured response |
| Stream JSON | `--output-format stream-json` | Real-time events |

### JSON Output

Get structured JSON response:

```bash
claude -p --output-format json "analyze this code"
```

Response structure:

```json
{
  "type": "result",
  "subtype": "success",
  "cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 1100,
  "result": "The analysis shows...",
  "session_id": "abc123",
  "num_turns": 1
}
```

### Stream JSON

Real-time streaming events:

```bash
claude -p --output-format stream-json --include-partial-messages "task"
```

Events include:

- `init` - Session started
- `assistant` - Assistant messages
- `tool_use` - Tool invocations
- `tool_result` - Tool outputs
- `result` - Final result

### Parsing JSON Output

```bash
# Extract result text
claude -p --output-format json "query" | jq -r '.result'

# Get cost
claude -p --output-format json "query" | jq '.cost_usd'

# Check for errors
claude -p --output-format json "query" | jq '.is_error'

# Get session ID for resume
SESSION=$(claude -p --output-format json "task" | jq -r '.session_id')
claude -r "$SESSION" "continue"
```

## JSON Schema Validation

### Basic Schema

Force output to match a JSON schema:

```bash
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "summary": {"type": "string"},
    "score": {"type": "number"}
  },
  "required": ["summary", "score"]
}' "evaluate this code"
```

### Array Output

```bash
claude -p --json-schema '{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "file": {"type": "string"},
      "issues": {"type": "array", "items": {"type": "string"}}
    }
  }
}' "find issues in all Python files"
```

### Enum Constraints

```bash
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "severity": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"]
    },
    "category": {
      "type": "string",
      "enum": ["bug", "security", "performance", "style"]
    },
    "description": {"type": "string"}
  },
  "required": ["severity", "category", "description"]
}' "classify this bug report"
```

### Complex Schema Example

```bash
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "analysis": {
      "type": "object",
      "properties": {
        "complexity": {"type": "number", "minimum": 1, "maximum": 10},
        "maintainability": {"type": "number", "minimum": 1, "maximum": 10}
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "line": {"type": "integer"},
          "type": {"type": "string"},
          "message": {"type": "string"}
        },
        "required": ["type", "message"]
      }
    },
    "recommendations": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "required": ["analysis", "issues", "recommendations"]
}' "comprehensive code review"
```

### Shell Script with Schema

```bash
#!/bin/bash
# analyze.sh - Structured analysis with schema validation

SCHEMA='{
  "type": "object",
  "properties": {
    "bugs": {"type": "array", "items": {"type": "string"}},
    "security": {"type": "array", "items": {"type": "string"}},
    "suggestions": {"type": "array", "items": {"type": "string"}}
  }
}'

RESULT=$(cat "$1" | claude -p --json-schema "$SCHEMA" "analyze this code")

# Process structured output
echo "$RESULT" | jq -r '.bugs[]' | while read bug; do
    echo "BUG: $bug"
done
```

## Multi-Agent Patterns

### Single Custom Agent

Override the agent persona:

```bash
claude --agent security-reviewer "review authentication code"
```

### Define Subagents

Create specialized subagents with `--agents`:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer for quality and best practices",
    "prompt": "You are a senior engineer. Focus on code quality, maintainability, and edge cases.",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  },
  "security-auditor": {
    "description": "Security specialist for vulnerability detection",
    "prompt": "You are a security expert. Identify vulnerabilities, injection risks, and auth issues.",
    "tools": ["Read", "Grep"],
    "model": "opus"
  },
  "test-writer": {
    "description": "Test generation specialist",
    "prompt": "Generate comprehensive tests with edge cases and error scenarios.",
    "tools": ["Read", "Write", "Bash"],
    "model": "sonnet"
  }
}' "review and test the auth module"
```

### Agent Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | When to invoke this agent |
| `prompt` | Yes | System prompt for the agent |
| `tools` | No | Array of tool names (default: inherit all) |
| `model` | No | Model alias: `sonnet`, `opus`, `haiku` |

### Agent File Pattern

Store agents in a JSON file:

```json
// agents.json
{
  "reviewer": {
    "description": "Code review specialist",
    "prompt": "Focus on code quality and best practices.",
    "tools": ["Read", "Grep"],
    "model": "sonnet"
  },
  "documenter": {
    "description": "Documentation writer",
    "prompt": "Generate clear, concise documentation.",
    "tools": ["Read", "Write"],
    "model": "haiku"
  }
}
```

Use with:

```bash
claude --agents "$(cat agents.json)" "task"
```

## SDK Integration

### Node.js/TypeScript

```typescript
import { execSync } from 'child_process';

function queryClaudeCode(prompt: string, options?: {
  model?: 'sonnet' | 'opus' | 'haiku';
  maxTurns?: number;
  jsonSchema?: object;
}): string {
  const args = ['-p'];

  if (options?.model) args.push('--model', options.model);
  if (options?.maxTurns) args.push('--max-turns', options.maxTurns.toString());
  if (options?.jsonSchema) {
    args.push('--json-schema', JSON.stringify(options.jsonSchema));
  }

  args.push('--output-format', 'json');
  args.push(prompt);

  const result = execSync(`claude ${args.join(' ')}`, {
    encoding: 'utf-8',
    maxBuffer: 10 * 1024 * 1024
  });

  return JSON.parse(result).result;
}

// Usage
const analysis = queryClaudeCode('analyze this codebase', {
  model: 'opus',
  maxTurns: 5
});
```

### Python

```python
import subprocess
import json
from typing import Optional

def query_claude_code(
    prompt: str,
    model: Optional[str] = None,
    max_turns: Optional[int] = None,
    json_schema: Optional[dict] = None,
    timeout: int = 300
) -> str:
    """Query Claude Code CLI and return result."""
    args = ['claude', '-p', '--output-format', 'json']

    if model:
        args.extend(['--model', model])
    if max_turns:
        args.extend(['--max-turns', str(max_turns)])
    if json_schema:
        args.extend(['--json-schema', json.dumps(json_schema)])

    args.append(prompt)

    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        raise RuntimeError(f"Claude Code error: {result.stderr}")

    return json.loads(result.stdout)['result']

# Usage
analysis = query_claude_code(
    "analyze this code for security issues",
    model="opus",
    max_turns=3
)
```

### Streaming in Python

```python
import subprocess
import json

def stream_claude_code(prompt: str):
    """Stream Claude Code responses."""
    process = subprocess.Popen(
        ['claude', '-p', '--output-format', 'stream-json',
         '--include-partial-messages', prompt],
        stdout=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        if line.strip():
            event = json.loads(line)
            yield event

    process.wait()

# Usage
for event in stream_claude_code("explain this code"):
    if event.get('type') == 'assistant':
        print(event.get('message', ''), end='', flush=True)
```

## Agentic Loop Control

### Limit Turns

Prevent runaway loops:

```bash
# Maximum 3 autonomous turns
claude -p --max-turns 3 "refactor this module"

# Single turn (no follow-ups)
claude -p --max-turns 1 "quick analysis"
```

### When to Limit Turns

| Scenario | Recommended Max Turns |
|----------|----------------------|
| Quick query | 1 |
| Code review | 3-5 |
| Refactoring | 5-10 |
| Complex multi-file changes | 10-20 |
| Autonomous development | 20+ (with monitoring) |

### Combining with Tool Restrictions

```bash
# Read-only analysis with limited turns
claude -p --max-turns 3 --tools "Read,Grep,Glob" "find all security issues"

# Careful editing
claude -p --max-turns 5 --tools "Read,Edit" "fix the bug in auth.py"
```

## Production Patterns

### Wrapper Script

```bash
#!/bin/bash
# claude-prod.sh - Production Claude Code wrapper

set -euo pipefail

LOG_DIR="${CLAUDE_LOG_DIR:-/var/log/claude}"
MAX_TURNS="${CLAUDE_MAX_TURNS:-10}"
TIMEOUT="${CLAUDE_TIMEOUT:-300}"

log() {
    echo "[$(date -Iseconds)] $*" >> "$LOG_DIR/claude.log"
}

query() {
    local prompt="$1"
    local start_time=$(date +%s)

    log "START: $prompt"

    local result
    if result=$(timeout "$TIMEOUT" claude -p \
        --max-turns "$MAX_TURNS" \
        --output-format json \
        "$prompt" 2>&1); then

        local duration=$(($(date +%s) - start_time))
        local cost=$(echo "$result" | jq -r '.cost_usd // "unknown"')
        log "SUCCESS: duration=${duration}s cost=$cost"
        echo "$result" | jq -r '.result'
    else
        log "FAILED: $result"
        return 1
    fi
}

query "$@"
```

### Health Check

```bash
#!/bin/bash
# healthcheck.sh - Verify Claude Code is working

if claude -p --max-turns 1 "respond with OK" | grep -q "OK"; then
    echo "Claude Code: healthy"
    exit 0
else
    echo "Claude Code: unhealthy"
    exit 1
fi
```

### Rate Limiting

```bash
#!/bin/bash
# rate-limited-claude.sh

RATE_FILE="/tmp/claude_rate"
MAX_PER_MINUTE=10

current_minute=$(date +%Y%m%d%H%M)
count=$(grep -c "^$current_minute$" "$RATE_FILE" 2>/dev/null || echo 0)

if [ "$count" -ge "$MAX_PER_MINUTE" ]; then
    echo "Rate limit exceeded" >&2
    exit 1
fi

echo "$current_minute" >> "$RATE_FILE"

# Clean old entries
grep "^$current_minute$" "$RATE_FILE" > "${RATE_FILE}.tmp"
mv "${RATE_FILE}.tmp" "$RATE_FILE"

claude -p "$@"
```

### Monitoring Dashboard Data

```bash
#!/bin/bash
# metrics.sh - Collect metrics for monitoring

claude -p --output-format json "status check" | jq '{
  timestamp: now | todate,
  cost_usd: .cost_usd,
  duration_ms: .duration_ms,
  turns: .num_turns,
  success: (if .is_error then 0 else 1 end)
}' >> /var/log/claude/metrics.jsonl
```

### Error Recovery

```python
import subprocess
import time
from typing import Optional

def robust_claude_query(
    prompt: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Optional[str]:
    """Query with exponential backoff retry."""

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['claude', '-p', '--output-format', 'json', prompt],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                return json.loads(result.stdout)['result']

            # Check if retriable
            if 'overloaded' in result.stderr.lower():
                wait = backoff_factor ** attempt
                time.sleep(wait)
                continue
            else:
                raise RuntimeError(result.stderr)

        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                continue
            raise

    return None
```
