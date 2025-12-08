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
  },
  "devDependencies": {
    "@raycast/eslint-config": "^1.0.11",
    "typescript": "^5.4.5"
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

## Core Components

### List

Primary component for displaying items:

```tsx
import { List, ActionPanel, Action, Icon } from "@raycast/api";
import { useState } from "react";

export default function Command() {
  const [items] = useState([
    { id: "1", title: "First", subtitle: "Item" },
    { id: "2", title: "Second", subtitle: "Item" },
  ]);

  return (
    <List searchBarPlaceholder="Search items...">
      {items.map((item) => (
        <List.Item
          key={item.id}
          icon={Icon.Document}
          title={item.title}
          subtitle={item.subtitle}
          accessories={[{ text: "Info" }]}
          actions={
            <ActionPanel>
              <Action.CopyToClipboard content={item.title} />
              <Action.OpenInBrowser url={`https://example.com/${item.id}`} />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

### List Sections

```tsx
<List>
  <List.Section title="Recent">
    <List.Item title="Item 1" />
  </List.Section>
  <List.Section title="Favorites">
    <List.Item title="Item 2" />
  </List.Section>
</List>
```

### List with Search Filtering

```tsx
import { List } from "@raycast/api";
import { useState, useMemo } from "react";

export default function Command() {
  const [searchText, setSearchText] = useState("");
  const items = ["Apple", "Banana", "Cherry"];

  const filtered = useMemo(
    () => items.filter((item) =>
      item.toLowerCase().includes(searchText.toLowerCase())
    ),
    [searchText]
  );

  return (
    <List onSearchTextChange={setSearchText}>
      {filtered.map((item) => (
        <List.Item key={item} title={item} />
      ))}
    </List>
  );
}
```

### Form

For user input:

```tsx
import { Form, ActionPanel, Action, showToast, Toast } from "@raycast/api";

interface FormValues {
  name: string;
  email: string;
  newsletter: boolean;
}

export default function Command() {
  async function handleSubmit(values: FormValues) {
    await showToast({
      style: Toast.Style.Success,
      title: "Submitted",
      message: `Name: ${values.name}`,
    });
  }

  return (
    <Form
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Submit" onSubmit={handleSubmit} />
        </ActionPanel>
      }
    >
      <Form.TextField id="name" title="Name" placeholder="Your name" />
      <Form.TextField id="email" title="Email" placeholder="email@example.com" />
      <Form.Checkbox id="newsletter" label="Subscribe to newsletter" />
      <Form.Dropdown id="country" title="Country">
        <Form.Dropdown.Item value="us" title="United States" />
        <Form.Dropdown.Item value="uk" title="United Kingdom" />
      </Form.Dropdown>
      <Form.TextArea id="bio" title="Bio" placeholder="Tell us about yourself" />
      <Form.DatePicker id="birthday" title="Birthday" />
      <Form.FilePicker id="avatar" title="Avatar" />
      <Form.PasswordField id="secret" title="API Key" />
    </Form>
  );
}
```

### Detail

Rich markdown content display:

```tsx
import { Detail, ActionPanel, Action } from "@raycast/api";

export default function Command() {
  const markdown = `
# Project Details

## Description
This is a **detailed** view with _markdown_ support.

## Features
- Feature 1
- Feature 2

\`\`\`typescript
const hello = "world";
\`\`\`
`;

  return (
    <Detail
      markdown={markdown}
      metadata={
        <Detail.Metadata>
          <Detail.Metadata.Label title="Status" text="Active" />
          <Detail.Metadata.Link
            title="Website"
            target="https://example.com"
            text="Visit"
          />
          <Detail.Metadata.TagList title="Tags">
            <Detail.Metadata.TagList.Item text="React" color="#61dafb" />
            <Detail.Metadata.TagList.Item text="TypeScript" color="#3178c6" />
          </Detail.Metadata.TagList>
          <Detail.Metadata.Separator />
          <Detail.Metadata.Label title="Created" text="2024-01-01" />
        </Detail.Metadata>
      }
      actions={
        <ActionPanel>
          <Action.CopyToClipboard content={markdown} />
        </ActionPanel>
      }
    />
  );
}
```

### Grid

Image-focused layout:

```tsx
import { Grid, ActionPanel, Action } from "@raycast/api";

export default function Command() {
  const images = [
    { id: "1", title: "Photo 1", url: "https://example.com/1.jpg" },
    { id: "2", title: "Photo 2", url: "https://example.com/2.jpg" },
  ];

  return (
    <Grid columns={4} inset={Grid.Inset.Medium}>
      {images.map((img) => (
        <Grid.Item
          key={img.id}
          content={img.url}
          title={img.title}
          actions={
            <ActionPanel>
              <Action.OpenInBrowser url={img.url} />
            </ActionPanel>
          }
        />
      ))}
    </Grid>
  );
}
```

## Actions

### Built-in Actions

```tsx
import { ActionPanel, Action, Icon } from "@raycast/api";

<ActionPanel>
  <ActionPanel.Section title="Primary">
    <Action.CopyToClipboard content="text" />
    <Action.OpenInBrowser url="https://example.com" />
    <Action.Open title="Open File" target="/path/to/file" />
    <Action.Paste content="paste this" />
    <Action.ShowInFinder path="/path/to/file" />
    <Action.Trash paths={["/path/to/file"]} />
    <Action.Push title="Details" target={<DetailView />} />
    <Action.Pop title="Back" />
  </ActionPanel.Section>
  <ActionPanel.Section title="Secondary">
    <Action
      title="Custom Action"
      icon={Icon.Star}
      shortcut={{ modifiers: ["cmd"], key: "s" }}
      onAction={() => console.log("Custom!")}
    />
  </ActionPanel.Section>
</ActionPanel>
```

### Navigation

```tsx
import { List, Action, ActionPanel } from "@raycast/api";
import { useState } from "react";

function DetailView({ item }: { item: string }) {
  return <Detail markdown={`# ${item}`} />;
}

export default function Command() {
  return (
    <List>
      <List.Item
        title="View Details"
        actions={
          <ActionPanel>
            <Action.Push title="Open" target={<DetailView item="Hello" />} />
          </ActionPanel>
        }
      />
    </List>
  );
}
```

## Data Fetching

### Using @raycast/utils

```tsx
import { List, Detail } from "@raycast/api";
import { useFetch } from "@raycast/utils";

interface Post {
  id: number;
  title: string;
  body: string;
}

export default function Command() {
  const { isLoading, data, error } = useFetch<Post[]>(
    "https://jsonplaceholder.typicode.com/posts"
  );

  if (error) {
    return <Detail markdown={`# Error\n${error.message}`} />;
  }

  return (
    <List isLoading={isLoading}>
      {data?.map((post) => (
        <List.Item key={post.id} title={post.title} subtitle={post.body} />
      ))}
    </List>
  );
}
```

### useCachedPromise

```tsx
import { List } from "@raycast/api";
import { useCachedPromise } from "@raycast/utils";

async function fetchData() {
  const response = await fetch("https://api.example.com/data");
  return response.json();
}

export default function Command() {
  const { isLoading, data, revalidate } = useCachedPromise(fetchData);

  return (
    <List isLoading={isLoading}>
      {data?.map((item) => (
        <List.Item key={item.id} title={item.name} />
      ))}
    </List>
  );
}
```

## Preferences

### Define in package.json

```json
{
  "preferences": [
    {
      "name": "apiKey",
      "type": "password",
      "required": true,
      "title": "API Key",
      "description": "Your API key"
    },
    {
      "name": "defaultView",
      "type": "dropdown",
      "required": false,
      "title": "Default View",
      "description": "Choose default view",
      "default": "list",
      "data": [
        { "title": "List", "value": "list" },
        { "title": "Grid", "value": "grid" }
      ]
    },
    {
      "name": "showDetails",
      "type": "checkbox",
      "required": false,
      "title": "Show Details",
      "label": "Show item details",
      "default": true
    }
  ]
}
```

### Use in Code

```tsx
import { getPreferenceValues } from "@raycast/api";

interface Preferences {
  apiKey: string;
  defaultView: "list" | "grid";
  showDetails: boolean;
}

export default function Command() {
  const preferences = getPreferenceValues<Preferences>();
  console.log(preferences.apiKey);
  return <List />;
}
```

### Command-Specific Preferences

```json
{
  "commands": [
    {
      "name": "search",
      "title": "Search",
      "mode": "view",
      "preferences": [
        {
          "name": "maxResults",
          "type": "textfield",
          "title": "Max Results",
          "default": "10"
        }
      ]
    }
  ]
}
```

## Storage

### LocalStorage

```tsx
import { LocalStorage } from "@raycast/api";

// Store value
await LocalStorage.setItem("key", "value");
await LocalStorage.setItem("data", JSON.stringify({ foo: "bar" }));

// Retrieve value
const value = await LocalStorage.getItem<string>("key");
const data = JSON.parse(await LocalStorage.getItem<string>("data") || "{}");

// Remove value
await LocalStorage.removeItem("key");

// Clear all
await LocalStorage.clear();

// Get all items
const allItems = await LocalStorage.allItems();
```

### useLocalStorage Hook

```tsx
import { List, ActionPanel, Action } from "@raycast/api";
import { useLocalStorage } from "@raycast/utils";

export default function Command() {
  const { value: favorites, setValue: setFavorites } = useLocalStorage<string[]>("favorites", []);

  const toggleFavorite = (id: string) => {
    const newFavorites = favorites?.includes(id)
      ? favorites.filter((f) => f !== id)
      : [...(favorites || []), id];
    setFavorites(newFavorites);
  };

  return (
    <List>
      <List.Item
        title="Item 1"
        accessories={[{ icon: favorites?.includes("1") ? "⭐" : undefined }]}
        actions={
          <ActionPanel>
            <Action title="Toggle Favorite" onAction={() => toggleFavorite("1")} />
          </ActionPanel>
        }
      />
    </List>
  );
}
```

## Toasts and HUD

```tsx
import { showToast, showHUD, Toast } from "@raycast/api";

// Simple toast
await showToast({ title: "Success!" });

// Styled toast
await showToast({
  style: Toast.Style.Success,
  title: "Completed",
  message: "Operation finished",
});

// Loading toast with update
const toast = await showToast({
  style: Toast.Style.Animated,
  title: "Processing...",
});
// ... do work
toast.style = Toast.Style.Success;
toast.title = "Done!";

// HUD (closes Raycast)
await showHUD("Copied to clipboard");
```

## Clipboard

```tsx
import { Clipboard } from "@raycast/api";

// Copy text
await Clipboard.copy("Hello World");

// Copy with transient (doesn't add to history)
await Clipboard.copy("secret", { transient: true });

// Read clipboard
const text = await Clipboard.readText();

// Paste
await Clipboard.paste("Pasted text");
```

## OAuth

### Setup OAuth Provider

```tsx
import { OAuth } from "@raycast/api";

const client = new OAuth.PKCEClient({
  redirectMethod: OAuth.RedirectMethod.Web,
  providerName: "GitHub",
  providerIcon: "github-icon.png",
  providerId: "github",
  description: "Connect your GitHub account",
});

export async function authorize(): Promise<string> {
  const tokenSet = await client.getTokens();
  if (tokenSet?.accessToken && !tokenSet.isExpired()) {
    return tokenSet.accessToken;
  }

  const authRequest = await client.authorizationRequest({
    endpoint: "https://github.com/login/oauth/authorize",
    clientId: "your-client-id",
    scope: "repo user",
  });

  const { authorizationCode } = await client.authorize(authRequest);

  const tokens = await exchangeCodeForTokens(authorizationCode);
  await client.setTokens(tokens);

  return tokens.access_token;
}
```

## Keyboard Shortcuts

```tsx
<Action
  title="Refresh"
  shortcut={{ modifiers: ["cmd"], key: "r" }}
  onAction={() => revalidate()}
/>

<Action
  title="Delete"
  shortcut={{ modifiers: ["cmd", "shift"], key: "backspace" }}
  onAction={() => deleteItem()}
/>
```

Common shortcuts:
- `cmd + enter` - Primary action
- `cmd + k` - Secondary action panel
- `cmd + shift + c` - Copy
- `cmd + o` - Open
- `cmd + r` - Refresh

## Icons

```tsx
import { Icon, Color } from "@raycast/api";

// Built-in icons
<List.Item icon={Icon.Star} title="Favorite" />
<List.Item icon={Icon.Document} title="File" />
<List.Item icon={Icon.Globe} title="Web" />

// Colored icon
<List.Item
  icon={{ source: Icon.Circle, tintColor: Color.Green }}
  title="Active"
/>

// Custom icon from assets
<List.Item icon="custom-icon.png" title="Custom" />

// Image from URL
<List.Item icon="https://example.com/icon.png" title="Remote" />
```

## Arguments

### Define in package.json

```json
{
  "commands": [
    {
      "name": "search",
      "title": "Search",
      "mode": "view",
      "arguments": [
        {
          "name": "query",
          "placeholder": "Search term",
          "type": "text",
          "required": true
        },
        {
          "name": "category",
          "placeholder": "Category",
          "type": "dropdown",
          "required": false,
          "data": [
            { "title": "All", "value": "all" },
            { "title": "Code", "value": "code" }
          ]
        }
      ]
    }
  ]
}
```

### Use in Command

```tsx
import { LaunchProps } from "@raycast/api";

interface Arguments {
  query: string;
  category?: string;
}

export default function Command(props: LaunchProps<{ arguments: Arguments }>) {
  const { query, category } = props.arguments;
  return <List searchBarPlaceholder={`Searching for: ${query}`} />;
}
```

## Environment

```tsx
import { environment } from "@raycast/api";

// Check if development mode
if (environment.isDevelopment) {
  console.log("Dev mode");
}

// Get extension info
console.log(environment.extensionName);
console.log(environment.commandName);

// Paths
console.log(environment.assetsPath);
console.log(environment.supportPath);
```

## Development

### Run in Development

```bash
npm run dev
```

### Build

```bash
npm run build
```

### Lint

```bash
npm run lint
npm run fix-lint
```

### Publish

```bash
npm run publish
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

interface Preferences {
  username: string;
}

export default function Command() {
  const { username } = getPreferenceValues<Preferences>();
  const [searchText, setSearchText] = useState("");

  const { isLoading, data: repos, error } = useFetch<Repo[]>(
    `https://api.github.com/users/${username}/repos?sort=updated`,
    {
      keepPreviousData: true,
    }
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
          accessories={[{ text: `⭐ ${repo.stargazers_count}` }]}
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
- Provide meaningful accessories and subtitles
- Test with both light and dark themes
- Keep UI responsive with proper async handling
- Use `@raycast/utils` hooks when possible
- Follow Raycast design guidelines for consistency

## Documentation

- [Raycast API Reference](https://developers.raycast.com/api-reference)
- [Raycast Utils](https://developers.raycast.com/utils-reference)
- [Extension Store](https://raycast.com/store)
- [Community Extensions](https://github.com/raycast/extensions)
