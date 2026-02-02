---
name: raycast-extensions
description: Build Raycast extensions with React and TypeScript. Covers project setup, components (List, Form, Detail, Grid, Action Panel), API usage, preferences, storage, OAuth, and publishing. Use when creating rich Raycast extensions with interactive UI, API integrations, or complex workflows.
---

# Raycast Extensions

Guide for building Raycast extensions using React, TypeScript, and the @raycast/api package.

## When to Use

- Building extensions with rich UI (lists, forms, grids)
- Creating integrations with external APIs
- Adding preferences and persistent storage
- Building OAuth-authenticated extensions
- Creating complex multi-view workflows

## Quick Start

### Create Extension

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

## Command Modes

| Mode | Use Case |
|------|----------|
| `view` | Interactive UI with React components |
| `no-view` | Background operations, opens other apps |
| `menu-bar` | Menu bar extra with dropdown |

### View Command

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

### No-View Command

```tsx
import { showHUD, Clipboard } from "@raycast/api";

export default async function Command() {
  const uuid = crypto.randomUUID();
  await Clipboard.copy(uuid);
  await showHUD(`Copied: ${uuid}`);
}
```

### Menu Bar Command

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

## Complete Example

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

## Best Practices

- Use `isLoading` prop to show loading states
- Implement proper error handling with toasts
- Use `useCachedPromise` for data that can be cached
- Add keyboard shortcuts for common actions
- Use sections to organize long lists
- Follow Raycast design guidelines for consistency

## Reference Files

- [Components Guide](references/components-guide.md) - List, Form, Detail, Grid, Actions
- [API Reference](references/api-reference.md) - Data fetching, preferences, storage, OAuth

## Documentation

- [Raycast API Reference](https://developers.raycast.com/api-reference)
- [Raycast Utils](https://developers.raycast.com/utils-reference)
- [Extension Store](https://raycast.com/store)
