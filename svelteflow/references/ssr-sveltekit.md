# SSR & SvelteKit

Svelte Flow reads DOM dimensions and attaches mouse/touch handlers. It cannot render on the server and is mostly useless in SSR output. Either render only in the browser, or render a minimal SSR-safe placeholder.

## Option 1: `{#if browser}` guard (simplest)

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { browser } from '$app/environment';
  import { SvelteFlow, Background, Controls } from '@xyflow/svelte';
  import '@xyflow/svelte/dist/style.css';

  let nodes = $state.raw([...]);
  let edges = $state.raw([...]);
</script>

<div style:width="100%" style:height="100vh">
  {#if browser}
    <SvelteFlow bind:nodes bind:edges fitView>
      <Background />
      <Controls />
    </SvelteFlow>
  {:else}
    <div class="placeholder">Loading flow…</div>
  {/if}
</div>
```

This prevents hydration mismatch warnings and server-side DOM access errors.

## Option 2: Dynamic `{#await}` import

Keeps the Svelte Flow chunk out of the initial SSR bundle:

```svelte
<script lang="ts">
  const flowModule = import('$lib/FlowCanvas.svelte');
</script>

{#await flowModule then { default: FlowCanvas }}
  <FlowCanvas />
{/await}
```

## Option 3: `onMount` mount

Render into a client-only container:

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { mount } from 'svelte';
  import FlowCanvas from '$lib/FlowCanvas.svelte';

  let target: HTMLDivElement;
  onMount(() => {
    const app = mount(FlowCanvas, { target });
    return () => app;
  });
</script>

<div bind:this={target} style:height="100vh"></div>
```

Usually overkill. Prefer option 1.

## Disable SSR for the route (if needed)

```ts
// +page.ts
export const ssr = false;
```

Use sparingly — costs you SEO/streaming for that route.

## Common SvelteKit errors

- `ReferenceError: window is not defined` → not guarded; wrap with `{#if browser}`.
- `Hydration mismatch` → your server HTML doesn't match client HTML after mount. Ensure the `{#if browser}` branch renders a stable placeholder on the server.
- Attribution panel flashes → fine, happens once per hydration. Ignore or preload CSS.
- Tailwind classes missing after hydration → ensure `@import '@xyflow/svelte/dist/style.css'` is above `@import 'tailwindcss'` in your `app.css`.

## vite.config

No special config required for v1. If you see circular-dep warnings from `@xyflow/system`, they are harmless.
