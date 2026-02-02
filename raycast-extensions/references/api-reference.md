# Raycast API Reference

Detailed reference for Raycast API features: data fetching, preferences, storage, OAuth, and more.

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
        accessories={[{ icon: favorites?.includes("1") ? "star" : undefined }]}
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

## Development Commands

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
