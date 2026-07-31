# Fix Strategies — Before/After Patterns

Reference file for the code-prop-drilling skill. Each strategy shows the drilling problem and its fix.

## 1. React Context API

**When:** Localised drilling (depth ≤3), no existing state management, data used by multiple siblings.

**Before — drilling:**
```tsx
function App() {
  const [user, setUser] = useState<User>(initialUser);
  return <Layout user={user} />;
}

function Layout({ user }: { user: User }) {
  // Does NOT use user — just passes it down
  return <Sidebar user={user} />;
}

function Sidebar({ user }: { user: User }) {
  return <p>{user.name}</p>;
}
```

**After — Context:**
```tsx
const UserContext = createContext<User>(initialUser);

function App() {
  const [user, setUser] = useState<User>(initialUser);
  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}

function Layout() {
  return <Sidebar />;
}

function Sidebar() {
  const user = useContext(UserContext);
  return <p>{user.name}</p>;
}
```

## 2. Zustand

**When:** React, systemic drilling (4+ depth or 3+ chains), or need for fine-grained subscriptions.

**Before — drilling:**
```tsx
function App() {
  const [theme, setTheme] = useState('light');
  return <Shell theme={theme} setTheme={setTheme} />;
}
// Shell -> Panel -> Header -> ThemeToggle (4 levels)
```

**After — Zustand store:**
```tsx
// stores/theme.ts
import { create } from 'zustand';

interface ThemeStore {
  theme: string;
  setTheme: (theme: string) => void;
}

export const useThemeStore = create<ThemeStore>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}));

// ThemeToggle.tsx — consumes directly
function ThemeToggle() {
  const { theme, setTheme } = useThemeStore();
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>{theme}</button>;
}
```

## 3. Jotai

**When:** React, atomic state needed, multiple independent pieces drilled separately.

**Before — multiple drilled props:**
```tsx
function App() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  return <Dashboard count={count} name={name} setCount={setCount} setName={setName} />;
}
```

**After — atoms:**
```tsx
// atoms.ts
import { atom } from 'jotai';
export const countAtom = atom(0);
export const nameAtom = atom('');

// DeepChild.tsx — subscribes to only what it needs
import { useAtom } from 'jotai';
import { countAtom } from './atoms';

function DeepChild() {
  const [count, setCount] = useAtom(countAtom);
  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>;
}
```

## 4. Vue provide/inject

**When:** Vue, localised drilling (depth ≤3).

**Before — drilling:**
```vue
<!-- Parent.vue -->
<template>
  <MiddleLayer :user="user" />
</template>

<!-- MiddleLayer.vue — doesn't use user -->
<template>
  <DeepChild :user="user" />
</template>
<script setup>
defineProps<{ user: User }>();
</script>
```

**After — provide/inject:**
```vue
<!-- Parent.vue -->
<script setup>
import { provide } from 'vue';
provide('user', user);
</script>
<template>
  <MiddleLayer />
</template>

<!-- MiddleLayer.vue — no props needed -->
<template>
  <DeepChild />
</template>

<!-- DeepChild.vue -->
<script setup>
import { inject } from 'vue';
const user = inject<User>('user');
</script>
```

## 5. Pinia

**When:** Vue, systemic drilling (4+ depth or 3+ chains), or need for devtools support.

**Before — drilling through 4+ layers:**
```vue
<!-- App -> Layout -> Panel -> Sidebar -> UserCard -->
<script setup>
defineProps<{ user: User; updateUser: (u: User) => void }>();
</script>
```

**After — Pinia store:**
```ts
// stores/user.ts
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
  const user = ref<User>(initialUser);
  function updateUser(newUser: User) { user.value = newUser; }
  return { user, updateUser };
});
```

```vue
<!-- UserCard.vue — consumes directly -->
<script setup>
import { useUserStore } from '@/stores/user';
const { user, updateUser } = useUserStore();
</script>
```

## 6. Svelte stores

**When:** Svelte, any drilling depth. Svelte stores are lightweight enough for localised use.

**Before — drilling (Svelte 4):**
```svelte
<!-- Parent.svelte -->
<MiddleLayer {user} />

<!-- MiddleLayer.svelte — doesn't use user -->
<script>
  export let user;
</script>
<DeepChild {user} />
```

**After — writable store:**
```ts
// stores/user.ts
import { writable } from 'svelte/store';
export const user = writable<User>(initialUser);
```

```svelte
<!-- DeepChild.svelte — subscribes directly -->
<script>
  import { user } from '../stores/user';
</script>
<p>{$user.name}</p>
```

**Svelte 5 variant — module-level $state:**
```svelte
<!-- stores/user.svelte.ts -->
<script module>
  export const user = $state<User>(initialUser);
</script>
```

## 7. Python — contextvars

**When:** Python, localised drilling (depth ≤3), request-scoped data (e.g., current user, db session).

**Before — drilling:**
```python
def handle_request(db: Database, user: User):
    result = process_order(db, user)
    return result

def process_order(db: Database, user: User):
    # Does NOT use user — just passes it down
    return save_order(db, user)

def save_order(db: Database, user: User):
    db.save(Order(owner=user.id))
```

**After — contextvars:**
```python
from contextvars import ContextVar

current_user: ContextVar[User] = ContextVar('current_user')

def handle_request(db: Database, user: User):
    current_user.set(user)
    return process_order(db)

def process_order(db: Database):
    return save_order(db)

def save_order(db: Database):
    user = current_user.get()
    db.save(Order(owner=user.id))
```

## 8. Python — FastAPI Depends (dependency injection)

**When:** FastAPI project, systemic drilling of db sessions, auth, config through route → service → repo.

**Before — drilling:**
```python
@router.post("/orders")
def create_order(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.create()

class OrderService:
    def __init__(self, db: Session):
        self.db = db  # only stored to pass to repo

    def create(self):
        repo = OrderRepo(self.db)
        return repo.insert(Order())

class OrderRepo:
    def __init__(self, db: Session):
        self.db = db
```

**After — DI at each layer:**
```python
class OrderRepo:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def insert(self, order: Order):
        self.db.add(order)

class OrderService:
    def __init__(self, repo: OrderRepo = Depends()):
        self.repo = repo

    def create(self):
        return self.repo.insert(Order())

@router.post("/orders")
def create_order(service: OrderService = Depends()):
    return service.create()
```

## 9. Python — Module-level / singleton config

**When:** Config or settings object drilled through many layers, app-wide shared state.

**Before — drilling config:**
```python
def main():
    config = load_config()
    app = App(config)

class App:
    def __init__(self, config: Config):
        self.config = config  # only to pass down
        self.processor = Processor(config)

class Processor:
    def __init__(self, config: Config):
        self.timeout = config.timeout
```

**After — module-level access:**
```python
# config.py
from functools import lru_cache

@lru_cache
def get_config() -> Config:
    return load_config()

# processor.py
from .config import get_config

class Processor:
    def __init__(self):
        self.timeout = get_config().timeout

# app.py
class App:
    def __init__(self):
        self.processor = Processor()
```

## 10. Python — Restructure call chain

**When:** Functions receive params only to forward them. Simplify by letting the caller compose directly.

**Before — drilling:**
```python
def handle(data: dict, formatter: Formatter, output: Output):
    result = transform(data, formatter, output)
    return result

def transform(data: dict, formatter: Formatter, output: Output):
    # Only uses data, passes formatter and output down
    formatted = format_result(data, formatter, output)
    return formatted

def format_result(data: dict, formatter: Formatter, output: Output):
    text = formatter.format(data)
    output.write(text)
```

**After — restructured:**
```python
def handle(data: dict, formatter: Formatter, output: Output):
    transformed = transform(data)
    text = formatter.format(transformed)
    output.write(text)

def transform(data: dict):
    # Pure data transformation, no forwarding
    return processed_data
```

## 11. Component composition (restructure tree)

**When:** Drilling exists because intermediate components render children they don't control. Works in all frameworks.

**Before — drilling:**
```tsx
function Page({ user }: { user: User }) {
  return <Layout user={user} />;
}

function Layout({ user }: { user: User }) {
  return (
    <div className="layout">
      <UserBadge user={user} />
    </div>
  );
}
```

**After — composition via children:**
```tsx
function Page({ user }: { user: User }) {
  return (
    <Layout>
      <UserBadge user={user} />
    </Layout>
  );
}

function Layout({ children }: { children: ReactNode }) {
  return <div className="layout">{children}</div>;
}
```

Layout no longer needs `user` — the parent composes children directly.

## 12. Compound components

**When:** A set of related components share implicit state (tabs, accordions, menus). React pattern.

**Before — drilling config through levels:**
```tsx
<Tabs activeTab={activeTab} onTabChange={setActiveTab}>
  <TabList activeTab={activeTab} onTabChange={setActiveTab}>
    <Tab activeTab={activeTab} onTabChange={setActiveTab} index={0}>One</Tab>
  </TabList>
</Tabs>
```

**After — compound with context:**
```tsx
const TabsContext = createContext<TabsContextValue>(null!);

function Tabs({ children, defaultTab = 0 }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function Tab({ children, index }: { children: ReactNode; index: number }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return (
    <button onClick={() => setActiveTab(index)} data-active={activeTab === index}>
      {children}
    </button>
  );
}

// Usage — no drilling
<Tabs>
  <TabList><Tab index={0}>One</Tab></TabList>
</Tabs>
```

---

# Family B — call chains and object graphs

Fixes 13–19 apply to TypeScript services, Python, C++, Zig, C#, and Kotlin/Java. Try §13 before any of the others.

## 13. Narrow the signature (try this first, every language)

**When:** A layer takes a whole owner object (`Config`, `App`, `Session`) to read one or two fields off it.

This is the only fix that *deletes* a chain rather than rerouting it, and it needs no container, no global, and no new file. It also makes the dependency visible in the signature, which is what the drilling was hiding.

**Before — the owner travels three layers so a leaf can read one field:**
```cpp
class Encoder {
  public:
    explicit Encoder(const Config& cfg) : cfg_(cfg), packer_(cfg) {}
  private:
    const Config& cfg_;      // never read except to build packer_
    Packer packer_;
};

class Packer {
  public:
    explicit Packer(const Config& cfg) : cfg_(cfg) {}
    void run() { resize(cfg_.gutter_px); }   // reads exactly one field
  private:
    const Config& cfg_;
};
```

**After — pass the field:**
```cpp
class Encoder {
  public:
    explicit Encoder(const Config& cfg) : packer_(cfg.gutter_px) {}
  private:
    Packer packer_;          // Encoder no longer stores cfg_ at all
};

class Packer {
  public:
    explicit Packer(uint16_t gutter_px) : gutter_px_(gutter_px) {}
    void run() { resize(gutter_px_); }
  private:
    uint16_t gutter_px_;
};
```

The chain is gone, `Packer` is now unit-testable without a `Config`, and the coupling is honest. Reach for §14–§19 only when 3+ items travel together and narrowing would just produce a long parameter list.

## 14. TypeScript — composition root + closure capture

**When:** TypeScript service/server/CLI code, localised drilling, deps created once at startup.

**Before — drilling `db` through two layers that never touch it:**
```ts
export async function handleRequest(db: Db, req: Request) {
  return route(db, req);
}

async function route(db: Db, req: Request) {
  // does NOT use db
  return loadUser(db, req.userId);
}

async function loadUser(db: Db, id: string) {
  return db.query('select * from users where id = $1', [id]);
}
```

**After — bind deps once at the root, hand down only data:**
```ts
export function createHandler(db: Db) {
  const loadUser = (id: string) => db.query('select * from users where id = $1', [id]);
  const route = (req: Request) => loadUser(req.userId);
  return (req: Request) => route(req);
}

// composition root
const handle = createHandler(db);
```

Intermediate layers take only what they read. `db` is captured, not threaded.

## 15. TypeScript — AsyncLocalStorage (request-scoped ambient)

**When:** Node, systemic drilling of per-request values (request id, current user, trace context) through 4+ layers.

**Before:**
```ts
async function handler(reqId: string, req: Request) { return service(reqId, req.body); }
async function service(reqId: string, body: Body) { return repo(reqId, body); }
async function repo(reqId: string, body: Body) { log.info({ reqId }, 'writing'); }
```

**After:**
```ts
import { AsyncLocalStorage } from 'node:async_hooks';

const requestCtx = new AsyncLocalStorage<{ reqId: string }>();

async function handler(reqId: string, req: Request) {
  return requestCtx.run({ reqId }, () => service(req.body));
}
async function service(body: Body) { return repo(body); }
async function repo(body: Body) {
  log.info({ reqId: requestCtx.getStore()?.reqId }, 'writing');
}
```

Use only for genuinely ambient, request-scoped values. Business data threaded this way becomes invisible coupling — worse than the drilling it replaced.

## 16. C++ — a const Deps struct passed at construction

**When:** C++, systemic drilling (3+ items travelling together through 3+ layers), narrowing (§13) would produce an unreadable parameter list.

**Before — four params re-declared at every level:**
```cpp
class Pipeline {
  public:
    Pipeline(const Config& cfg, Clock& clock, Metrics& metrics, Logger& log)
        : stage_(cfg, clock, metrics, log) {}   // uses none of them itself
  private:
    Stage stage_;
};

class Stage {
  public:
    Stage(const Config& cfg, Clock& clock, Metrics& metrics, Logger& log)
        : worker_(cfg, clock, metrics, log) {}  // also uses none of them
  private:
    Worker worker_;
};
```

**After — one immutable context, bound once:**
```cpp
// deps.h — no ownership, no mutation; every reference outlives the graph.
struct Deps {
    const Config& cfg;
    Clock&        clock;
    Metrics&      metrics;
    Logger&       log;
};

class Pipeline {
  public:
    explicit Pipeline(const Deps& d) : stage_(d) {}
  private:
    Stage stage_;
};

class Stage {
  public:
    explicit Stage(const Deps& d) : worker_(d) {}
  private:
    Worker worker_;
};

class Worker {
  public:
    explicit Worker(const Deps& d) : clock_(d.clock) {}  // takes only what it reads
  private:
    Clock& clock_;
};
```

Rules that keep this from becoming a service locator: `Deps` is **const**, holds **references not owners**, is **constructed once at the composition root**, and each leaf still stores only the members it reads.

## 17. Zig — a Context struct passed by pointer

**When:** Zig, 3+ items threaded through 3+ `init` calls. Note the allocator is NOT one of them — passing an allocator explicitly is idiomatic and must stay.

**Before:**
```zig
pub const Supervisor = struct {
    cfg: Config,
    clock: *Clock,
    metrics: *Metrics,

    pub fn init(gpa: Allocator, cfg: Config, clock: *Clock, metrics: *Metrics) !Supervisor {
        return .{ .cfg = cfg, .clock = clock, .metrics = metrics,
                  .runner = try Runner.init(gpa, cfg, clock, metrics) };
    }
};

pub const Runner = struct {
    pub fn init(gpa: Allocator, cfg: Config, clock: *Clock, metrics: *Metrics) !Runner {
        // reads only cfg.timeout_ms and clock
        return .{ .timeout_ms = cfg.timeout_ms, .clock = clock };
    }
};
```

**After — group the ambient deps, keep the allocator explicit:**
```zig
/// Built once at the composition root; every layer borrows it.
pub const Ctx = struct {
    cfg: Config,
    clock: *Clock,
    metrics: *Metrics,
};

pub const Supervisor = struct {
    pub fn init(gpa: Allocator, ctx: *const Ctx) !Supervisor {
        return .{ .runner = try Runner.init(gpa, ctx) };
    }
};

pub const Runner = struct {
    timeout_ms: u32,
    clock: *Clock,

    pub fn init(gpa: Allocator, ctx: *const Ctx) !Runner {
        _ = gpa;
        return .{ .timeout_ms = ctx.cfg.timeout_ms, .clock = ctx.clock };
    }
};
```

`*const Ctx` (not a copy) keeps it one pointer wide and makes the immutability explicit. If a layer reads exactly one field, prefer §13 and pass that field instead.

## 18. C# — IServiceCollection and IOptions&lt;T&gt;

**When:** C#/.NET, ctor-injected deps threaded through 3+ classes, or a config object drilled to leaves.

**Before:**
```csharp
public sealed class GuardRunner {
    private readonly GuardConfig _config;      // only forwarded
    private readonly IClock _clock;            // only forwarded
    private readonly GuardEngine _engine;

    public GuardRunner(GuardConfig config, IClock clock) {
        _config = config;
        _clock  = clock;
        _engine = new GuardEngine(config, clock);
    }
}

public sealed class GuardEngine {
    public GuardEngine(GuardConfig config, IClock clock) { /* reads config.DebounceMs */ }
}
```

**After — register once, inject where read:**
```csharp
// Program.cs — the composition root
services.Configure<GuardConfig>(config.GetSection("Guard"));
services.AddSingleton<IClock, SystemClock>();
services.AddSingleton<GuardEngine>();
services.AddSingleton<GuardRunner>();

public sealed class GuardRunner {
    private readonly GuardEngine _engine;
    public GuardRunner(GuardEngine engine) => _engine = engine;   // no config, no clock
}

public sealed class GuardEngine {
    private readonly int _debounceMs;
    private readonly IClock _clock;
    public GuardEngine(IOptions<GuardConfig> options, IClock clock) {
        _debounceMs = options.Value.DebounceMs;
        _clock = clock;
    }
}
```

`IOptions<T>` also gives live reload via `IOptionsMonitor<T>` if the config can change at runtime. Never "fix" a drilled `CancellationToken` this way — it must stay threaded.

## 19. Kotlin / Java — Hilt, or a CompositionLocal for Compose

**When:** Android, deps threaded through 3+ classes. Rare in a thin native-shell app; common in a full Kotlin app.

**Before:**
```kotlin
class WakeListener(private val prefs: Prefs, private val net: NetClient) {
    private val poller = Poller(prefs, net)   // uses neither itself
}
class Poller(private val prefs: Prefs, private val net: NetClient) {
    fun poll() = net.get(prefs.endpoint)
}
```

**After — constructor injection resolved by Hilt:**
```kotlin
@Singleton
class Poller @Inject constructor(
    private val prefs: Prefs,
    private val net: NetClient,
) { fun poll() = net.get(prefs.endpoint) }

class WakeListener @Inject constructor(private val poller: Poller)
```

**Compose variant — ambient value instead of a threaded param:**
```kotlin
val LocalPrefs = compositionLocalOf<Prefs> { error("no Prefs provided") }

@Composable fun App(prefs: Prefs) {
    CompositionLocalProvider(LocalPrefs provides prefs) { Screen() }
}

@Composable fun Screen() = Panel()          // no prefs param

@Composable fun Panel() {
    val prefs = LocalPrefs.current
    Text(prefs.endpoint)
}
```

Never hoist an Android `Context` into a singleton to shorten a chain — that leaks the Activity. Use `@ApplicationContext` if a long-lived context is genuinely needed.

## 20. The realtime exception — when NOT to fix

**When:** The chain runs on an audio callback, a render thread, an encode worker, an ISR, or any lock-free hot path.

Threading is often the *design* there: it keeps the data flow lock-free, makes lifetimes visible, and avoids a shared-state dependency the thread cannot safely take. A "fix" that introduces a mutable singleton, a lock, or an allocation on that path trades a readability nit for a glitch.

```cpp
// This is NOT a defect. The recv thread owns its params by design.
void AudioPlayer::recv_loop(const AudioConfig& cfg, PcmRing& ring, Metrics& m) {
    decode_into(cfg, ring, m);   // forwarded, not read here
}
```

Acceptable fixes on a realtime path, in order of preference:
1. Narrow the signature (§13) — free, no runtime cost
2. A `const` context struct bound at setup, before the thread starts (§16/§17)
3. Nothing — record it as accepted and move on

Unacceptable: mutable globals, lazily-initialised singletons, locks, `AsyncLocalStorage`-style ambient lookup, anything that allocates. Say so explicitly in the report.
