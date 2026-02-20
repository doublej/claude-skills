# PixiJS Debug Scripts

JavaScript snippets for browser execution via `mcp__claude-in-chrome__javascript_tool`.

## Shared Utility

All scripts use this pattern to locate PixiJS:

```javascript
function findPixi() {
  const sources = [
    window.__PIXI_DEVTOOLS__,
    window.__PIXI_APP__,
    { stage: window.__PIXI_STAGE__, renderer: window.__PIXI_RENDERER__ }
  ];
  for (const s of sources) {
    if (s && (s.app || s.stage || s.renderer)) {
      return {
        stage: s.stage || s.app?.stage || window.__PIXI_STAGE__,
        renderer: s.renderer || s.app?.renderer || window.__PIXI_RENDERER__,
        version: s.version || window.PIXI?.VERSION || ''
      };
    }
  }
  return null;
}
```

---

## All-in-One Info Script

Returns version, renderer config, and node stats in one call.

```javascript
(() => {
  const findPixi = () => {
    const sources = [window.__PIXI_DEVTOOLS__, window.__PIXI_APP__, { stage: window.__PIXI_STAGE__, renderer: window.__PIXI_RENDERER__ }];
    for (const s of sources) {
      if (s && (s.app || s.stage || s.renderer)) {
        return { stage: s.stage || s.app?.stage || window.__PIXI_STAGE__, renderer: s.renderer || s.app?.renderer || window.__PIXI_RENDERER__, version: s.version || window.PIXI?.VERSION || '' };
      }
    }
    return null;
  };
  const getType = (c) => {
    if (!c) return 'Unknown';
    if (c.renderPipeId === 'text' || c.renderPipeId === 'htmlText' || c.renderPipeId === 'BitmapText') return 'Text';
    if (c.renderPipeId === 'graphics') return 'Graphics';
    if (c.renderPipeId === 'sprite') return 'Sprite';
    if (c.renderPipeId === 'mesh') return 'Mesh';
    if ('children' in c) return 'Container';
    return 'Unknown';
  };
  const collectStats = (c, s = { total: 0 }) => {
    if (!c) return s;
    const t = getType(c).toLowerCase();
    s[t] = (s[t] || 0) + 1;
    s.total++;
    if (c.children) c.children.forEach(x => collectStats(x, s));
    return s;
  };
  const p = findPixi();
  if (!p) return { error: 'PixiJS not found. Ensure app exposes __PIXI_APP__ or __PIXI_DEVTOOLS__.' };
  const r = p.renderer, canvas = r.canvas || r.view;
  return {
    version: p.version,
    renderer: { type: r.type === 2 ? 'WebGPU' : 'WebGL', width: canvas?.width, height: canvas?.height, resolution: r.resolution, background: r.background?.color?.toHex?.() },
    stats: collectStats(p.stage)
  };
})()
```

---

## Benchmark Script

Measures FPS over a duration. Pass duration in ms (default 3000).

```javascript
((duration = 3000) => {
  const p = window.__PIXI_APP__ || { stage: window.__PIXI_STAGE__, renderer: window.__PIXI_RENDERER__ };
  const { renderer, stage } = p.app || p;
  if (!renderer || !stage) return { error: 'PixiJS app not found' };
  const start = performance.now();
  const frames = [];
  while (performance.now() - start < duration) {
    const t = performance.now();
    renderer.render(stage);
    frames.push(performance.now() - t);
  }
  frames.sort((a, b) => a - b);
  const total = performance.now() - start;
  return {
    duration: Math.round(total),
    frames: frames.length,
    fps: (frames.length / (total / 1000)).toFixed(1),
    frameTime: {
      avg: (frames.reduce((a, b) => a + b, 0) / frames.length).toFixed(2),
      min: frames[0].toFixed(2),
      max: frames[frames.length - 1].toFixed(2),
      p95: frames[Math.floor(frames.length * 0.95)].toFixed(2)
    }
  };
})(3000)
```

---

## Scene Graph Script

Returns hierarchical scene tree. Pass `true` for flat list with paths.

```javascript
((flat = false) => {
  const findStage = () => {
    const s = window.__PIXI_DEVTOOLS__ || window.__PIXI_APP__ || { stage: window.__PIXI_STAGE__ };
    return s?.stage || s?.app?.stage || window.__PIXI_STAGE__;
  };
  const getType = (c) => {
    if (c.renderPipeId === 'text') return 'Text';
    if (c.renderPipeId === 'graphics') return 'Graphics';
    if (c.renderPipeId === 'sprite') return 'Sprite';
    if ('children' in c) return 'Container';
    return 'Unknown';
  };
  const build = (c, depth = 0) => {
    if (!c || depth > 50) return null;
    const node = { name: c.label || c.name || getType(c), type: getType(c), visible: c.visible, x: c.x, y: c.y, children: [] };
    if (c.children) c.children.forEach(x => { const n = build(x, depth + 1); if (n) node.children.push(n); });
    return node;
  };
  const flatten = (n, path = '', results = []) => {
    const p = path ? `${path}/${n.name}` : n.name;
    results.push({ path: p, type: n.type, visible: n.visible, childCount: n.children.length });
    n.children.forEach(c => flatten(c, p, results));
    return results;
  };
  const stage = findStage();
  if (!stage) return { error: 'Stage not found' };
  const tree = build(stage);
  return flat ? flatten(tree) : tree;
})(false)
```

---

## Textures Script

Lists all managed GPU textures.

```javascript
(() => {
  const r = window.__PIXI_APP__?.renderer || window.__PIXI_RENDERER__;
  if (!r?.texture?.managedTextures) return { error: 'Texture manager not accessible', textures: [] };
  return r.texture.managedTextures
    .filter(t => t.resource)
    .map(t => ({ label: t.label || 'unnamed', width: t.width, height: t.height, format: t.format }));
})()
```

---

## Query Script

Find nodes by name pattern (supports * wildcards).

```javascript
((pattern = '*') => {
  const findStage = () => {
    const s = window.__PIXI_DEVTOOLS__ || window.__PIXI_APP__ || { stage: window.__PIXI_STAGE__ };
    return s?.stage || s?.app?.stage || window.__PIXI_STAGE__;
  };
  const search = (c, regex, results = [], path = '') => {
    if (!c) return;
    const name = c.label || c.name || '';
    const currentPath = path ? `${path}/${name}` : name;
    if (regex.test(name)) results.push({ path: currentPath, name, x: c.x, y: c.y, visible: c.visible });
    if (c.children) c.children.forEach(x => search(x, regex, results, currentPath));
    return results;
  };
  const stage = findStage();
  if (!stage) return { error: 'Stage not found' };
  const regex = new RegExp(pattern.replace(/\*/g, '.*'), 'i');
  return search(stage, regex);
})('*Player*')
```
