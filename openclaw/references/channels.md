# Channels

Messaging surfaces OpenClaw can bind. Each is either **core** (lives in `src/<channel>`) or a **bundled plugin** (workspace plugin tree). Setup per-channel lives at `https://docs.openclaw.ai/channels/<name>`.

## Core channels (in `src/<channel>/`)

| Channel | Code path | Setup doc |
|---|---|---|
| Telegram | `src/telegram` | `/channels/telegram` — fastest setup, just a bot token |
| Discord | `src/discord` | `/channels/discord` |
| Slack | `src/slack` | `/channels/slack` |
| Signal | `src/signal` | `/channels/signal` |
| iMessage | `src/imessage` | `/channels/imessage` |
| WhatsApp (web) | `src/web` (provides `provider-web.ts`, Baileys-based) | `/channels/whatsapp` |

## Bundled plugin channels (workspace plugin tree)

| Channel | Doc |
|---|---|
| Matrix | `/channels/matrix` |
| Zalo (bot) | `/channels/zalo` |
| ZaloUser | `/channels/zalouser` |
| Voice Call | `docs/plugins/voice-call.md` |
| Feishu | `/channels/feishu` |
| Google Chat | `/channels/googlechat` |
| Microsoft Teams | `/channels/msteams` |
| LINE | `/channels/line` |
| IRC | `/channels/irc` |
| Mattermost | `/channels/mattermost` |
| Nextcloud Talk | `/channels/nextcloud-talk` |
| Nostr | `/channels/nostr` |
| Synology Chat | `/channels/synology-chat` |
| Tlon | `/channels/tlon` |
| Twitch | `/channels/twitch` |
| QQ Bot | `/channels/qqbot` |
| BlueBubbles | `/channels/bluebubbles` |

Other listed in canonical README: WeChat, WebChat.

## Cross-cutting topics (docs/channels/*.md)

| Topic | Doc |
|---|---|
| Pairing (device-based trust) | `/channels/pairing` |
| Channel routing | `/channels/channel-routing` |
| Group messages + broadcast groups | `/channels/group-messages`, `/channels/broadcast-groups`, `/channels/groups` |
| Location handling | `/channels/location` |
| Troubleshooting | `/channels/troubleshooting` |
| QA channel | `/channels/qa-channel` |

## Health / status

```bash
openclaw channels status --probe
```

Probes all configured channels; returns per-channel status (connected / paired / error).

## Refactor reminder

From `AGENTS.md`: when touching shared logic (routing, allowlists, pairing, command gating, onboarding, docs), consider **all** built-in + bundled plugin channels. Easy to miss Matrix/Zalo/Voice-Call when only editing the core channel list.

## Labels

When adding channels/plugins/apps/docs to the repo, update `.github/labeler.yml` and create matching GitHub labels (use existing channel/plugin label colors).
