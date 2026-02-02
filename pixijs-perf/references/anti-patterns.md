# PixiJS Anti-Patterns

Common performance mistakes and their fixes.

## Texture Anti-Patterns

### Creating Textures in Loops
```javascript
// BAD: Creates texture lookup/cache check 1000x
for (let i = 0; i < 1000; i++) {
  const sprite = Sprite.from('particle.png');
  container.addChild(sprite);
}

// GOOD: Single texture, reused
const texture = Texture.from('particle.png');
for (let i = 0; i < 1000; i++) {
  const sprite = new Sprite(texture);
  container.addChild(sprite);
}
```

### Loading Individual Images
```javascript
// BAD: 50 HTTP requests, 50 textures, breaks batching
const images = ['a.png', 'b.png', /* ... 50 more */];
for (const img of images) {
  await Assets.load(img);
}

// GOOD: 1 request, 1 texture atlas, batches perfectly
await Assets.load('spritesheet.json');
```

### Forgetting to Destroy Textures
```javascript
// BAD: Memory leak on scene change
function changeScene() {
  container.removeChildren();
  // Textures still in GPU memory!
}

// GOOD: Clean up properly
function changeScene() {
  container.children.forEach(child => {
    child.destroy({ texture: true, baseTexture: true });
  });
}
```

## Graphics Anti-Patterns

### Rebuilding Graphics Every Frame
```javascript
// BAD: Rebuilds geometry every frame (expensive!)
app.ticker.add(() => {
  healthBar.clear();
  healthBar.rect(0, 0, health * 2, 20);
  healthBar.fill(0x00ff00);
});

// GOOD: Scale existing geometry
healthBar.rect(0, 0, 200, 20);
healthBar.fill(0x00ff00);
app.ticker.add(() => {
  healthBar.scale.x = health / 100;
});
```

### Using Graphics for Static Shapes
```javascript
// BAD: Graphics for hundreds of static objects
for (let i = 0; i < 500; i++) {
  const g = new Graphics();
  g.circle(0, 0, 10);
  g.fill(0xff0000);
  container.addChild(g);
}

// GOOD: Render to texture once, use sprites
const g = new Graphics();
g.circle(0, 0, 10);
g.fill(0xff0000);
const texture = app.renderer.generateTexture(g);
g.destroy();

for (let i = 0; i < 500; i++) {
  container.addChild(new Sprite(texture));
}
```

### Complex Graphics Objects
```javascript
// BAD: Complex path with many points
const g = new Graphics();
for (let i = 0; i < 1000; i++) {
  g.lineTo(points[i].x, points[i].y);
}
g.stroke({ width: 2, color: 0xffffff });
// Can't batch, slow to render

// GOOD: Use mesh or texture for complex shapes
const rope = new MeshRope({ texture, points });
```

## Container Anti-Patterns

### Deep Nesting Without Purpose
```javascript
// BAD: Unnecessary depth, slows transform updates
const wrapper1 = new Container();
const wrapper2 = new Container();
const wrapper3 = new Container();
wrapper1.addChild(wrapper2);
wrapper2.addChild(wrapper3);
wrapper3.addChild(actualContent);

// GOOD: Flat when possible
container.addChild(actualContent);
```

### Not Using cacheAsTexture for Static UI
```javascript
// BAD: Renders 50 children every frame
const settingsPanel = new Container();
// ... add 50 UI elements
stage.addChild(settingsPanel);

// GOOD: Single texture for static panel
const settingsPanel = new Container();
// ... add 50 UI elements
settingsPanel.cacheAsTexture();
```

### Caching Dynamic Content
```javascript
// BAD: Constant cache updates are expensive
const dynamicContainer = new Container();
dynamicContainer.cacheAsTexture();
app.ticker.add(() => {
  // Content changes every frame
  dynamicContainer.updateCacheTexture(); // Expensive!
});

// GOOD: Don't cache frequently changing content
const dynamicContainer = new Container();
// No caching - let it render normally
```

## Event Anti-Patterns

### Interactive on Everything
```javascript
// BAD: Every sprite checks for events
sprites.forEach(s => {
  s.eventMode = 'static'; // 10,000 hit tests!
});

// GOOD: One hit area on container
const bulletContainer = new Container();
bulletContainer.eventMode = 'static';
bulletContainer.interactiveChildren = false;
bulletContainer.hitArea = app.screen;
bulletContainer.on('pointerdown', (e) => {
  // Manually check which bullet was hit
});
```

### Not Removing Event Listeners
```javascript
// BAD: Listeners accumulate
function showDialog() {
  dialog.on('pointerdown', handleClick);
}

// GOOD: Clean up
function showDialog() {
  dialog.on('pointerdown', handleClick);
}
function hideDialog() {
  dialog.off('pointerdown', handleClick);
}
```

## Text Anti-Patterns

### Updating Text Every Frame
```javascript
// BAD: Text regenerates texture each update
app.ticker.add(() => {
  scoreText.text = `Score: ${score}`; // Slow!
});

// GOOD: BitmapText for frequent updates
const scoreText = new BitmapText({ style: { fontFamily: 'GameFont' } });
app.ticker.add(() => {
  scoreText.text = `Score: ${score}`; // Fast!
});

// ALTERNATIVE: Only update when value changes
let lastScore = -1;
app.ticker.add(() => {
  if (score !== lastScore) {
    scoreText.text = `Score: ${score}`;
    lastScore = score;
  }
});
```

### High Resolution Text
```javascript
// BAD: 4x memory on retina displays
const label = new Text({ text: 'Hello' });
// Uses devicePixelRatio by default

// GOOD: Control resolution
const label = new Text({
  text: 'Hello',
  resolution: 1, // or Math.min(2, devicePixelRatio)
});
```

## Filter Anti-Patterns

### Filters Without filterArea
```javascript
// BAD: Measures bounds every frame
container.filters = [new BlurFilter()];

// GOOD: Fixed filter area
container.filters = [new BlurFilter()];
container.filterArea = new Rectangle(0, 0, 800, 600);
```

### Empty Filters Array
```javascript
// BAD: Still allocates filter system
container.filters = [];

// GOOD: Null removes filter system entirely
container.filters = null;
```

### Filter on Large Container
```javascript
// BAD: Filter renders entire stage
stage.filters = [new BlurFilter()];

// GOOD: Filter only what needs it
const blurredLayer = new Container();
blurredLayer.filters = [new BlurFilter()];
blurredLayer.filterArea = new Rectangle(100, 100, 200, 200);
```

## Memory Anti-Patterns

### No Object Pooling for Particles
```javascript
// BAD: Constant allocation/GC
function spawnBullet() {
  const bullet = new Sprite(bulletTexture);
  bullets.addChild(bullet);
}
function removeBullet(bullet) {
  bullets.removeChild(bullet);
  bullet.destroy();
}

// GOOD: Pool and reuse
const bulletPool = [];
function spawnBullet() {
  const bullet = bulletPool.pop() || new Sprite(bulletTexture);
  bullet.visible = true;
  bullets.addChild(bullet);
  return bullet;
}
function removeBullet(bullet) {
  bullet.visible = false;
  bullets.removeChild(bullet);
  bulletPool.push(bullet);
}
```

### Creating Objects in Ticker
```javascript
// BAD: Allocations every frame trigger GC
app.ticker.add(() => {
  const pos = { x: sprite.x, y: sprite.y }; // New object!
  const color = new Color(0xff0000); // New object!
});

// GOOD: Reuse objects
const pos = { x: 0, y: 0 };
const color = new Color();
app.ticker.add(() => {
  pos.x = sprite.x;
  pos.y = sprite.y;
  color.setValue(0xff0000);
});
```

## Render Order Anti-Patterns

### Interleaved Types
```javascript
// BAD: Breaks batching constantly
container.addChild(sprite1);  // Batch 1
container.addChild(graphics1); // Batch 2 (flush)
container.addChild(sprite2);  // Batch 3
container.addChild(graphics2); // Batch 4 (flush)
// = 4 draw calls

// GOOD: Grouped by type
container.addChild(sprite1, sprite2);     // Batch 1
container.addChild(graphics1, graphics2); // Batch 2
// = 2 draw calls
```

### Mixed Blend Modes
```javascript
// BAD: Each blend mode change flushes batch
sprites.forEach((s, i) => {
  s.blendMode = i % 2 ? 'normal' : 'add';
  container.addChild(s);
});

// GOOD: Sort by blend mode
const normal = sprites.filter((_, i) => i % 2 === 0);
const additive = sprites.filter((_, i) => i % 2 === 1);
normal.forEach(s => container.addChild(s));
additive.forEach(s => {
  s.blendMode = 'add';
  container.addChild(s);
});
```
