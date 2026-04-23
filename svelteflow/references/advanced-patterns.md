# Advanced Patterns

## Undo / Redo

Snapshot `{ nodes, edges }` on every committed change.

```ts
// lib/history.svelte.ts
import type { Node, Edge } from '@xyflow/svelte';

type Snapshot = { nodes: Node[]; edges: Edge[] };

export function createHistory() {
  let past  = $state.raw<Snapshot[]>([]);
  let future = $state.raw<Snapshot[]>([]);

  return {
    push(snap: Snapshot) {
      past = [...past, snap];
      future = [];
    },
    undo(current: Snapshot): Snapshot | undefined {
      const prev = past[past.length - 1];
      if (!prev) return;
      past = past.slice(0, -1);
      future = [current, ...future];
      return prev;
    },
    redo(current: Snapshot): Snapshot | undefined {
      const next = future[0];
      if (!next) return;
      future = future.slice(1);
      past = [...past, current];
      return next;
    },
    get canUndo() { return past.length > 0; },
    get canRedo() { return future.length > 0; },
  };
}
```

Commit on drag stop, connect, delete — not on every drag tick.

## Copy / Paste

```ts
import { useSvelteFlow } from '@xyflow/svelte';
const { toObject, addNodes, addEdges, screenToFlowPosition } = useSvelteFlow();

let clipboard: { nodes: Node[]; edges: Edge[] } | null = null;

function copy(selection: { nodes: Node[]; edges: Edge[] }) {
  clipboard = structuredClone(selection);
}

function paste(screen: { x: number; y: number }) {
  if (!clipboard) return;
  const origin = screenToFlowPosition(screen);
  const minX = Math.min(...clipboard.nodes.map(n => n.position.x));
  const minY = Math.min(...clipboard.nodes.map(n => n.position.y));

  const idMap = new Map<string, string>();
  const newNodes = clipboard.nodes.map(n => {
    const id = crypto.randomUUID();
    idMap.set(n.id, id);
    return { ...n, id, selected: true, position: {
      x: origin.x + (n.position.x - minX),
      y: origin.y + (n.position.y - minY),
    } };
  });
  const newEdges = clipboard.edges
    .filter(e => idMap.has(e.source) && idMap.has(e.target))
    .map(e => ({ ...e, id: crypto.randomUUID(), source: idMap.get(e.source)!, target: idMap.get(e.target)! }));

  addNodes(newNodes);
  addEdges(newEdges);
}
```

## Save / Restore (localStorage)

```ts
const { toObject } = useSvelteFlow();

function save() {
  const flow = toObject();  // { nodes, edges, viewport }
  localStorage.setItem('flow', JSON.stringify(flow));
}

function restore() {
  const raw = localStorage.getItem('flow');
  if (!raw) return;
  const { nodes: n, edges: e, viewport: v } = JSON.parse(raw);
  nodes = n;
  edges = e;
  setViewport(v);
}
```

## Computed flow (propagate values along edges)

Pattern: each node reads upstream node data via `useNodesData`, derives its own output in `data`, writes back with `updateNodeData`. Run topologically (build adjacency, BFS/DFS).

```svelte
<script lang="ts">
  import { useNodesData, useNodeConnections, useSvelteFlow, type NodeProps } from '@xyflow/svelte';
  let { id, data }: NodeProps<{ value: number }> = $props();

  const incoming = useNodeConnections({ id, handleType: 'target' });
  const upstreamIds = $derived(incoming.current.map(c => c.source));
  const upstreamData = useNodesData(upstreamIds);

  const { updateNodeData } = useSvelteFlow();
  $effect(() => {
    const sum = upstreamData.current.reduce((acc, n) => acc + (n?.data?.value ?? 0), 0);
    if (sum !== data.value) updateNodeData(id, { value: sum });
  });
</script>
```

Guard `$effect` against infinite loops by diffing before calling `updateNodeData`.

## Dynamic handles

```svelte
<script lang="ts">
  import { Handle, Position, useUpdateNodeInternals, type NodeProps } from '@xyflow/svelte';
  let { id, data }: NodeProps<{ inputs: string[] }> = $props();
  const update = useUpdateNodeInternals();

  $effect(() => { update(id); }); // whenever inputs change
</script>

{#each data.inputs as input, i (input)}
  <Handle type="target" id={input} position={Position.Left} style="top: {20 + i * 24}px" />
{/each}
```

## Sub-flows

Parent `type: 'group'` with fixed width/height, children reference `parentId` and `extent: 'parent'`.

```ts
let nodes = $state.raw([
  { id: 'g', type: 'group', position: { x: 0, y: 0 }, style: 'width:320px;height:200px;', data: {} },
  { id: 'a', parentId: 'g', extent: 'parent', position: { x: 20, y: 40 }, data: { label: 'A' } },
  { id: 'b', parentId: 'g', extent: 'parent', position: { x: 180, y: 40 }, data: { label: 'B' } },
]);
```

Parent must come BEFORE children in the array.

## Collaboration (Yjs-style)

Keep `nodes`/`edges` as plain arrays, sync via a Y.Array observer:

```ts
yNodes.observeDeep(() => {
  nodes = yNodes.toArray().map(y => y.toJSON());
});

onnodeschange = (changes) => {
  Y.transact(doc, () => {
    changes.forEach(/* mirror into yNodes */);
  });
  nodes = applyNodeChanges(changes, nodes);
};
```

Use `structuredClone` when crossing CRDT boundaries to avoid accidental proxy leaks.
