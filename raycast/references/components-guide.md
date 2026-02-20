# Raycast Components Guide

Detailed reference for Raycast UI components.

## List

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

## Form

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

## Detail

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

## Grid

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
