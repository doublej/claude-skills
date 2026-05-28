---
name: tui-kit
description: "Node.js terminal apps: colors, menus, inputs, progress, screen buffers"
---

# Terminal-Kit

Full-featured Node.js terminal library (3.3k stars, MIT). No ncurses dependency.
Features: 256/24-bit colors, styles, key/mouse input, menus, input fields, progress bars, tables, spinners, screen buffers (32-bit compositing), image rendering, document model widgets.

## Setup

```js
const termkit = require('terminal-kit');
const term = termkit.terminal;
```

Always use `term.processExit()` instead of `process.exit()` to restore terminal state.

<quick_patterns>

### Styled Output
```js
term.bold.underline.red('styled text\n');
term.colorRgbHex('#ff6600', 'True color\n');
term("^rRed^ normal ^+bold^: ^[bg:blue]blue bg^:\n");  // markup syntax
```

### User Input
```js
term('Enter name: ');
const name = await term.inputField({ cancelable: true }).promise;

// With auto-complete
const cmd = await term.inputField({
    autoComplete: ['install', 'update', 'remove'],
    autoCompleteMenu: true,
    autoCompleteHint: true
}).promise;
```

### Yes/No
```js
term('Continue? [Y|n] ');
const yes = await term.yesOrNo({ yes: ['y', 'ENTER'], no: ['n'] }).promise;
```

### Menus
```js
// Horizontal
const { selectedIndex, selectedText } = await term.singleLineMenu(
    ['File', 'Edit', 'View', 'Help']
).promise;

// Vertical
const resp = await term.singleColumnMenu(
    ['Option A', 'Option B', 'Option C'],
    { cancelable: true }
).promise;

// Grid
const resp2 = await term.gridMenu(items).promise;
```

### Progress Bar
```js
const bar = term.progressBar({
    width: 80, title: 'Processing:', eta: true, percent: true
});
bar.update(0.5);  // 0-1 float
// Item mode: bar = term.progressBar({ items: 5 });
// bar.startItem('task1'); bar.itemDone('task1');
```

### Table
```js
term.table([
    ['Name', 'Role', 'Status'],
    ['Alice', 'Dev', 'Active'],
    ['Bob', 'Design', 'Away']
], {
    hasBorder: true, borderChars: 'lightRounded',
    borderAttr: { color: 'blue' },
    firstRowTextAttr: { bgColor: 'yellow' },
    width: 60, fit: true
});
```

### Keyboard/Mouse Input
```js
term.grabInput({ mouse: 'button' });
term.on('key', (name, matches, data) => {
    if (name === 'CTRL_C') { term.processExit(); }
});
term.on('mouse', (name, data) => { /* data.x, data.y */ });
```

### Fullscreen App
```js
term.fullscreen(true);
term.grabInput({ mouse: 'button' });
// ... app logic ...
term.fullscreen(false);
term.processExit();
```

</quick_patterns>

<key_concepts>

**Chainable styles**: `term.red.bold.bgBlue('text')` — order doesn't matter.

**Printf formatting**: `term.green("Name: %s, Age: %d\n", name, age)`.

**Markup**: `^r`red `^g`green `^b`blue `^+`bold `^_`underline `^:`reset. Background: `^#r`. Complex: `^[#ff6600]`, `^[bg:blue]`.

**Promises**: all interactive methods return an object with `.promise`. Use `await method().promise`.

**Events**: after `grabInput()`, term emits 'key', 'mouse', 'terminal', 'resize'.

**Modifiers**: `.str()` returns string instead of outputting. `.error()` writes to stderr. `.wrap()` enables word-wrapping. `.noFormat()` disables printf/markup.

</key_concepts>

<pitfalls>

1. **Process won't exit**: interactive methods open stdin. Call `term.grabInput(false)` or `term.processExit()`.
2. **Cursor visible in fullscreen**: use `term.hideCursor()` / `term.hideCursor(false)`.
3. **Broken terminal after crash**: terminal state not restored. Wrap in try/catch and call `term.processExit()`.
4. **inputField not showing**: ensure cursor is positioned first with `term()` output.
5. **Mouse coordinates**: (1,1) is upper-left corner, not (0,0).

</pitfalls>

<document_model>

For full terminal applications with multiple simultaneous widgets, use the document model.
All widgets require a Document parent. Use `term.createDocument()` for setup.

```js
term.clear();
const document = term.createDocument();
// Add widgets as children of document
document.focusNext();
```

Available widgets: Button, ColumnMenu, DropDownMenu, EditableTextBox, Form, LabeledInput, Layout, SelectList, SelectListMulti, Slider, Text, TextBox, TextTable, ToggleButton, Window, Border.

Key doc-model patterns (all in `references/design-patterns.md`):
- **Responsive layouts** — `Layout` with rows/columns, percent/fixed/auto sizing
- **Forms** — `Form` with text, select, multi-select, password, multiline inputs + buttons
- **Dropdown menus** — `DropDownMenu` with nested submenus and toggle items
- **Select/picker** — `SelectList` / `SelectListMulti` dropdown pickers
- **Popup windows** — `Window` with title bar, movable, scrollable, closable
- **Vertical menus** — `ColumnMenu` with `Border` shadow, pagination, markup
- **Text editor** — `EditableTextBox` with scroll, word wrap, syntax highlighting
- **Data tables** — `TextTable` with cell selection, dynamic updates, markup
- **Sliders** — `Slider` horizontal/vertical value picker
- **Search/filter** — `inputField` + custom async autoComplete for fuzzy search
- **Status bar** — cursor-positioned bottom bar with `saveCursor`/`restoreCursor`

</document_model>

<reference_files>

For detailed API signatures and all options, load these references as needed:

- `references/design-patterns.md` — **START HERE** — complete recipes for layouts, forms, popups, menus, search, tables, sliders, and app boilerplate
  - Search: `Layout`, `Form`, `DropDownMenu`, `SelectList`, `Window`, `ColumnMenu`, `EditableTextBox`, `TextTable`, `Slider`, `Search`, `Status Bar`
- `references/low-level-api.md` — colors, styles, cursor, screen editing, markup, events, global API
  - Search: `Foreground Colors`, `Background Colors`, `Cursor Movement`, `Screen Editing`, `Style Markup`, `Events`, `Global API`
- `references/high-level-api.md` — inputField, menus, progressBar, table, spinner, drawImage, yesOrNo, etc.
  - Search: `.inputField`, `.singleLineMenu`, `.singleColumnMenu`, `.gridMenu`, `.progressBar`, `.table`, `.spinner`, `.drawImage`, `.yesOrNo`, `.fileInput`, `.slowTyping`
- `references/screen-buffer.md` — ScreenBuffer for composited UIs, sprites, off-screen rendering
  - Search: `ScreenBuffer`, `.put()`, `.draw()`, `.fill()`, `Attribute Object`

</reference_files>
