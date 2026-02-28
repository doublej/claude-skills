# Detection Patterns — Framework-Specific Heuristics

Reference file for the prop-drilling skill. Contains grep patterns and search strategies per framework.

## 1. React prop signatures

### Function component destructuring
```
pattern: function\s+\w+\s*\(\s*\{([^}]+)\}
pattern: const\s+\w+\s*[:=]\s*(?:\([^)]*\)\s*=>|function)\s*\(\s*\{([^}]+)\}
```

### FC/Component type annotation
```
pattern: :\s*(?:React\.)?FC<(\w+)>
pattern: :\s*(?:React\.)?ComponentProps<
```
Then find the Props interface/type to get the full prop list.

### Props interface/type
```
pattern: (?:interface|type)\s+\w*Props\w*\s*[={]
```

### forwardRef wrapper
```
pattern: React\.forwardRef<[^,]+,\s*(\w+)>
pattern: forwardRef\(\s*\(\s*\{([^}]+)\}
```

## 2. Vue prop signatures

### Composition API (defineProps)
```
pattern: defineProps<\{([^}]+)\}>
pattern: defineProps\(\[([^\]]+)\]\)
pattern: defineProps\(\{([^}]+)\}\)
```

### Options API
```
pattern: props\s*:\s*\{
pattern: props\s*:\s*\[
```

### v-bind shorthand
```
pattern: v-bind="\$attrs"
pattern: v-bind="[^"]*"
```

## 3. Svelte prop signatures

### Svelte 4 (export let)
```
pattern: export\s+let\s+(\w+)
```

### Svelte 5 ($props)
```
pattern: let\s+\{([^}]+)\}\s*=\s*\$props\(\)
```

### $$restProps / $$props
```
pattern: \$\$restProps
pattern: \$\$props
```

## 4. Prop forwarding patterns

These indicate a component is passing props through without using them.

### Explicit pass-through
```
React:   <Child propName={propName} />
         pattern: <(\w+)\s[^>]*\b(\w+)=\{(\2)\}

Vue:     <Child :propName="propName" />
         pattern: <(\w+)\s[^>]*:(\w+)="(\2)"

Svelte:  <Child {propName} />
         pattern: <(\w+)\s[^>]*\{(\w+)\}
```

### Spread forwarding
```
React:   {...props}
         pattern: \{\s*\.\.\.(?:props|rest\w*)\s*\}

Vue:     v-bind="$attrs"
         pattern: v-bind="\$attrs"

Svelte:  {...$$restProps}
         pattern: \{\s*\.\.\.\$\$restProps\s*\}
```

## 5. Child component rendering patterns

### React JSX
```
pattern: <([A-Z]\w+)\s
```
Match PascalCase tags to find child component renders. Extract prop attributes:
```
pattern: <([A-Z]\w+)\s([^>]+)>
```

### Vue template
```
pattern: <([A-Z]\w+|[a-z]+-[a-z]+)\s
```
Match PascalCase or kebab-case component tags.

### Svelte template
```
pattern: <([A-Z]\w+)\s
```
Same as React — PascalCase denotes components.

## 6. False positive filters

### Callback/event handler props
Skip props matching these patterns — they are intentional pass-down:
```
pattern: ^on[A-Z]         # onClick, onSubmit, onChange
pattern: ^handle[A-Z]     # handleClick, handleSubmit
pattern: ^set[A-Z]        # setState-style setters (still flag if drilled 3+ levels)
```

Exception: still flag `set*` callbacks if drilled through 3+ intermediaries.

### Render props
Skip components where the prop is a function returning JSX:
```
pattern: render[A-Z]\w*    # renderItem, renderHeader
pattern: \w+\s*=\s*\{?\s*\([^)]*\)\s*=>.*<  # arrow returning JSX
```

### Ref forwarding
Skip `ref` prop in `forwardRef` wrappers:
```
pattern: forwardRef
```
The `ref` prop in these is architectural, not drilling.

### Children/slot props
Skip these entirely:
```
React:   children
Vue:     slot, $slots
Svelte:  slot, $$slots
```

### HOC patterns
Skip components that are HOC wrappers spreading all props:
```
pattern: export\s+default\s+\w+\(\w+\)   # withRouter(Comp), connect()(Comp)
pattern: \{\s*\.\.\.(?:props|rest)\s*\}   # full spread = intentional pass-through
```

### Common non-drilling props
Skip these utility props that are typically passed at every level:
```
className, class, style, id, key, data-testid, aria-*, role, tabIndex
```

## Search strategy

### Efficient scanning order

1. **Start with imports** — grep for component imports to build the dependency graph faster than reading every file
2. **Focus on intermediaries** — components that both receive and pass down props are the drilling suspects
3. **Depth-first from leaves** — start from leaf components with props, trace upward to find the source
4. **Skip utility components** — components like `Button`, `Input`, `Icon` that intentionally accept many props are not drilling

### Performance tips

- For large codebases (500+ components), scan in batches of ~50 files
- Use Grep with `files_with_matches` mode first to narrow candidates before reading full files
- Skip files under 10 lines — too small to be intermediaries
