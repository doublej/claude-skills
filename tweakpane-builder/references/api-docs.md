# Tweakpane v4 API Reference

## Pane Class

```typescript
const pane = new Pane(config?: PaneConfig);
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `children` | `BladeApi[]` | Blade APIs in container |
| `disabled` | `boolean` | Enable/disable the pane |
| `element` | `HTMLElement` | Root HTML element |
| `expanded` | `boolean` | Expansion state |
| `hidden` | `boolean` | Visibility |
| `title` | `string \| undefined` | Pane title |

## Auto-Detection Rules

Tweakpane picks controls based on the JS type of the bound value + options provided:

| Value Type | Options | Resulting Control |
|------------|---------|-------------------|
| `number` | none | Text input (number) |
| `number` | `min` + `max` | **Slider** + text |
| `number` | `options: {...}` | **Dropdown** |
| `number` | `view: 'color'` | **Color picker** |
| `string` | none (not color-like) | Text input |
| `string` | none (CSS color string) | **Color picker** (auto) |
| `string` | `view: 'text'` | Text input (forced) |
| `string` | `options: {...}` | **Dropdown** |
| `boolean` | none | **Checkbox** |
| `{r, g, b}` | none | **Color picker** (auto) |
| `{r, g, b, a}` | none | **Color picker** + alpha |
| `{x, y}` | none | **Point 2D** picker |
| `{x, y, z}` | none | **Point 3D** fields |
| `{x, y, z, w}` | none | **Point 4D** fields |

## addBinding — Input Bindings

### Number

```typescript
// Text input (unbounded)
pane.addBinding(params, 'seed');

// Slider (bounded range)
pane.addBinding(params, 'speed', { min: 0, max: 100 });

// Slider with step
pane.addBinding(params, 'gridSize', { min: 8, max: 64, step: 8 });

// Dropdown (named values)
pane.addBinding(params, 'quality', {
  options: { Low: 1, Medium: 2, High: 3 },
});

// Custom display format
pane.addBinding(params, 'angle', {
  min: 0, max: 360,
  format: (v) => `${v.toFixed(0)}°`,
});
```

Options: `min`, `max`, `step`, `format: (v) => string`, `options: { label: value }`

### String

```typescript
// Text input (free text)
pane.addBinding(params, 'name');

// Dropdown (fixed choices)
pane.addBinding(params, 'easing', {
  options: { Linear: 'linear', Ease: 'ease-in-out', Bounce: 'bounce' },
});

// Force text input on color-like string
pane.addBinding(params, 'cssVar', { view: 'text' });
```

Options: `options: { label: value }`, `view: 'text'`

### Boolean

```typescript
// Checkbox (always)
pane.addBinding(params, 'enabled');
```

No additional options.

### Color

```typescript
// Auto-detected from CSS string
pane.addBinding(params, 'color');  // '#ff0055'

// Auto-detected from object
pane.addBinding(params, 'bg');  // { r: 255, g: 0, b: 85 }

// Force color on hex number
pane.addBinding(params, 'tint', { view: 'color' });  // 0xff0055

// Float range for shaders (0.0-1.0 instead of 0-255)
pane.addBinding(params, 'diffuse', { color: { type: 'float' } });

// With alpha channel
pane.addBinding(params, 'overlay', { color: { alpha: true } });

// Inline picker (always visible)
pane.addBinding(params, 'color', { picker: 'inline', expanded: true });
```

Options: `view: 'color'`, `color: { type: 'int'|'float', alpha: boolean }`, `picker: 'inline'`, `expanded: boolean`

### Point 2D

```typescript
// Auto-detected from {x, y}
pane.addBinding(params, 'position');

// With axis constraints
pane.addBinding(params, 'pos', {
  x: { min: -100, max: 100, step: 1 },
  y: { min: -100, max: 100, step: 1, inverted: true },
  picker: 'inline',
});
```

Options: `x: { min, max, step }`, `y: { min, max, step, inverted }`, `picker: 'inline'`, `expanded`

### Point 3D / 4D

```typescript
pane.addBinding(params, 'rotation');  // { x, y, z }
pane.addBinding(params, 'quat');     // { x, y, z, w }
// Per-axis: x/y/z/w: { min, max, step }
```

## addBinding — Monitor Bindings (readonly)

Add `readonly: true` to create non-editable displays.

```typescript
// Numeric display
pane.addBinding(params, 'fps', { readonly: true });

// Numeric graph
pane.addBinding(params, 'frameTime', {
  readonly: true,
  view: 'graph',
  min: 0,
  max: 33,
});

// Text display
pane.addBinding(params, 'status', { readonly: true });

// Multiline log
pane.addBinding(params, 'log', {
  readonly: true,
  multiline: true,
  rows: 5,
});

// Custom poll interval (default 200ms)
pane.addBinding(params, 'memory', {
  readonly: true,
  interval: 500,
});

// Buffer size (keep last N values for graph)
pane.addBinding(params, 'cpu', {
  readonly: true,
  view: 'graph',
  min: 0,
  max: 100,
  bufferSize: 120,
});
```

Monitor options: `readonly: true`, `view: 'graph'`, `multiline: boolean`, `rows: number`, `interval: number`, `bufferSize: number`

## Structural Controls

### Folder

```typescript
const folder = pane.addFolder({ title: 'Advanced', expanded: false });
folder.addBinding(params, 'key');
```

### Button

```typescript
const btn = pane.addButton({ title: 'Reset', label: 'action' });
btn.on('click', () => { /* ... */ });
```

### Tab

```typescript
const tab = pane.addTab({
  pages: [{ title: 'General' }, { title: 'Advanced' }],
});
tab.pages[0].addBinding(params, 'key');
```

## Blade Types (addBlade)

Standalone UI elements not bound to data.

```typescript
// Separator
pane.addBlade({ view: 'separator' });

// Text blade
pane.addBlade({
  view: 'text',
  label: 'info',
  parse: (v) => String(v),
  value: 'hello',
});

// List blade (standalone dropdown)
// Note: uses [{text, value}] format, not {label: value}
pane.addBlade({
  view: 'list',
  label: 'scene',
  options: [
    { text: 'Loading', value: 'ldg' },
    { text: 'Menu', value: 'mnu' },
  ],
  value: 'ldg',
});

// Slider blade (standalone slider)
pane.addBlade({
  view: 'slider',
  label: 'brightness',
  min: 0, max: 1, value: 0.5,
});
```

## Plugin: @tweakpane/plugin-essentials

```typescript
import * as EssentialsPlugin from '@tweakpane/plugin-essentials';
pane.registerPlugin(EssentialsPlugin);
```

### FPS Graph

```typescript
const fps = pane.addBlade({ view: 'fpsgraph', label: 'fps', rows: 2 });
// Call fps.begin() / fps.end() each frame
```

### Interval (range with two handles)

```typescript
// Value must be { min: number, max: number }
pane.addBinding(params, 'range', { min: 0, max: 100, step: 1 });
```

### Radio Grid

```typescript
pane.addBlade({
  view: 'radiogrid',
  groupName: 'theme',
  size: [3, 1],
  cells: (x, y) => ({
    title: ['Light', 'Dark', 'Auto'][x],
    value: ['light', 'dark', 'auto'][x],
  }),
  label: 'Theme',
});
```

### Button Grid

```typescript
const grid = pane.addBlade({
  view: 'buttongrid',
  size: [3, 1],
  cells: (x, y) => ({ title: ['Undo', 'Redo', 'Reset'][x] }),
  label: 'Actions',
});
grid.on('click', (ev) => console.log(ev.index));
```

### Cubic Bezier

```typescript
// Value must be [x1, y1, x2, y2] array
pane.addBinding(params, 'easing', {
  view: 'cubicbezier',
  expanded: true,
});
```

## Plugin: @tweakpane/plugin-camerakit

```typescript
import * as CamerakitPlugin from '@tweakpane/plugin-camerakit';
pane.registerPlugin(CamerakitPlugin);
```

### Camera Ring

```typescript
pane.addBinding(params, 'angle', {
  view: 'cameraring',
  series: 0, // 0, 1, or 2 (appearance)
});
```

### Camera Wheel

```typescript
pane.addBinding(params, 'zoom', {
  view: 'camerawheel',
  amount: 10, // value change per pixel
});
```

## Universal Options

Apply to any `addBinding()` call:

| Option | Type | Effect |
|--------|------|--------|
| `label` | `string` | Custom display label |
| `disabled` | `boolean` | Grey out control |
| `hidden` | `boolean` | Hide control |
| `index` | `number` | Insert position |

## Events

```typescript
// On specific binding
binding.on('change', (ev) => {
  ev.value;  // new value
  ev.last;   // true if final change in drag sequence
});

// On pane (all changes)
pane.on('change', (ev) => {
  console.log(ev.presetKey, ev.value);
});

// Folder fold
folder.on('fold', (ev) => {
  console.log('expanded:', ev.expanded);
});
```

## Common Patterns

### Preset System

```typescript
const presets = {
  default: { speed: 50, color: '#fff' },
  fast: { speed: 100, color: '#f00' },
};
pane.addBinding(params, 'preset', {
  options: Object.keys(presets).reduce((o, k) => ({ ...o, [k]: k }), {}),
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
// Option A: readonly binding with interval
pane.addBinding(params, 'fps', {
  readonly: true,
  view: 'graph',
  min: 0, max: 120,
  interval: 100,
});

// Option B: manual refresh
setInterval(() => {
  params.fps = calculateFPS();
  pane.refresh();
}, 100);
```

### State Persistence

```typescript
const state = pane.exportState();
localStorage.setItem('pane', JSON.stringify(state));

pane.importState(JSON.parse(localStorage.getItem('pane')));
```
