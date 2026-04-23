# Layouting

## Dagre (recommended for tree/DAG structures)

```bash
npm install @dagrejs/dagre
```

```ts
// lib/layout.ts
import dagre from '@dagrejs/dagre';
import type { Node, Edge } from '@xyflow/svelte';

const NODE_W = 172;
const NODE_H = 36;

export function layout(nodes: Node[], edges: Edge[], direction: 'TB' | 'LR' = 'TB') {
  const g = new dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: direction });

  nodes.forEach(n => g.setNode(n.id, { width: n.width ?? NODE_W, height: n.height ?? NODE_H }));
  edges.forEach(e => g.setEdge(e.source, e.target));

  dagre.layout(g);

  const laidOut = nodes.map(n => {
    const { x, y } = g.node(n.id);
    const w = n.width ?? NODE_W, h = n.height ?? NODE_H;
    return {
      ...n,
      position: { x: x - w / 2, y: y - h / 2 },
      targetPosition: direction === 'LR' ? 'left'   : 'top',
      sourcePosition: direction === 'LR' ? 'right'  : 'bottom',
    };
  });

  return { nodes: laidOut, edges };
}
```

Use it:

```svelte
<script lang="ts">
  import { layout } from '$lib/layout';
  let nodes = $state.raw([...]);
  let edges = $state.raw([...]);

  function autoLayout() {
    const out = layout(nodes, edges, 'LR');
    nodes = out.nodes;
    edges = out.edges;
  }
</script>
```

Call `autoLayout()` after node dimensions are known — use `useNodesInitialized()` to wait.

## elkjs (async, more configurable)

```bash
npm install elkjs
```

```ts
import ELK from 'elkjs/lib/elk.bundled.js';
import type { Node, Edge } from '@xyflow/svelte';

const elk = new ELK();

const options = {
  'elk.algorithm': 'layered',
  'elk.direction': 'RIGHT',
  'elk.layered.spacing.nodeNodeBetweenLayers': '100',
  'elk.spacing.nodeNode': '80',
};

export async function elkLayout(nodes: Node[], edges: Edge[]) {
  const graph = {
    id: 'root',
    layoutOptions: options,
    children: nodes.map(n => ({ id: n.id, width: n.width ?? 150, height: n.height ?? 50 })),
    edges: edges.map(e => ({ id: e.id, sources: [e.source], targets: [e.target] })),
  };

  const laid = await elk.layout(graph);

  return {
    nodes: nodes.map(n => {
      const c = laid.children!.find(c => c.id === n.id)!;
      return { ...n, position: { x: c.x!, y: c.y! } };
    }),
    edges,
  };
}
```

## Waiting for node dimensions

```svelte
<script lang="ts">
  import { useNodesInitialized, useSvelteFlow } from '@xyflow/svelte';
  const initialized = useNodesInitialized();
  const { fitView } = useSvelteFlow();

  $effect(() => {
    if (initialized.current) {
      const laid = layout(nodes, edges);
      nodes = laid.nodes;
      edges = laid.edges;
      queueMicrotask(() => fitView());
    }
  });
</script>
```

## Sub-flows (parent / child nodes)

Mark the parent with `type: 'group'`, children reference `parentId` and can constrain to `extent: 'parent'`.

```ts
let nodes = $state.raw([
  {
    id: 'group-1', type: 'group',
    position: { x: 0, y: 0 },
    style: 'width: 320px; height: 200px;',
    data: {},
  },
  {
    id: 'child-1', parentId: 'group-1', extent: 'parent',
    position: { x: 20, y: 40 },
    data: { label: 'child' },
  },
]);
```

**Parent MUST appear before its children in the array** or children render behind the parent.
