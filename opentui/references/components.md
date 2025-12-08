# OpenTUI Components Reference

## TextRenderable

Displays styled text with color and attribute support.

### Props
| Prop | Type | Description |
|------|------|-------------|
| `content` | `string` | Text content or template literal |
| `fg` | `string` | Foreground color (hex/name) |
| `bg` | `string` | Background color |
| `position` | `"absolute" \| "relative"` | Layout mode |
| `left`, `top`, `right`, `bottom` | `number` | Position offsets |

### Styled Text

Use template literals with style functions:

```typescript
import { t, bold, italic, underline, fg, bg, dim, strikethrough } from "@opentui/core"

const text = new TextRenderable(renderer, {
  content: t`${bold("Bold")} ${italic("Italic")} ${fg("#FF0000")("Red")} ${bg("#0000FF")("Blue BG")}`,
})

// Combine styles
const combined = t`${bold(fg("#00FF00")("Green Bold"))}`
```

---

## Box

Container with borders, backgrounds, and child layout.

### Props
| Prop | Type | Description |
|------|------|-------------|
| `title` | `string` | Title displayed in border |
| `border` | `"single" \| "double" \| "rounded" \| "bold"` | Border style |
| `bg` | `string` | Background color |
| `width`, `height` | `number \| string` | Dimensions |
| `padding` | `number` | Inner padding |
| `flexDirection` | `"row" \| "column"` | Child layout |

```typescript
const box = new Box(renderer, {
  id: "panel",
  title: "My Panel",
  border: "rounded",
  width: 50,
  height: 20,
  bg: "#1a1a2e",
  padding: 1,
})

box.add(childRenderable)
```

---

## Input

Text input field with cursor control and focus states.

### Props
| Prop | Type | Description |
|------|------|-------------|
| `placeholder` | `string` | Placeholder text |
| `value` | `string` | Initial value |
| `width` | `number` | Field width |
| `fg`, `bg` | `string` | Colors |
| `focusFg`, `focusBg` | `string` | Colors when focused |

### Usage

```typescript
const input = new Input(renderer, {
  id: "username",
  placeholder: "Enter username...",
  width: 30,
  fg: "#FFFFFF",
  bg: "#333333",
  focusBg: "#444444",
})

input.focus() // Must be focused to receive input

input.on("CHANGE", (value) => {
  console.log("Value:", value)
})
```

---

## Select

Vertical list selection component.

### Props
| Prop | Type | Description |
|------|------|-------------|
| `options` | `string[]` | Selection options |
| `selectedIndex` | `number` | Initial selection |
| `width` | `number` | Component width |
| `fg`, `bg` | `string` | Normal colors |
| `selectedFg`, `selectedBg` | `string` | Selected item colors |

### Navigation
- `up` / `k` - Move up
- `down` / `j` - Move down
- `enter` - Select

```typescript
const select = new Select(renderer, {
  id: "menu",
  options: ["Option 1", "Option 2", "Option 3"],
  selectedIndex: 0,
  width: 20,
  selectedBg: "#00FF00",
})

select.focus()

select.on("SELECT", (index, value) => {
  console.log("Selected:", value)
})
```

---

## TabSelect

Horizontal tab-based selection with descriptions.

### Props
| Prop | Type | Description |
|------|------|-------------|
| `tabs` | `{ label: string, description?: string }[]` | Tab items |
| `selectedIndex` | `number` | Initial selection |
| `width` | `number` | Component width |

### Navigation
- `left` / `[` - Previous tab
- `right` / `]` - Next tab
- `enter` - Select

```typescript
const tabs = new TabSelect(renderer, {
  id: "tabs",
  tabs: [
    { label: "General", description: "General settings" },
    { label: "Advanced", description: "Advanced options" },
    { label: "About", description: "About this app" },
  ],
  selectedIndex: 0,
})

tabs.focus()

tabs.on("SELECT", (index, tab) => {
  console.log("Selected tab:", tab.label)
})
```

---

## ASCIIFont

Renders text as ASCII art using large character fonts.

```typescript
const title = new ASCIIFont(renderer, {
  id: "title",
  text: "HELLO",
  font: "standard", // or other figlet fonts
})
```

---

## FrameBuffer

Low-level rendering surface for custom graphics.

### Methods
| Method | Description |
|--------|-------------|
| `setCell(x, y, char, fg, bg)` | Set a single cell |
| `setCellWithAlphaBlending(...)` | Set cell with transparency |
| `drawText(x, y, text, fg, bg)` | Draw text string |
| `fillRect(x, y, w, h, char, fg, bg)` | Fill rectangle |
| `drawFrameBuffer(x, y, buffer)` | Composite another buffer |

```typescript
const buffer = new FrameBuffer(renderer, {
  id: "canvas",
  width: 80,
  height: 24,
})

// Draw a box
buffer.fillRect(0, 0, 10, 5, " ", "#FFFFFF", "#0000FF")
buffer.drawText(2, 2, "Hello", "#FFFFFF", "#0000FF")
```

---

## GroupRenderable

Flex-based layout container for organizing children.

```typescript
const group = new GroupRenderable(renderer, {
  id: "layout",
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
  width: "100%",
  height: 3,
})

group.add(leftComponent)
group.add(rightComponent)
```

### Flex Props
All Yoga layout properties are supported:
- `flexDirection`, `flexWrap`
- `justifyContent`, `alignItems`, `alignContent`
- `flex`, `flexGrow`, `flexShrink`
- `gap`, `rowGap`, `columnGap`
