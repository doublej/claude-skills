# PixiJS Performance Patterns

## Texture Optimization

### Spritesheet Loading
```javascript
// Load spritesheet instead of individual images
await Assets.load('spritesheet.json');
const sprite = Sprite.from('frame1.png'); // Uses atlas
```

### Texture Resolution Variants
```javascript
// File naming convention for auto-resolution
// image.png      - Full resolution
// image@0.5x.png - Half resolution (auto-selected on low-DPI)

await Assets.load('image.png'); // Resolver picks appropriate version
```

### Manual Texture Cleanup
```javascript
// Stagger destruction to prevent frame drops
const textures = [...texturesToDestroy];
textures.forEach((tex, i) => {
  setTimeout(() => tex.destroy(), i * 16); // ~1 per frame
});
```

## Batching Optimization

### Group by Render Type
```javascript
// BAD: Interleaved types break batches
container.addChild(sprite1);
container.addChild(graphics1);
container.addChild(sprite2);
container.addChild(graphics2);

// GOOD: Grouped types batch efficiently
const spriteLayer = new Container();
const graphicsLayer = new Container();
spriteLayer.addChild(sprite1, sprite2);
graphicsLayer.addChild(graphics1, graphics2);
container.addChild(spriteLayer, graphicsLayer);
```

### Blend Mode Grouping
```javascript
// Group same blend modes together
const normalBlend = new Container();
const additiveBlend = new Container();

normalSprites.forEach(s => normalBlend.addChild(s));
additiveSprites.forEach(s => {
  s.blendMode = 'add';
  additiveBlend.addChild(s);
});
```

## Container Optimization

### Cache Static Content
```javascript
// Static UI panel - cache it
const uiPanel = new Container();
uiPanel.addChild(background, icon, label);
uiPanel.cacheAsTexture(); // Single draw call now

// Update only when content changes
function updateLabel(text) {
  label.text = text;
  uiPanel.updateCacheTexture();
}
```

### Render Groups for Complex Scenes
```javascript
// Separate static background from dynamic gameplay
const background = new Container();
background.isRenderGroup = true; // GPU-optimized transforms

const gameLayer = new Container();
// gameLayer updates every frame, background rarely changes
```

### Flatten Deep Hierarchies
```javascript
// BAD: Deep nesting
const root = new Container();
const level1 = new Container();
const level2 = new Container();
const level3 = new Container();
root.addChild(level1);
level1.addChild(level2);
level2.addChild(level3);
level3.addChild(sprite);

// GOOD: Flat structure with calculated positions
const root = new Container();
sprite.x = combinedX;
sprite.y = combinedY;
root.addChild(sprite);
```

## Particle Systems

### ParticleContainer for Large Counts
```javascript
const particles = new ParticleContainer({
  dynamicProperties: {
    position: true,  // Updates every frame
    rotation: true,  // Updates every frame
    scale: false,    // Static - set once
    tint: false,     // Static - set once
  },
});

// Create particles
for (let i = 0; i < 10000; i++) {
  const p = new Particle({ texture: sparkTexture });
  particles.addParticle(p);
}

// Update loop - only position/rotation uploaded to GPU
app.ticker.add(() => {
  for (const p of particles.particleChildren) {
    p.x += p.vx;
    p.y += p.vy;
  }
});
```

## Filter Optimization

### Define Filter Area
```javascript
// BAD: PixiJS measures bounds every frame
container.filters = [blurFilter];

// GOOD: Explicit bounds, no measurement
container.filters = [blurFilter];
container.filterArea = new Rectangle(0, 0, 800, 600);
```

### Clear Unused Filters
```javascript
// Remove filters when not needed
container.filters = null; // Not empty array!
```

## Event Optimization

### Disable Child Traversal
```javascript
// Container with many non-interactive children
const bulletContainer = new Container();
bulletContainer.eventMode = 'static';
bulletContainer.interactiveChildren = false; // Skip children
bulletContainer.hitArea = new Rectangle(0, 0, 800, 600);
```

### Simple Hit Areas
```javascript
// BAD: Complex shape requires point-in-polygon
sprite.eventMode = 'static';

// GOOD: Rectangle hit area
sprite.eventMode = 'static';
sprite.hitArea = new Rectangle(0, 0, sprite.width, sprite.height);
```

## Text Optimization

### BitmapText for Dynamic Text
```javascript
// Install bitmap font
BitmapFont.install({
  name: 'ScoreFont',
  style: { fontFamily: 'Arial', fontSize: 32 },
});

// Use for frequently changing text
const score = new BitmapText({
  text: '0',
  style: { fontFamily: 'ScoreFont' },
});

// Updates are cheap
app.ticker.add(() => {
  score.text = String(currentScore);
});
```

### Lower Text Resolution
```javascript
// Reduce memory for large text
const text = new Text({
  text: 'Hello',
  style: { fontSize: 48 },
  resolution: 1, // Instead of window.devicePixelRatio
});
```

## Culling

### Enable for Off-screen Objects
```javascript
// Large scrolling world
worldContainer.children.forEach(child => {
  child.cullable = true;
});

// Or use CullerPlugin
import { extensions, CullerPlugin } from 'pixi.js';
extensions.add(CullerPlugin);
```

## Memory Patterns

### Object Pooling
```javascript
class BulletPool {
  constructor(texture, size = 100) {
    this.pool = [];
    this.texture = texture;
    for (let i = 0; i < size; i++) {
      this.pool.push(new Sprite(texture));
    }
  }

  get() {
    return this.pool.pop() || new Sprite(this.texture);
  }

  release(bullet) {
    bullet.visible = false;
    this.pool.push(bullet);
  }
}
```

### Proper Cleanup
```javascript
function destroyScene(container) {
  // Remove all event listeners
  container.removeAllListeners();

  // Destroy children recursively
  container.destroy({
    children: true,
    texture: false, // Keep shared textures
    baseTexture: false,
  });
}
```
