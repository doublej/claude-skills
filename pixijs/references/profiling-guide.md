# PixiJS Profiling Guide

How to measure performance and diagnose bottlenecks.

## pixi-debug CLI (Recommended)

Use [pixi-devtools-cli](https://github.com/doublej/pixi-devtools-cli) for terminal-based profiling:

```bash
# Launch with debugging
pixi-debug launch http://localhost:3000

# Get performance stats
pixi-debug stats

# Capture frame with render analysis
pixi-debug capture

# Inspect scene hierarchy
pixi-debug scene --tree

# Query specific objects
pixi-debug query --type Sprite --name "player*"

# List all textures
pixi-debug textures --sort size

# Watch console output
pixi-debug console --level error
```

### Key Commands

| Command | Purpose |
|---------|---------|
| `stats` | Frame time, draw calls, memory |
| `capture` | Render pipeline analysis |
| `scene` | Display object hierarchy |
| `inspect` | Instruction tree with shader/texture details |
| `textures` | Texture inventory |
| `query` | Find objects by name/type/pattern |

Output is JSON - pipe to `jq` for filtering.

## Performance Targets

| Metric | Target (60fps) | Target (30fps) |
|--------|---------------|----------------|
| Frame time | < 16.67ms | < 33.33ms |
| JS time | < 8ms | < 16ms |
| Draw calls | < 100 | < 200 |
| Texture switches | < 20 | < 40 |
| Sprite count | < 10,000 | < 20,000 |

## GPU vs CPU Bound

**CPU Bound Signs:**
- JS execution time dominates
- Reducing object count helps
- Adding culling helps

**GPU Bound Signs:**
- Short JS time but long frames
- High texture memory
- Many draw calls or large textures
- Reducing resolution helps

## Common Bottlenecks

### 1. Too Many Draw Calls
**Diagnose:** `pixi-debug stats` - check draw call count
**Fix:** Use spritesheets, group by type, reduce filters

### 2. Texture Thrashing
**Diagnose:** `pixi-debug textures` - check count and sizes
**Fix:** Preload textures, use atlases

### 3. Memory Leak
**Diagnose:** `pixi-debug stats` over time - watch memory grow
**Fix:** Proper destroy() calls, remove listeners

### 4. Complex Geometry
**Diagnose:** `pixi-debug capture` - inspect render instructions
**Fix:** Convert to textures, simplify paths

### 5. Deep Scene Graph
**Diagnose:** `pixi-debug scene --tree` - check nesting depth
**Fix:** Flatten hierarchy, use render groups

## Quick Diagnostic Checklist

- [ ] Frame time under 16.67ms? (`pixi-debug stats`)
- [ ] Draw calls under 100? (`pixi-debug stats`)
- [ ] Textures using atlases? (`pixi-debug textures`)
- [ ] Scene graph flat? (`pixi-debug scene --tree`)
- [ ] No unused textures? (`pixi-debug textures`)
- [ ] Proper cleanup on scene change?
- [ ] Object pools for particles?
- [ ] Culling enabled for large worlds?
- [ ] Filters have filterArea set?
- [ ] Text using BitmapText where needed?
