---
name: pixijs-performance-optimizer
description: Analyze PixiJS code for performance issues and suggest optimizations. Use this skill when reviewing PixiJS applications for bottlenecks, memory leaks, or rendering inefficiencies.
---

# PixiJS Performance Optimizer

Analyze existing PixiJS code to identify performance issues and suggest targeted optimizations.

## When to Use

- Reviewing PixiJS code for performance bottlenecks
- Diagnosing slow rendering or high memory usage
- Auditing texture, sprite, and graphics usage
- Optimizing particle systems or complex scenes

## Performance Review Checklist

### 1. Texture Management
| Issue | Detection | Fix |
|-------|-----------|-----|
| Too many textures | Multiple `Texture.from()` calls for related images | Use spritesheets |
| Texture leaks | No `destroy()` calls on removed textures | Call `texture.destroy()` |
| Large textures | Single textures > 2048px | Split or compress |
| No resolution variants | Missing `@0.5x` versions | Add scaled variants |

### 2. Batching & Draw Calls
| Issue | Detection | Fix |
|-------|-----------|-----|
| Broken batches | Alternating sprite/graphics types | Group by type |
| Blend mode breaks | Different blend modes interleaved | Group same blend modes |
| Filter overhead | `container.filters` without `filterArea` | Define explicit `filterArea` |

### 3. Graphics Objects
| Issue | Detection | Fix |
|-------|-----------|-----|
| Redrawing every frame | `graphics.clear()` in ticker | Cache or use sprites |
| Complex shapes | > 100 points per graphic | Use textures instead |
| Many graphics objects | Hundreds of graphics | Convert to sprite-based |

### 4. Container Optimization
| Issue | Detection | Fix |
|-------|-----------|-----|
| Deep nesting | > 5 levels of containers | Flatten hierarchy |
| Missing cacheAsTexture | Static UI containers | Add `cacheAsTexture()` |
| Large cached textures | Cached containers > 4096px | Split into smaller parts |

### 5. Events & Interaction
| Issue | Detection | Fix |
|-------|-----------|-----|
| Unnecessary traversal | Interactive parent, non-interactive children | Set `interactiveChildren = false` |
| Missing hitArea | Complex interactive shapes | Define `hitArea` as Rectangle |

### 6. Text Rendering
| Issue | Detection | Fix |
|-------|-----------|-----|
| Text changes every frame | `text.text = ...` in ticker | Use BitmapText |
| High-res text | Default resolution on retina | Lower `resolution` property |

### 7. Memory & Cleanup
| Issue | Detection | Fix |
|-------|-----------|-----|
| No destroy on removal | `removeChild()` without `destroy()` | Always destroy removed objects |
| Stale references | Objects removed but referenced | Clear references |
| Event listener leaks | `on()` without `off()` | Remove listeners on destroy |

## Code Smell Patterns

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

## Quick Wins

1. **Enable culling** for off-screen objects: `displayObject.cullable = true`
2. **Use ParticleContainer** for > 100 similar sprites
3. **Set `interactiveChildren = false`** on non-interactive containers
4. **Define `filterArea`** when using filters
5. **Disable context alpha** on older devices: `useContextAlpha: false`

## Reference Files

See `references/` for:
- `performance-patterns.md` - Optimized code patterns
- `anti-patterns.md` - Common mistakes with fixes
- `profiling-guide.md` - How to measure and diagnose
