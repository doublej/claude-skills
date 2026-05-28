# Troubleshooting

> **Note:** This skill uses Claude-in-Chrome, not Playwright MCP.

## Diagnosis Flowchart

```
MCP tools available? (`mcp__claude-in-chrome__*`)
├─ NO  → Install extension
└─ YES → Connection working?
         ├─ NO  → Restart browser (don't reinstall!)
         └─ YES → Check PixiJS detection below
```

## Claude-in-Chrome Extension Issues

### 1. Chrome Not Running

If connection fails immediately, check if Chrome is running:

```bash
pgrep -x "Google Chrome" || echo "Chrome is not running"
```

**Solution:** Start Chrome and navigate to your PixiJS app first.

### 2. MCP Tools Missing

If `mcp__claude-in-chrome__*` tools don't exist at all:

**Solution:** Install the Claude-in-Chrome browser extension:
1. Install from Chrome Web Store or load unpacked
2. Configure MCP connection in Claude Code settings
3. Restart Claude Code

### 3. Tools Exist But Won't Connect

If MCP tools exist but return connection errors or timeouts:

**DO NOT reinstall the extension.** This is a browser state issue.

**Solution:** Restart the browser:
1. Close all Chrome windows completely
2. Reopen Chrome
3. Navigate to your PixiJS app
4. Retry the debug command

If still failing after browser restart:
- Check `chrome://extensions` - is the extension enabled?
- Check if the extension has permissions for the current domain

---

## PixiJS Detection Issues

### "PixiJS not found" Error

The debug scripts look for PixiJS in these locations (in order):
1. `window.__PIXI_DEVTOOLS__` - PixiJS DevTools extension
2. `window.__PIXI_APP__` - Common convention for exposing app
3. `window.__PIXI_STAGE__` / `window.__PIXI_RENDERER__` - Direct exposure

**Solutions:**

**Option 1: Expose your app globally (recommended)**
```javascript
// In your app initialization
const app = new Application();
await app.init({ ... });
window.__PIXI_APP__ = app;
```

**Option 2: Install PixiJS DevTools**
- Chrome extension that auto-detects PixiJS apps
- Exposes `__PIXI_DEVTOOLS__` automatically

**Option 3: Expose stage and renderer separately**
```javascript
window.__PIXI_STAGE__ = app.stage;
window.__PIXI_RENDERER__ = app.renderer;
```

### App Found But Stats Empty

The app may not have rendered yet. Ensure:
- `app.ticker` is running
- At least one frame has been rendered
- Stage has children added

---

## Output Issues

### Benchmark Shows 0 FPS

The benchmark forces synchronous renders. If FPS is 0:
- Page may be in background tab (browsers throttle)
- Renderer may be paused
- Duration may be too short (try 5000ms)

### Scene Graph Too Large

For complex scenes (>1000 nodes), use:
- `scene --flat` for compressed output
- `query <pattern>` to filter specific nodes
