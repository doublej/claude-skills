# Docs index — topic → docs.openclaw.ai path

All paths are relative to `https://docs.openclaw.ai/`. To fetch the source markdown instead, use `gh api repos/openclaw/openclaw/contents/docs/<path>.md --jq '.content' | base64 -d`.

## Getting started

| Topic | Path |
|---|---|
| Getting Started (fastest path) | `/start/getting-started` |
| Quickstart | `/start/quickstart` |
| Bootstrapping | `/start/bootstrapping` |
| Onboarding wizard (full reference) | `/start/wizard` |
| Onboarding overview | `/start/onboarding-overview` |
| Onboarding details | `/start/onboarding` |
| Showcase (what's possible) | `/start/showcase` |
| Setup | `/start/setup` |
| Docs about this docs tree | `/start/docs-directory` |

## Install

| Topic | Path |
|---|---|
| Install overview | `/install` |
| Docker | `/install/docker` |
| Node setup | `/install/node` |
| Updating | `/install/updating` |

## Concepts

| Topic | Path |
|---|---|
| Architecture (gateway, channels, protocol) | `/concepts/architecture` |
| Agent loop | `/concepts/agent-loop` |
| Agent workspace | `/concepts/agent-workspace` |
| Active memory | `/concepts/active-memory` |
| Built-in memory | `/concepts/memory-builtin` |
| Honcho memory | `/concepts/memory-honcho` |
| Qmd memory | `/concepts/memory-qmd` |
| Memory overview | `/concepts/memory` |
| Memory search | `/concepts/memory-search` |
| Context engine | `/concepts/context-engine` |
| Context | `/concepts/context` |
| Compaction | `/concepts/compaction` |
| Delegate architecture | `/concepts/delegate-architecture` |
| Dreaming | `/concepts/dreaming` |
| Features | `/concepts/features` |
| Markdown formatting | `/concepts/markdown-formatting` |
| Messages | `/concepts/messages` |
| Model failover | `/concepts/model-failover` |
| Model providers | `/concepts/model-providers` |
| Models | `/concepts/models` |
| Multi-agent | `/concepts/multi-agent` |
| OAuth | `/concepts/oauth` |
| Presence | `/concepts/presence` |
| Queue (command queue + concurrency) | `/concepts/queue` |
| Retry | `/concepts/retry` |
| Session pruning | `/concepts/session-pruning` |
| Session tool | `/concepts/session-tool` |
| Session | `/concepts/session` |
| Soul | `/concepts/soul` |
| Streaming | `/concepts/streaming` |
| System prompt | `/concepts/system-prompt` |
| Timezone | `/concepts/timezone` |
| Typing indicators | `/concepts/typing-indicators` |
| Usage tracking | `/concepts/usage-tracking` |
| QA E2E automation | `/concepts/qa-e2e-automation` |

## Gateway

| Topic | Path |
|---|---|
| Gateway architecture | `/concepts/architecture` (shares page) |
| WS protocol contract | `/gateway/protocol` |
| Bridge protocol | `/gateway/bridge-protocol` |
| Security (trust model, hardening) | `/gateway/security` |

## CLI

Every CLI command has a reference page under `/cli/<name>`:

```
acp       agent       agents      approvals   backup
browser   channels    clawbot     completion  config
configure cron        daemon      dashboard   devices
directory dns         docs        doctor      flows
gateway   health      hooks       infer       logs
mcp       memory      message     models      node
nodes     onboard     pairing     plugins     qr
reset     sandbox     secrets     security    sessions
setup     skills      status      system      tui
uninstall update      voicecall   webhooks    wiki
```

Most commonly needed:
- `/cli/onboard`
- `/cli/gateway`
- `/cli/doctor`
- `/cli/skills`
- `/cli/plugins`
- `/cli/channels`
- `/cli/config`
- `/cli/dashboard`
- `/cli/sessions`

## Plugins

| Topic | Path |
|---|---|
| Building plugins (how-to) | `/plugins/building-plugins` |
| Building extensions | `/plugins/building-extensions` |
| Architecture + capability model | `/plugins/architecture` |
| Manifest (`openclaw.plugin.json`) | `/plugins/manifest` |
| SDK overview (import map) | `/plugins/sdk-overview` |
| SDK entrypoints | `/plugins/sdk-entrypoints` |
| SDK runtime | `/plugins/sdk-runtime` |
| SDK setup | `/plugins/sdk-setup` |
| SDK testing | `/plugins/sdk-testing` |
| SDK migration | `/plugins/sdk-migration` |
| SDK agent harness | `/plugins/sdk-agent-harness` |
| Channel plugins guide | `/plugins/sdk-channel-plugins` |
| Provider plugins guide | `/plugins/sdk-provider-plugins` |
| Codex harness | `/plugins/codex-harness` |
| Community plugin listing + PR bar | `/plugins/community` |
| Compatible bundles (Claude/Codex/Cursor) | `/plugins/bundles` |
| Agent tools | `/plugins/agent-tools` |
| Voice Call plugin | `/plugins/voice-call` |
| Webhooks | `/plugins/webhooks` |
| Memory wiki | `/plugins/memory-wiki` |
| ZaloUser | `/plugins/zalouser` |

## Tools

| Topic | Path |
|---|---|
| Skills system overview | `/tools/skills` |
| Skills config | `/tools/skills-config` |
| ClawHub integration | `/tools/clawhub` |
| Plugin system | `/tools/plugin` |

## Channels

See `references/channels.md` for the full list. Root path: `/channels/<name>`.

## Providers

| Topic | Path |
|---|---|
| Providers overview | `/providers` |
| Brave Search | `/brave-search` |
| Perplexity | `/perplexity` |

## Platforms

| Topic | Path |
|---|---|
| Platforms overview | `/platforms` |
| Windows (WSL2 strongly recommended) | `/platforms/windows` |

## Help

| Topic | Path |
|---|---|
| Environment variables | `/help/environment` |
| FAQ | `/help/faq` |

## Miscellaneous (docs root)

| Topic | Path |
|---|---|
| Docs home | `/` |
| Config schema | `/configuration` |
| CI | `/ci` |
| Logging | `/logging` |
| Network | `/network` |
| Prose | `/prose` |
| TTS | `/tts` |
| Pi config | `/pi`, `/pi-dev` |
| VPS | `/vps` |
| Auth credential semantics | `/auth-credential-semantics` |
| Date/time | `/date-time` |

## Fetching strategy

**Mintlify link rules** (when replying or editing):
- Internal links in `docs/**/*.md`: root-relative, no `.md`/`.mdx`: `[Config](/configuration)`
- Anchor cross-references: `[Hooks](/configuration#hooks)`
- Avoid em dashes and apostrophes in headings (breaks Mintlify anchor generation)
- When the user asks for a link, reply with the full `https://docs.openclaw.ai/...` URL
- README (GitHub-hosted) keeps absolute docs URLs so links work on GitHub

**Fetch workflow.** Prefer `gh api` on the source repo when available — Mintlify pages may lag a commit behind:

```bash
gh api repos/openclaw/openclaw/contents/docs/<path>.md --jq '.content' | base64 -d
```

Fall back to WebFetch on `https://docs.openclaw.ai/<path>` for rendered content.
