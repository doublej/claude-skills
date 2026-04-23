# Migration: v0 → v1

v1 is Svelte 5 only. v0 used Svelte 4 stores. Every `nodes`/`edges` declaration and every hook usage changes.

## Package

No rename. Stay on `@xyflow/svelte`, just bump to v1.x. Svelte must be ^5.

```bash
npm install @xyflow/svelte@latest svelte@latest
```

## State: stores → `$state.raw`

```svelte
<!-- v0 -->
<script>
  import { writable } from 'svelte/store';
  const nodes = writable([...]);
  const edges = writable([...]);
</script>
<SvelteFlow {nodes} {edges} />

<!-- v1 -->
<script>
  let nodes = $state.raw([...]);
  let edges = $state.raw([...]);
</script>
<SvelteFlow bind:nodes bind:edges />
```

## Props: value → `bind:`

`nodes`, `edges`, `viewport` all switch from value props to two-way binding.

```svelte
<!-- v0 -->
<SvelteFlow {nodes} {edges} {viewport} />

<!-- v1 -->
<SvelteFlow bind:nodes bind:edges bind:viewport />
```

## Hooks: writable store → `{ current }`

```svelte
<!-- v0 -->
<script>
  const edges = useEdges();
  $: count = $edges.length;
</script>

<!-- v1 -->
<script>
  const edges = useEdges();
  const count = $derived(edges.current.length);
</script>
```

Affected: `useNodes`, `useEdges`, `useViewport`, `useConnection`, `useNodeConnections`, `useNodesData`, `useNodesInitialized`.

## Custom nodes: `$$Props` → `$props()`

```svelte
<!-- v0 -->
<script lang="ts">
  import type { NodeProps } from '@xyflow/svelte';
  type $$Props = NodeProps;
  export let id: $$Props['id'];
  export let data: $$Props['data'];
  export let selected: $$Props['selected'];
</script>

<!-- v1 -->
<script lang="ts">
  import type { NodeProps } from '@xyflow/svelte';
  let { id, data, selected }: NodeProps = $props();
</script>
```

## Events: `on:xxx` → `onxxx`

All Svelte Flow events are now component props, not DOM events. Lowercase, no colon.

| v0 | v1 |
|---|---|
| `on:nodeclick` | `onnodeclick` |
| `on:edgeclick` | `onedgeclick` |
| `on:connect` | `onconnect` |
| `on:connectstart` | `onconnectstart` |
| `on:connectend` | `onconnectend` |
| `on:paneclick` | `onpaneclick` |
| `on:selectionchange` | `onselectionchange` |
| `on:move`, `on:moveend` | `onmove`, `onmoveend` |

## API renames

| v0 | v1 |
|---|---|
| `onEdgeCreate` | `onbeforeconnect` |
| `<EdgeLabelRenderer>` | `<EdgeLabel>` |
| Slot `connectionLine` | Prop `connectionLineComponent` |

## Viewport

```svelte
<!-- v0 -->
<script>
  const viewport = writable({ x: 0, y: 0, zoom: 1 });
</script>
<SvelteFlow {viewport} />

<!-- v1 -->
<script>
  let viewport = $state({ x: 0, y: 0, zoom: 1 });
</script>
<SvelteFlow bind:viewport />
```

## Data updates

v0 code that did `$nodes[0].data.label = 'x'` must become:

```ts
// option A: array reassignment
nodes = nodes.map(n => n.id === '1' ? { ...n, data: { ...n.data, label: 'x' } } : n);

// option B: helper
useSvelteFlow().updateNodeData('1', { label: 'x' });
```

## Module-scoped state (cross-component)

```ts
// v0: lib/flow.ts
export const nodes = writable<Node[]>([]);

// v1: lib/flow.svelte.ts
export const flow = $state({ nodes: [] as Node[], edges: [] as Edge[] });
```

Pass to `<SvelteFlow>` via getter/setter bindings:
```svelte
<SvelteFlow
  bind:nodes={() => flow.nodes, (v) => flow.nodes = v}
  bind:edges={() => flow.edges, (v) => flow.edges = v}
/>
```

## Migration checklist

- [ ] Svelte bumped to ^5
- [ ] `writable` replaced with `$state.raw`
- [ ] All props use `bind:` where needed
- [ ] `$store` accesses → `store.current`
- [ ] All `on:xxx` → `onxxx` props
- [ ] All custom nodes use `$props()` with `NodeProps` generic
- [ ] `<EdgeLabelRenderer>` → `<EdgeLabel>`
- [ ] `onEdgeCreate` → `onbeforeconnect`
- [ ] Direct `data` mutations replaced with `updateNodeData` or array reassign
