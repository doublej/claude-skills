# Interactivity

## Event handlers

Svelte 5 lowercase props on `<SvelteFlow>`:

```svelte
<SvelteFlow
  bind:nodes bind:edges
  onnodeclick={({ node, event }) => ...}
  onnodedragstart={({ node, nodes: dragged }) => ...}
  onnodedrag={({ node }) => ...}
  onnodedragstop={({ node }) => ...}
  onnodecontextmenu={({ node, event }) => ...}
  onedgeclick={({ edge, event }) => ...}
  onedgecontextmenu={({ edge, event }) => ...}
  onpaneclick={({ event }) => ...}
  onpanecontextmenu={({ event }) => ...}
  onconnect={(connection) => ...}
  onconnectstart={(connection) => ...}
  onconnectend={(event, connection) => ...}
  onbeforeconnect={(connection) => true | false | Edge}
  onbeforedelete={({ nodes, edges }) => true | false}
  onselectionchange={({ nodes, edges }) => ...}
  onmovestart={({ viewport }) => ...}
  onmove={({ viewport }) => ...}
  onmoveend={({ viewport }) => ...}
/>
```

## Connection validation

Block a connection before it's added:

```ts
function onbeforeconnect(connection: Connection): boolean {
  if (connection.source === connection.target) return false;
  const sourceNode = getNode(connection.source);
  if (sourceNode?.data.locked) return false;
  return true;
}
```

Return an `Edge` object to customize the created edge:
```ts
function onbeforeconnect(c: Connection): Edge {
  return { ...c, id: crypto.randomUUID(), type: 'custom-edge', animated: true };
}
```

## Per-handle validation

```svelte
<Handle
  type="source"
  position={Position.Bottom}
  isValidConnection={(connection) => connection.target !== 'blocked-node'}
/>
```

Returned edges from the connection line reflect validity styling automatically.

## Selection

```svelte
<SvelteFlow
  selectionMode="partial"              <!-- or "full" -->
  selectionOnDrag                       <!-- drag pane to select -->
  selectNodesOnDrag={false}
  multiSelectionKeyCode="Shift"
  deleteKeyCode="Backspace"
  panOnDrag={[1, 2]}                    <!-- middle/right mouse only -->
  onselectionchange={({ nodes: sel, edges: selE }) => {...}}
/>
```

## Keyboard

Built-in codes (pass `null` to disable):

```svelte
<SvelteFlow
  deleteKeyCode={['Delete', 'Backspace']}
  selectionKeyCode="Shift"
  multiSelectionKeyCode={['Meta', 'Control']}
  zoomActivationKeyCode="Meta"
  panActivationKeyCode="Space"
/>
```

Delete behavior goes through `onbeforedelete` — return `false` to block.

## Pane / viewport interactions

```svelte
<SvelteFlow
  panOnScroll               <!-- wheel pans instead of zooms -->
  panOnScrollSpeed={0.5}
  zoomOnScroll={false}
  zoomOnPinch
  zoomOnDoubleClick={false}
  preventScrolling={false}
  minZoom={0.1} maxZoom={4}
  translateExtent={[[-1000, -1000], [1000, 1000]]}
  nodeExtent={[[0, 0], [800, 800]]}
/>
```

## Programmatic interactions

```ts
const { fitView, setCenter, zoomTo, setViewport } = useSvelteFlow();

fitView({ padding: 0.2, duration: 400 });
setCenter(100, 200, { zoom: 1.5, duration: 500 });
zoomTo(2);
setViewport({ x: 0, y: 0, zoom: 1 }, { duration: 300 });
```

## Screen ↔ flow coordinates

```ts
const { screenToFlowPosition, flowToScreenPosition } = useSvelteFlow();

// e.g. drop a node at cursor
const pos = screenToFlowPosition({ x: event.clientX, y: event.clientY });
```
