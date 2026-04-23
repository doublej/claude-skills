# Fundamentals

## Install

```bash
npm install @xyflow/svelte
# pnpm add @xyflow/svelte
# bun add @xyflow/svelte
```

Requires: **Svelte 5** (runes mode). v1+ is not compatible with Svelte 4.

## Minimal flow

```svelte
<script lang="ts">
  import { SvelteFlow, Background, Controls, MiniMap } from '@xyflow/svelte';
  import '@xyflow/svelte/dist/style.css';

  let nodes = $state.raw([
    { id: '1', type: 'input',  position: { x: 0,   y: 0   }, data: { label: 'Hello' } },
    { id: '2', type: 'output', position: { x: 100, y: 100 }, data: { label: 'World' } },
  ]);

  let edges = $state.raw([
    { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', label: 'to the' },
  ]);
</script>

<div style:width="100vw" style:height="100vh">
  <SvelteFlow bind:nodes bind:edges fitView>
    <Background />
    <Controls />
    <MiniMap />
  </SvelteFlow>
</div>
```

Critical details:
- `$state.raw(...)` — not `$state(...)`. Deep reactivity on per-node props is a known perf footgun.
- `bind:nodes` and `bind:edges` — two-way. Required for built-in drag/connect behavior to update your state.
- Outer `<div>` must have width AND height.
- Import `style.css` exactly once per app (usually `src/routes/+layout.svelte` or `src/main.ts`).

## Node object shape

```ts
interface Node<T = Record<string, unknown>> {
  id: string;                     // required, unique
  position: { x: number; y: number };
  data: T;                        // arbitrary payload for custom nodes
  type?: string;                  // 'default' | 'input' | 'output' | custom key
  width?: number;
  height?: number;
  selected?: boolean;
  dragging?: boolean;
  draggable?: boolean;
  selectable?: boolean;
  connectable?: boolean;
  deletable?: boolean;
  hidden?: boolean;
  zIndex?: number;
  parentId?: string;              // for sub-flows
  extent?: 'parent' | [[number, number], [number, number]];
  className?: string;
  style?: string;
}
```

## Edge object shape

```ts
interface Edge<T = Record<string, unknown>> {
  id: string;
  source: string;                 // source node id
  target: string;                 // target node id
  sourceHandle?: string | null;   // required if source node has multiple handles
  targetHandle?: string | null;
  type?: string;                  // 'default' (bezier) | 'straight' | 'step' | 'smoothstep' | custom
  data?: T;
  label?: string;
  animated?: boolean;
  selected?: boolean;
  markerStart?: string | { type: MarkerType };
  markerEnd?: string | { type: MarkerType };
  style?: string;
}
```

## Built-in node types

- `input` — source handle only
- `output` — target handle only
- `default` — both handles
- `group` — no handles, used for sub-flow parents

Prefer **custom nodes** for real apps. See `custom-nodes.md`.

## Key concepts

- **Canvas** — infinite zoom/pan viewport
- **Nodes** — positioned Svelte components
- **Edges** — SVG paths between handles
- **Handles** — `<Handle type="source|target" position={Position.Bottom} />` connection points
- **Viewport** — `{ x, y, zoom }` for the current pan/zoom state
