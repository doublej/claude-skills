---
name: raycast
description: >
  Unified Raycast development skill. Use when:
  (1) building Raycast extensions with React/TypeScript UI (List, Form, Detail, Grid, ActionPanel), API integrations, preferences, storage, or OAuth;
  (2) creating script commands for macOS automation in Bash, Python, Swift, AppleScript, JavaScript, or Ruby;
  (3) generating importable snippet collections with text expansion, dynamic placeholders, and keyword triggers.
  Replaces raycast-extensions, raycast-scripts, raycast-snippets.
---

# Raycast Development Skill

Three branches. Pick the right one, or combine.

## Which Branch?

| Task | Branch |
|------|--------|
| Rich UI extension with React/TypeScript, API integrations, OAuth | [Extensions](#extensions) |
| Executable script commands for macOS automation | [Scripts](#scripts) |
| Text expansion snippets with dynamic placeholders | [Snippets](#snippets) |

---

## Extensions

Build Raycast extensions using React, TypeScript, and the @raycast/api package.

### When to Use

- Building extensions with rich UI (lists, forms, grids)
- Creating integrations with external APIs
- Adding preferences and persistent storage
- Building OAuth-authenticated extensions
- Creating complex multi-view workflows

### Quick Start

```bash
npm create raycast-extension@latest
```

### Project Structure

```
my-extension/
├── src/
│   ├── index.tsx          # Main command entry
│   └── other-command.tsx  # Additional commands
├── assets/                # Icons and images
├── package.json           # Extension manifest
└── tsconfig.json
```

### package.json Manifest

```json
{
  "name": "my-extension",
  "title": "My Extension",
  "description": "What this extension does",
  "icon": "extension-icon.png",
  "author": "your-name",
  "categories": ["Productivity"],
  "license": "MIT",
  "commands": [
    {
      "name": "index",
      "title": "Main Command",
      "description": "Primary command description",
      "mode": "view"
    }
  ],
  "dependencies": {
    "@raycast/api": "^1.83.0",
    "@raycast/utils": "^1.17.0"
  }
}
```

### Command Modes

| Mode | Use Case |
|------|----------|
| `view` | Interactive UI with React components |
| `no-view` | Background operations, opens other apps |
| `menu-bar` | Menu bar extra with dropdown |

#### View Command

```tsx
import { List } from "@raycast/api";

export default function Command() {
  return (
    <List>
      <List.Item title="Hello World" />
    </List>
  );
}
```

#### No-View Command

```tsx
import { showHUD, Clipboard } from "@raycast/api";

export default async function Command() {
  const uuid = crypto.randomUUID();
  await Clipboard.copy(uuid);
  await showHUD(`Copied: ${uuid}`);
}
```

#### Menu Bar Command

```tsx
import { MenuBarExtra } from "@raycast/api";

export default function Command() {
  return (
    <MenuBarExtra icon="icon.png" title="Status">
      <MenuBarExtra.Item title="Action" onAction={() => {}} />
    </MenuBarExtra>
  );
}
```

### Complete Extension Example

```tsx
import {
  List,
  ActionPanel,
  Action,
  Icon,
  showToast,
  Toast,
  getPreferenceValues,
} from "@raycast/api";
import { useFetch } from "@raycast/utils";
import { useState } from "react";

interface Repo {
  id: number;
  name: string;
  description: string;
  html_url: string;
  stargazers_count: number;
}

export default function Command() {
  const { username } = getPreferenceValues<{ username: string }>();
  const [searchText, setSearchText] = useState("");

  const { isLoading, data: repos, error } = useFetch<Repo[]>(
    `https://api.github.com/users/${username}/repos?sort=updated`
  );

  if (error) {
    showToast({ style: Toast.Style.Failure, title: "Failed to fetch repos" });
  }

  const filtered = repos?.filter((repo) =>
    repo.name.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <List
      isLoading={isLoading}
      searchBarPlaceholder="Filter repositories..."
      onSearchTextChange={setSearchText}
    >
      {filtered?.map((repo) => (
        <List.Item
          key={repo.id}
          icon={Icon.Book}
          title={repo.name}
          subtitle={repo.description}
          accessories={[{ text: `* ${repo.stargazers_count}` }]}
          actions={
            <ActionPanel>
              <Action.OpenInBrowser url={repo.html_url} />
              <Action.CopyToClipboard
                title="Copy URL"
                content={repo.html_url}
                shortcut={{ modifiers: ["cmd"], key: "c" }}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

### Extension Best Practices

- Use `isLoading` prop to show loading states
- Implement proper error handling with toasts
- Use `useCachedPromise` for data that can be cached
- Add keyboard shortcuts for common actions
- Use sections to organize long lists
- Follow Raycast design guidelines for consistency

### Development Commands

```bash
# Run in development
npm run dev

# Build
npm run build

# Lint
npm run lint
npm run fix-lint

# Publish
npm run publish
```

### Reference Files

- [Components Guide](references/components-guide.md) - List, Form, Detail, Grid, Actions
- [API Reference](references/api-reference.md) - Data fetching, preferences, storage, OAuth

---

## Scripts

Create Raycast script commands - executable scripts that integrate with the Raycast launcher on macOS.

### When to Use

- Building custom Raycast commands
- Creating macOS automation scripts
- Adding quick-access utilities to Raycast
- Building inline dashboard widgets
- Creating scripts with user input arguments

### Supported Languages

| Language | Extension | Shebang |
|----------|-----------|---------|
| Bash | `.sh` | `#!/bin/bash` |
| Python | `.py` | `#!/usr/bin/env python3` |
| Swift | `.swift` | `#!/usr/bin/swift` |
| AppleScript | `.applescript` | `#!/usr/bin/osascript` |
| JavaScript | `.js` | `#!/usr/bin/env node` |
| Ruby | `.rb` | `#!/usr/bin/env ruby` |

### Required Metadata

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

#### Schema Version

Always use version 1:
```
# @raycast.schemaVersion 1
```

#### Title

Display name in Raycast search:
```
# @raycast.title Open Project
```

#### Mode

How output is displayed:

| Mode | Behavior |
|------|----------|
| `compact` | Shows last output line in toast notification |
| `silent` | Shows last line in HUD after Raycast closes |
| `fullOutput` | Shows all output in terminal-like view |
| `inline` | Shows first line in command item (dashboard widget) |

### Optional Metadata

#### Package Name

Groups commands together (auto-inferred from directory if omitted):
```
# @raycast.packageName Developer Tools
```

#### Icon

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

#### Description

Shown in command details:
```
# @raycast.description Opens the current project in VS Code
```

#### Author Info

```
# @raycast.author Your Name
# @raycast.authorURL https://github.com/username
```

#### Confirmation Dialog

For destructive operations:
```
# @raycast.needsConfirmation true
```

#### Working Directory

Script execution path:
```
# @raycast.currentDirectoryPath ~/Projects
```

#### Refresh Time (inline mode only)

Auto-refresh interval (minimum 10s):
```
# @raycast.refreshTime 1m
```

Valid formats: `10s`, `30s`, `1m`, `5m`, `1h`, `12h`, `1d`

### Script Arguments

Scripts support up to 3 arguments. Arguments are passed as positional variables (`$1`, `$2`, `$3` in bash).

#### Basic Text Argument

```
# @raycast.argument1 { "type": "text", "placeholder": "Search query" }
```

#### Optional Argument

```
# @raycast.argument2 { "type": "text", "placeholder": "Optional filter", "optional": true }
```

#### Password (Masked Input)

```
# @raycast.argument1 { "type": "password", "placeholder": "API Key" }
```

#### URL Encoded

Automatically URL-encodes the value:
```
# @raycast.argument1 { "type": "text", "placeholder": "Search term", "percentEncoded": true }
```

#### Dropdown Selection

```
# @raycast.argument1 { "type": "dropdown", "placeholder": "Environment", "data": [{"title": "Production", "value": "prod"}, {"title": "Staging", "value": "stage"}, {"title": "Development", "value": "dev"}] }
```

### Output Modes Details

#### compact

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

#### silent

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

#### fullOutput

Terminal-like view for detailed output:
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Git Status
# @raycast.mode fullOutput

git status
```

#### inline

Dashboard widget with auto-refresh:
```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title CPU Usage
# @raycast.mode inline
# @raycast.refreshTime 10s

top -l 1 | grep "CPU usage" | awk '{print $3}'
```

### ANSI Color Support

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

### Script Error Handling

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

### Complete Script Examples

#### Web Search with Arguments

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

#### Python Script with API Call

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

#### Swift Script

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

#### AppleScript for macOS Control

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

#### Dropdown Selection

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

#### Clipboard Utility

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

### Script Installation

1. Create script file with proper extension
2. Add metadata comments at the top
3. Make executable: `chmod +x script.sh`
4. In Raycast: Add Script Directory -> Select folder containing scripts

### Script Best Practices

- Run bash scripts through ShellCheck before use
- Use `#!/bin/bash -l` if you need login shell environment
- `/usr/local/bin` is automatically in `$PATH`
- Avoid scripts with excessive partial output in compact/silent/inline modes
- Use `zip -q` and similar quiet flags for verbose commands
- Keep inline mode scripts fast (they refresh periodically)
- Use `needsConfirmation` for destructive operations
- Test scripts in terminal before adding to Raycast

### File Naming

- Use descriptive hyphenated names: `git-status.sh`, `copy-uuid.py`
- Files with `.template.` need value configuration before use
- Group related scripts in subdirectories (becomes package name)

---

## Snippets

Create importable snippet collections for Raycast's text expansion feature.

### When to Use

- Creating keyboard shortcuts and code snippets
- Building boilerplate expansions or text macros
- Generating importable JSON snippet files for Raycast

### JSON Output Format

```json
[
  {
    "name": "Console Log",
    "text": "console.log({cursor})",
    "keyword": "!clog"
  }
]
```

Fields:
- `name`: Display name in Raycast
- `text`: Content to expand (supports dynamic placeholders)
- `keyword`: Trigger prefix (optional, e.g., `!clog`, `@@`, `;;js`)

### Dynamic Placeholders

See [references/placeholders.md](references/placeholders.md) for full reference.

**Most useful for code:**
- `{cursor}` - Cursor position after expansion
- `{clipboard}` - Last copied text
- `{argument}` - Prompt for input (max 3)
- `{argument name="var"}` - Named/reusable argument

**Date/time:**
- `{date format="yyyy-MM-dd"}` - Custom format
- `{datetime}` - Full timestamp
- `{date offset="+1d"}` - Relative dates

### Code Snippet Patterns

#### Logging
```json
{"name": "Console Log", "text": "console.log({cursor})", "keyword": "!clog"}
{"name": "Console Log Variable", "text": "console.log('{clipboard}:', {clipboard})", "keyword": "!clogv"}
```

#### Functions
```json
{"name": "Arrow Function", "text": "const {argument name=\"fn\"} = ({argument name=\"params\"}) => {\n  {cursor}\n}", "keyword": "!afn"}
{"name": "Async Function", "text": "async function {argument}() {\n  {cursor}\n}", "keyword": "!afunc"}
```

#### React Hooks
```json
{"name": "useState", "text": "const [{argument name=\"state\"}, set{argument name=\"state\"}] = useState({cursor})", "keyword": "!us"}
{"name": "useEffect", "text": "useEffect(() => {\n  {cursor}\n}, [])", "keyword": "!ue"}
```

#### Comments/Headers
```json
{"name": "TODO", "text": "// TODO: {cursor}", "keyword": "!todo"}
{"name": "File Header", "text": "/**\n * {argument name=\"description\"}\n * @author {argument name=\"author\"}\n * Created: {date format=\"yyyy-MM-dd\"}\n */", "keyword": "!header"}
```

### Snippet Workflow

1. Gather requirements: what snippets does user need?
2. Build JSON array with appropriate keywords
3. Save as `.json` file
4. User imports via Raycast "Import Snippets" command

### Keyword Conventions

- `!` prefix for code: `!clog`, `!fn`, `!todo`
- `;;` prefix for language: `;;js`, `;;py`, `;;css`
- `@@` for personal info: `@@email`, `@@phone`
- `//` for comments: `//todo`, `//fix`

---

## Reference Files

- [Components Guide](references/components-guide.md) - List, Form, Detail, Grid, Actions
- [API Reference](references/api-reference.md) - Data fetching, preferences, storage, OAuth
- [Placeholders Reference](references/placeholders.md) - Dynamic placeholders for snippets

## Documentation

- [Raycast API Reference](https://developers.raycast.com/api-reference)
- [Raycast Utils](https://developers.raycast.com/utils-reference)
- [Extension Store](https://raycast.com/store)
- [Script Commands Repository](https://github.com/raycast/script-commands)
- [Raycast Manual](https://manual.raycast.com/script-commands)
