---
name: prop-drilling
description: Detect and fix prop drilling in React, Vue, and Svelte. Scans components to find props passed through 2+ layers unused, recommends fixes (Context, Zustand, Pinia, stores, composition). Use when user mentions prop drilling, passing props through layers, or simplifying component data flow.
---

# Prop Drilling Detector

Scan component trees to find props passed through 2+ intermediate components without being used, rank by severity, and recommend framework-appropriate fixes.

Pure analysis skill — uses Glob, Grep, Read. No scripts.

## Phase 1 — Detect Framework & State Management

### Detect framework

Glob for component files and check `package.json` dependencies:

| Signal | Framework |
|--------|-----------|
| `*.tsx`, `*.jsx`, `react` in deps | React |
| `*.vue`, `vue` in deps | Vue |
| `*.svelte`, `svelte` in deps | Svelte |

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

If `codebase-mapper` is installed, load its output for structural context. Otherwise proceed with direct scanning.

## Phase 2 — Build Prop-Flow Map

This is the core detection phase. Load `{SKILL_DIR}/references/detection-patterns.md` for framework-specific grep patterns.

### Step 1: Inventory components

Glob for all component files:

```
React:   **/*.{tsx,jsx}
Vue:     **/*.vue
Svelte:  **/*.svelte
```

Exclude `node_modules`, `dist`, `build`, `.next`, `.nuxt`, `.svelte-kit`, test files, and story files.

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

### Step 3: Classify prop usage

For each prop in each component, classify as:

| Classification | Meaning |
|---------------|---------|
| **Used directly** | Referenced in logic, template, or computed values |
| **Passed down only** | Appears only as an attribute on a child component |
| **Spread-forwarded** | Part of `{...props}`, `v-bind="$attrs"`, or `$$restProps` |

A prop classified as "passed down only" is a drilling candidate.

### Step 4: Build parent-child chains

Scan JSX/template for child component renders:

```
React:   <ChildComp propName={propName} />
Vue:     <ChildComp :propName="propName" /> or v-bind
Svelte:  <ChildComp {propName} /> or propName={propName}
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

See `{SKILL_DIR}/references/detection-patterns.md` for specific patterns to filter.

## Phase 3 — Recommend Fix Strategy

Load `{SKILL_DIR}/references/fix-strategies.md` for before/after code patterns.

### Decision tree

```
Has existing state management?
├─ YES → Add drilled state to existing store
│        (Redux slice, Zustand store, Pinia store, Svelte store)
└─ NO
   ├─ Localised drilling (depth ≤3, ≤2 chains)
   │  ├─ React → Context API or component composition
   │  ├─ Vue → provide/inject
   │  └─ Svelte → Svelte stores or $state
   └─ Systemic drilling (depth 4+ or 3+ chains)
      ├─ React → Zustand (lightweight) or Jotai (atomic)
      ├─ Vue → Pinia
      └─ Svelte → Svelte stores with module-level state
```

### Composition first

Before adding state management, check if the drilling can be solved by restructuring the component tree:

- Move the consumer component up (closer to the data source)
- Use compound components to share implicit context
- Use render props or slots to pass data without intermediate props

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

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `codebase-mapper` | Optional — provides structural context for faster scanning |
| `modularize` | Post-fix — split components that grew from drilling workarounds |
| `dev-refactor` | Can consume findings in broader audit |
