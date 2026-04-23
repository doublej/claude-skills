# Architecture

Distilled from `docs/concepts/architecture.md`, `docs/gateway/*`, `AGENTS.md` in `openclaw/openclaw`.

## Gateway daemon

- One long-lived Gateway per host. Owns **all** messaging surfaces (WhatsApp via Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat). Invariant: exactly one Gateway controls a single Baileys session per host.
- Default bind: `127.0.0.1:18789` (loopback). Change via `gateway.bind` / `gateway.port` in config.
- Supervision: `launchd` (macOS) or `systemd --user` (Linux) installed by `openclaw onboard --install-daemon`.
- Foreground run: `openclaw gateway run --bind loopback --port 18789 --force`.
- Status: `openclaw gateway status`.
- Restart: `openclaw gateway restart` (or `pkill -9 -f openclaw-gateway` then re-run).
- Logs: stdout when foreground; `/tmp/openclaw-gateway.log` pattern if running nohup.

## Canvas host (HTTP side of Gateway)

Same port (`18789`) serves:
- `/__openclaw__/canvas/` — agent-editable HTML/CSS/JS surface
- `/__openclaw__/a2ui/` — A2UI host

## Clients vs Nodes

| Role | Purpose | Declared in `connect` |
|---|---|---|
| Client | CLI, Control UI, mac app, automations | default |
| Node | Device (macOS/iOS/Android/headless) exposing device-local caps | `role: "node"` + caps/commands |

Nodes expose commands like `canvas.*`, `camera.*`, `screen.record`, `location.get`. Pairing is **device-based** — new device IDs require approval; Gateway issues a device token for reconnects. Local loopback can be auto-approved; non-local connects always require explicit approval. All connects must sign a `connect.challenge` nonce; signature payload `v3` binds `platform` + `deviceFamily`.

## Wire protocol

- Transport: **WebSocket**, text frames, JSON payloads.
- Schema source: TypeBox (`src/gateway/protocol/schema/*.ts`) → JSON Schema → Swift models (codegen).
- First frame **must** be `connect`. Any non-JSON / non-connect first frame = hard close.
- After handshake:
  - Request: `{ type:"req", id, method, params }` → `{ type:"res", id, ok, payload|error }`
  - Event (server push): `{ type:"event", event, payload, seq?, stateVersion? }`
- Events are **not** replayed; clients must refresh on seq gaps.
- `hello-ok.features.methods` / `events` are discovery metadata — not a full dump.
- Idempotency keys required for side-effecting methods (`send`, `agent`); short-lived dedupe cache server-side.
- Core events: `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`, `tick`, `shutdown`.

## Auth modes (`gateway.auth.mode`)

| Mode | Use |
|---|---|
| shared-secret (default) | `connect.params.auth.token` or `connect.params.auth.password` |
| `"trusted-proxy"` (non-loopback) | Identity from request headers |
| `allowTailscale: true` | Tailscale Serve ingress satisfies auth from headers |
| `"none"` | Disables shared-secret; **only** for private-ingress; NEVER on public ingress |

Gateway auth applies to **all** connections, local or remote. Pairing approval is a **separate** gate on top of auth.

## Connection lifecycle (single client)

```
Client → Gateway : req:connect
Gateway → Client : res(ok) payload=hello-ok (presence+health snapshot)
Gateway → Client : event:presence
Gateway → Client : event:tick
Client → Gateway : req:agent
Gateway → Client : res:agent ack {runId, status:"accepted"}
Gateway → Client : event:agent (streaming)
Gateway → Client : res:agent final {runId, status, summary}
```

## Remote access

- Preferred: Tailscale or VPN.
- Alternative: SSH tunnel — `ssh -N -L 18789:127.0.0.1:18789 user@host`.
- Same handshake + auth apply over the tunnel.
- Optional TLS + cert pinning for WS in remote setups.

## Prompt cache stability (correctness-critical)

- Any code assembling model/tool payloads from maps, sets, registries, plugin lists, MCP catalogs, filesystem reads, or network results **must** sort deterministically before building the request.
- Don't rewrite older transcript/history bytes on every turn — that invalidates the cached prefix on Anthropic and costs real money.
- If truncation/compaction is needed, mutate newest/tail content first so the cached prefix stays byte-identical.

## Architecture boundaries (for plugin authors)

- `src/plugin-sdk/*` — public plugin contract. Allowed import surface.
- `src/channels/*` — core channel impl. Do NOT import from plugins.
- `src/plugins/*` — discovery, manifest validation, loader, registry.
- `src/gateway/protocol/*` — typed WS protocol. Changes = contract changes; prefer additive evolution.

Rules:
- Extensions import only `openclaw/plugin-sdk/*` + their own `api.ts` / `runtime-api.ts` barrels.
- Core must stay extension-agnostic — no hardcoded bundled plugin id lists.
- Bundled plugin helper seams in plugin-sdk (feishu, zalo, matrix…) are compatibility surfaces, not the recommended import path for new third-party plugins.

## Key docs pages (docs.openclaw.ai)

- `/concepts/architecture` — gateway architecture
- `/gateway/protocol` — wire protocol contract
- `/gateway/bridge-protocol` — bridge
- `/gateway/security` — trust model + hardening
- `/channels/pairing` — device pairing flow
- `/concepts/agent-loop` — agent execution cycle
- `/concepts/queue` — command queue + concurrency
