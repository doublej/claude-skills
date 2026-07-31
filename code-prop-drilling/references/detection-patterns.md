# Detection Patterns — Framework-Specific Heuristics

Reference file for the code-prop-drilling skill. Contains grep patterns and search strategies per framework.

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

## 4. Python parameter signatures

### Function parameters
```
pattern: def\s+(\w+)\s*\(([^)]+)\)
```
Extract param names, skip `self`, `cls`, `*args`, `**kwargs`.

### __init__ parameters
```
pattern: def\s+__init__\s*\(\s*self\s*,([^)]+)\)
```

### Dataclass / Pydantic fields
```
pattern: (\w+)\s*:\s*\w+.*=\s*(?:Field|field)\(
pattern: @dataclass
pattern: class\s+\w+\(BaseModel\)
```

### FastAPI route parameters
```
pattern: @(?:app|router)\.(?:get|post|put|delete|patch)\(
pattern: Depends\(\w+\)
```

### Self-assignment (stored for forwarding)
```
pattern: self\.(\w+)\s*=\s*(\1)
```
A param stored as `self.x = x` that is only used as `self.x` in calls to sub-objects is drilling.

## 5. TypeScript (non-component) signatures

Family B. A `.ts` module exporting plain functions/classes — servers, CLIs, services, transports. Distinguish from family A by the absence of JSX/`.svelte` syntax in the file.

### Function parameters
```
pattern: export\s+(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)
pattern: const\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*(?::[^=]+)?=>
```

### Constructor-injected members (parameter properties)
```
pattern: constructor\s*\(([^)]*)\)
pattern: (?:private|public|protected|readonly)\s+(\w+)\s*:
```
`constructor(private readonly db: Db)` declares AND assigns in one step — if `this.db` is only read inside calls to another object, that is drilling.

### Deps / context object threading
```
pattern: (?:deps|ctx|context|env|services)\s*:\s*\{
pattern: interface\s+(\w*(?:Deps|Context|Ctx|Services))\b
```
A `Deps` object is only drilling when a layer receives it, reads none of its fields, and hands it on. A layer that reads even one field is a legitimate consumer.

### Factory closures (the composition root)
```
pattern: export\s+function\s+create(\w+)\s*\(([^)]*)\)
```
Params captured by a returned closure are NOT drilled — the closure is the injection point.

## 6. C++ signatures

Family B. The drilling signature is a constructor param stored in a trailing-underscore member that is only ever read to construct or call something else.

### Constructor parameters
```
pattern: explicit\s+(\w+)\s*\(([^)]*)\)
pattern: ^\s*(\w+)\s*\(([^)]*)\)\s*(?::|;|\{)
```

### Member-initialiser list (param → member binding)
```
pattern: \)\s*:\s*((?:\w+_?\(\w+\)\s*,?\s*)+)
pattern: (\w+_)\s*\(\s*(\w+)\s*\)
```
Match `member_(param)` pairs, then check whether `member_` is read anywhere except as an argument.

### Member declarations
```
pattern: ^\s*(?:const\s+)?[\w:<>,\s*&]+\s+(\w+_)\s*(?:=|;)
```

### Sub-object construction (the forwarding edge)
```
pattern: std::make_(?:unique|shared)<(\w+)>\(([^)]*)\)
pattern: new\s+(\w+)\s*\(([^)]*)\)
pattern: (\w+)_?\s*\{\s*([^}]*)\s*\}      # brace init of a member
```

### Free-function parameter forwarding
```
pattern: \b(\w+)\s*\(([^)]*\b\w+\b[^)]*)\)\s*;
```
Narrow to calls whose arguments are verbatim the enclosing function's params.

## 7. Zig signatures

Family B. Zig has no hidden injection — everything is an explicit param or struct field, which makes the graph easy to read and makes over-reporting easy too. Filter hard (see §12).

### Function parameters
```
pattern: pub\s+fn\s+(\w+)\s*\(([^)]*)\)
pattern: fn\s+(\w+)\s*\(([^)]*)\)
```

### init / deinit constructors
```
pattern: pub\s+fn\s+init\s*\(([^)]*)\)
```
`init(gpa, cfg)` storing `.cfg = cfg` into the struct, where `self.cfg` is only read to build a sub-struct, is drilling.

### Struct fields set from params
```
pattern: (\w+)\s*:\s*[\w\.\[\]\*\?!]+\s*(?:=\s*[^,]+)?,
pattern: \.(\w+)\s*=\s*(\1)\b        # .cfg = cfg — field bound straight from a param
```

### Sub-struct construction (the forwarding edge)
```
pattern: (\w+)\.init\(([^)]*)\)
pattern: (\w+)\{\s*(\.\w+\s*=\s*[^,}]+,?\s*)+\}
```

### Context-struct convention
```
pattern: (?:Context|Ctx|Deps|Env)\s*=\s*struct\s*\{
```
Already-grouped deps — a layer passing an existing `Context` through is the intended design, not drilling.

## 8. C# signatures

Family B, constructor injection.

### Constructor parameters
```
pattern: public\s+(\w+)\s*\(([^)]*)\)\s*(?:\{|:)
```

### Injected readonly fields
```
pattern: private\s+readonly\s+([\w<>,\s]+)\s+(_\w+)\s*;
pattern: (_\w+)\s*=\s*(\w+)\s*;        # _config = config
```

### Primary constructors (C# 12+)
```
pattern: (?:class|record|struct)\s+(\w+)\s*\(([^)]*)\)
```

### Sub-object construction (the forwarding edge)
```
pattern: new\s+(\w+)\s*\(([^)]*)\)
```

### DI registration (the destination, not a finding)
```
pattern: services\.Add(?:Singleton|Scoped|Transient)<
pattern: IOptions<(\w+)>
```

## 9. Kotlin / Java signatures

Family B. On Android the layer graph is usually shallow; expect few real findings and many `Context` false positives.

### Kotlin constructor / function params
```
pattern: class\s+(\w+)\s*(?:@\w+\s*)?\(([^)]*)\)
pattern: fun\s+(\w+)\s*\(([^)]*)\)
pattern: (?:private\s+)?val\s+(\w+)\s*:\s*(\w+)
```

### Java constructor / fields
```
pattern: public\s+(\w+)\s*\(([^)]*)\)\s*\{
pattern: private\s+final\s+([\w<>]+)\s+(\w+)\s*;
```

### DI annotations (the destination, not a finding)
```
pattern: @(?:Inject|Provides|Binds|Module|HiltAndroidApp|AndroidEntryPoint)
pattern: CompositionLocal(?:Of|Provider)
```

## 10. Prop forwarding patterns

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

### Python explicit pass-through
```
Python:  child_func(config=config) or Child(db=self.db)
         pattern: (\w+)\s*=\s*(?:self\.)?(\1)
         pattern: \w+\(.*\b(\w+)\s*=\s*(?:self\.)?(\1)
```

### Spread forwarding
```
React:   {...props}
         pattern: \{\s*\.\.\.(?:props|rest\w*)\s*\}

Vue:     v-bind="$attrs"
         pattern: v-bind="\$attrs"

Svelte:  {...$$restProps}
         pattern: \{\s*\.\.\.\$\$restProps\s*\}

Python:  **kwargs
         pattern: \*\*kwargs
         pattern: \*\*\w+
```

### Family B explicit pass-through

A param handed on under the same name, or a stored member handed on, with no read in between:

```
TypeScript:  child(ctx) / new Child(this.db)
             pattern: \w+\(\s*(?:this\.)?(\w+)\s*[,)]

C++:         Child(cfg) / std::make_unique<Child>(cfg_)
             pattern: (?:make_unique|make_shared)<\w+>\(\s*(\w+_?)\s*[,)]
             pattern: \w+\(\s*(\w+_)\s*[,)]

Zig:         Child.init(gpa, cfg) / .{ .cfg = cfg }
             pattern: \w+\.init\(\s*[^)]*\b(\w+)\b[^)]*\)
             pattern: \.(\w+)\s*=\s*(?:self\.)?(\1)\b

C#:          new Child(_config)
             pattern: new\s+\w+\(\s*(?:this\.)?(_?\w+)\s*[,)]

Kotlin/Java: Child(config) / new Child(this.config)
             pattern: \w+\(\s*(?:this\.)?(\w+)\s*[,)]
```

### Family B spread / variadic forwarding (never drilling)

```
C++:         std::forward<Args>(args)...   perfect forwarding
             pattern: std::forward<[^>]+>\(

Zig:         args: anytype  /  @call(.auto, f, args)
             pattern: :\s*anytype\b

C#:          params object[] args
             pattern: \bparams\s+\w+\[\]

Kotlin:      vararg args
             pattern: \bvararg\b
```

## 11. Child component/function call patterns

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

### Python function/constructor calls
```
pattern: (\w+)\(                    # function calls
pattern: self\.(\w+)\s*=\s*(\w+)\(  # constructor assignment
```
Track which params from the current function are passed as arguments to these calls.

### Family B ownership edges

For C++, Zig, C#, Kotlin/Java and class-based TypeScript, the graph edge is usually **ownership**, not a call: layer A owns an instance of layer B, so A's constructor is where B's dependencies get handed over.

```
C++:         member declared as std::unique_ptr<Child> child_;
             pattern: (?:unique_ptr|shared_ptr|optional)<(\w+)>\s+(\w+_)

Zig:         field declared as child: Child,
             pattern: (\w+)\s*:\s*([A-Z]\w+)\s*,

C#:          private readonly Child _child;
             pattern: private\s+readonly\s+(\w+)\s+(_\w+)

Kotlin:      private val child: Child
             pattern: private\s+val\s+(\w+)\s*:\s*(\w+)
```

Resolve the owned type to its own file, then continue the walk there. An ownership chain three classes deep with the same ctor param at each level is the canonical family-B CRITICAL finding.

## 12. False positive filters

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

### Python-specific false positives
Skip these — they are NOT parameter drilling:

```
# self, cls — implicit instance/class reference
pattern: ^(self|cls)$

# *args, **kwargs — intentional forwarding
pattern: ^\*

# Logging/debug params — commonly passed everywhere
pattern: ^(logger|log|verbose|debug|quiet)$

# FastAPI Depends() — DI-resolved, not drilled
pattern: Depends\(

# Abstract/protocol method implementations — params required by interface
# Check if class inherits ABC or Protocol
pattern: class\s+\w+\(.*(?:ABC|Protocol)

# Decorator-injected params (click, typer, etc.)
pattern: @click\.|@typer\.
```

### The mandatory-threading set — NEVER flag

These must appear at every layer for the code to be *correct*. Reporting them is worse than reporting nothing: the "fix" breaks cancellation, leaks memory, or leaks an Activity.

```
Zig:          std.mem.Allocator, allocator, gpa, arena
              pattern: :\s*(?:std\.mem\.)?Allocator\b
              Explicit allocator passing IS the language convention. Never a finding.

C#:           CancellationToken
              pattern: CancellationToken\s+\w+
              Cooperative cancellation only works if threaded to every await point.

TypeScript:   AbortSignal, signal
              pattern: :\s*AbortSignal\b

Kotlin/Java:  android.content.Context, Activity, Application
              pattern: :\s*Context\b  |  \bContext\s+\w+
              Platform APIs require it at the call site; hoisting it leaks the Activity.

Go-style ctx: ctx, context (TypeScript/Hono/Koa/Express handler signatures)
              pattern: \bctx\b|\bcontext\b
```

### TypeScript (family B) false positives
```
# Framework handler signature — req/res/next/ctx are the contract, not drilling
pattern: \((?:req|request|res|response|next|ctx|c)\b

# Factory closure params — captured, which IS the injection
pattern: export\s+function\s+create\w+\s*\(

# Generic type params and branded types
pattern: <[A-Z]\w*(?:\s*extends\b)?
```

### C++ false positives
```
# Perfect forwarding / variadic templates — deliberate pass-through
pattern: std::forward<|template\s*<[^>]*\.\.\.

# Allocator, executor, io_context — same mandatory-threading logic as Zig's allocator
pattern: \b(?:allocator|executor|io_context|io_service)\b

# Pimpl handle — impl_ exists precisely to be forwarded
pattern: (?:std::unique_ptr<\w*Impl>|\bimpl_\b)

# Non-owning observer params required by an API contract
pattern: \bconst\s+\w+\s*&\s*\w+\s*\)   # const& is often read-only borrow, verify before flagging

# RAII scope guards / lock guards
pattern: \b(?:lock_guard|unique_lock|scoped_lock|shared_lock)\b
```

Also skip anything under `third_party/`, `vendor/`, or a vendored upstream library (opus, ffmpeg, quirc, ggwave, stb, imgui). The project does not own that code.

### Zig false positives
```
# Allocator — see the mandatory set above. This is the #1 Zig false positive.
pattern: (?:gpa|allocator|arena|alloc)\s*:\s*(?:std\.mem\.)?Allocator

# comptime params — resolved at compile time, no runtime flow
pattern: comptime\s+\w+\s*:

# anytype varargs — deliberate forwarding
pattern: :\s*anytype\b

# self receiver
pattern: self\s*:\s*(?:\*|\*const\s+)?@This\(\)|self\s*:\s*(?:\*)?\w+

# Error-set and type params
pattern: :\s*type\b
```

### C# false positives
```
# CancellationToken — see the mandatory set above
pattern: CancellationToken

# Framework-injected services that are meant to reach every layer
pattern: \b(?:IServiceProvider|ILogger<|ILoggerFactory|IConfiguration)\b

# IOptions<T> — already the DI answer to config drilling
pattern: IOptions<

# Records with positional params (data carriers, not layers)
pattern: record\s+(?:class\s+|struct\s+)?\w+\s*\(
```

### Kotlin / Java false positives
```
# Android Context — see the mandatory set above
pattern: \bContext\b

# DI-annotated ctors — already wired, not drilled
pattern: @Inject|@AssistedInject|@HiltViewModel

# Coroutine scope / dispatcher — threading these is the concurrency contract
pattern: \b(?:CoroutineScope|CoroutineDispatcher|CoroutineContext)\b

# data class primary ctor — a data carrier, not a layer
pattern: data\s+class\s+\w+\s*\(
```

### Common non-drilling props/params
Skip these utility props that are typically passed at every level:
```
Frontend:    className, class, style, id, key, data-testid, aria-*, role, tabIndex
Python:      self, cls, logger, verbose, debug
TypeScript:  ctx, req, res, next, signal, logger
C++:         allocator, alloc, logger, impl_
Zig:         gpa, allocator, arena, self, comptime params
C#:          CancellationToken, ILogger, IServiceProvider
Kotlin/Java: Context, CoroutineScope, savedStateHandle
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

### Python-specific search strategy

1. **Start with `__init__` methods** — classes storing params as `self.x = x` only to pass to sub-objects are the primary drilling pattern
2. **Trace service layers** — route handler → service → repository chains are common drilling paths
3. **Check config/settings objects** — a `config` param passed 3+ levels deep is often better served by DI or module-level access
4. **Focus on non-`__init__` functions** — functions receiving params only to forward them to other functions

### Family B search strategy (TypeScript, C++, Zig, C#, Kotlin/Java)

1. **Start at the constructors.** In every one of these languages the drilling signature is the same shape: a ctor param stored into a field (`this.x`, `x_`, `_x`, `.x = x`) that is only ever read as an argument. Grep the assignment, then grep the field's every read.
2. **Follow ownership, not calls.** A layer is usually a class that *owns* the next class. Resolve `unique_ptr<Child> child_` / `private readonly Child _child` / `child: Child` to that type's file and continue there. Call-graph walking finds far fewer real chains than ownership walking.
3. **The composition root is the boundary.** `main()`, `Program.cs`, `createServer()`, `Application.onCreate()` — a param that originates there and reaches a leaf unchanged is the classic chain. Start from the root and walk down once, rather than tracing every leaf upward.
4. **Config objects are the usual culprit.** A `Config`/`Settings`/`Options` struct threaded 3+ levels where each level reads one or two fields is the highest-value finding in family B, and narrowing the signature fixes it without any container.
5. **Header-first in C++.** Read `.h`/`.hpp` only to build the graph — ctor signatures and member declarations both live there. Open the `.cpp` only to confirm whether a member is *read* or merely forwarded.
6. **Watch the LoC-split files.** Codebases with a per-file line cap split one logical layer across siblings (`foo.zig` + `foo_impl.zig`, `layout.zig` + `layout_pack.zig`). Those are one layer, not two — collapse them before counting depth, or every chain inflates by one.

### Polyglot repos

Scan one language at a time and keep the chains separate. A prop cannot drill across a C-ABI boundary or a socket — where a value crosses from TypeScript to Zig to C++, that is a *protocol*, not a call chain, and its "layers" are wire messages. Report those boundaries as the natural chain terminators, never as intermediaries.
