# Custom Edges

## Minimal custom edge

```svelte
<!-- CustomEdge.svelte -->
<script lang="ts">
  import { BaseEdge, getBezierPath, type EdgeProps } from '@xyflow/svelte';

  let {
    sourceX, sourceY, targetX, targetY,
    sourcePosition, targetPosition,
    markerEnd, style,
  }: EdgeProps = $props();

  const [path] = $derived(getBezierPath({
    sourceX, sourceY, targetX, targetY,
    sourcePosition, targetPosition,
  }));
</script>

<BaseEdge {path} {markerEnd} {style} />
```

## Register edgeTypes

```svelte
<script lang="ts">
  import { SvelteFlow } from '@xyflow/svelte';
  import CustomEdge from './CustomEdge.svelte';

  const edgeTypes = { 'custom-edge': CustomEdge };
</script>

<SvelteFlow {edgeTypes} bind:nodes bind:edges />
```

Reference in edge objects: `{ ...edge, type: 'custom-edge' }`.

## Path utilities

All return `[path, labelX, labelY]`:

```ts
import { getBezierPath, getSmoothStepPath, getStraightPath } from '@xyflow/svelte';

getBezierPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition, curvature? });
getSmoothStepPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition, borderRadius?, centerX?, centerY?, offset? });
getStraightPath({ sourceX, sourceY, targetX, targetY });
```

## Edge label

Use `<EdgeLabel>` (formerly `<EdgeLabelRenderer>` in v0). It portals into the edge label layer. Always add `nodrag nopan` if label contains interactive content.

```svelte
<script lang="ts">
  import { BaseEdge, EdgeLabel, getSmoothStepPath, type EdgeProps } from '@xyflow/svelte';

  let props: EdgeProps = $props();
  const [path, labelX, labelY] = $derived(getSmoothStepPath(props));
</script>

<BaseEdge {path} markerEnd={props.markerEnd} />
<EdgeLabel
  x={labelX}
  y={labelY}
  class="nodrag nopan"
>
  <button onclick={() => console.log('clicked edge', props.id)}>×</button>
</EdgeLabel>
```

## EdgeProps fields

```ts
interface EdgeProps<T = Record<string, unknown>> {
  id: string;
  source: string;
  target: string;
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  sourcePosition: Position;
  targetPosition: Position;
  sourceHandleId?: string | null;
  targetHandleId?: string | null;
  animated: boolean;
  selected: boolean;
  label?: string;
  labelStyle?: string;
  data?: T;
  style?: string;
  markerStart?: string;
  markerEnd?: string;
  interactionWidth?: number;
}
```

## Markers / arrowheads

```svelte
<script lang="ts">
  import { MarkerType } from '@xyflow/svelte';

  let edges = $state.raw([
    {
      id: 'e1', source: '1', target: '2',
      markerEnd: { type: MarkerType.ArrowClosed, color: '#f00' },
    },
  ]);
</script>
```

## Custom SVG path

For non-standard shapes, build the `d` string yourself:

```ts
const path = `M ${sourceX} ${sourceY} Q ${midX} ${midY} ${targetX} ${targetY}`;
```

Then pass as `<BaseEdge {path} />`.

## Default edge types

- `default` → bezier
- `straight`
- `step`
- `smoothstep`
- `simplebezier`
