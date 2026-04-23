# E2E Testing with Playwright

Svelte Flow's DOM is transformed (scale + translate) and its handles are small targets. Use class selectors and the `@xyflow/svelte` attributes.

## Useful selectors

| Target | Selector |
|---|---|
| Root | `.svelte-flow` |
| Viewport (transformed) | `.svelte-flow__viewport` |
| Pane (event surface) | `.svelte-flow__pane` |
| Any node | `.svelte-flow__node` |
| Node by id | `[data-id="NODE_ID"]` |
| Node by type | `.svelte-flow__node-custom` (replace `custom`) |
| Handle | `.svelte-flow__handle` |
| Handle on node | `[data-id="NODE_ID"] .svelte-flow__handle-right` |
| Edge | `.svelte-flow__edge` |
| Edge by id | `.svelte-flow__edge[data-id="EDGE_ID"]` |
| Controls button | `.svelte-flow__controls-button` |
| MiniMap | `.svelte-flow__minimap` |

## Drag a node

Playwright's `dragTo()` dispatches HTML5 drag events which Svelte Flow does not use. Use manual mouse events:

```ts
async function dragNode(page, id: string, dx: number, dy: number) {
  const node = page.locator(`[data-id="${id}"]`);
  const box = await node.boundingBox();
  if (!box) throw new Error('no box');
  const start = { x: box.x + box.width / 2, y: box.y + box.height / 2 };
  await page.mouse.move(start.x, start.y);
  await page.mouse.down();
  await page.mouse.move(start.x + dx / 2, start.y + dy / 2, { steps: 10 });
  await page.mouse.move(start.x + dx,     start.y + dy,     { steps: 10 });
  await page.mouse.up();
}
```

Move must be in multiple steps — single-step moves are ignored by the drag logic.

## Connect two handles

```ts
async function connect(page, from: string, fromHandle: 'right'|'bottom'|'left'|'top', to: string, toHandle: 'right'|'bottom'|'left'|'top') {
  const source = page.locator(`[data-id="${from}"] .svelte-flow__handle-${fromHandle}`);
  const target = page.locator(`[data-id="${to}"] .svelte-flow__handle-${toHandle}`);
  const sBox = await source.boundingBox();
  const tBox = await target.boundingBox();

  await page.mouse.move(sBox!.x + sBox!.width/2, sBox!.y + sBox!.height/2);
  await page.mouse.down();
  await page.mouse.move(tBox!.x + tBox!.width/2, tBox!.y + tBox!.height/2, { steps: 15 });
  await page.mouse.up();
}
```

## Assertions

```ts
await expect(page.locator('.svelte-flow__node')).toHaveCount(3);
await expect(page.locator('.svelte-flow__edge')).toHaveCount(2);
await expect(page.locator(`[data-id="node-1"]`)).toHaveAttribute('data-handlepos-top', /.+/);
await expect(page.locator('.svelte-flow__edge[data-id="e1-2"]')).toBeVisible();
```

## Viewport pan / zoom

```ts
// pan with modifier
await page.keyboard.down('Space');
await page.mouse.move(300, 300);
await page.mouse.down();
await page.mouse.move(500, 400, { steps: 10 });
await page.mouse.up();
await page.keyboard.up('Space');

// zoom
await page.locator('.svelte-flow__pane').hover();
await page.mouse.wheel(0, -500);
```

## Get serialized flow state for assertions

Expose `toObject()` in dev:

```svelte
<script lang="ts">
  import { useSvelteFlow } from '@xyflow/svelte';
  const sf = useSvelteFlow();
  // @ts-expect-error - test helper
  if (typeof window !== 'undefined') window.__flow = () => sf.toObject();
</script>
```

Then in test:

```ts
const flow = await page.evaluate(() => (window as any).__flow());
expect(flow.nodes).toHaveLength(3);
```

## Tips

- Give nodes stable ids; never rely on `nth-child`.
- Wait for `.svelte-flow__node` to be visible before interacting — layout can settle a frame or two after mount.
- Disable animations in tests: set `viewport` directly via `setViewport({x,y,zoom}, { duration: 0 })` via a test hook.
- In headed mode, `fitView` animation can race with drags; call `fitView({ duration: 0 })` first.
