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

## Control Selection

| Data Type | Control |
|-----------|---------|
| Number (range) | Slider |
| Number (unbounded) | Number input |
| Boolean | Checkbox |
| String (enum) | Dropdown |
| Color | Color picker |
| Point {x,y} | Point 2D |

## Example

```typescript
import { Pane } from 'tweakpane';

const pane = new Pane({ title: 'Settings' });
const params = { speed: 50, enabled: true, color: '#ff0055' };

pane.addBinding(params, 'speed', { min: 0, max: 100 });
pane.addBinding(params, 'enabled');
pane.addBinding(params, 'color');
```

## Reference Files

See `references/` for API documentation.
