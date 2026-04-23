# Troubleshooting

## Blank canvas

1. Parent has no height. `<div style:height="100vh">` or a fixed px value.
2. Stylesheet missing. `import '@xyflow/svelte/dist/style.css'` once per app.
3. `nodes` is empty and `fitView` prop is set — try removing `fitView` or adding a node.

## Edges not rendering

1. Custom node missing `<Handle type="source" ... />` or `<Handle type="target" ... />`.
2. Handle uses `display: none` → switch to `visibility: hidden` or `opacity: 0`.
3. Edge references a node id that doesn't exist → console will warn.
4. `sourceHandle` / `targetHandle` point to an id that isn't on the node.
5. Edge `type` points to an `edgeTypes` key that isn't registered → falls back to default, but custom styling is ignored.

## "Couldn't create edge for source/target handle"

Source or target node wasn't measured yet (common during initial render + programmatic `addEdges`). Delay until `useNodesInitialized().current` is true, or call `useUpdateNodeInternals()` on the target.

## Reactivity "broken" — UI doesn't update

You're mutating `node.data` directly with `$state.raw`. Either reassign:
```ts
nodes = nodes.map(n => n.id === id ? { ...n, data: { ...n.data, x: 1 } } : n);
```
Or use the helper:
```ts
useSvelteFlow().updateNodeData(id, { x: 1 });
```

## `nodeTypes`/`edgeTypes` warning

> "It looks like you've created a new nodeTypes or edgeTypes object. If this wasn't on purpose, please define the object outside of the component."

Define at module scope, or wrap with `$derived`:
```ts
const nodeTypes = $derived({ custom: CustomNode });
```

## Cursor inside node input doesn't work / dragging instead of typing

Add `class="nodrag"` to the input/button/select.

## Scrolling inside a node zooms the canvas

Add `class="nowheel"` on the scrollable container.

## Node snaps back after drag

`onnodeschange` not wired and `bind:nodes` not used. Pick one:
- Easy: `<SvelteFlow bind:nodes bind:edges />`
- Controlled: pass `onnodeschange={(c) => nodes = applyNodeChanges(c, nodes)}`.

## Connection line appears but no edge is created

`onconnect` is missing. Either `bind:edges` (auto-wired) or add `onconnect={(c) => edges = addEdge(c, edges)}`.

## `window is not defined` in SvelteKit

Wrap with `{#if browser}` from `$app/environment`. See `ssr-sveltekit.md`.

## Sub-flow children render behind parent

Order: parent node must appear **before** children in the `nodes` array.

## Selection box doesn't appear

- `selectionOnDrag` not set.
- `panOnDrag` overrides selection for left mouse → set `panOnDrag={[1, 2]}` (middle/right only).

## MiniMap has wrong colors / flickers

`nodeColor` reads `data` reactively on each render; make it a pure function of `node` only.

## Hooks return stale data

You're accessing without `.current`. Hooks in v1 return `{ current }` — use `useNodes().current`, not the hook's return value directly.

## "Two versions of @xyflow/system installed"

Run `npm dedupe` or check that no dependency pulls in an older peer. Only one copy should exist in `node_modules`.

## Console floods with logs when dragging

Either a custom `onnodedrag` handler is doing heavy work or `$state` (not `$state.raw`) is tracking every position tick.

## Attribution is showing and you don't like it

It's required for free use. To remove it (Pro license), set:
```svelte
<SvelteFlow proOptions={{ hideAttribution: true }} />
```
