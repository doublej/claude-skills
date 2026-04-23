# Theming

## CSS variables (recommended for tweaks)

Svelte Flow exposes ~30 CSS custom properties. Override selectively:

```css
.svelte-flow {
  --xy-background-color: #fafafa;
  --xy-background-pattern-color: #ddd;

  --xy-node-background-color-default: #ffffff;
  --xy-node-border-default: 1px solid #777;
  --xy-node-color-default: #222;
  --xy-node-border-radius-default: 6px;
  --xy-node-boxshadow-hover-default: 0 1px 4px 1px rgba(0, 0, 0, 0.15);
  --xy-node-boxshadow-selected-default: 0 0 0 2px #0af;

  --xy-edge-stroke-default: #b1b1b7;
  --xy-edge-stroke-width-default: 1;
  --xy-edge-stroke-selected-default: #555;

  --xy-handle-background-color-default: #1a192b;
  --xy-handle-border-color-default: #ffffff;

  --xy-controls-button-background-color-default: #fefefe;
  --xy-controls-button-background-color-hover-default: #f4f4f4;

  --xy-minimap-background-color-default: #ffffff;

  --xy-attribution-background-color-default: rgba(255, 255, 255, 0.5);
}
```

## Dark mode

Use plain CSS + media query OR prop-driven classes:

```css
@media (prefers-color-scheme: dark) {
  .svelte-flow {
    --xy-background-color: #0b0b0f;
    --xy-node-background-color-default: #1b1b22;
    --xy-node-color-default: #eee;
    --xy-node-border-default: 1px solid #444;
    --xy-edge-stroke-default: #666;
    --xy-controls-button-background-color-default: #222;
    --xy-minimap-background-color-default: #1b1b22;
  }
}
```

## Base styles only (own design system)

If you want everything un-styled except positioning math:

```ts
import '@xyflow/svelte/dist/base.css';  // not style.css
```

Then target classes yourself.

## Class targets

Key classes for deep overrides:

- `.svelte-flow` — root
- `.svelte-flow__node`, `.svelte-flow__node-<type>`, `.svelte-flow__node.selected`
- `.svelte-flow__edge`, `.svelte-flow__edge-path`, `.svelte-flow__edge.selected`
- `.svelte-flow__handle`, `.svelte-flow__handle-top|bottom|left|right`, `.svelte-flow__handle.connecting`, `.svelte-flow__handle.valid`
- `.svelte-flow__controls`, `.svelte-flow__controls-button`
- `.svelte-flow__minimap`, `.svelte-flow__minimap-node`
- `.svelte-flow__background`
- `.svelte-flow__panel`
- `.svelte-flow__attribution`

## Tailwind integration

Import Tailwind AFTER Svelte Flow styles so utility classes win:

```css
/* app.css */
@import '@xyflow/svelte/dist/style.css';
@import 'tailwindcss';
```

Then use utilities on custom nodes:

```svelte
<div class="rounded-lg border border-zinc-300 bg-white px-3 py-2 shadow-sm">
  <Handle type="target" position={Position.Top} class="!bg-zinc-800" />
  <span class="text-sm">{data.label}</span>
  <Handle type="source" position={Position.Bottom} class="!bg-zinc-800" />
</div>
```

The `!` prefix overrides Svelte Flow's handle defaults.

## Animated edges

Built-in, just set `animated: true`:
```ts
{ id: 'e1', source: '1', target: '2', animated: true }
```
Uses the class `.svelte-flow__edge.animated` with a CSS dash animation.
