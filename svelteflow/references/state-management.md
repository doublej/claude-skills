# State Management

## $state.raw vs $state

**Use `$state.raw`** for `nodes` and `edges`. The docs are explicit: reactive tracking on every node property is a perf footgun.

```ts
let nodes = $state.raw([...]);  // ✅
let edges = $state.raw([...]);  // ✅

// ❌ AVOID — per-property tracking on large graphs is slow
let nodes = $state([...]);
```

Tradeoff: with `$state.raw`, mutating a nested property does NOT trigger reactivity. You must reassign the top-level array:

```ts
// ❌ does not update UI
nodes[0].data.label = 'new';

// ✅ reassigns
nodes = nodes.map(n => n.id === '1' ? { ...n, data: { ...n.data, label: 'new' } } : n);

// ✅ or use the helper
const { updateNodeData } = useSvelteFlow();
updateNodeData('1', { label: 'new' });
```

## useSvelteFlow() helpers

```ts
import { useSvelteFlow } from '@xyflow/svelte';

const {
  getNode, getNodes, getEdges, getEdge,
  addNodes, addEdges,
  setNodes, setEdges,
  updateNode, updateNodeData,
  updateEdge, updateEdgeData,
  deleteElements,
  getInternalNode,
  getIntersectingNodes, isNodeIntersecting,
  fitView, zoomIn, zoomOut, zoomTo,
  setCenter, setViewport, getViewport,
  screenToFlowPosition, flowToScreenPosition,
  toObject, fromObject,
  viewport, // $state rune
} = useSvelteFlow();
```

`updateNodeData(id, partial)` shallow-merges into `node.data`. `updateNode(id, partial)` merges into the node itself.

## Two-way binding

```svelte
<SvelteFlow bind:nodes bind:edges bind:viewport />
```

Without `bind:`, drag/connect/select will not persist — the built-in `onNodesChange`/`onEdgesChange` handlers write back through the binding.

## Function bindings (for modules / derived state)

When `nodes`/`edges` live outside the component (a store module, class, etc.), use the getter/setter binding syntax:

```svelte
<SvelteFlow
  bind:nodes={() => store.nodes, (v) => store.nodes = v}
  bind:edges={() => store.edges, (v) => store.edges = v}
/>
```

## Hook return shape: `.current`

In v1, reactive hooks return an object with a `current` getter (not a writable store). No `$` prefix.

```svelte
<script lang="ts">
  import { useNodes, useEdges, useViewport } from '@xyflow/svelte';

  const nodes = useNodes();
  const edges = useEdges();
  const viewport = useViewport();
</script>

<p>Node count: {nodes.current.length}</p>
<p>Zoom: {viewport.current.zoom}</p>
```

## Controlled flow (explicit handlers)

For undo/redo, persistence, or validation, take full control:

```svelte
<script lang="ts">
  import { SvelteFlow, applyNodeChanges, applyEdgeChanges, addEdge } from '@xyflow/svelte';
  import type { NodeChange, EdgeChange, Connection } from '@xyflow/svelte';

  let nodes = $state.raw([...]);
  let edges = $state.raw([...]);

  function onnodeschange(changes: NodeChange[]) {
    nodes = applyNodeChanges(changes, nodes);
  }
  function onedgeschange(changes: EdgeChange[]) {
    edges = applyEdgeChanges(changes, edges);
  }
  function onconnect(connection: Connection) {
    edges = addEdge(connection, edges);
  }
</script>

<SvelteFlow
  {nodes} {edges}
  {onnodeschange} {onedgeschange} {onconnect}
/>
```

Note: lowercase event props in Svelte 5 (`onconnect`, not `onConnect`).

## Cross-component state pattern (svelte module)

```ts
// lib/flow.svelte.ts
export const flow = $state({
  nodes: [] as Node[],
  edges: [] as Edge[],
});
```

Use from a component with function bindings (see above).
