---
name: code-prop-drilling
description: "Detect/fix props passed through 2+ layers unused in React, Vue, Svelte, Python"
---

# Prop Drilling Detector

Scan component trees or call chains to find props/parameters passed through 2+ intermediate layers without being used, rank by severity, and recommend framework-appropriate fixes.

Pure analysis skill — uses Glob, Grep, Read. No scripts.

<phase1>
## Phase 1 — Detect Framework & State Management

### Detect framework

Glob for component files and check `package.json` dependencies:

| Signal | Framework |
|--------|-----------|
| `*.tsx`, `*.jsx`, `react` in deps | React |
| `*.vue`, `vue` in deps | Vue |
| `*.svelte`, `svelte` in deps | Svelte |
| `*.py`, `pyproject.toml`, `setup.py` | Python |

### Detect existing state management

Check `package.json` and imports:

| Package / Import | State system |
|------------------|-------------|
| `redux`, `@reduxjs/toolkit` | Redux |
| `zustand` | Zustand |
| `jotai` | Jotai |
| `createContext`, `useContext` | React Context |
| `pinia` | Pinia |
| `provide`, `inject` | Vue provide/inject |
| `svelte/store`, `$state` | Svelte stores |
| `dependency_injector` | Python DI container |
| `contextvars` | Python context variables |
| `fastapi`, `Depends` | FastAPI dependency injection |

If `codebase-mapper` is installed, load its output for structural context. Otherwise proceed with direct scanning.
</phase1>

<phase2>
## Phase 2 — Build Prop-Flow Map

This is the core detection phase. Load `{SKILL_DIR}/references/detection-patterns.md` for framework-specific grep patterns.

### Step 1: Inventory components

Glob for all component/module files:

```
React:   **/*.{tsx,jsx}
Vue:     **/*.vue
Svelte:  **/*.svelte
Python:  **/*.py
```

Exclude `node_modules`, `dist`, `build`, `.next`, `.nuxt`, `.svelte-kit`, `.venv`, `venv`, `__pycache__`, test files, and story files.

### Step 2: Extract prop signatures

Read each component and extract declared props per framework:

**React:**
- Function params: `function Comp({ prop1, prop2 })`
- FC type: `const Comp: FC<Props>` then find `Props` interface/type
- `React.memo`, `forwardRef` wrappers

**Vue:**
- `defineProps<{ prop1: string }>()` or `defineProps(['prop1'])`
- Options API: `props: { prop1: { type: String } }`

**Svelte:**
- Svelte 4: `export let prop1`
- Svelte 5: `let { prop1, prop2 } = $props()`

**Python:**
- Function params: `def func(param1, param2, config):`
- `__init__` params: `def __init__(self, db, config, logger):`
- Dataclass/Pydantic fields used only to pass to sub-objects
- FastAPI route params passed through to service layers

### Step 3: Classify prop usage

For each prop in each component, classify as:

| Classification | Meaning |
|---------------|---------|
| **Used directly** | Referenced in logic, template, or computed values |
| **Passed down only** | Appears only as an attribute on a child component |
| **Spread-forwarded** | Part of `{...props}`, `v-bind="$attrs"`, or `$$restProps` |

A prop classified as "passed down only" is a drilling candidate.

**Python-specific classifications:**

| Classification | Meaning |
|---------------|---------|
| **Used directly** | Referenced in method body, computation, or return value |
| **Passed down only** | Only appears as argument in a call to another function/constructor |
| **Stored and forwarded** | Assigned to `self.x` but only used to pass to sub-objects |

### Step 4: Build parent-child chains

Scan JSX/template for child component renders:

```
React:   <ChildComp propName={propName} />
Vue:     <ChildComp :propName="propName" /> or v-bind
Svelte:  <ChildComp {propName} /> or propName={propName}
Python:  child_func(param=param) or ChildClass(config=self.config)
```

Build a map: `Parent -> [{ child, propsPassedDown }]`.

### Step 5: Identify drilling chains

Walk the parent-child map to find chains where a prop flows through 2+ intermediaries:

```
Source -> Passthrough1 -> Passthrough2 -> Consumer
         (not used)      (not used)      (used)
```

Record each chain as: `{ prop, path: [components...], depth, sourceComponent, consumerComponent }`.

### Step 6: Rank by severity

| Depth | Props in chain | Severity |
|-------|---------------|----------|
| 2 | any | LOW |
| 3 | any | MEDIUM |
| 4+ | 1-2 | HIGH |
| 4+ | 3+ | CRITICAL |

Also flag when 3+ separate chains share intermediate components (systemic drilling).

### False positive filters

Skip these patterns — they are NOT prop drilling:

- **Callback props** — functions passed down for event handling (`onClick`, `onSubmit`)
- **Render props** — functions returning JSX
- **Ref forwarding** — `React.forwardRef` wrappers
- **HOC pass-through** — higher-order components spreading props
- **Slot/children props** — `children`, Vue slots, Svelte slots
- **Compound component internals** — props within a compound component pattern
- **Python `self` params** — `self` is not a drilled parameter
- **Python `*args`/`**kwargs` forwarding** — intentional pass-through pattern
- **Logger/debug params** — `logger`, `verbose`, `debug` passed through layers
- **FastAPI `Depends()` results** — DI-resolved, not manually drilled

See `{SKILL_DIR}/references/detection-patterns.md` for specific patterns to filter.
</phase2>

<phase3>
## Phase 3 — Recommend Fix Strategy

Load `{SKILL_DIR}/references/fix-strategies.md` for before/after code patterns.

### Decision tree

```
Has existing state management / DI?
├─ YES → Add drilled state to existing store / DI container
│        (Redux slice, Zustand store, Pinia store, Svelte store, DI container)
└─ NO
   ├─ Localised drilling (depth ≤3, ≤2 chains)
   │  ├─ React → Context API or component composition
   │  ├─ Vue → provide/inject
   │  ├─ Svelte → Svelte stores or $state
   │  └─ Python → Module-level state, contextvars, or restructure call chain
   └─ Systemic drilling (depth 4+ or 3+ chains)
      ├─ React → Zustand (lightweight) or Jotai (atomic)
      ├─ Vue → Pinia
      ├─ Svelte → Svelte stores with module-level state
      └─ Python → Dependency injection (FastAPI Depends, dependency-injector) or config object
```

### Composition first

Before adding state management, check if the drilling can be solved by restructuring the component tree:

- Move the consumer component up (closer to the data source)
- Use compound components to share implicit context
- Use render props or slots to pass data without intermediate props
</phase3>

<phase4>
## Phase 4 — Generate Report

Output a markdown report with these sections:

### Summary table

```markdown
| Severity | Count | Deepest chain |
|----------|-------|---------------|
| CRITICAL | N     | A → B → C → D → E |
| HIGH     | N     | ...           |
| MEDIUM   | N     | ...           |
| LOW      | N     | ...           |
```

### Per-chain detail

For each drilling chain (ordered by severity):

```markdown
#### Chain: `propName` (SEVERITY)

**Path:** ComponentA → ComponentB → ComponentC → ComponentD
**Depth:** 3 intermediaries
**Props drilled:** propName, otherProp
**Recommended fix:** [strategy name]

**Before:** (code sketch of current drilling)
**After:** (code sketch with fix applied)
```

### Action plan

Ordered list of fixes, grouped by strategy:

1. **Composition changes** — restructure these component trees
2. **Context/provide-inject** — add these context providers
3. **State management** — add these stores

Each item: files to modify, estimated scope (small/medium/large).
</phase4>

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `codebase-mapper` | Optional — provides structural context for faster scanning |
| `modularize` | Post-fix — split components that grew from drilling workarounds |
| `dev-refactor` | Can consume findings in broader audit |
