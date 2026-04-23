---
name: openclaw
description: Reference for OpenClaw — the self-hosted personal AI assistant (github.com/openclaw/openclaw, docs.openclaw.ai). Covers gateway architecture, CLI (`openclaw` + `clawhub`), skills format, plugin system (`openclaw.plugin.json` + plugin-sdk), messaging channels, and Claude/Codex/Cursor bundle compatibility. Use when writing/debugging OpenClaw skills or plugins, bridging OpenClaw and Claude Code, interpreting `~/.openclaw/` state, reading docs.openclaw.ai, or advising a user running OpenClaw alongside Claude Code.
---

# OpenClaw

**What it is.** Self-hosted personal AI assistant. TypeScript/ESM, Node 22+ (Node 24 recommended) or Bun. MIT. Runs a long-lived **Gateway** daemon on `127.0.0.1:18789` that owns all messaging channels (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Matrix, …), brokers clients (CLI, Control UI, mac app, nodes), and executes agent turns. Terminal-first onboarding. Docs hosted on Mintlify at docs.openclaw.ai.

**Name conventions.** `OpenClaw` in prose/headings. `openclaw` for the CLI binary, npm package, paths, config keys. Don't confuse with `pjasicek/OpenClaw` — that's a C++ remake of the 1997 Captain Claw platformer, unrelated.

## When to use this skill

- User mentions OpenClaw, ClawHub, `openclaw` CLI, `~/.openclaw/`, or `openclaw.plugin.json`
- Writing or debugging an OpenClaw skill or plugin
- Bridging OpenClaw and Claude Code (async delegation, shared memory, bundle compat)
- Translating docs.openclaw.ai URLs or routing lookups
- Understanding gateway / node / channel architecture before touching config

Not the right skill for: general Claude Code tips, Captain Claw game remakes, random lobster metaphors.

## Core concepts (memorize these)

| Concept | Key fact |
|---|---|
| **Gateway** | Long-lived daemon. One per host. Owns all channel sessions. WebSocket API on `127.0.0.1:18789`. launchd/systemd user service. |
| **Client** | Anything connecting to the Gateway over WS: CLI, Control UI (web dashboard), mac app, automations. |
| **Node** | Device connection with `role: node` (macOS/iOS/Android/headless). Exposes device-local commands: `canvas.*`, `camera.*`, `screen.record`, `location.get`. Pairing is device-based. |
| **Channel** | Messaging surface (WhatsApp/Telegram/Slack/etc). Core channels live in `src/<channel>`; others are bundled plugins. |
| **Plugin** | Extensibility unit. Two kinds: **native** (ships `openclaw.plugin.json` + plugin-sdk imports) and **compatible bundle** (Claude `.claude-plugin/`, Codex `.codex-plugin/`, Cursor `.cursor-plugin/`). Installed via `openclaw plugins install`. |
| **Skill** | Lighter baseline-UX capability: markdown + optional manifest, published to **ClawHub** (clawhub.ai). New capabilities should ship as plugins; skills are for lightweight prompts/workflows. |
| **ClawHub** | Public skills + plugins registry. CLI: `openclaw skills {search,install,update,list,info,check}` and `openclaw plugins install clawhub:<pkg>`. |
| **Memory** | Single-slot plugin (`kind: "memory"` in manifest). Multiple options ship; project plans to converge. |
| **MCP** | Not native. OpenClaw bridges MCP through `mcporter` (github.com/steipete/mcporter) — add/change MCP servers without restarting the Gateway. |
| **Provider** | Model provider plugin. Registered via `defineSingleProviderPluginEntry` from `openclaw/plugin-sdk/provider-entry`. |
| **Gateway control plane** | Typed WS protocol via TypeBox → JSON Schema → Swift codegen. Frames: `req`/`res`/`event`. First frame MUST be `connect`. |

## Install paths (filesystem layout)

```
~/.openclaw/                    # OPENCLAW_HOME (override: OPENCLAW_HOME env)
  skills/                       # global skills (priority: LOW)
  control-ui-custom/             # optional custom Control UI build
<project>/skills/               # workspace skills (priority: HIGH)
~/.openclaw/state/              # state dir (override: OPENCLAW_STATE_DIR)
~/.openclaw/config.json         # config (override: OPENCLAW_CONFIG_PATH)
```

**Skill resolution order:** workspace > global > bundled. Workspace always wins.

## Quickstart CLI (cheat sheet)

```bash
# Install & bootstrap
curl -fsSL https://openclaw.ai/install.sh | bash          # macOS/Linux
openclaw onboard --install-daemon                          # wizard + daemon install
openclaw gateway status                                    # verify daemon on 18789
openclaw dashboard                                         # open Control UI

# Day-to-day ops
openclaw config set <key> <value>                          # edit config
openclaw doctor --fix                                      # repair drift, legacy config
openclaw channels status --probe                           # channel health check
openclaw gateway restart

# Skills (ClawHub-backed)
openclaw skills search "<query>"
openclaw skills install <slug> [--version <v>] [--force]
openclaw skills list [--eligible] [--json]
openclaw skills info <name>
openclaw skills check                                      # debug missing bins/env

# Plugins
openclaw plugins list [--enabled] [--verbose] [--json]
openclaw plugins install <pkg>                             # ClawHub first, then npm
openclaw plugins install clawhub:<pkg>                     # force ClawHub
openclaw plugins install <path> [--link]                   # local dev
openclaw plugins install <plugin>@<marketplace>
openclaw plugins inspect <id>
openclaw plugins enable|disable|uninstall <id>
openclaw plugins doctor
```

Full CLI surface → `references/cli.md`.

## Topic → reference map

| Question | Read |
|---|---|
| Gateway, WS protocol, nodes, pairing, ports, invariants | `references/architecture.md` |
| Every CLI command + flags | `references/cli.md` |
| Writing a `SKILL.md` for OpenClaw (frontmatter, metadata block, install hints) | `references/skills-format.md` |
| Writing a plugin (`openclaw.plugin.json`, plugin-sdk subpaths, channel/provider plugin shape) | `references/plugins-format.md` |
| Interop with Claude Code / Codex / Cursor bundles + MCP via mcporter | `references/bundle-compat.md` |
| Channel catalogue + setup pointers | `references/channels.md` |
| Topic → `docs.openclaw.ai/<path>` lookup map | `references/docs-index.md` |

## Doc lookup strategy

OpenClaw docs live at **docs.openclaw.ai** (Mintlify). When the user wants authoritative detail:

1. Check `references/docs-index.md` for the canonical path.
2. Fetch `https://docs.openclaw.ai/<path>` via WebFetch, or read the source markdown from `openclaw/openclaw` repo under `docs/<path>.md` via `gh api repos/openclaw/openclaw/contents/docs/<path>.md`.
3. Internal doc links use root-relative paths without `.md` extension: `[Config](/configuration)`. When replying with links, always give the full `https://docs.openclaw.ai/...` URL.
4. Foreign-language docs are autogenerated in a sibling `openclaw/docs` repo — don't cite or edit them; English is the source of truth.

## Critical invariants to respect

- **One Gateway per host.** Never start a second one; it collides on the WS port and the WhatsApp/Baileys session.
- **Prompt-cache stability matters.** Code that assembles model/tool payloads must be deterministic in order. Don't rewrite old transcript bytes on every turn — it kills the Anthropic prompt cache.
- **Extension boundary.** Plugin production code imports from `openclaw/plugin-sdk/<subpath>` only. Never deep-import `src/**` of core or another plugin.
- **Manifest ≠ runtime.** `openclaw.plugin.json` is metadata-only. It validates config, declares identity, and provides cheap activation/setup/auth hints. It does NOT register runtime — that's the job of `definePluginEntry`, `defineChannelPluginEntry`, `defineSingleProviderPluginEntry` in code.
- **ClawHub-first for installs.** Bare `openclaw plugins install <pkg>` checks ClawHub before npm. Stable-track only: prerelease npm specs are rejected unless explicit (`@beta`, `@rc`, or exact `@x.y.z-beta.N`).
- **Security defaults.** `--dangerously-force-unsafe-install` bypasses the dangerous-code scanner for false positives only. It does NOT bypass `before_install` hook blocks.

## Most useful third-party entry points

| Repo | Why |
|---|---|
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | Canonical source; `docs/`, `skills/`, bundled workspace plugin tree |
| [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | Curated 5,200+ skills from ClawHub |
| [VsevolodUstinov/openclaw-skill-claude-code](https://github.com/VsevolodUstinov/openclaw-skill-claude-code) | Async delegate OpenClaw → Claude Code CLI. $0 on Max sub. See `references/bundle-compat.md`. |
| [freema/openclaw-mcp](https://github.com/freema/openclaw-mcp) | MCP server exposing OpenClaw → Claude.ai with OAuth2 |
| [ourmem/omem](https://github.com/ourmem/omem) | Shared memory across OpenClaw + Claude Code + OpenCode |
| [steipete/mcporter](https://github.com/steipete/mcporter) | The MCP bridge OpenClaw uses — how MCP servers get wired in |
