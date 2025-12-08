---
name: raycast-scripts
description: Create Raycast script commands for macOS automation. Covers metadata syntax, output modes (fullOutput, compact, silent, inline), arguments, supported languages (Bash, Python, Swift, AppleScript, JavaScript, Ruby), and best practices. Use when building custom Raycast commands, launcher scripts, or macOS automation tools.
---

# Raycast Script Commands

Guide for creating Raycast script commands - executable scripts that integrate with the Raycast launcher on macOS.

## When to Use

- Building custom Raycast commands
- Creating macOS automation scripts
- Adding quick-access utilities to Raycast
- Building inline dashboard widgets
- Creating scripts with user input arguments

## Supported Languages

| Language | Extension | Shebang |
|----------|-----------|---------|
| Bash | `.sh` | `#!/bin/bash` |
| Python | `.py` | `#!/usr/bin/env python3` |
| Swift | `.swift` | `#!/usr/bin/swift` |
| AppleScript | `.applescript` | `#!/usr/bin/osascript` |
| JavaScript | `.js` | `#!/usr/bin/env node` |
| Ruby | `.rb` | `#!/usr/bin/env ruby` |

## Required Metadata

All scripts need comment-based metadata. Use `#` for shell/python/ruby or `//` for swift/javascript.

```bash
#!/bin/bash

# Required:
# @raycast.schemaVersion 1
# @raycast.title My Command
# @raycast.mode compact

# Recommended:
# @raycast.packageName Utils
# @raycast.description What this command does
```

### Schema Version

Always use version 1:
```
# @raycast.schemaVersion 1
```

### Title

Display name in Raycast search:
```
# @raycast.title Open Project
```

### Mode

How output is displayed:

| Mode | Behavior |
|------|----------|
| `compact` | Shows last output line in toast notification |
| `silent` | Shows last line in HUD after Raycast closes |
| `fullOutput` | Shows all output in terminal-like view |
| `inline` | Shows first line in command item (dashboard widget) |

## Optional Metadata

### Package Name

Groups commands together (auto-inferred from directory if omitted):
```
# @raycast.packageName Developer Tools
```

### Icon

Emoji, file path, or HTTPS URL (64px PNG/JPEG recommended):
```
# @raycast.icon 🚀
# @raycast.icon ./icon.png
# @raycast.icon https://example.com/icon.png
```

Dark mode variant:
```
# @raycast.iconDark ./icon-dark.png
```

### Description

Shown in command details:
```
# @raycast.description Opens the current project in VS Code
```

### Author Info

```
# @raycast.author Your Name
# @raycast.authorURL https://github.com/username
```

### Confirmation Dialog

For destructive operations:
```
# @raycast.needsConfirmation true
```

### Working Directory

Script execution path:
```
# @raycast.currentDirectoryPath ~/Projects
```

### Refresh Time (inline mode only)

Auto-refresh interval (minimum 10s):
```
# @raycast.refreshTime 1m
```

Valid formats: `10s`, `30s`, `1m`, `5m`, `1h`, `12h`, `1d`

## Arguments

Scripts support up to 3 arguments. Arguments are passed as positional variables (`$1`, `$2`, `$3` in bash).

### Basic Text Argument

```
# @raycast.argument1 { "type": "text", "placeholder": "Search query" }
```

### Optional Argument

```
# @raycast.argument2 { "type": "text", "placeholder": "Optional filter", "optional": true }
```

### Password (Masked Input)

```
# @raycast.argument1 { "type": "password", "placeholder": "API Key" }
```

### URL Encoded

Automatically URL-encodes the value:
```
# @raycast.argument1 { "type": "text", "placeholder": "Search term", "percentEncoded": true }
```

### Dropdown Selection

```
# @raycast.argument1 { "type": "dropdown", "placeholder": "Environment", "data": [{"title": "Production", "value": "prod"}, {"title": "Staging", "value": "stage"}, {"title": "Development", "value": "dev"}] }
```

## Output Modes Details

### compact

Best for quick confirmations:
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Copy UUID
# @raycast.mode compact

uuid=$(uuidgen)
echo "$uuid" | pbcopy
echo "Copied: $uuid"
```

### silent

Minimal notification after Raycast closes:
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Clear Downloads
# @raycast.mode silent
# @raycast.needsConfirmation true

rm -rf ~/Downloads/*
echo "Downloads cleared"
```

### fullOutput

Terminal-like view for detailed output:
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Git Status
# @raycast.mode fullOutput

git status
```

### inline

Dashboard widget with auto-refresh:
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title CPU Usage
# @raycast.mode inline
# @raycast.refreshTime 10s

top -l 1 | grep "CPU usage" | awk '{print $3}'
```

## ANSI Color Support

`inline` and `fullOutput` modes support ANSI colors:

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Colorful Output
# @raycast.mode fullOutput

echo -e "\033[32mSuccess\033[0m"  # Green
echo -e "\033[31mError\033[0m"    # Red
echo -e "\033[33mWarning\033[0m"  # Yellow
echo -e "\033[34mInfo\033[0m"     # Blue
```

## Error Handling

Non-zero exit codes trigger failure notifications:

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Check Service
# @raycast.mode compact

if ! curl -s http://localhost:3000/health > /dev/null; then
    echo "Service is down"
    exit 1
fi
echo "Service is healthy"
```

## Complete Examples

### Web Search with Arguments

```bash
#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Google Search
# @raycast.mode silent
# @raycast.icon 🔍
# @raycast.packageName Web
# @raycast.argument1 { "type": "text", "placeholder": "Search query", "percentEncoded": true }

open "https://www.google.com/search?q=$1"
```

### Python Script with API Call

```python
#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title Weather
# @raycast.mode inline
# @raycast.refreshTime 30m
# @raycast.icon 🌤️
# @raycast.packageName Utils
# @raycast.argument1 { "type": "text", "placeholder": "City", "optional": true }

import urllib.request
import json
import sys

city = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "Amsterdam"
url = f"https://wttr.in/{city}?format=%t"

try:
    with urllib.request.urlopen(url, timeout=5) as response:
        print(f"{city}: {response.read().decode().strip()}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

### Swift Script

```swift
#!/usr/bin/swift

// @raycast.schemaVersion 1
// @raycast.title System Info
// @raycast.mode fullOutput
// @raycast.icon 💻
// @raycast.packageName System

import Foundation

let process = ProcessInfo.processInfo
print("Host: \(process.hostName)")
print("OS: \(process.operatingSystemVersionString)")
print("Uptime: \(Int(process.systemUptime / 3600))h")
print("Memory: \(process.physicalMemory / 1_073_741_824)GB")
```

### AppleScript for macOS Control

```applescript
#!/usr/bin/osascript

# @raycast.schemaVersion 1
# @raycast.title Toggle Dark Mode
# @raycast.mode silent
# @raycast.icon 🌙
# @raycast.packageName System

tell application "System Events"
    tell appearance preferences
        set dark mode to not dark mode
    end tell
end tell

return "Dark mode toggled"
```

### Dropdown Selection

```bash
#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Open Project
# @raycast.mode silent
# @raycast.icon 📁
# @raycast.packageName Dev
# @raycast.argument1 { "type": "dropdown", "placeholder": "Project", "data": [{"title": "Frontend", "value": "~/Projects/frontend"}, {"title": "Backend", "value": "~/Projects/backend"}, {"title": "Mobile", "value": "~/Projects/mobile"}] }

cd "$1" && code .
```

### Clipboard Utility

```bash
#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Base64 Encode Clipboard
# @raycast.mode compact
# @raycast.icon 🔐
# @raycast.packageName Utils

content=$(pbpaste)
encoded=$(echo -n "$content" | base64)
echo -n "$encoded" | pbcopy
echo "Encoded and copied!"
```

## Installation

1. Create script file with proper extension
2. Add metadata comments at the top
3. Make executable: `chmod +x script.sh`
4. In Raycast: Add Script Directory → Select folder containing scripts

## Best Practices

- Run bash scripts through ShellCheck before use
- Use `#!/bin/bash -l` if you need login shell environment
- `/usr/local/bin` is automatically in `$PATH`
- Avoid scripts with excessive partial output in compact/silent/inline modes
- Use `zip -q` and similar quiet flags for verbose commands
- Keep inline mode scripts fast (they refresh periodically)
- Use `needsConfirmation` for destructive operations
- Test scripts in terminal before adding to Raycast

## File Naming

- Use descriptive hyphenated names: `git-status.sh`, `copy-uuid.py`
- Files with `.template.` need value configuration before use
- Group related scripts in subdirectories (becomes package name)

## Documentation

- [Script Commands Repository](https://github.com/raycast/script-commands)
- [Raycast Manual](https://manual.raycast.com/script-commands)
