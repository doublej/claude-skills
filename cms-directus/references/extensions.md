# Extensions

Directus extensions extend the admin App, the API, or both. Nine types across two categories.

## Types at a glance

### App extensions (Vue 3 components, loaded into the admin UI)

| Type | Purpose |
|---|---|
| `interface` | Custom field editor (form input) |
| `display` | Read-only field renderer (tables, detail views) |
| `layout` | Full collection view layout (alt to tabular) |
| `module` | Top-level admin page + nav item |
| `panel` | Dashboard widget (Insights page) |

### API extensions (Node.js modules, loaded by the Directus server)

| Type | Purpose |
|---|---|
| `hook` | Intercept lifecycle events (item CRUD, auth, init) |
| `endpoint` | Custom HTTP routes mounted under `/<name>/...` |
| `operation` | Custom block for Flows |
| `bundle` | Ship multiple extensions as one package |

## Scaffold

```bash
npx create-directus-extension@latest
# Prompts for: type, name, language (TS/JS)
```

Output structure:

```
my-extension/
├── package.json          # keywords: ['directus-extension', 'directus-extension-<type>']
├── src/
│   └── index.ts          # export default { ... } or export default (register) => { ... }
└── dist/                 # built by `npm run build` — where Directus loads from
```

Install an extension into a running Directus:
- Local dev: symlink into `extensions/` directory of Directus install
- Docker: bind-mount `./extensions:/directus/extensions`
- Marketplace: install via admin UI

## Interface

A Vue 3 component that edits a field value. Minimum:

```ts
// src/index.ts
import InterfaceComponent from './interface.vue'

export default {
  id: 'my-slider',
  name: 'Custom Slider',
  icon: 'tune',
  description: 'A draggable numeric slider',
  component: InterfaceComponent,
  types: ['integer', 'float', 'decimal'],
  options: [
    { field: 'min', name: 'Min', type: 'integer', meta: { interface: 'input' } },
    { field: 'max', name: 'Max', type: 'integer', meta: { interface: 'input' } },
  ],
}
```

```vue
<!-- src/interface.vue -->
<template>
  <input type="range" :min="min" :max="max" :value="value" @input="$emit('input', Number($event.target.value))" />
</template>
<script setup lang="ts">
defineProps<{ value: number; min: number; max: number }>()
defineEmits<{ (e: 'input', value: number): void }>()
</script>
```

## Display

Read-only renderer. Often a tiny function component.

```ts
import DisplayComponent from './display.vue'

export default {
  id: 'status-badge',
  name: 'Status Badge',
  icon: 'label',
  description: 'Color-coded status chip',
  component: DisplayComponent,
  types: ['string'],
  handler: (value: string) => value?.toUpperCase(),  // optional non-component form
}
```

## Module

A full admin page + sidebar item.

```ts
import ModuleComponent from './module.vue'

export default {
  id: 'analytics',
  name: 'Analytics',
  icon: 'bar_chart',
  routes: [
    { path: '', component: ModuleComponent },
    { path: ':id', component: DetailComponent },
  ],
  preRegisterCheck: (user) => user.role.admin_access,
}
```

## Panel (Insights dashboard)

```ts
export default {
  id: 'kpi-card',
  name: 'KPI Card',
  icon: 'insights',
  description: 'Show a single KPI from a collection',
  component: PanelComponent,
  options: [
    { field: 'collection', name: 'Collection', type: 'string', meta: { interface: 'system-collection' } },
    { field: 'field',      name: 'Field',      type: 'string', meta: { interface: 'system-field', options: { collectionField: 'collection' } } },
  ],
  minWidth: 6,
  minHeight: 4,
}
```

## Hook

Register against lifecycle events.

```ts
// src/index.ts
import { defineHook } from '@directus/extensions-sdk'

export default defineHook(({ action, filter, init, schedule }, { services, database, env, logger }) => {
  // Filter: mutate payload BEFORE write (can abort by throwing)
  filter('posts.items.create', (payload) => {
    if (!payload.slug) payload.slug = slugify(payload.title)
    return payload
  })

  // Action: fire-and-forget AFTER write
  action('posts.items.create', ({ payload, key, collection }, { accountability }) => {
    logger.info(`Post ${key} created by ${accountability?.user}`)
  })

  // Init: once at server start
  init('app.after', () => {
    logger.info('Directus app initialized')
  })

  // Schedule: cron
  schedule('0 2 * * *', async () => {
    // daily at 02:00 UTC
  })
})
```

### Common event names

| Event | Fires |
|---|---|
| `<collection>.items.create` | Before/after item create |
| `<collection>.items.update` | |
| `<collection>.items.delete` | |
| `auth.login` | Successful login |
| `auth.jwt` | JWT issued |
| `server.start` | HTTP server started |
| `app.after` / `cli.after` | Init complete |

## Endpoint

Custom HTTP route — mounted at `/<id>/*`.

```ts
import { defineEndpoint } from '@directus/extensions-sdk'

export default defineEndpoint((router, { services, database, exceptions }) => {
  const { ItemsService } = services
  const { ServiceUnavailableException } = exceptions

  router.get('/stats', async (req, res, next) => {
    try {
      const svc = new ItemsService('posts', { schema: req.schema, accountability: req.accountability })
      const count = await svc.readByQuery({ aggregate: { count: ['*'] } })
      res.json({ count: count[0]?.count })
    } catch (e) {
      next(new ServiceUnavailableException('Failed to read stats'))
    }
  })
})
```

Register as `GET /stats/stats` (prefixed with extension id).

Use `ItemsService` from injected `services` so permissions are respected. Bypass with `new ItemsService(..., { schema, accountability: null })` only for trusted admin tasks.

## Operation (for Flows)

Custom block in the flow editor.

```ts
// src/api.ts
import { defineOperationApi } from '@directus/extensions-sdk'

type Options = { url: string }

export default defineOperationApi<Options>({
  id: 'ping-url',
  handler: async ({ url }) => {
    const res = await fetch(url)
    return { status: res.status }
  },
})
```

```ts
// src/app.ts  (UI side)
import { defineOperationApp } from '@directus/extensions-sdk'

export default defineOperationApp({
  id: 'ping-url',
  name: 'Ping URL',
  icon: 'wifi',
  description: 'GET a URL, return status',
  overview: ({ url }) => [{ label: 'URL', text: url }],
  options: [
    { field: 'url', name: 'URL', type: 'string', meta: { interface: 'input' } },
  ],
})
```

## Bundle

Package multiple extensions under one npm module. `package.json`:

```json
{
  "directus:extension": {
    "type": "bundle",
    "entries": [
      { "type": "interface", "name": "my-slider", "source": "src/slider/index.ts" },
      { "type": "hook",      "name": "audit-log",  "source": "src/audit/index.ts" }
    ],
    "host": "^10.0.0"
  }
}
```

Run `npm run build` — outputs to `dist/`.

## Development loop

```bash
cd my-extension
npm run dev        # watches src/ → rebuilds dist/
# Directus with EXTENSIONS_AUTO_RELOAD=true picks up changes on save
```

Env var in Directus: `EXTENSIONS_AUTO_RELOAD=true` (dev only).

## Shipping

- **Private**: commit `dist/` or add to your CI; mount via Docker volume
- **Marketplace**: publish to npm with `directus-extension` keyword; Directus ≥11 pulls from npm directly

## Gotchas

- **Permissions in endpoints**: always pass `accountability` to `ItemsService` — otherwise all requests run as root
- **Hook ordering**: `filter` runs before the operation (can mutate payload, throw to abort); `action` runs after (cannot mutate)
- **App extensions need rebuild** when you change `options` — the admin UI caches schema
- **Bundle host range**: must match your Directus major version; update `host` on upgrade
- **TypeScript**: `@directus/extensions-sdk` gives you `defineHook`, `defineEndpoint`, etc. — use them for type safety
