# Performance

## The three rules

1. **`$state.raw`** for `nodes`/`edges`. Non-negotiable above ~100 nodes.
2. **Stable `nodeTypes` / `edgeTypes`** — define at module scope or `$derived`. Rebuilding the object remounts every node.
3. **Memoize heavy derived values** in custom nodes with `$derived(...)` — never recompute inside the template.

## Large graphs (500+ nodes)

- `onlyRenderVisibleElements` culls off-screen nodes: `<SvelteFlow onlyRenderVisibleElements />`.
- Disable MiniMap, or give it a cheap `nodeColor` function (avoid per-node reads of `data`).
- Avoid Tailwind `@apply` in custom nodes; inline class names render faster.
- Batch state updates: build the next `nodes` array once and assign, don't assign in a loop.

## Custom node perf

```svelte
<script lang="ts">
  import { useNodesData } from '@xyflow/svelte';
  let { id, data }: NodeProps = $props();

  // reactively read only specific upstream node data
  const upstream = useNodesData(['source-id']);
  const computed = $derived(expensive(upstream.current));
</script>
```

`useNodesData` subscribes to *data only*, not to position changes — far cheaper than re-reading via `useNodes()`.

## Avoid re-renders from object identity

```svelte
<script lang="ts">
  // ❌ new object each render; nodeTypes warning
  function render() {
    const nodeTypes = { custom: CustomNode };
  }

  // ✅ module scope
  const nodeTypes = { custom: CustomNode };

  // ✅ inside component, use $derived (stable for static refs)
  const nodeTypes2 = $derived({ custom: CustomNode });
</script>
```

## Handlers

Inline arrow functions in props (`onnodeclick={(e) => ...}`) are fine in Svelte 5 — no equivalent of the React re-render cost. But keep them small; heavy work should go through `useSvelteFlow()` helpers that batch internal updates.

## Batching updates via helpers

```ts
const { setNodes } = useSvelteFlow();
// one array rewrite vs. many
setNodes((prev) => prev.map(n => ({ ...n, data: { ...n.data, tick: n.data.tick + 1 } })));
```

## Profiling

- Chrome devtools performance: look for long `patch` tasks on drag — usually stale `nodeTypes` or per-property reactivity.
- Watch console for `[Svelte Flow]: The 'nodeTypes' prop…` — that warning directly signals a perf bug.
- Consider `<SvelteFlow nodeDragThreshold={4}>` to cut drag events when zoomed out.
