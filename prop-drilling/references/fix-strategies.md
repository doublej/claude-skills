# Fix Strategies — Before/After Patterns

Reference file for the prop-drilling skill. Each strategy shows the drilling problem and its fix.

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
