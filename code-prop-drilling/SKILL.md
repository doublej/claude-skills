---
name: code-prop-drilling
description: "Detect/fix prop drilling — props, parameters, or constructor-injected members threaded through 2+ layers that never use them. Component trees (React, Vue, Svelte) and call chains / object graphs (TypeScript services, Python, C++, Zig, C#, Kotlin/Java). Use only when the user explicitly asks about prop drilling, parameter threading, dependency threading, or refactoring how data flows through a component tree or call chain. NOT for generic UI, styling, or layout work."
---

# Prop Drilling Detector

Scan component trees or call chains to find props, parameters, and injected members passed through 2+ intermediate layers without being used, rank by severity, and recommend language-appropriate fixes.

Pure analysis skill — uses Glob, Grep, Read. No scripts.

<scope>
## When to use

Only when the user explicitly asks about prop drilling, data/state threading, parameter threading, or dependency threading through a component tree or call chain.

## When NOT to use

Do not run this skill for generic UI, styling, layout, label-wrapping, or visual-polish tasks — even if a screenshot of components is attached. Those are unrelated to prop-drilling detection. If the request is about how something *looks* rather than how data *flows*, this skill does not apply; stop and let the appropriate UI work proceed.
</scope>

<families>
## The two families

Every supported language falls into one of two shapes. Detect the family first — it decides what "a layer" means and which false-positive filters apply.

| Family | Languages | A "layer" is | Drilling looks like |
|--------|-----------|-------------|---------------------|
| **A — Component tree** | React, Vue, Svelte | A component that renders a child | A prop declared, never read, passed straight to a child |
| **B — Call chain / object graph** | TypeScript (non-component), Python, C++, Zig, C#, Kotlin/Java | A function that calls another, or a class that owns another | A param or ctor-injected member stored/forwarded but never read |

A polyglot repo has both. Scan each family separately and report them in one table — a chain never crosses a language boundary, so they never merge.
</families>

<phase1>
## Phase 1 — Detect languages & existing wiring

### Detect language / framework

Glob for source files and check manifests:

| Signal | Language | Family |
|--------|----------|--------|
| `*.tsx`, `*.jsx`, `react` in deps | React | A |
| `*.vue`, `vue` in deps | Vue | A |
| `*.svelte`, `svelte` in deps | Svelte | A |
| `*.ts`/`*.js` with no component framework in the file | TypeScript (services, CLIs, servers) | B |
| `*.py`, `pyproject.toml`, `setup.py` | Python | B |
| `*.cpp`, `*.cc`, `*.h`, `*.hpp`, `CMakeLists.txt` | C++ | B |
| `*.zig`, `build.zig`, `build.zig.zon` | Zig | B |
| `*.cs`, `*.csproj`, `*.sln` | C# | B |
| `*.kt`, `*.java`, `build.gradle(.kts)` | Kotlin / Java | B |

A single `.ts` file can be either family: a `.svelte`/`.tsx` file is family A, a `.ts` module exporting plain functions or classes is family B. Classify per file, not per repo.

### Detect existing state management / DI

Check manifests and imports — an existing container is almost always the right destination for drilled state:

| Package / Import | Wiring system |
|------------------|--------------|
| `redux`, `@reduxjs/toolkit` | Redux |
| `zustand` / `jotai` | Zustand / Jotai |
| `createContext`, `useContext` | React Context |
| `pinia` / `provide`, `inject` | Pinia / Vue provide-inject |
| `svelte/store`, `$state` | Svelte stores / runes |
| `AsyncLocalStorage` (node:async_hooks) | Node request-scoped context |
| `dependency_injector` / `contextvars` | Python DI container / context vars |
| `fastapi`, `Depends` | FastAPI dependency injection |
| A `struct Deps`/`Context`/`Ctx` passed by reference | C++ / Zig hand-rolled context |
| `IServiceCollection`, `AddSingleton`, `IOptions<T>` | .NET DI |
| `AsyncLocal<T>` | .NET ambient scope |
| `@Inject`, `@HiltAndroidApp`, `dagger` | Dagger / Hilt |
| `CompositionLocal` | Jetpack Compose ambient |

If `code-map` is installed, load its output for structural context. Otherwise proceed with direct scanning.
</phase1>

<phase2>
## Phase 2 — Build the flow map

Core detection phase. Load `{SKILL_DIR}/references/detection-patterns.md` for per-language grep patterns and the full false-positive list.

### Step 1: Inventory

Glob per detected language:

```
React:        **/*.{tsx,jsx}
Vue:          **/*.vue
Svelte:       **/*.svelte
TypeScript:   **/*.{ts,mts,cts}      (family B: exclude files with component syntax)
Python:       **/*.py
C++:          **/*.{cpp,cc,cxx,h,hpp}
Zig:          **/*.zig
C#:           **/*.cs
Kotlin/Java:  **/*.{kt,java}
```

Exclude: `node_modules`, `dist`, `build`, `.next`, `.nuxt`, `.svelte-kit`, `.venv`, `venv`, `__pycache__`, `.zig-cache`, `zig-out`, `target`, `obj`, `bin`, `third_party`, `vendor`, generated bindings, test files, story files.

**Vendored native code is the big trap.** C/C++ trees routinely contain an upstream library (opus, ffmpeg, quirc, ggwave) under `third_party/` or a sibling repo. Never report drilling inside code the project does not own — check whether the directory has its own upstream provenance before scanning it.

### Step 2: Extract signatures

Per language, extract what each layer declares it needs. Details in `references/detection-patterns.md`; the shape is:

| Language | Declaration to extract |
|----------|----------------------|
| React | Destructured params, `FC<Props>` + the `Props` type, `forwardRef`/`memo` wrappers |
| Vue | `defineProps<{}>()`, `defineProps([])`, Options-API `props:` |
| Svelte | `export let x` (v4), `let { x } = $props()` (v5) |
| TypeScript (B) | Function params, `constructor(private x: T)`, factory-closure params, a `Deps`/`Ctx` object's fields |
| Python | Function params, `__init__` params, dataclass/Pydantic fields |
| C++ | Ctor params + the `x_` members they initialise, function params (incl. `const&` and pointer deps) |
| Zig | `fn` params, `init()` params, struct fields set from those params |
| C# | Ctor params + the `readonly _x` fields they assign, method params |
| Kotlin/Java | Ctor params, `val`/`private final` fields, method params |

### Step 3: Classify each declared item

| Classification | Meaning |
|---------------|---------|
| **Used directly** | Read in logic, template, computation, or return value |
| **Passed down only** | Appears only as an argument to a child component / function / constructor |
| **Stored and forwarded** | Assigned to a field (`self.x`, `this.x`, `x_`, `_x`) that is only ever read to pass along |
| **Spread-forwarded** | Part of `{...props}`, `v-bind="$attrs"`, `$$restProps`, `**kwargs`, `std::forward`, `args: anytype` |

"Passed down only" and "stored and forwarded" are the drilling candidates. Spread-forwarding is deliberate — do not flag it.

### Step 4: Build the layer graph

| Family | Edge to detect |
|--------|---------------|
| A | Child renders: `<Child prop={prop} />`, `:prop="prop"`, `{prop}` |
| B | Calls and constructions: `child(x)`, `Child(x)`, `Child{ .x = x }`, `new Child(x)`, `std::make_unique<Child>(x_)` |

Build `Layer -> [{ callee, itemsForwarded }]`.

### Step 5: Identify drilling chains

Walk the graph for items flowing through 2+ intermediaries:

```
Source -> Passthrough1 -> Passthrough2 -> Consumer
         (not used)      (not used)      (used)
```

Record: `{ item, language, path: [layers...], depth, sourceLayer, consumerLayer }`.

### Step 6: Rank by severity

| Depth | Items in chain | Severity |
|-------|---------------|----------|
| 2 | any | LOW |
| 3 | any | MEDIUM |
| 4+ | 1-2 | HIGH |
| 4+ | 3+ | CRITICAL |

Also flag when 3+ separate chains share intermediate layers (systemic drilling).

**Downgrade one level** when every layer in the chain is in the same file — the fix is a local edit, not an architecture change.

### False positive filters

These are NOT prop drilling. The per-language list is the difference between a useful report and a useless one — read `references/detection-patterns.md` §12 before reporting.

**All languages:**
- Callback/handler params (`onClick`, `onSubmit`) and render props
- Logger/tracing params (`logger`, `verbose`, `debug`)
- Anything an external API or framework *requires* at every layer

**The four that dominate false positives in polyglot repos — never flag these:**

| Item | Language | Why it is not drilling |
|------|----------|----------------------|
| `std::mem.Allocator` | Zig | Explicit allocator passing is the language's central convention; every layer receiving one is idiomatic, not a defect |
| `CancellationToken` | C# | Cooperative cancellation is only correct if threaded through every await point |
| `android.content.Context` | Kotlin/Java | Platform APIs demand it at the call site; hoisting it into a singleton leaks activities |
| `AbortSignal` / `req`,`res`,`ctx` | TypeScript | Same cancellation contract; `ctx` in Hono/Koa/Express handlers is the framework's signature |

Also skip: React `children`/slots, `forwardRef` refs, HOC spreads, Python `self`/`*args`/`**kwargs`/`Depends()`, C++ perfect forwarding and pimpl handles, Zig `comptime` params and `anytype` varargs, C# `IServiceProvider`/`ILogger<T>`.
</phase2>

<phase3>
## Phase 3 — Recommend fix strategy

Load `{SKILL_DIR}/references/fix-strategies.md` for before/after code per language.

### Decision tree

```
Has existing state management / DI container?
├─ YES → Register the drilled item there
│        (Redux/Zustand slice, Pinia, Svelte store, FastAPI Depends,
│         IServiceCollection, Hilt module, an existing Deps/Ctx struct)
└─ NO
   ├─ Localised drilling (depth ≤3, ≤2 chains)
   │  ├─ React            → Context API or composition
   │  ├─ Vue              → provide/inject
   │  ├─ Svelte           → stores or module-level $state
   │  ├─ TypeScript (B)   → closure capture at the composition root
   │  ├─ Python           → contextvars or restructure the call chain
   │  ├─ C++              → narrow the signature: pass what the callee reads, not the owner
   │  ├─ Zig              → same narrowing, or a small const Context struct
   │  ├─ C#               → constructor injection one level down
   │  └─ Kotlin/Java      → constructor injection / CompositionLocal (Compose)
   └─ Systemic drilling (depth 4+ or 3+ chains)
      ├─ React            → Zustand (lightweight) or Jotai (atomic)
      ├─ Vue              → Pinia
      ├─ Svelte           → stores with module-level state
      ├─ TypeScript (B)   → a Deps object built once, or AsyncLocalStorage if request-scoped
      ├─ Python           → DI (FastAPI Depends, dependency-injector) or a config accessor
      ├─ C++              → a const Deps/Context struct passed by reference at construction
      ├─ Zig              → a Context struct owned by the caller, passed by pointer
      ├─ C#               → register in IServiceCollection; IOptions<T> for config
      └─ Kotlin/Java      → Dagger/Hilt, or an application-scoped container
```

### Narrowing before wiring

In family B the cheapest fix is usually not a container — it is **passing less**. If `Renderer` takes a whole `Config` only to read `config.timeout`, take `timeout`. That deletes the chain instead of rerouting it, and it makes the dependency legible in the signature. Try this first; reach for a container only when 3+ items travel together.

### Composition first (family A)

Before adding state management, check whether restructuring removes the drilling:
- Move the consumer up, closer to the data source
- Use compound components to share implicit context
- Use render props, slots, or `children` to pass data without intermediate props

### Realtime and embedded constraint

In hot paths — audio/video callbacks, render threads, encode workers, interrupt handlers — do **not** recommend a mutable global or a lock-protected singleton to fix drilling. The threading is often deliberate: it keeps the data flow lock-free and the lifetime obvious. Prefer a `const` context struct passed by reference at setup, or narrowing the signature. Say so explicitly in the report when a chain sits on such a path.
</phase3>

<phase4>
## Phase 4 — Generate report

Output a markdown report with these sections:

### Summary table

```markdown
| Severity | Count | Language | Deepest chain |
|----------|-------|----------|---------------|
| CRITICAL | N     | C++      | A → B → C → D → E |
| HIGH     | N     | ...      | ...           |
| MEDIUM   | N     | ...      | ...           |
| LOW      | N     | ...      | ...           |
```

### Per-chain detail

For each chain (ordered by severity):

```markdown
#### Chain: `itemName` (SEVERITY, <language>)

**Path:** LayerA → LayerB → LayerC → LayerD
**Depth:** 3 intermediaries
**Items drilled:** itemName, otherItem
**Recommended fix:** [strategy name]

**Before:** (code sketch of current drilling)
**After:** (code sketch with fix applied)
```

Cite each layer as `path/to/file.ext:line` so the chain is clickable.

### Action plan

Ordered list of fixes, grouped by strategy:

1. **Narrow signatures** — pass the field, not the owner
2. **Composition / restructure** — reshape these trees or call chains
3. **Context / provide-inject / ambient scope** — add these providers
4. **State management / DI container** — add or extend these

Each item: files to modify, estimated scope (small/medium/large). Flag any chain on a realtime path as **do not hoist to global**.
</phase4>

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `code-map` | Optional — provides structural context for faster scanning |
| `code-modularize` | Post-fix — split layers that grew from drilling workarounds |
| `code-arch-drift` | Sibling — drilling often marks an eroding layer boundary |
| `code-optimize` | Can consume findings in broader audit |
</content>
</invoke>
