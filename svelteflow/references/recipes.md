# Recipes

## Drag-and-drop sidebar → canvas

```svelte
<!-- Sidebar.svelte -->
<script>
  function ondragstart(e, type) {
    e.dataTransfer.setData('application/svelteflow', type);
    e.dataTransfer.effectAllowed = 'move';
  }
</script>

<aside>
  <div draggable="true" ondragstart={(e) => ondragstart(e, 'input')}>Input node</div>
  <div draggable="true" ondragstart={(e) => ondragstart(e, 'default')}>Default node</div>
</aside>
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { SvelteFlow, useSvelteFlow } from '@xyflow/svelte';
  const { screenToFlowPosition } = useSvelteFlow();

  let nodes = $state.raw([]);
  let edges = $state.raw([]);

  function ondragover(e: DragEvent) {
    e.preventDefault();
    e.dataTransfer!.dropEffect = 'move';
  }
  function ondrop(e: DragEvent) {
    e.preventDefault();
    const type = e.dataTransfer?.getData('application/svelteflow');
    if (!type) return;
    const position = screenToFlowPosition({ x: e.clientX, y: e.clientY });
    nodes = [...nodes, { id: crypto.randomUUID(), type, position, data: { label: type } }];
  }
</script>

<div style:height="100vh" {ondragover} {ondrop}>
  <SvelteFlow bind:nodes bind:edges fitView />
</div>
```

## Context menu — add node on right-click

```svelte
<script lang="ts">
  import { SvelteFlow, useSvelteFlow } from '@xyflow/svelte';
  const { screenToFlowPosition } = useSvelteFlow();

  let menu = $state<{ x: number; y: number } | null>(null);

  function onpanecontextmenu({ event }) {
    event.preventDefault();
    menu = { x: event.clientX, y: event.clientY };
  }

  function addHere(type: string) {
    if (!menu) return;
    const position = screenToFlowPosition(menu);
    nodes = [...nodes, { id: crypto.randomUUID(), type, position, data: { label: type } }];
    menu = null;
  }
</script>

<SvelteFlow bind:nodes bind:edges {onpanecontextmenu} />

{#if menu}
  <div class="menu" style:top="{menu.y}px" style:left="{menu.x}px">
    <button onclick={() => addHere('default')}>Default node</button>
    <button onclick={() => addHere('input')}>Input node</button>
  </div>
{/if}
```

## Detail panel for selected node

```svelte
<script lang="ts">
  import { useNodes } from '@xyflow/svelte';
  const all = useNodes();
  const selected = $derived(all.current.find(n => n.selected));
</script>

{#if selected}
  <aside class="details">
    <h3>{selected.id}</h3>
    <pre>{JSON.stringify(selected.data, null, 2)}</pre>
  </aside>
{/if}
```

## Export canvas as PNG

Use [`html-to-image`](https://github.com/bubkoo/html-to-image):

```bash
npm install html-to-image
```

```ts
import { toPng } from 'html-to-image';
import { useSvelteFlow } from '@xyflow/svelte';

const { getNodes } = useSvelteFlow();

async function exportPng() {
  const nodes = getNodes();
  const [minX, minY, maxX, maxY] = nodes.reduce(
    ([l, t, r, b], n) => [
      Math.min(l, n.position.x),
      Math.min(t, n.position.y),
      Math.max(r, n.position.x + (n.width ?? 150)),
      Math.max(b, n.position.y + (n.height ?? 40)),
    ],
    [Infinity, Infinity, -Infinity, -Infinity]
  );

  const width = maxX - minX + 100;
  const height = maxY - minY + 100;

  const viewport = document.querySelector('.svelte-flow__viewport') as HTMLElement;
  const url = await toPng(viewport, {
    backgroundColor: '#ffffff',
    width,
    height,
    style: {
      width: `${width}px`,
      height: `${height}px`,
      transform: `translate(${-minX + 50}px, ${-minY + 50}px) scale(1)`,
    },
  });

  const a = document.createElement('a');
  a.href = url;
  a.download = 'flow.png';
  a.click();
}
```

## Animated data flow dots

Simple CSS animation on custom edge:

```svelte
<BaseEdge {path} class="data-flow" />

<style>
  :global(.data-flow) {
    stroke-dasharray: 5;
    animation: dashdraw 0.6s linear infinite;
  }
  @keyframes dashdraw { to { stroke-dashoffset: -10; } }
</style>
```

## Fit view on initial load after async data

```svelte
<script lang="ts">
  import { useNodesInitialized, useSvelteFlow } from '@xyflow/svelte';
  const initialized = useNodesInitialized();
  const { fitView } = useSvelteFlow();

  $effect(() => {
    if (initialized.current) queueMicrotask(() => fitView({ padding: 0.2 }));
  });
</script>
```
