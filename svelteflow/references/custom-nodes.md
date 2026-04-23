# Custom Nodes

## Basic custom node

```svelte
<!-- CustomNode.svelte -->
<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';

  type Data = { label: string; value?: number };
  let { id, data, selected }: NodeProps<Data> = $props();
</script>

<div class="custom-node" class:selected>
  <Handle type="target" position={Position.Top} />
  <div>{data.label}</div>
  <Handle type="source" position={Position.Bottom} />
</div>

<style>
  .custom-node {
    padding: 8px 12px;
    border: 1px solid #777;
    border-radius: 6px;
    background: white;
  }
  .selected { border-color: #0af; }
</style>
```

## Register nodeTypes

**Define at module scope** (or `$derived` inside a component). Re-creating the object on every render triggers a console warning and thrashes node mounts.

```svelte
<script lang="ts">
  import { SvelteFlow } from '@xyflow/svelte';
  import CustomNode from './CustomNode.svelte';

  const nodeTypes = { custom: CustomNode };

  let nodes = $state.raw([
    { id: 'a', type: 'custom', position: { x: 0, y: 0 }, data: { label: 'A' } },
  ]);
  let edges = $state.raw([]);
</script>

<SvelteFlow {nodeTypes} bind:nodes bind:edges />
```

## Interactive elements inside a node

Dragging a node intercepts pointer events. Add `nodrag` so inputs/buttons stay usable. Add `nowheel` so scrollable areas don't zoom the canvas.

```svelte
<div class="custom-node">
  <Handle type="target" position={Position.Top} />
  <input class="nodrag" bind:value={data.label} />
  <button class="nodrag" onclick={doThing}>Go</button>
  <div class="nowheel" style:overflow="auto" style:max-height="120px">
    <!-- scrollable content -->
  </div>
  <Handle type="source" position={Position.Bottom} />
</div>
```

## Multiple handles of the same type

Assign **unique `id`** per handle, and position them with CSS so they don't stack.

```svelte
<Handle type="source" position={Position.Right} id="a" style:top="30%" />
<Handle type="source" position={Position.Right} id="b" style:top="70%" />
```

Edges then reference them:
```ts
{ id: 'e1', source: 'n1', sourceHandle: 'a', target: 'n2' }
```

## Dynamic handles

Whenever handles are added/removed programmatically, notify Svelte Flow:

```svelte
<script lang="ts">
  import { useUpdateNodeInternals } from '@xyflow/svelte';
  let { id }: NodeProps = $props();
  const updateNodeInternals = useUpdateNodeInternals();

  let handleCount = $state(1);

  function addHandle() {
    handleCount++;
    updateNodeInternals(id);
  }
</script>
```

## Drag handle (node only draggable from a grip)

Set `dragHandle` selector on the node, or use the `.custom-drag-handle` class.

```ts
{ id: 'n1', type: 'custom', position: {...}, data: {...}, dragHandle: '.drag-grip' }
```

```svelte
<div class="drag-grip">≡</div>
```

## NodeProps fields

```ts
interface NodeProps<T = Record<string, unknown>> {
  id: string;
  data: T;
  type: string;
  selected: boolean;
  dragging: boolean;
  draggable: boolean;
  selectable: boolean;
  connectable: boolean;
  deletable: boolean;
  positionAbsoluteX: number;
  positionAbsoluteY: number;
  width?: number;
  height?: number;
  sourcePosition: Position;
  targetPosition: Position;
  zIndex: number;
  parentId?: string;
}
```

## Hiding handles

Never `display: none`. Use `visibility: hidden` or `opacity: 0`:
```svelte
<Handle type="source" position={Position.Bottom} style:visibility="hidden" />
```
