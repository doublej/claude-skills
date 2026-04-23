---
name: svelteflow
description: Expert guidance for Svelte Flow (@xyflow/svelte v1+ with Svelte 5 runes). Build interactive node-based UIs, custom nodes and edges, handles, layouting (dagre/elkjs), state management with $state.raw, TypeScript, theming, SvelteKit SSR, and migration from v0. Use when writing Svelte Flow code, creating flow editors / diagrams / workflow builders / node-based canvases in Svelte, debugging blank canvas or edge rendering issues, migrating from Svelte Flow v0, or integrating @xyflow/svelte.
---

# Svelte Flow (@xyflow/svelte)

## Overview

Use this skill to build, customize, debug, and optimize interactive node-based UIs with Svelte Flow (`@xyflow/svelte` v1+, Svelte 5 only). Covers fundamentals, custom nodes/edges, state with runes, layouting, SvelteKit SSR, and v0→v1 migration.

## Agent behavior contract (follow these rules)

1. Always import from `@xyflow/svelte`. No legacy packages.
2. Always import the stylesheet once per app: `import '@xyflow/svelte/dist/style.css'` (or `base.css` for custom theming).
3. The `<SvelteFlow>` parent container **must** have explicit width and height — #1 cause of blank canvas.
4. Use `$state.raw(nodes)` and `$state.raw(edges)` — not deeply reactive `$state`. Mutations on individual node/edge properties do NOT trigger updates with `$state.raw`; reassign the array: `nodes = [...nodes]` or use `updateNode()` / `updateNodeData()` from `useSvelteFlow()`.
5. Use `bind:nodes` and `bind:edges` on `<SvelteFlow>` for two-way binding. For modules, pass getter/setter function bindings.
6. Define `nodeTypes` and `edgeTypes` **outside** the component or wrap with `$derived` to avoid re-renders.
7. Add `class="nodrag"` to interactive elements inside custom nodes (inputs, buttons, selects) so dragging the node doesn't swallow events.
8. Add `class="nowheel"` to scrollable elements inside custom nodes so they don't trigger zoom.
9. Add `class="nodrag nopan"` to edge labels that contain interactive content.
10. Hide handles with `visibility: hidden` or `opacity: 0` — never `display: none` (breaks layout math).
11. Assign unique `id` props to multiple handles of the same type on a single node.
12. After programmatically adding/removing handles, call `useUpdateNodeInternals()` with the node id to refresh.
13. Custom node/edge components read props via `let { id, data, selected }: NodeProps = $props()` (Svelte 5 runes only).
14. Hooks return `{ current }` objects in v1 — access via `nodes.current`, not a `$` store subscription.
15. For SvelteKit SSR, guard `<SvelteFlow>` with `{#if browser}` (from `$app/environment`) or render only after `onMount`.
16. v1 requires Svelte 5. Legacy Svelte 4 store patterns (`writable`) are removed.

## First 60 seconds (triage template)

- Clarify goal: new flow setup, custom nodes/edges, state mgmt, layouting, performance, theming, SSR, E2E, migration, or debugging.
- Collect facts:
  - Svelte Flow version (v0 uses stores; v1 uses runes). Check `package.json` for `@xyflow/svelte`.
  - Svelte version (v1 requires Svelte 5).
  - SvelteKit or plain Svelte + Vite?
  - TypeScript? Expected node count (affects perf strategy)? Styling (CSS / Tailwind)?
- Branch fast:
  - Migrating from v0 → `references/migration.md`
  - Blank canvas / missing nodes → container sizing OR missing CSS import → `references/troubleshooting.md`
  - Edges not rendering → missing `<Handle>` OR `display: none` on handle
  - Reactivity broken / updates don't reflect → `$state.raw` requires array reassignment → `references/state-management.md`
  - Connections don't create edges → missing `onconnect` handler or `addEdge` call
  - SSR error `window is not defined` → guard with `browser` or `onMount`
  - Layout / positioning → external layout library → `references/layouting.md`
  - Type errors on NodeProps → Svelte 5 generic patterns → `references/typescript.md`

## Routing map (read the right reference fast)

- Installation, setup, minimal flow, node/edge objects, key concepts → `references/fundamentals.md`
- Custom node components, `<Handle>`, multiple handles, `NodeProps` with `$props()` → `references/custom-nodes.md`
- Custom edges, `BaseEdge`, `getBezierPath`/`getSmoothStepPath`/`getStraightPath`, `EdgeLabel` → `references/custom-edges.md`
- `onnodeclick`, `onedgeclick`, `onconnect`, `onbeforeconnect`, selection, keyboard, connection validation → `references/interactivity.md`
- `$state.raw` pattern, `updateNode`/`updateNodeData`, controlled vs uncontrolled, hook returns with `.current` → `references/state-management.md`
- `Node<T>`, `Edge<T>`, `NodeProps<T>`, `EdgeProps<T>`, type guards, generic helpers → `references/typescript.md`
- dagre, elkjs, d3-hierarchy; sub-flows with parent nodes → `references/layouting.md`
- `<Background>`, `<Controls>`, `<MiniMap>`, `<Panel>`, `<NodeToolbar>`, `<NodeResizer>`, all hooks → `references/components-and-hooks.md`
- CSS variables, class overrides, Tailwind integration, colorMode, theming → `references/theming.md`
- SvelteKit SSR, `{#if browser}` guards, dynamic imports, hydration issues → `references/ssr-sveltekit.md`
- Memoization, `$derived` for stable refs, perf with large graphs → `references/performance.md`
- Blank canvas, edge issues, connection debugging, hydration errors → `references/troubleshooting.md`
- Playwright selectors, node/edge/viewport/connection tests → `references/e2e-testing.md`
- Undo/redo, copy/paste, save/restore, computed flows, sub-flows, dynamic handles → `references/advanced-patterns.md`
- Drag-and-drop sidebar, context menu add-node, detail panel, export as PNG → `references/recipes.md`
- v0 → v1 migration (stores → runes, bind props, hook return shape, API renames) → `references/migration.md`

## Common pitfalls → next best move

- Blank canvas, no errors → parent has no height; set `style:height="100vh"` or fixed px.
- Nodes render but no edges → custom nodes missing `<Handle>`, or handle has `display: none`.
- Edits to `node.data.foo` don't update UI → `$state.raw` doesn't deep-track; use `updateNodeData(id, { foo })` or reassign `nodes = [...nodes]`.
- `nodeTypes`/`edgeTypes` warning → defined inside component; move to module scope or wrap with `$derived`.
- Inputs inside nodes eat first click / drag the node instead → add `class="nodrag"`.
- Scrollable content zooms the canvas → add `class="nowheel"`.
- Multiple handles overlap → position with CSS `top` offsets AND assign unique `id` per handle.
- Programmatic handle added but edges won't connect → call `useUpdateNodeInternals()(nodeId)` after change.
- `window is not defined` in SvelteKit → wrap `<SvelteFlow>` in `{#if browser}` from `$app/environment`.
- v0 code won't compile on v1 → stores → `$state.raw`, `{nodes}`→`bind:nodes`, `$edges`→`edges.current`, `onEdgeCreate`→`onbeforeconnect`, `<EdgeLabelRenderer>`→`<EdgeLabel>`.
- Sub-flow children render behind parent → order parent nodes BEFORE children in the nodes array.

## Verification checklist

- `@xyflow/svelte/dist/style.css` imported exactly once.
- Parent container has explicit width AND height.
- `nodes` and `edges` declared with `$state.raw(...)`.
- `<SvelteFlow bind:nodes bind:edges>` (two-way binding).
- `nodeTypes` / `edgeTypes` defined at module scope or via `$derived`.
- Custom nodes include at least one `<Handle>` and use `$props()` with `NodeProps` type.
- SvelteKit routes wrap the component with `{#if browser}` or mount in `onMount`.
- Svelte version is 5.x; `@xyflow/svelte` is v1.x.
