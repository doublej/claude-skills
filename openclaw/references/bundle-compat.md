# Bundle compatibility + Claude Code / Codex / Cursor interop

OpenClaw auto-detects and loads bundles from three other AI coding ecosystems in-place. This is the main interop surface if you're running Claude Code + OpenClaw side-by-side.

## Supported compatible bundle formats

| Bundle | Manifest path | Notes |
|---|---|---|
| **Codex** | `.codex-plugin/plugin.json` | Codex-compatible bundles + hook directories |
| **Claude** | `.claude-plugin/plugin.json` OR default Claude component layout (no manifest) | Reads skill roots, command-skills, `settings.json` defaults, `.lsp.json` / manifest `lspServers`, supported hook packs |
| **Cursor** | `.cursor-plugin/plugin.json` | Cursor-compatible command-skills |

OpenClaw **does not** validate these against the native `openclaw.plugin.json` schema. It reads bundle metadata + declared skill roots + defaults when the layout matches OpenClaw runtime expectations.

`openclaw plugins list` shows a `Format: bundle` column plus the detected subtype (`codex`, `claude`, `cursor`) in verbose output.

### Installing bundles

```bash
# Local path (auto-detect format)
openclaw plugins install ./my-claude-plugin

# Archive (.zip/.tgz/.tar.gz/.tar)
openclaw plugins install ./my-plugin.tgz

# Claude marketplace shorthand (uses ~/.claude/plugins/known_marketplaces.json)
openclaw plugins install <plugin>@<marketplace>

# Explicit marketplace source
openclaw plugins install <plugin> --marketplace <owner/repo>
openclaw plugins install <plugin> --marketplace https://github.com/<owner>/<repo>
openclaw plugins install <plugin> --marketplace ./my-marketplace
```

Marketplace sources can be:
- A Claude known-marketplace name from `~/.claude/plugins/known_marketplaces.json`
- A local marketplace root or `marketplace.json` path
- A GitHub repo shorthand (`owner/repo`)
- A GitHub repo URL
- A git URL

For remote marketplaces: plugin entries must stay inside the cloned marketplace repo. HTTP(S), absolute paths, git URLs, and other non-path plugin sources from remote manifests are **rejected**.

### What gets wired in today (Claude bundles)

- Skill roots + command-skills → loaded
- `settings.json` defaults → applied
- `.lsp.json` / manifest-declared `lspServers` → applied
- Hook packs in supported layouts → loaded
- Other detected capabilities → shown in diagnostics/info but **not yet** wired into runtime execution

## Claude Code ↔ OpenClaw bridge skills

### `openclaw-skill-claude-code` (VsevolodUstinov, upstream)

Async delegate pattern: OpenClaw agent launches long-running Claude Code tasks detached, gets heartbeat pings every 60s, receives the result through `sessions_send` when done.

**Architecture:**
```
OpenClaw agent (PM — coordinates, prioritizes, messages)
    ↓ nohup launch
Claude Code CLI (senior dev — executes, codes, researches)
    ↓ spawns
Claude Code sub-agents (junior devs — parallel subtasks)
```

**Notification flow:**
1. Task launches → WhatsApp/Telegram launch confirmation with task details
2. Every 60s → heartbeat ping (📡 prefix) shows tool calls + token count + current activity
3. On completion → result delivered two ways:
   - Direct WhatsApp/Telegram DM (you see it)
   - `sessions_send` to OpenClaw session (agent wakes, processes result, sends a summary)
4. On error/timeout/crash → same dual delivery

**Cost model.** Claude Code runs on a Max subscription → $0 per task regardless of length. OpenClaw's summary turn (that wakes on `sessions_send`) costs ~$0.01–$0.05 Sonnet-class. Changes the economics of always-on agents doing deep research/refactors.

**Requirements:**
- OpenClaw running locally (default port `18789`)
- Claude Code CLI (`claude`) installed + authenticated
- Claude Max subscription (for the $0 cost model)
- Python 3.10+ with `requests`
- WhatsApp/Telegram connected to OpenClaw

**Upstream:** `VsevolodUstinov/openclaw-skill-claude-code`. Multiple forks exist (hw10181913, rgzn7, fabianomonteiro, josgraha, denisonegin94-sketch, tjsx1, manthis/openclaw-skill-claude-usage) — upstream is VsevolodUstinov.

### `openclaw-skill-claude-code-setup` (rgzn7)

One-command bootstrapper wiring Claude Code ↔ OpenClaw both ways.

## MCP: reverse bridge (Claude.ai → OpenClaw)

### `freema/openclaw-mcp`

MCP server exposing OpenClaw Gateway tools to Claude.ai / Claude Desktop / Cursor / VS Code Copilot Chat with OAuth2 authentication. Plug it into the `mcpServers` section of your Claude client config.

### Other MCP bridges

| Repo | Role |
|---|---|
| `openclaw-mcp-plugin` (lunarpulse) | MCP over streamable HTTP |
| `openclaw-mcp-bridge` (AIWerk / ChrisLAS / gabrielekarra) | Bridges external MCP servers **into** OpenClaw via `registerTool` — so OpenClaw can consume MCP tools from the Claude/Cursor ecosystem |
| `openclaw-mcp-adapter` (androidStern) | Plugin exposing MCP server tools as native OpenClaw agent tools |
| `openclaw-mcp-server` (Helms-AI) | Exposes OpenClaw Gateway tools to MCP-compatible clients |

## OpenClaw's own MCP story

Per `VISION.md`: OpenClaw does NOT implement MCP first-class in core. It integrates via **`mcporter`** (github.com/steipete/mcporter). Rationale:
- Add/change MCP servers without restarting the Gateway
- Keep core tool/context surface lean
- Reduce MCP churn impact on core stability

If an MCP server or feature isn't supported, the project asks you to open an issue in `mcporter`, not OpenClaw.

## Shared memory across harnesses

### `ourmem/omem`

Persistent memory shared across agents with "space-based" scoping. Plugins for OpenCode, Claude Code, OpenClaw, and a standalone MCP server. Use when you want your Claude Code session and your always-on OpenClaw agent to see the same memory graph.

## Practical setups

### Setup A: OpenClaw as messenger-facing PM, Claude Code as autonomous dev

1. Install OpenClaw + run `openclaw onboard --install-daemon`
2. Connect WhatsApp or Telegram channel
3. Install `openclaw-skill-claude-code` into `~/.openclaw/skills/` (or `<project>/skills/`)
4. Authenticate Claude Code CLI (`claude auth` → use Max subscription)
5. Talk to OpenClaw from your phone → OpenClaw delegates to Claude Code → result pings back

### Setup B: Claude Desktop driving OpenClaw Gateway via MCP

1. Install `freema/openclaw-mcp` locally
2. Add it to Claude Desktop's `mcpServers` config
3. Complete OAuth2 flow
4. Claude.ai can now read/write OpenClaw Gateway state (sessions, channels, messages)

### Setup C: bidirectional — Claude sessions use OpenClaw tools AND OpenClaw agent delegates to Claude Code

1. Setup A for OpenClaw → Claude Code delegation
2. Setup B for Claude → OpenClaw MCP surface
3. Install `ourmem/omem` on both for shared memory
4. Optionally `openclaw-mcp-bridge` so OpenClaw's agent can consume any other MCP servers you have in the Claude ecosystem

## Gotchas

- **Port collision.** OpenClaw default `127.0.0.1:18789` — don't run two Gateways on one host. If you also run Claude Code in an unrelated server mode on 18789, change one of them.
- **Config file conflicts.** `openclaw plugins install @marketplace` reads `~/.claude/plugins/known_marketplaces.json` — make sure it exists + is valid JSON if you're using Claude marketplace shortcuts.
- **Bundle detection is strict.** Claude bundles without `.claude-plugin/plugin.json` must follow the default Claude component layout exactly. If detection fails, check `openclaw plugins inspect <id>` for the detected subtype.
- **Compatible bundle capabilities aren't all wired yet.** Detected != executed. Check `openclaw plugins inspect <id>` output for which capabilities are live.
