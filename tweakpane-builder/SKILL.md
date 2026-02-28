---
name: tweakpane-builder
description: Build Tweakpane debug UIs with intelligent control suggestions based on data types
---

# Tweakpane Builder Skill

Build Tweakpane debug UIs with intelligent control suggestions.

## When to Use

- Building debug/settings panels with Tweakpane
- Need UI control recommendations for parameter types
- Creating Tweakpane configurations

## Control Selection Decision Tree

Pick the right control by asking: **what is the user choosing?**

### Numbers

| Scenario | Control | How |
|----------|---------|-----|
| Bounded range (e.g. volume 0-100) | Slider | `{ min: 0, max: 100 }` |
| Bounded + discrete steps (e.g. grid size 8/16/32) | Slider with step | `{ min: 8, max: 64, step: 8 }` |
| Named presets (e.g. quality: low/med/high) | **Dropdown** | `{ options: { Low: 1, Medium: 2, High: 3 } }` |
| Unbounded/free value (e.g. seed, ID) | Text input | no min/max |
| Read-only metric (e.g. FPS) | Monitor | `{ readonly: true, interval: 100 }` |
| Read-only trend (e.g. frame time) | Graph | `{ readonly: true, view: 'graph', min: 0, max: 60 }` |

### Strings

| Scenario | Control | How |
|----------|---------|-----|
| Free text (e.g. label, name) | Text input | no options |
| Fixed choices (e.g. mode: "ease"/"linear") | **Dropdown** | `{ options: { Ease: 'ease', Linear: 'linear' } }` |
| CSS color value | Color picker | auto-detected from `'#ff0055'` |
| Color-like string as plain text | Text input | `{ view: 'text' }` to suppress color detection |
| Read-only log output | Monitor | `{ readonly: true, multiline: true, rows: 5 }` |

### Booleans

| Scenario | Control | How |
|----------|---------|-----|
| On/off toggle | Checkbox | auto (always checkbox) |

### Colors

| Scenario | Control | How |
|----------|---------|-----|
| CSS string `'#ff0055'` | Color picker | auto-detected |
| Object `{r, g, b}` | Color picker | auto-detected |
| Hex number `0xff0055` | Color picker | `{ view: 'color' }` (must force) |
| Shader float `{r: 1.0, g: 0, b: 0}` | Color picker (float) | `{ color: { type: 'float' } }` |
| With alpha | Color picker + alpha | `{ color: { alpha: true } }` |
| Inline (always visible) | Inline picker | `{ picker: 'inline', expanded: true }` |

### Coordinates

| Scenario | Control | How |
|----------|---------|-----|
| Position `{x, y}` | Point 2D picker | auto-detected |
| Screen coords (Y-down) | Point 2D (inverted) | `{ y: { inverted: true } }` |
| 3D position `{x, y, z}` | Point 3D fields | auto-detected |
| Quaternion `{x, y, z, w}` | Point 4D fields | auto-detected |

### Actions & Structure

| Scenario | Control | How |
|----------|---------|-----|
| Trigger action (e.g. Reset) | Button | `pane.addButton({ title: 'Reset' })` |
| Group related controls | Folder | `pane.addFolder({ title: 'Group' })` |
| Separate sections | Separator | `pane.addBlade({ view: 'separator' })` |
| Multiple pages | Tab | `pane.addTab({ pages: [...] })` |
| Static label/info | Text blade | `pane.addBlade({ view: 'text', ... })` |
| Standalone dropdown | List blade | `pane.addBlade({ view: 'list', ... })` |

### Plugin Controls (@tweakpane/plugin-essentials)

| Scenario | Control | How |
|----------|---------|-----|
| FPS counter | FPS graph | `pane.addBlade({ view: 'fpsgraph', rows: 2 })` |
| Range min/max | Interval | `addBinding(obj, 'range', { min: 0, max: 100 })` |
| Grid of radio options | Radio grid | `pane.addBlade({ view: 'radiogrid', ... })` |
| Grid of buttons | Button grid | `pane.addBlade({ view: 'buttongrid', ... })` |
| Easing curve | Cubic bezier | `addBinding(obj, 'ease', { view: 'cubicbezier' })` |

## Common Mistakes

- **Slider for enum values** — use dropdown (`options: {}`) when there are named choices
- **Slider for unbounded numbers** — omit min/max for a text input when range is unknown
- **Slider for discrete options** — if there are only 3-5 fixed values, prefer dropdown
- **Missing `view: 'color'`** — hex numbers like `0xff0055` need explicit `view: 'color'`
- **No monitors** — use `readonly: true` for values the user shouldn't edit (FPS, timing, state)

## Example

```typescript
import { Pane } from 'tweakpane';
import * as EssentialsPlugin from '@tweakpane/plugin-essentials';

const pane = new Pane({ title: 'Settings' });
pane.registerPlugin(EssentialsPlugin);

const params = {
  speed: 50,
  enabled: true,
  color: '#ff0055',
  mode: 'linear',
  position: { x: 0, y: 0 },
  fps: 60,
};

// Slider — bounded range
pane.addBinding(params, 'speed', { min: 0, max: 100, step: 1 });

// Checkbox — boolean
pane.addBinding(params, 'enabled');

// Color picker — auto-detected from CSS string
pane.addBinding(params, 'color');

// Dropdown — fixed string choices
pane.addBinding(params, 'mode', {
  options: { Linear: 'linear', Ease: 'ease', Bounce: 'bounce' },
});

// Point 2D — auto-detected from {x, y}
pane.addBinding(params, 'position', {
  x: { min: -100, max: 100 },
  y: { min: -100, max: 100, inverted: true },
});

// Graph monitor — read-only trend
pane.addBinding(params, 'fps', {
  readonly: true,
  view: 'graph',
  min: 0,
  max: 120,
});

// Button — action trigger
pane.addButton({ title: 'Reset' }).on('click', () => {
  Object.assign(params, { speed: 50, enabled: true });
  pane.refresh();
});
```

## Reference Files

See `references/` for API documentation.
