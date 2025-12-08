# Claude Code Hooks in Cookiecutter Templates

Generate projects with pre-configured Claude Code hooks for automation, validation, and security.

## What Are Claude Code Hooks?

Shell commands that execute automatically at specific points in Claude Code's lifecycle. They provide deterministic control through scripts rather than relying on LLM decisions.

## Hook Events

| Event | Trigger | Can Block | Use Case |
|-------|---------|-----------|----------|
| `SessionStart` | Session begins | No | Load context, set env vars |
| `UserPromptSubmit` | Prompt submitted | Yes | Validate prompts, add context |
| `PreToolUse` | Before tool runs | Yes | Allow/deny tools, modify inputs |
| `PermissionRequest` | Permission dialog | Yes | Auto-allow/deny permissions |
| `PostToolUse` | After tool completes | No | Validate results, auto-format |
| `Notification` | Notifications sent | No | Route/filter alerts |
| `PreCompact` | Before compaction | Yes | Preserve context |
| `Stop` | Agent finishes | Yes | Decide continuation |
| `SubagentStop` | Subagent finishes | Yes | Control subagent flow |
| `SessionEnd` | Session ends | No | Cleanup, logging |

## Hook Configuration in Templates

### Directory Structure

```
{{ cookiecutter.project_slug }}/
├── .claude/
│   ├── CLAUDE.md
│   ├── settings.json              # Committed hooks (shared)
│   └── hooks/                     # Hook scripts
│       ├── protect-files.sh
│       ├── auto-format.sh
│       └── audit-log.sh
```

### settings.json Template

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/protect-files.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/auto-format.sh"
          }
        ]
      }
    ]
  }
}
```

## Hook Input/Output

### Input (JSON via stdin)

All hooks receive:

```json
{
  "session_id": "abc-123",
  "transcript_path": "/path/to/transcript",
  "cwd": "/project/root",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

Event-specific additions:
- `PreToolUse`: `tool_name`, `tool_input`
- `PostToolUse`: `tool_name`, `tool_output`, `tool_exit_code`
- `UserPromptSubmit`: `user_prompt`
- `PermissionRequest`: `tool_name`, `permission_type`

### Exit Codes

| Code | Behavior |
|------|----------|
| `0` | Success, continue |
| `2` | Block operation, show stderr to Claude |
| Other | Warning only, continue |

### Structured Output (JSON)

```json
{
  "continue": true,
  "stopReason": "explanation",
  "suppressOutput": false,
  "systemMessage": "context for Claude"
}
```

## Hook Script Templates

### File Protection (PreToolUse)

**File:** `.claude/hooks/protect-files.sh`

```bash
#!/bin/bash
# Prevent modifications to sensitive files
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
tool_input=$(echo "$input" | jq -r '.tool_input')

if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" ]]; then
    file_path=$(echo "$tool_input" | jq -r '.file_path // .path // empty')

    # Block sensitive patterns
    case "$file_path" in
        *.env.production*|*secrets*|*.pem|*.key)
            echo "BLOCKED: Cannot modify sensitive file: $file_path" >&2
            exit 2
            ;;
    esac
fi

exit 0
```

### Auto-Format (PostToolUse)

**File:** `.claude/hooks/auto-format.sh`

```bash
#!/bin/bash
# Auto-format files after write
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
exit_code=$(echo "$input" | jq -r '.tool_exit_code')

if [[ "$tool_name" == "Write" && "$exit_code" == "0" ]]; then
    file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')

    case "$file_path" in
        *.py)
            uv run ruff format "$file_path" 2>/dev/null || true
            ;;
        *.js|*.ts|*.jsx|*.tsx)
            npx prettier --write "$file_path" 2>/dev/null || true
            ;;
    esac
fi

exit 0
```

### Audit Logging (PostToolUse)

**File:** `.claude/hooks/audit-log.sh`

```bash
#!/bin/bash
# Log all tool executions
set -euo pipefail

input=$(cat)
log_dir="${CLAUDE_PROJECT_DIR:-.}/.claude/logs"
mkdir -p "$log_dir"

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
session_id=$(echo "$input" | jq -r '.session_id')
tool_name=$(echo "$input" | jq -r '.tool_name')

jq -nc \
    --arg ts "$timestamp" \
    --arg sid "$session_id" \
    --arg tool "$tool_name" \
    '{timestamp: $ts, session: $sid, tool: $tool}' \
    >> "$log_dir/audit.jsonl"

exit 0
```

### Permission Auto-Approval (PermissionRequest)

**File:** `.claude/hooks/auto-approve.sh`

```bash
#!/bin/bash
# Auto-approve safe tools
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

case "$tool_name" in
    Read|Glob|Grep)
        decision="allow"
        ;;
    Write|Edit)
        # Allow in src/, deny elsewhere
        file_path=$(echo "$input" | jq -r '.permission_context.file_path // empty')
        if [[ "$file_path" == src/* || "$file_path" == tests/* ]]; then
            decision="allow"
        else
            decision="ask"
        fi
        ;;
    Bash)
        decision="ask"
        ;;
    *)
        decision="ask"
        ;;
esac

jq -nc --arg d "$decision" '{"hookSpecificOutput":{"permissionDecision":$d}}'
exit 0
```

### Session Setup (SessionStart)

**File:** `.claude/hooks/session-start.sh`

```bash
#!/bin/bash
# Initialize session with project context
set -euo pipefail

input=$(cat)
cwd=$(echo "$input" | jq -r '.cwd')
env_file="${CLAUDE_ENV_FILE:-}"

# Set project variables
if [[ -n "$env_file" ]]; then
    echo "PROJECT_NAME={{ cookiecutter.project_name }}" >> "$env_file"
    echo "PACKAGE_NAME={{ cookiecutter.package_name }}" >> "$env_file"

    # Load .env if exists
    if [[ -f "$cwd/.env" ]]; then
        grep -v '^#' "$cwd/.env" | grep '=' >> "$env_file" 2>/dev/null || true
    fi
fi

echo "Session initialized for {{ cookiecutter.project_name }}"
exit 0
```

### Prompt Validation (UserPromptSubmit)

**File:** `.claude/hooks/validate-prompt.sh`

```bash
#!/bin/bash
# Block dangerous prompts
set -euo pipefail

input=$(cat)
prompt=$(echo "$input" | jq -r '.user_prompt')

# Dangerous patterns
if echo "$prompt" | grep -qiE 'rm -rf|chmod -R 777|curl.*\|.*sh|eval\('; then
    jq -nc '{
        "continue": false,
        "stopReason": "Prompt contains potentially dangerous patterns"
    }'
    exit 0
fi

# Add project context to all prompts
jq -nc --arg ctx "Project: {{ cookiecutter.project_name }}" \
    '{"systemMessage": $ctx}'
exit 0
```

## Cookiecutter Integration

### cookiecutter.json

```json
{
    "project_name": "My Project",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
    "use_hooks": ["none", "basic", "full"],
    "_hooks_enabled": "{{ cookiecutter.use_hooks != 'none' }}"
}
```

### Conditional Hook Generation

In `post_gen_project.py`:

```python
#!/usr/bin/env python
import os
import shutil

USE_HOOKS = "{{ cookiecutter.use_hooks }}"

if USE_HOOKS == "none":
    # Remove hooks directory
    shutil.rmtree(".claude/hooks", ignore_errors=True)

    # Remove hooks from settings.json
    import json
    settings_path = ".claude/settings.json"
    if os.path.exists(settings_path):
        with open(settings_path) as f:
            settings = json.load(f)
        settings.pop("hooks", None)
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=2)

elif USE_HOOKS == "basic":
    # Keep only essential hooks
    keep = {"protect-files.sh", "auto-format.sh"}
    hooks_dir = ".claude/hooks"
    for f in os.listdir(hooks_dir):
        if f not in keep:
            os.remove(os.path.join(hooks_dir, f))

# Make all hook scripts executable
for script in Path(".claude/hooks").glob("*.sh"):
    os.chmod(script, 0o755)
```

## Security Best Practices

### Input Validation

```bash
# Always validate JSON input
input=$(cat)
if ! echo "$input" | jq -e . >/dev/null 2>&1; then
    echo "Invalid JSON input" >&2
    exit 1
fi

# Validate required fields
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
if [[ -z "$tool_name" ]]; then
    echo "Missing tool_name" >&2
    exit 1
fi
```

### Path Safety

```bash
# Prevent path traversal
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

if [[ "$file_path" == *".."* ]]; then
    echo "Path traversal blocked" >&2
    exit 2
fi

# Require absolute paths or project-relative
if [[ "$file_path" != /* && "$file_path" != ./* ]]; then
    file_path="./$file_path"
fi
```

### Environment Isolation

```bash
# Use CLAUDE_PROJECT_DIR for safety
project_root="${CLAUDE_PROJECT_DIR:-.}"

# Never trust user-provided paths directly
safe_path="$project_root/$(basename "$file_path")"
```

## CLAUDE.md Hook Documentation

Include in generated `.claude/CLAUDE.md`:

```markdown
## Configured Hooks

This project includes Claude Code hooks for:

{% if cookiecutter.use_hooks in ['basic', 'full'] %}
### File Protection
- Blocks modifications to `.env.production`, secrets, and key files
- Location: `.claude/hooks/protect-files.sh`

### Auto-Formatting
- Runs `ruff format` on Python files after write
- Runs `prettier` on JS/TS files after write
- Location: `.claude/hooks/auto-format.sh`
{% endif %}

{% if cookiecutter.use_hooks == 'full' %}
### Audit Logging
- Logs all tool executions to `.claude/logs/audit.jsonl`
- Location: `.claude/hooks/audit-log.sh`

### Permission Management
- Auto-approves Read/Glob/Grep
- Requires confirmation for Bash commands
- Location: `.claude/hooks/auto-approve.sh`
{% endif %}

### Modifying Hooks
Edit `.claude/settings.json` to add/remove hooks.
Edit scripts in `.claude/hooks/` to modify behavior.
```

## Testing Hooks

### Manual Test Script

```bash
#!/bin/bash
# test-hooks.sh - Test hook scripts locally

test_hook() {
    local hook=$1
    local input=$2

    echo "Testing: $hook"
    echo "$input" | .claude/hooks/"$hook"
    echo "Exit code: $?"
    echo "---"
}

# Test file protection
test_hook "protect-files.sh" '{
    "tool_name": "Write",
    "tool_input": {"file_path": ".env.production"}
}'

# Test allowed file
test_hook "protect-files.sh" '{
    "tool_name": "Write",
    "tool_input": {"file_path": "src/main.py"}
}'
```

### Pytest Integration

```python
# tests/test_hooks.py
import subprocess
import json
from pathlib import Path

HOOKS_DIR = Path(".claude/hooks")

def run_hook(hook_name: str, input_data: dict) -> tuple[int, str, str]:
    """Run hook script with JSON input."""
    result = subprocess.run(
        [str(HOOKS_DIR / hook_name)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr

def test_protect_files_blocks_secrets():
    code, stdout, stderr = run_hook("protect-files.sh", {
        "tool_name": "Write",
        "tool_input": {"file_path": ".env.production"}
    })
    assert code == 2
    assert "BLOCKED" in stderr

def test_protect_files_allows_src():
    code, stdout, stderr = run_hook("protect-files.sh", {
        "tool_name": "Write",
        "tool_input": {"file_path": "src/main.py"}
    })
    assert code == 0
```

## Checklist

Template hooks should:

- [ ] Use `set -euo pipefail` for safety
- [ ] Validate JSON input before parsing
- [ ] Quote all variables (`"$var"` not `$var`)
- [ ] Use exit code 2 for blocking errors
- [ ] Include clear error messages in stderr
- [ ] Be executable (`chmod +x`)
- [ ] Have corresponding tests
- [ ] Be documented in CLAUDE.md
- [ ] Handle missing optional fields gracefully
- [ ] Use `CLAUDE_PROJECT_DIR` for paths
