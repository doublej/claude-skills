# Terminal-Kit Design Patterns

Recipes for common TUI patterns using the document model and inline mode.

## App Boilerplate (Document Model)

Every document-model app follows this skeleton:

```js
const termkit = require('terminal-kit');
const term = termkit.terminal;

term.clear();
const document = term.createDocument();

// ... add widgets here ...

document.focusNext(); // or document.giveFocusTo(widget)

term.on('key', key => {
    if (key === 'CTRL_C') {
        term.grabInput(false);
        term.hideCursor(false);
        term.styleReset();
        term.clear();
        process.exit();
    }
});
```

## Responsive Column Layout

Use `Layout` for multi-pane UIs that resize with the terminal. Supports rows, columns, percent/fixed/auto widths.

```js
const layout = new termkit.Layout({
    parent: document,
    boxChars: 'double',  // 'single', 'double', 'rounded', 'dotted'
    layout: {
        id: 'main',
        y: 2,
        widthPercent: 100,
        heightPercent: 80,
        rows: [
            {
                id: 'top',
                heightPercent: 70,
                columns: [
                    { id: 'sidebar', widthPercent: 25 },
                    { id: 'content' },         // auto-sized
                    { id: 'inspector', width: 30 }  // fixed width
                ]
            },
            {
                id: 'bottom',
                columns: [
                    { id: 'statusBar' }
                ]
            }
        ]
    }
});

// Access panes via document.elements
new termkit.Text({
    parent: document.elements.sidebar,
    content: 'Sidebar content',
    attr: { color: 'cyan' }
});

new termkit.Text({
    parent: document.elements.content,
    content: 'Main content area'
});
```

## Form with Multiple Input Types

`Form` groups LabeledInput fields with text, select, multi-select, and multiline.

```js
const form = new termkit.Form({
    parent: document,
    x: 10, y: 3, width: 50,
    inputs: [
        { key: 'name', label: 'Name: ' },
        { key: 'email', label: 'Email: ', content: 'user@example.com' },
        { key: 'password', label: 'Password: ', hiddenContent: true },
        {
            key: 'role', label: 'Role: ', type: 'select', value: 'dev',
            items: [
                { content: 'Developer', value: 'dev' },
                { content: 'Designer', value: 'design' },
                { content: 'Manager', value: 'mgr' }
            ]
        },
        {
            key: 'skills', label: 'Skills: ', type: 'selectMulti',
            items: [
                { content: 'JavaScript', key: 'js' },
                { content: 'Python', key: 'py' },
                { content: 'Go', key: 'go' }
            ]
        },
        {
            key: 'bio', label: 'Bio: ',
            height: 4, scrollable: true, vScrollBar: true
        }
    ],
    buttons: [
        { content: '<Submit>', value: 'submit' },
        { content: '<Cancel>', value: 'cancel' }
    ]
});

form.on('submit', (data) => {
    // data = { name: '...', email: '...', role: 'dev', skills: {...}, bio: '...' }
});
document.giveFocusTo(form);
```

## Dropdown Menu Bar

Classic File/Edit/View menu bar with submenus and toggle items.

```js
const menu = new termkit.DropDownMenu({
    parent: document,
    x: 0, y: 0,
    clearColumnMenuOnSubmit: true,
    items: [
        {
            content: 'File', value: 'file',
            items: [
                { content: 'New', value: 'new' },
                { content: 'Open', value: 'open' },
                { content: 'Save', value: 'save' },
                { content: 'Exit', value: 'exit' }
            ]
        },
        {
            content: 'Edit', value: 'edit',
            items: [
                { content: 'Undo', value: 'undo' },
                { content: 'Redo', value: 'redo' },
                { content: 'Auto-indent', key: 'autoIndent', type: 'toggle' },
                { content: 'Word wrap', key: 'wordWrap', type: 'toggle' }
            ]
        },
        {
            content: 'Help', value: 'help',
            items: [
                { content: 'About', value: 'about' }
            ]
        }
    ],
    value: { autoIndent: true }  // initial toggle states
});

menu.on('blinked', (value, action) => { /* handle menu selection */ });
document.giveFocusTo(menu);
```

## Select List (Dropdown/Picker)

Single-select dropdown that expands on focus.

```js
const select = new termkit.SelectList({
    parent: document,
    x: 10, y: 5,
    master: { content: 'Status' },  // collapsed label
    items: [
        { content: 'Todo', value: 'todo' },
        { content: 'In Progress', value: 'in-progress' },
        { content: 'Done', value: 'done' }
    ]
});

select.on('submit', (value) => { /* value = 'todo' | 'in-progress' | 'done' */ });
// Read current: select.getValue()
```

For multi-select, use `SelectListMulti` with the same API.

## Popup Window

Movable, scrollable overlay window with title bar.

```js
const popup = new termkit.Window({
    parent: document,
    x: 15, y: 5,
    width: 50, height: 15,
    inputHeight: 40,  // virtual height for scrolling
    title: "^c^+Details^:",
    titleHasMarkup: true,
    movable: true,
    scrollable: true,
    vScrollBar: true
});

new termkit.Text({
    parent: popup,
    content: ['Line 1', 'Line 2', '...many more lines...'],
    attr: { color: 'green' }
});

// Close popup: popup.destroy()
// Show/hide: popup.show() / popup.hide()
```

## Vertical Menu with Border/Shadow

Column menu with styled border and shadow effect.

```js
const menu = new termkit.ColumnMenu({
    parent: document,
    x: 10, y: 5,
    width: 25,
    pageMaxHeight: 8,  // paginate if more items
    multiLineItems: true,
    items: [
        { content: 'Option 1', value: 'opt1' },
        { content: 'Option 2', value: 'opt2' },
        { content: 'Disabled', value: 'dis', disabled: true },
        { content: '^[fg:*royal-blue]Styled^:', markup: true, value: 'styled' }
    ]
});

// Wrap with shadow border
new termkit.Border({ parent: menu, shadow: true });

menu.on('submit', (value) => { /* ... */ });
menu.focusValue('opt1');  // pre-select by value
```

## Editable Text Area (Code Editor)

Multi-line text editor with scrolling and optional syntax highlighting.

```js
const editor = new termkit.EditableTextBox({
    parent: document,
    content: 'initial content',
    attr: { bgColor: 'black' },
    x: 5, y: 3,
    width: 60, height: 20,
    scrollable: true,
    vScrollBar: true,
    wordWrap: true
    // stateMachine: sm  // optional, for syntax highlighting
});

document.giveFocusTo(editor);

// Get content: editor.getContent()
// Set content: editor.setContent('new text')
```

## Data Table (Interactive)

Table widget with cell selection, markup, and dynamic updates.

```js
const table = new termkit.TextTable({
    parent: document,
    cellContents: [
        ['Name', 'Role', 'Status'],
        ['Alice', 'Dev', '^gActive^:'],
        ['Bob', 'Design', '^rAway^:']
    ],
    contentHasMarkup: true,
    x: 0, y: 2,
    width: 60, height: 15,
    borderAttr: { color: 'blue' },
    firstRowTextAttr: { bgColor: 'gray' },
    firstColumnTextAttr: { bgColor: 'blue' },
    selectedTextAttr: { bgColor: 'blue' },
    selectable: 'cell',  // 'cell' | 'row' | 'column'
    fit: true
});

// Dynamic updates:
// table.setCellContent(col, row, 'New value')
// table.setRowAttr(row, { bgColor: 'cyan' })
// table.resetRowAttr(row)
```

## Slider (Value Picker)

Horizontal or vertical slider for numeric values.

```js
const slider = new termkit.Slider({
    parent: document,
    x: 5, y: 3,
    width: 30,          // horizontal
    // isVertical: true, height: 10  // for vertical
});

slider.on('slideStep', d => {
    slider.setSlideRate(slider.getSlideRate() + 0.1 * d);
});

// Get value: slider.getSlideRate()  (0-1)
// Set value: slider.setSlideRate(0.5)
```

## Search/Filter Pattern (Inline Mode)

Terminal-kit doesn't have a built-in search widget, but combine inputField with autoComplete:

```js
const items = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig'];

term('Search: ');
const result = await term.inputField({
    autoComplete: items,
    autoCompleteMenu: true,
    autoCompleteHint: true
}).promise;
```

For custom fuzzy search, use an async auto-completer:

```js
const fuzzySearch = async (input) => {
    const pattern = input.toLowerCase();
    const matches = allItems.filter(item =>
        item.toLowerCase().includes(pattern)
    );
    return matches.length ? matches : input;
};

const result = await term.inputField({
    autoComplete: fuzzySearch,
    autoCompleteMenu: true,
    autoCompleteHint: true
}).promise;
```

## Status Bar Pattern

Fixed bottom-line status bar using cursor positioning.

```js
function updateStatusBar(message) {
    term.saveCursor();
    term.moveTo(1, term.height);
    term.bgWhite.black.eraseLine(
        ' %s | %dx%d | %s ',
        'MyApp', term.width, term.height, message
    );
    term.restoreCursor();
}

term.on('resize', (w, h) => updateStatusBar('Resized'));
```

## Confirmation Dialog Pattern

Inline yes/no with custom labels and exit handling.

```js
async function confirm(prompt, defaultYes = true) {
    term(prompt + (defaultYes ? ' [Y|n] ' : ' [y|N] '));
    const yes = defaultYes ? ['y', 'ENTER'] : ['y'];
    const no = defaultYes ? ['n'] : ['n', 'ENTER'];
    return await term.yesOrNo({ yes, no }).promise;
}

if (await confirm('Delete file?', false)) { /* proceed */ }
```

## Element Properties Cheatsheet

All doc-model widgets share these `Element` options:
- `parent`: parent Element (required)
- `x`, `y`: position relative to parent
- `width`, `height`: dimensions
- `autoWidth`, `autoHeight`: 0-1 proportion of parent (true = 100%)
- `zIndex` / `z`: stacking order
- `content`, `contentHasMarkup`: text content
- `hidden`, `disabled`: visibility/interactivity
- `label`, `key`, `value`: identification
- `noDraw`: skip initial draw

Element methods: `.destroy()`, `.show()`, `.hide()`, `.setContent(str, hasMarkup)`, `.topZ()`, `.bottomZ()`, `.draw()`, `.outerDraw()`

Container adds: `.scrollTo(x,y)`, `.scroll(dx,dy)`, `.scrollToTop()`, `.scrollToBottom()`, `.move(dx,dy)`, `.moveTo(x,y)`, `.resize(rect)`, `scrollable`, `hasVScrollBar`, `hasHScrollBar`, `movable`
