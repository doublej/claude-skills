---
name: pixijs
description: >
  Unified PixiJS development skill. Use when:
  (1) building PixiJS applications — sprites, textures, containers, animations, interactions;
  (2) analyzing PixiJS code for performance bottlenecks, memory leaks, or rendering inefficiencies;
  (3) debugging a running PixiJS app in the browser via Claude-in-Chrome — scene stats, textures, benchmarks.
  Replaces pixijs-dev, pixijs-perf, pixi-debug.
---

# PixiJS Development Skill

Three branches. Pick the right one, or combine.

## Which Branch?

| Task | Branch |
|------|--------|
| Build PixiJS apps, sprites, textures, animations, interactions | [Development](#development) |
| Review code for performance bottlenecks, optimize rendering | [Performance](#performance) |
| Debug a running PixiJS app in Chrome, inspect scene graph | [Debugging](#debugging) |

---

## Shared Fundamentals

### Asset Loading

```js
import { Assets } from 'pixi.js';
await Assets.init({ manifest });
```

### Accessibility

```ts
import 'pixi.js/accessibility';
import { Container } from 'pixi.js';

const button = new Container();
button.accessible = true;
```

### PixiJS Detection (Browser Globals)

Scripts detect PixiJS via (in order):
1. `window.__PIXI_DEVTOOLS__`
2. `window.__PIXI_APP__`
3. `window.__PIXI_STAGE__` / `window.__PIXI_RENDERER__`

If your app is not detected, expose one of these globals:

```javascript
// Recommended: expose the app
const app = new Application();
await app.init({ ... });
window.__PIXI_APP__ = app;
```

### Never Ship

- `Texture.from()` in loops without reusing the texture
- `removeChild()` without `destroy()` — memory leak
- `graphics.clear()` in ticker — rebuild geometry every frame
- Filters without `filterArea` — bounds measured every frame
- `container.filters = []` — use `null` to fully remove
- `on()` without matching `off()` — listener leak

---

## Development

Build 2D graphics, games, and interactive applications with PixiJS.

### When to Use

- Building PixiJS applications
- Working with sprites, textures, containers
- Implementing animations and interactions
- Setting up asset loading and manifests

### Documentation Links

The `references/llms.md` file contains the full PixiJS documentation table of contents with links to all guides:

| Topic | Content |
|-------|---------|
| Getting Started | Ecosystem, Quick Start |
| Concepts | Architecture, Environments, Garbage Collection, Performance Tips, Render Groups, Render Layers, Render Loop, Scene Graph |
| Components | Accessibility, Assets, Color, Events, Filters/Blend Modes, Math, Renderers, Textures, Ticker |
| Scene Objects | Container, Graphics, Mesh, NineSlice Sprite, Particle Container, Sprite, Text, Tiling Sprite |
| Application | Application, CullerPlugin, ResizePlugin, TickerPlugin |
| Assets | Background Loader, Bundles/Manifests, Compressed Textures, Resolver, SVGs |
| Text | BitmapText, Canvas Text, HTML Text, SplitText, Text Style |
| Advanced | Cache As Texture, Graphics Fill, Graphics Pixel Line, Mixing PixiJS and Three.js |
| Migration | v8 Migration Guide |

### Reference Files

- `references/llms.md` — Documentation table of contents with links
- `references/llms-txt.md` — Full text of all documentation pages (53 pages)
- `references/llms-full.md` — Complete documentation dump including API details
- `references/other.md` — Additional API doc links
- `references/index.md` — Reference file index

---

## Performance

Analyze existing PixiJS code to identify performance issues and suggest targeted optimizations.

### When to Use

- Reviewing PixiJS code for performance bottlenecks
- Diagnosing slow rendering or high memory usage
- Auditing texture, sprite, and graphics usage
- Optimizing particle systems or complex scenes

### Performance Targets

| Metric | Target (60fps) | Target (30fps) |
|--------|---------------|----------------|
| Frame time | < 16.67ms | < 33.33ms |
| JS time | < 8ms | < 16ms |
| Draw calls | < 100 | < 200 |
| Texture switches | < 20 | < 40 |
| Sprite count | < 10,000 | < 20,000 |

### Performance Review Checklist

#### 1. Texture Management

| Issue | Detection | Fix |
|-------|-----------|-----|
| Too many textures | Multiple `Texture.from()` calls for related images | Use spritesheets |
| Texture leaks | No `destroy()` calls on removed textures | Call `texture.destroy()` |
| Large textures | Single textures > 2048px | Split or compress |
| No resolution variants | Missing `@0.5x` versions | Add scaled variants |

#### 2. Batching & Draw Calls

| Issue | Detection | Fix |
|-------|-----------|-----|
| Broken batches | Alternating sprite/graphics types | Group by type |
| Blend mode breaks | Different blend modes interleaved | Group same blend modes |
| Filter overhead | `container.filters` without `filterArea` | Define explicit `filterArea` |

#### 3. Graphics Objects

| Issue | Detection | Fix |
|-------|-----------|-----|
| Redrawing every frame | `graphics.clear()` in ticker | Cache or use sprites |
| Complex shapes | > 100 points per graphic | Use textures instead |
| Many graphics objects | Hundreds of graphics | Convert to sprite-based |

#### 4. Container Optimization

| Issue | Detection | Fix |
|-------|-----------|-----|
| Deep nesting | > 5 levels of containers | Flatten hierarchy |
| Missing cacheAsTexture | Static UI containers | Add `cacheAsTexture()` |
| Large cached textures | Cached containers > 4096px | Split into smaller parts |

#### 5. Events & Interaction

| Issue | Detection | Fix |
|-------|-----------|-----|
| Unnecessary traversal | Interactive parent, non-interactive children | Set `interactiveChildren = false` |
| Missing hitArea | Complex interactive shapes | Define `hitArea` as Rectangle |

#### 6. Text Rendering

| Issue | Detection | Fix |
|-------|-----------|-----|
| Text changes every frame | `text.text = ...` in ticker | Use BitmapText |
| High-res text | Default resolution on retina | Lower `resolution` property |

#### 7. Memory & Cleanup

| Issue | Detection | Fix |
|-------|-----------|-----|
| No destroy on removal | `removeChild()` without `destroy()` | Always destroy removed objects |
| Stale references | Objects removed but referenced | Clear references |
| Event listener leaks | `on()` without `off()` | Remove listeners on destroy |

### GPU vs CPU Bound

**CPU Bound Signs:**
- JS execution time dominates
- Reducing object count helps
- Adding culling helps

**GPU Bound Signs:**
- Short JS time but long frames
- High texture memory
- Many draw calls or large textures
- Reducing resolution helps

### Code Smell Patterns

```javascript
// BAD: Creating textures in a loop
for (let i = 0; i < 100; i++) {
  const sprite = Sprite.from('image.png'); // Creates new texture each time
}

// GOOD: Reuse texture
const texture = Texture.from('image.png');
for (let i = 0; i < 100; i++) {
  const sprite = new Sprite(texture);
}
```

```javascript
// BAD: Rebuilding graphics every frame
app.ticker.add(() => {
  graphics.clear();
  graphics.rect(0, 0, width, height);
  graphics.fill(0xff0000);
});

// GOOD: Only update transforms
graphics.rect(0, 0, width, height);
graphics.fill(0xff0000);
app.ticker.add(() => {
  graphics.x = newX; // Transforms are cheap
});
```

```javascript
// BAD: No cleanup
container.removeChild(sprite);

// GOOD: Proper cleanup
container.removeChild(sprite);
sprite.destroy({ children: true, texture: false });
```

### Quick Wins

1. **Enable culling** for off-screen objects: `displayObject.cullable = true`
2. **Use ParticleContainer** for > 100 similar sprites
3. **Set `interactiveChildren = false`** on non-interactive containers
4. **Define `filterArea`** when using filters
5. **Disable context alpha** on older devices: `useContextAlpha: false`
6. **Use render groups** for static backgrounds: `container.isRenderGroup = true`
7. **Object pool** particles and bullets instead of create/destroy cycles
8. **Use BitmapText** for text that changes every frame

### Reference Files

- `references/performance-patterns.md` — Optimized code patterns (spritesheets, batching, containers, particles, filters, events, text, culling, pooling)
- `references/anti-patterns.md` — Common mistakes with fixes (textures, graphics, containers, events, text, filters, memory, render order)
- `references/profiling-guide.md` — How to measure and diagnose with performance targets

---

## Debugging

Debug PixiJS applications running in Chrome using **Claude-in-Chrome** MCP tools.

> **Important:** This skill requires Claude-in-Chrome (not Playwright MCP).

### When to Use

- User asks to debug, inspect, or profile a PixiJS app
- Diagnosing rendering or performance issues in a running app
- Exploring scene graph structure
- Checking texture memory usage

### Prerequisites

Requires **Claude-in-Chrome** browser extension connected via MCP.

Check in order:
1. **Chrome not running?** -> Start Chrome and navigate to the PixiJS app
2. **MCP tools missing?** (`mcp__claude-in-chrome__*` not available) -> Install the extension
3. **Tools exist but won't connect?** -> Restart browser (do NOT reinstall)

See [troubleshooting.md](references/troubleshooting.md) for details.

### Commands

| Command | Description |
|---------|-------------|
| `info` | PixiJS version and app info |
| `stats` | Node counts by type |
| `rendering` | Renderer config (WebGL/WebGPU, size, resolution) |
| `textures` | List GPU textures |
| `scene` | Full scene graph |
| `scene --flat` | Flat node list with paths |
| `capture` | Performance capture (render times, memory) |
| `benchmark [ms]` | FPS benchmark (default 3000ms) |
| `query <pattern>` | Find nodes by name pattern |
| (no args) | Show all basic info |

### Best Practices

#### Use Subagents

Use a subagent (Task tool) to run debug commands. This keeps the main conversation context clean and avoids polluting it with verbose scene graphs or benchmark data.

```
Task(subagent_type="general-purpose", prompt="Use /pixi-debug to get stats from the PixiJS app at localhost:3000")
```

The subagent will:
1. Get tab context: `mcp__claude-in-chrome__tabs_context_mcp`
2. Execute scripts: `mcp__claude-in-chrome__javascript_tool`
3. Return a summarized result

#### Never Use Screenshots for Verification

**Do NOT use screenshots to verify fixes or debug issues.** Screenshots are:
- Imprecise (visual approximation, not ground truth)
- Unreliable for detecting subtle changes
- A waste of agent strengths

Instead, **use programmatic inspection**:
- Read actual application state (`app.stage.children.length`)
- Trace functionality into deep object hierarchies
- Measure exact values (positions, dimensions, alpha, visibility)
- Compare before/after numerical data

```javascript
// BAD: "Take a screenshot to see if the player moved"
// GOOD: Get exact position
const player = stage.children.find(c => c.label === 'Player');
return { x: player.x, y: player.y, visible: player.visible };
```

Agents excel at reading data structures and tracing code paths. Use these strengths.

### Quick Example

```javascript
// All-in-one info (version + renderer + stats)
mcp__claude-in-chrome__javascript_tool({
  action: 'javascript_exec',
  tabId: TAB_ID,
  text: '(() => { ... })()' // See debug-scripts.md
})
```

### Output Format

Present results clearly:
- **stats**: Table of node types and counts
- **rendering**: Config summary (type, size, resolution)
- **benchmark**: FPS and frame time percentiles (avg/min/max/p95)
- **scene --flat**: Path list for easy scanning
- **query**: Matching nodes with paths

### Common Bottlenecks (Diagnosis via Debug Tools)

| Bottleneck | Diagnose | Fix |
|------------|----------|-----|
| Too many draw calls | `stats` — check draw call count | Spritesheets, group by type, reduce filters |
| Texture thrashing | `textures` — check count and sizes | Preload textures, use atlases |
| Memory leak | `stats` over time — watch memory grow | Proper `destroy()` calls, remove listeners |
| Complex geometry | `capture` — inspect render instructions | Convert to textures, simplify paths |
| Deep scene graph | `scene` — check nesting depth | Flatten hierarchy, use render groups |

### Quick Diagnostic Checklist

- [ ] Frame time under 16.67ms? (`stats`)
- [ ] Draw calls under 100? (`stats`)
- [ ] Textures using atlases? (`textures`)
- [ ] Scene graph flat? (`scene`)
- [ ] No unused textures? (`textures`)
- [ ] Proper cleanup on scene change?
- [ ] Object pools for particles?
- [ ] Culling enabled for large worlds?
- [ ] Filters have filterArea set?
- [ ] Text using BitmapText where needed?

### Reference Files

- `references/debug-scripts.md` — JavaScript snippets for browser execution
- `references/troubleshooting.md` — Common issues and fixes (Chrome extension, PixiJS detection, output)

---

## Reference Files (All)

### Development
- `references/llms.md` — Documentation table of contents with links
- `references/llms-txt.md` — Full text of all documentation pages (53 pages)
- `references/llms-full.md` — Complete documentation dump including API details
- `references/other.md` — Additional API doc links
- `references/index.md` — Reference file index

### Performance
- `references/performance-patterns.md` — Optimized code patterns
- `references/anti-patterns.md` — Common mistakes with fixes
- `references/profiling-guide.md` — How to measure and diagnose

### Debugging
- `references/debug-scripts.md` — JavaScript snippets for browser execution
- `references/troubleshooting.md` — Common issues and fixes
