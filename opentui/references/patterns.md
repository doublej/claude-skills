# OpenTUI Patterns & Examples

## Renderer Setup

### Basic Setup

```typescript
import { createCliRenderer } from "@opentui/core"

const renderer = await createCliRenderer()

// Add components to root
renderer.root.add(myComponent)

// Start the render loop
renderer.start()

// Stop when done
renderer.stop()
```

### With Console Overlay

```typescript
import { createCliRenderer, ConsolePosition } from "@opentui/core"

const renderer = await createCliRenderer({
  consoleOptions: {
    position: ConsolePosition.BOTTOM,
    sizePercent: 30,
    colorInfo: "#00FFFF",
    colorWarn: "#FFFF00",
    colorError: "#FF0000",
    startInDebugMode: false,
  },
})

// Toggle console: renderer.console.toggle()
// Resize: +/- keys
// Scroll: arrow keys
```

---

## Keyboard Input

### Event Handling

```typescript
renderer.keyInput.on("keypress", (key) => {
  console.log("Key:", key.name)
  console.log("Ctrl:", key.ctrl)
  console.log("Shift:", key.shift)
  console.log("Meta:", key.meta)

  // Common patterns
  if (key.name === "escape") renderer.stop()
  if (key.ctrl && key.name === "c") process.exit(0)
  if (key.name === "tab") focusNext()
})
```

### Paste Events

```typescript
renderer.keyInput.on("paste", (text) => {
  console.log("Pasted:", text)
})
```

---

## Color System (RGBA)

Colors use normalized floats internally (0.0-1.0). Multiple creation methods:

```typescript
import { RGBA, parseColor } from "@opentui/core"

// From integers (0-255)
const red = RGBA.fromInts(255, 0, 0, 255)

// From floats (0.0-1.0)
const green = RGBA.fromValues(0.0, 1.0, 0.0, 1.0)

// From hex string
const blue = RGBA.fromHex("#0000FF")

// Using parseColor utility (accepts RGBA or string)
const color = parseColor("#FF00FF")
```

---

## Imperative vs Declarative

### Imperative (Direct Manipulation)

```typescript
// Create renderables directly with renderer context
const input = new Input(renderer, {
  id: "username",
  placeholder: "Username",
})

const box = new Box(renderer, {
  id: "form",
  border: "single",
})

box.add(input)
renderer.root.add(box)

// Access nested: need getRenderable()
const nestedInput = box.getRenderable("username")
nestedInput?.focus()
```

### Declarative (Constructs)

```typescript
// Define as lightweight VNode graph
function LabeledInput(label: string, id: string) {
  return Box({
    border: "single",
    children: [
      Text({ content: label }),
      Input({ id, placeholder: "Enter value..." })
        .delegate("focus", id), // Route focus() to this input
    ],
  })
}

// Instantiate later
const form = LabeledInput("Username:", "username-input")
const instance = form.instantiate(renderer)

// Direct access via delegation
instance.focus() // Calls focus on the delegated input
```

---

## Focus Management

```typescript
// Components must be focused to receive input
input.focus()
select.focus()
tabs.focus()

// Check focus state
if (input.isFocused()) { ... }

// Blur (unfocus)
input.blur()

// Focus cycling
const focusables = [input1, input2, select1]
let focusIndex = 0

function focusNext() {
  focusables[focusIndex].blur()
  focusIndex = (focusIndex + 1) % focusables.length
  focusables[focusIndex].focus()
}
```

---

## Layout with Yoga

OpenTUI uses Yoga (Facebook's flexbox implementation) for layout.

### Flex Container

```typescript
const container = new GroupRenderable(renderer, {
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
  width: "100%",
  height: 10,
  padding: 1,
  gap: 2,
})
```

### Common Layout Patterns

```typescript
// Centered content
{
  justifyContent: "center",
  alignItems: "center",
}

// Sidebar layout
{
  flexDirection: "row",
  children: [
    sidebar, // fixed width
    content, // flex: 1
  ],
}

// Stacked form
{
  flexDirection: "column",
  gap: 1,
  children: [field1, field2, field3],
}
```

---

## Event Handling

### Component Events

```typescript
// Input change (on Enter)
input.on("CHANGE", (value) => {
  console.log("New value:", value)
})

// Select/TabSelect selection
select.on("SELECT", (index, value) => {
  console.log("Selected:", index, value)
})
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTUI_USE_ALTERNATE_SCREEN` | `true` | Use alternate screen buffer |
| `OTUI_USE_CONSOLE` | `true` | Capture console output |
| `SHOW_CONSOLE` | `false` | Show console on startup |
| `OTUI_DEBUG_FFI` | `false` | Debug FFI bindings |
| `OTUI_NO_NATIVE_RENDER` | `false` | Disable native rendering |

---

## Complete Example: Simple Form

```typescript
import {
  createCliRenderer,
  Box,
  TextRenderable,
  Input,
  Select,
  t, bold
} from "@opentui/core"

async function main() {
  const renderer = await createCliRenderer()

  // Form container
  const form = new Box(renderer, {
    id: "form",
    title: "User Registration",
    border: "rounded",
    width: 50,
    height: 15,
    padding: 1,
    position: "absolute",
    left: 5,
    top: 2,
  })

  // Username input
  const usernameLabel = new TextRenderable(renderer, {
    content: t`${bold("Username:")}`,
  })
  const usernameInput = new Input(renderer, {
    id: "username",
    placeholder: "Enter username",
    width: 30,
  })

  // Role select
  const roleLabel = new TextRenderable(renderer, {
    content: t`${bold("Role:")}`,
  })
  const roleSelect = new Select(renderer, {
    id: "role",
    options: ["Admin", "User", "Guest"],
    width: 30,
  })

  form.add(usernameLabel)
  form.add(usernameInput)
  form.add(roleLabel)
  form.add(roleSelect)
  renderer.root.add(form)

  // Focus first input
  usernameInput.focus()

  // Handle keyboard
  renderer.keyInput.on("keypress", (key) => {
    if (key.name === "escape") renderer.stop()
    if (key.name === "tab") {
      if (usernameInput.isFocused()) {
        usernameInput.blur()
        roleSelect.focus()
      } else {
        roleSelect.blur()
        usernameInput.focus()
      }
    }
  })

  renderer.start()
}

main()
```
