---
name: pixi-debug
description: Debug PixiJS applications in the browser via Claude-in-Chrome. Get scene stats, rendering info, textures, performance benchmarks. Use when user asks to debug, inspect, profile, or analyze a PixiJS app.
invocation: user
command: pixi-debug
arguments: "[command]"
---

# PixiJS Browser Debugger

Debug PixiJS applications running in Chrome using **Claude-in-Chrome** MCP tools.

> **Important:** This skill requires Claude-in-Chrome (not Playwright MCP).

## When to Use

- User asks to debug, inspect, or profile a PixiJS app
- Diagnosing rendering or performance issues
- Exploring scene graph structure
- Checking texture memory usage

## Prerequisites

Requires **Claude-in-Chrome** browser extension connected via MCP.

Check in order:
1. **Chrome not running?** → Start Chrome and navigate to the PixiJS app
2. **MCP tools missing?** (`mcp__claude-in-chrome__*` not available) → Install the extension
3. **Tools exist but won't connect?** → Restart browser (do NOT reinstall)

See [troubleshooting.md](references/troubleshooting.md) for details.

## Commands

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

## Best Practices

### Use Subagents
Use a subagent (Task tool) to run debug commands. This keeps the main conversation context clean and avoids polluting it with verbose scene graphs or benchmark data.

### Never Use Screenshots for Verification

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

## Implementation

```
Task(subagent_type="general-purpose", prompt="Use /pixi-debug to get stats from the PixiJS app at localhost:3000")
```

The subagent will:
1. Get tab context: `mcp__claude-in-chrome__tabs_context_mcp`
2. Execute scripts: `mcp__claude-in-chrome__javascript_tool`
3. Return a summarized result

Scripts are in [references/debug-scripts.md](references/debug-scripts.md).

## Quick Example

```javascript
// All-in-one info (version + renderer + stats)
mcp__claude-in-chrome__javascript_tool({
  action: 'javascript_exec',
  tabId: TAB_ID,
  text: '(() => { ... })()' // See debug-scripts.md
})
```

## Output Format

Present results clearly:
- **stats**: Table of node types and counts
- **rendering**: Config summary (type, size, resolution)
- **benchmark**: FPS and frame time percentiles (avg/min/max/p95)
- **scene --flat**: Path list for easy scanning
- **query**: Matching nodes with paths

## PixiJS Detection

Scripts detect PixiJS via (in order):
1. `window.__PIXI_DEVTOOLS__`
2. `window.__PIXI_APP__`
3. `window.__PIXI_STAGE__` / `window.__PIXI_RENDERER__`

If "PixiJS not found", the app must expose one of these globals. See [troubleshooting.md](references/troubleshooting.md).

## References

- [debug-scripts.md](references/debug-scripts.md) - JavaScript snippets
- [troubleshooting.md](references/troubleshooting.md) - Common issues and fixes
