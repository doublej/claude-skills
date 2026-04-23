# OpenClaw plugin format

Distilled from `docs/plugins/manifest.md`, `docs/plugins/sdk-overview.md`, `docs/plugins/building-plugins.md`, `docs/plugins/architecture.md` in `openclaw/openclaw`.

A **plugin** is the preferred extensibility unit. Two kinds:

1. **Native OpenClaw plugin** — ships `openclaw.plugin.json` + imports from `openclaw/plugin-sdk/*`. Validated strictly by core.
2. **Compatible bundle** — a Claude/Codex/Cursor bundle auto-detected and loaded in-place. See `references/bundle-compat.md`.

This reference covers **native plugins**.

## Structure

```
my-plugin/
├── openclaw.plugin.json        # REQUIRED — identity + config schema + cheap metadata
├── package.json                # npm metadata, dependencies (npm install --omit=dev)
├── src/
│   ├── index.ts                # plugin entry (definePluginEntry / defineChannelPluginEntry / …)
│   ├── api.ts                  # local public surface for tests + sibling modules
│   └── runtime-api.ts          # lazy runtime barrel
└── skills/                     # optional — skill dirs declared in manifest `skills[]`
```

## `openclaw.plugin.json` — manifest (metadata only)

**Rule**: manifest is read **before** plugin code loads. Use it for identity, config validation, cheap activation hints, auth/onboarding metadata. DO NOT try to register runtime behavior here.

### Minimal example

```json
{
  "id": "voice-call",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

### Rich example (provider plugin)

```json
{
  "id": "openrouter",
  "name": "OpenRouter",
  "description": "OpenRouter provider plugin",
  "version": "1.0.0",
  "providers": ["openrouter"],
  "modelSupport": { "modelPrefixes": ["router-"] },
  "cliBackends": ["openrouter-cli"],
  "providerAuthEnvVars": {
    "openrouter": ["OPENROUTER_API_KEY"]
  },
  "providerAuthAliases": {
    "openrouter-coding": "openrouter"
  },
  "channelEnvVars": {
    "openrouter-chatops": ["OPENROUTER_CHATOPS_TOKEN"]
  },
  "providerAuthChoices": [
    {
      "provider": "openrouter",
      "method": "api-key",
      "choiceId": "openrouter-api-key",
      "choiceLabel": "OpenRouter API key",
      "groupId": "openrouter",
      "groupLabel": "OpenRouter",
      "optionKey": "openrouterApiKey",
      "cliFlag": "--openrouter-api-key",
      "cliOption": "--openrouter-api-key <key>",
      "cliDescription": "OpenRouter API key",
      "onboardingScopes": ["text-inference"]
    }
  ],
  "uiHints": {
    "apiKey": {
      "label": "API key",
      "placeholder": "sk-or-v1-...",
      "sensitive": true
    }
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" }
    }
  }
}
```

### Top-level fields

| Field | Required | Type | Purpose |
|---|---|---|---|
| `id` | ✅ | `string` | Canonical plugin id. Used in `plugins.entries.<id>`. |
| `configSchema` | ✅ | `object` | Inline JSON Schema (strict). Even if empty, ship it. |
| `name` | — | `string` | Human-readable display name |
| `description` | — | `string` | Short summary for plugin surfaces |
| `version` | — | `string` | Informational |
| `enabledByDefault` | — | `true` | Marks a bundled plugin enabled by default |
| `legacyPluginIds` | — | `string[]` | Legacy ids that normalize to this id |
| `autoEnableWhenConfiguredProviders` | — | `string[]` | Auto-enable when these provider ids are configured |
| `kind` | — | `"memory"` \| `"context-engine"` | Exclusive single-slot plugin kinds (`plugins.slots.*`) |
| `channels` | — | `string[]` | Channel ids owned by this plugin |
| `providers` | — | `string[]` | Provider ids owned by this plugin |
| `modelSupport` | — | `object` | Shorthand model-family ownership (auto-loads plugin on matching model id) |
| `cliBackends` | — | `string[]` | CLI inference backend ids owned here |
| `commandAliases` | — | `object[]` | Plugin-owned command names (diagnostics surface) |
| `providerAuthEnvVars` | — | `Record<string,string[]>` | Cheap provider-auth env metadata |
| `providerAuthAliases` | — | `Record<string,string>` | Provider id auth aliases |
| `channelEnvVars` | — | `Record<string,string[]>` | Cheap channel env metadata |
| `providerAuthChoices` | — | `object[]` | Onboarding/auth choice metadata |
| `activation` | — | `object` | Cheap activation hints (see below) |
| `setup` | — | `object` | Cheap setup/onboarding descriptors |
| `contracts` | — | `object` | Static bundled capability snapshot (speech, realtime, image-gen, web search, tool ownership, …) |
| `channelConfigs` | — | `Record<string,object>` | Manifest-owned channel config metadata |
| `skills` | — | `string[]` | Skill dir paths relative to plugin root |
| `uiHints` | — | `Record<string,object>` | UI labels/placeholders/sensitivity hints |

### `activation` block

Control-plane activation hints so the plugin gets loaded on-demand:

```json
{
  "activation": {
    "onProviders": ["openai"],
    "onCommands": ["models"],
    "onChannels": ["web"],
    "onRoutes": ["gateway-webhook"],
    "onCapabilities": ["provider", "tool"]
  }
}
```

Metadata only — does NOT replace `register(...)` / `definePluginEntry` runtime wiring.

### `commandAliases` block

```json
{
  "commandAliases": [
    {
      "name": "dreaming",
      "kind": "runtime-slash",
      "cliCommand": "memory"
    }
  ]
}
```

Use when a plugin owns a runtime command name that users may mistakenly put in `plugins.allow` or run as a root CLI command. `kind: "runtime-slash"` marks it as a chat slash command rather than a root CLI command.

### Do NOT use manifest for

- Registering runtime behavior
- Declaring code entrypoints
- npm install metadata

Those belong in plugin code + `package.json`.

## Plugin SDK (`openclaw/plugin-sdk/*`)

**Import convention.** Always import from a **specific subpath**, never the root:

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { defineChannelPluginEntry, createChatChannelPlugin } from "openclaw/plugin-sdk/channel-core";
import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";
import { OpenClawSchema } from "openclaw/plugin-sdk/config-schema";
```

Each subpath is a self-contained module — keeps startup fast, avoids circular deps. Full list (200+ subpaths) lives in `scripts/lib/plugin-sdk-entrypoints.json`.

### Most commonly used subpaths

| Subpath | Exports |
|---|---|
| `plugin-sdk/plugin-entry` | `definePluginEntry` |
| `plugin-sdk/core` | `defineChannelPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase`, `defineSetupPluginEntry`, `buildChannelConfigSchema` |
| `plugin-sdk/channel-core` | `defineChannelPluginEntry`, `defineSetupPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase` |
| `plugin-sdk/config-schema` | `OpenClawSchema` (root Zod schema) |
| `plugin-sdk/provider-entry` | `defineSingleProviderPluginEntry` |
| `plugin-sdk/provider-auth` | `createProviderApiKeyAuthMethod`, `ensureApiKeyFromOptionEnvOrPrompt`, `upsertApiKeyProfile`, `writeOAuthCredentials` |
| `plugin-sdk/channel-setup` | `createOptionalChannelSetupSurface`, `createOptionalChannelSetupAdapter`, setup wizard helpers |
| `plugin-sdk/channel-contract` | Channel contract types |
| `plugin-sdk/runtime` | Broad runtime/logging/backup/plugin-install helpers |
| `plugin-sdk/runtime-env` | Narrow runtime env + logger + timeout + retry + backoff helpers |
| `plugin-sdk/gateway-runtime` | Gateway client + channel-status patch helpers |
| `plugin-sdk/hook-runtime` | Webhook/internal hook pipeline helpers |
| `plugin-sdk/lazy-runtime` | Lazy import/binding: `createLazyRuntimeModule`, `createLazyRuntimeMethod`, `createLazyRuntimeSurface` |
| `plugin-sdk/security-runtime` | Trust, DM gating, external-content, secret-collection helpers |
| `plugin-sdk/ssrf-runtime` | Pinned dispatcher, SSRF-guarded fetch, policy helpers |

**Avoid**: provider-named convenience seams like `openclaw/plugin-sdk/slack`, `openclaw/plugin-sdk/discord`, etc. Bundled plugins compose generic subpaths inside their own `api.ts` / `runtime-api.ts` barrels.

## Dependency / packaging rules

- Install runs `npm install --omit=dev` in the plugin dir → runtime deps MUST live in `dependencies` (not `devDependencies`).
- Avoid `workspace:*` in `dependencies` — npm install breaks. Put `openclaw` in `devDependencies` or `peerDependencies` instead.
- Runtime resolves `openclaw/plugin-sdk` via jiti alias at load time.
- Plugin-only deps stay in the extension `package.json`; don't pollute root `package.json`.
- Extension package boundary: inside a bundled plugin, don't use relative imports resolving **outside** that package root. If shared, use `openclaw/plugin-sdk/<subpath>`.
- Dynamic import guardrail: don't mix `await import("x")` and static `import ... from "x"` for the same module. For lazy loading, create a dedicated `*.runtime.ts` boundary.

## Security

- `plugins install` respects a built-in dangerous-code scanner; `critical` findings block install unless `--dangerously-force-unsafe-install` is passed.
- `--dangerously-force-unsafe-install` does NOT bypass `before_install` hook policy blocks.
- Dependency installs run with `--ignore-scripts`.
- npm specs are registry-only (no git/URL/file, no semver ranges). Pin exact versions for sensitive installs.

## Key docs pages

- `/plugins/building-plugins` — getting-started guide
- `/plugins/architecture` — capability model + extension boundary
- `/plugins/manifest` — manifest schema reference (authoritative)
- `/plugins/sdk-overview` — SDK import map
- `/plugins/sdk-entrypoints` — entrypoint reference
- `/plugins/sdk-runtime` — runtime SDK surface
- `/plugins/sdk-channel-plugins` — channel plugin guide
- `/plugins/sdk-provider-plugins` — provider plugin guide
- `/plugins/bundles` — compatible bundle formats (Claude/Codex/Cursor)
- `/plugins/community` — community plugin listing + PR bar
- `/cli/plugins` — `openclaw plugins` CLI reference
