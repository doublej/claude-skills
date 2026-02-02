# Theatre.js Studio Reference

## Initialization

```typescript
import studio from '@theatre/studio'

// Dev-only initialization
if (import.meta.env.DEV) {
  studio.initialize()
}

// With extensions
import extension from '@theatre/r3f/dist/extension'
studio.initialize()
studio.extend(extension)
```

## UI Panels

| Panel | Description |
|-------|-------------|
| **Outline** | Project/sheet/object hierarchy |
| **Details** | Props for selected object |
| **Sequence Editor** | Timeline with keyframes (Dope Sheet) |
| **Toolbar** | Extension buttons and switches |
| **Extension Panes** | Custom windows from extensions |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt/Option + \` | Toggle Studio visibility |
| `Space` | Play/pause sequence |
| `Shift + drag` | Create focus range in timeline |
| `Right-click prop` | Sequence prop |
| `Click between keyframes` | Open easing editor |
| `Delete` | Delete selected keyframes |

## Mouse Controls

| Action | Description |
|--------|-------------|
| Left-click keyframe | Select and edit value |
| Right-click keyframe | Context menu (delete, copy) |
| Drag keyframe | Move in time |
| Shift + drag in timeline | Create focus range |
| Click diamond icon | Add keyframe |

## Studio API

### UI Control

```typescript
// Hide/show studio
studio.ui.hide()
studio.ui.restore()

// Check visibility
if (studio.ui.isHidden) { ... }
```

### Selection

```typescript
// Get current selection
const selected = studio.selection

// Listen to selection changes
studio.onSelectionChange((newSelection) => {
  console.log('Selected:', newSelection)
})

// Set selection programmatically
studio.setSelection([obj, sheet])
```

### Transactions (Atomic Changes)

```typescript
// Single undo level for multiple changes
studio.transaction(({ set }) => {
  set(obj.props.x, 10)
  set(obj.props.y, 20)
})
// Rolls back all changes if error occurs
```

### Scrubs (Temporary Changes)

```typescript
const scrub = studio.scrub()

// Make temporary changes
scrub.capture(({ set }) => {
  set(obj.props.x, 10)
})

// Commit to history
scrub.commit()

// Or discard
scrub.discard()

// Or reset and try again
scrub.reset()
```

### State Export

```typescript
// Get project state as JSON
const state = studio.createContentOfSaveFile('My Project')
console.log(JSON.stringify(state, null, 2))
```

## Creating Extensions

```typescript
const myExtension = {
  id: 'my-extension',

  toolbars: {
    global(set, studio) {
      // Add button
      set([{
        type: 'Icon',
        title: 'My Button',
        svgSource: '🔧',
        onClick: () => console.log('clicked')
      }])

      // Add switch
      set([{
        type: 'Switch',
        value: 'off',
        onChange: (value) => console.log(value),
        options: [
          { value: 'off', label: 'Off', svgSource: '⭕' },
          { value: 'on', label: 'On', svgSource: '✅' }
        ]
      }])
    }
  },

  panes: [{
    class: 'my-pane',
    mount({ paneId, node }) {
      node.innerHTML = '<h1>Custom Pane</h1>'
      return () => { /* cleanup */ }
    }
  }]
}

// Register BEFORE initialize
studio.extend(myExtension)
studio.initialize()

// Open custom pane
studio.createPane('my-pane')

// Render toolbar in pane
studio.ui.renderToolset('my-toolbar', containerNode)
```

## Extension State Persistence

```typescript
// Use Theatre.js object for extension state
const extState = studio.getStudioProject()
  .sheet('extension')
  .object('settings', {
    darkMode: types.boolean(false),
    gridSize: types.number(10)
  })

extState.onValuesChange((values) => {
  applySettings(values)
})
```

## Hot Reloading Extensions (v0.7.0+)

```typescript
studio.extend(extension, { __experimental_reconfigure: true })
```
