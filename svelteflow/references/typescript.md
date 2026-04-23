# TypeScript

## Typed nodes and edges

Use the generic `Node<Data, Type>` and `Edge<Data, Type>` types:

```ts
import type { Node, Edge } from '@xyflow/svelte';

type InputNode  = Node<{ label: string }, 'input'>;
type FilterNode = Node<{ query: string; caseSensitive: boolean }, 'filter'>;
type AppNode    = InputNode | FilterNode;

type DataEdge   = Edge<{ weight: number }, 'data'>;
type AppEdge    = DataEdge | Edge;

let nodes = $state.raw<AppNode[]>([
  { id: '1', type: 'input',  position: { x: 0, y: 0 }, data: { label: 'start' } },
  { id: '2', type: 'filter', position: { x: 0, y: 0 }, data: { query: '', caseSensitive: false } },
]);

let edges = $state.raw<AppEdge[]>([]);
```

## Typed SvelteFlow component

```svelte
<SvelteFlow<AppNode, AppEdge>
  bind:nodes bind:edges
  {nodeTypes} {edgeTypes}
/>
```

Typing the component gives you autocomplete on `onconnect`, `onnodeclick`, etc.

## NodeProps / EdgeProps

```svelte
<!-- FilterNode.svelte -->
<script lang="ts">
  import { Handle, Position, type NodeProps, type Node } from '@xyflow/svelte';

  type FilterNode = Node<{ query: string; caseSensitive: boolean }, 'filter'>;
  let { id, data, selected }: NodeProps<FilterNode> = $props();
</script>
```

```svelte
<!-- CustomEdge.svelte -->
<script lang="ts">
  import { BaseEdge, getBezierPath, type EdgeProps, type Edge } from '@xyflow/svelte';

  type DataEdge = Edge<{ weight: number }, 'data'>;
  let props: EdgeProps<DataEdge> = $props();
</script>
```

## Type guards

Narrow a union:

```ts
function isFilterNode(n: AppNode): n is FilterNode {
  return n.type === 'filter';
}

const filters = nodes.filter(isFilterNode);
```

## Typed helpers

```ts
import type { Connection, NodeChange, EdgeChange, Viewport } from '@xyflow/svelte';

function onconnect(c: Connection) { ... }
function onnodeschange(changes: NodeChange<AppNode>[]) { ... }
function onedgeschange(changes: EdgeChange<AppEdge>[]) { ... }
```

## Module with typed store

```ts
// lib/flow-store.svelte.ts
import type { Node, Edge } from '@xyflow/svelte';

export type AppNode = Node<{ label: string }> | Node<{ count: number }, 'counter'>;
export type AppEdge = Edge;

export const flow = $state({
  nodes: [] as AppNode[],
  edges: [] as AppEdge[],
});
```

## Common type errors

- `Type 'string' is not assignable to type 'unique literal'` → your `type` field doesn't match the `Node<Data, Type>` literal. Widen or add union member.
- `Property 'data' does not exist` when destructuring `NodeProps` → forgot generic: `NodeProps<MyNode>`.
- `bind:nodes` type mismatch → you're passing `Node[]` where generic expects `AppNode[]`. Type the `$state.raw` explicitly.
