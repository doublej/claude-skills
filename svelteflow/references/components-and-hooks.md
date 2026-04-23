# Components & Hooks

## Components

### `<Background />`
```svelte
<Background variant="dots" gap={16} size={1} bgColor="#fafafa" patternColor="#ccc" />
```
`variant`: `'dots' | 'lines' | 'cross'`.

### `<Controls />`
Zoom in / out / fit / lock buttons. Render inside `<SvelteFlow>`.
```svelte
<Controls position="bottom-right" showZoom showFitView showLock orientation="vertical" />
```

### `<MiniMap />`
```svelte
<MiniMap
  nodeColor={(n) => n.data.color ?? '#ddd'}
  nodeStrokeWidth={3}
  zoomable pannable
  position="bottom-right"
/>
```

### `<Panel />`
Pins content to a viewport corner.
```svelte
<Panel position="top-left">
  <button onclick={save}>Save</button>
</Panel>
```
Positions: `top-left | top-center | top-right | bottom-left | bottom-center | bottom-right`.

### `<NodeToolbar />`
Render a toolbar anchored to a node. Place inside a **custom node**.
```svelte
<NodeToolbar position={Position.Top} offset={10} isVisible={selected}>
  <button onclick={duplicate}>Duplicate</button>
  <button onclick={del}>Delete</button>
</NodeToolbar>
```

### `<NodeResizer />`
Resize handles + control. Inside a custom node.
```svelte
<NodeResizer minWidth={80} minHeight={40} isVisible={selected} />
```

### `<Handle />`
```svelte
<Handle
  type="source | target"
  position={Position.Top | Right | Bottom | Left}
  id="optional-id"
  isConnectable={true}
  isValidConnection={(c) => boolean}
  style="..."
/>
```

### `<BaseEdge />` / `<EdgeLabel />`
See `custom-edges.md`.

## Hooks

All return `{ current }` (reactive) unless noted.

| Hook | Purpose |
|---|---|
| `useSvelteFlow()` | Grab helpers: `updateNode`, `updateNodeData`, `addNodes`, `fitView`, `screenToFlowPosition`, `setViewport`, `toObject`, ... (non-reactive callable functions) |
| `useNodes()` | `.current` → current `Node[]` |
| `useEdges()` | `.current` → current `Edge[]` |
| `useViewport()` | `.current` → `{ x, y, zoom }` |
| `useConnection()` | `.current` → active connection state while dragging from a handle |
| `useNodeConnections({ id?, type?, handleType?, handleId? })` | Edges connected to a node/handle |
| `useNodesData(ids)` | Reactively read `.data` of given node ids without subscribing to position changes |
| `useInternalNode(id)` | Full internal node (measured dimensions, absolute position) |
| `useNodesInitialized()` | `.current: boolean` once all nodes are measured |
| `useUpdateNodeInternals()` | Callable: `(nodeId | nodeId[]) => void`. Call after adding/removing handles |
| `useOnSelectionChange({ onChange })` | Register a selection listener |
| `useStore()` | Escape hatch to the internal store. Avoid unless necessary |

### Example: read connected edges

```svelte
<script lang="ts">
  import { useNodeConnections, type NodeProps } from '@xyflow/svelte';
  let { id }: NodeProps = $props();
  const connections = useNodeConnections({ id, handleType: 'target' });
</script>

<div>Incoming: {connections.current.length}</div>
```

### Example: react to viewport

```svelte
<script lang="ts">
  import { useViewport } from '@xyflow/svelte';
  const viewport = useViewport();
</script>

<p>zoom: {viewport.current.zoom.toFixed(2)}</p>
```
