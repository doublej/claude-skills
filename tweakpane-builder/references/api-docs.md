# Tweakpane API Reference

## Pane Class

The root pane of Tweakpane, extends `RootApi`.

### Constructor

```typescript
const pane = new Pane(config?: PaneConfig);
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `children` | `BladeApi[]` | Array of blade APIs in container |
| `disabled` | `boolean` | Enable/disable the pane |
| `document` | `Document` | The document object |
| `element` | `HTMLElement` | The root HTML element |
| `expanded` | `boolean` | Expansion state |
| `hidden` | `boolean` | Visibility state |
| `title` | `string \| undefined` | Pane title |

### Methods

#### Content Addition

**addBinding(object, key, params?)**
```typescript
pane.addBinding(obj, 'property', {
  min: 0,
  max: 100,
  step: 1,
  label: 'Custom Label'
});
```

**addFolder(params)**
```typescript
const folder = pane.addFolder({
  title: 'Folder Name',
  expanded: true
});
```

**addBlade(params)**
```typescript
pane.addBlade({
  view: 'separator'
});

pane.addBlade({
  view: 'text',
  label: 'info',
  parse: (v) => String(v),
  value: 'hello'
});
```

**addButton(params)**
```typescript
const btn = pane.addButton({
  title: 'Click Me',
  label: 'action'
});
btn.on('click', () => console.log('clicked'));
```

**addTab(params)**
```typescript
const tab = pane.addTab({
  pages: [
    { title: 'Page 1' },
    { title: 'Page 2' }
  ]
});
tab.pages[0].addBinding(obj, 'prop');
```

#### Utilities

**on(eventName, handler)** / **off(eventName, handler)**
```typescript
pane.on('change', (ev) => {
  console.log(ev.value);
});
```

**refresh()**
```typescript
// Update display after external changes
params.value = newValue;
pane.refresh();
```

**dispose()**
```typescript
pane.dispose(); // Clean up resources
```

**exportState()** / **importState(state)**
```typescript
const state = pane.exportState();
localStorage.setItem('pane', JSON.stringify(state));

// Later...
pane.importState(JSON.parse(localStorage.getItem('pane')));
```

**registerPlugin(bundle)**
```typescript
import * as EssentialsPlugin from '@tweakpane/plugin-essentials';
pane.registerPlugin(EssentialsPlugin);
```

## Input Binding Parameters

### Number

```typescript
{
  min: number,           // Minimum value
  max: number,           // Maximum value (with min creates slider)
  step: number,          // Step increment
  format: (v) => string, // Display format
  options: {}            // Creates dropdown instead
}
```

### String

```typescript
{
  options: string[] | { label: value }  // Creates dropdown
}
```

### Boolean

No additional parameters (checkbox by default).

### Color

```typescript
{
  color: {
    alpha: boolean,     // Enable alpha channel
    type: 'int' | 'float'  // Value range (0-255 or 0-1)
  },
  view: 'color',        // Force color view
  picker: 'inline',     // Inline picker
  expanded: boolean     // Expand by default
}
```

### Point 2D/3D/4D

```typescript
{
  x: { min, max, step },
  y: { min, max, step, inverted: boolean },
  z: { min, max, step },  // 3D+
  w: { min, max, step },  // 4D only
  picker: 'inline'
}
```

## Blade Types

### Separator

```typescript
pane.addBlade({ view: 'separator' });
```

### Text

```typescript
pane.addBlade({
  view: 'text',
  label: 'name',
  parse: (v) => String(v),
  value: 'initial'
});
```

### List

```typescript
pane.addBlade({
  view: 'list',
  label: 'choice',
  options: [
    { text: 'Option A', value: 'a' },
    { text: 'Option B', value: 'b' }
  ],
  value: 'a'
});
```

### Slider

```typescript
pane.addBlade({
  view: 'slider',
  label: 'value',
  min: 0,
  max: 100,
  value: 50
});
```

## Events

### Change Event

```typescript
pane.on('change', (ev) => {
  console.log('changed:', ev.presetKey, ev.value);
});

// On specific binding
binding.on('change', (ev) => {
  console.log(ev.value);
});
```

### Fold Event

```typescript
folder.on('fold', (ev) => {
  console.log('expanded:', ev.expanded);
});
```

## Common Patterns

### Preset System

```typescript
const presets = {
  default: { speed: 50, color: '#fff' },
  fast: { speed: 100, color: '#f00' }
};

pane.addBinding(params, 'preset', {
  options: Object.keys(presets)
}).on('change', (ev) => {
  Object.assign(params, presets[ev.value]);
  pane.refresh();
});
```

### Conditional Controls

```typescript
const advanced = pane.addFolder({ title: 'Advanced', expanded: false });
pane.addBinding(params, 'showAdvanced').on('change', (ev) => {
  advanced.hidden = !ev.value;
});
```

### Real-time Monitoring

```typescript
setInterval(() => {
  params.fps = calculateFPS();
  pane.refresh();
}, 100);
```
