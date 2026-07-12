# Simplification Patterns

Language-specific patterns for code simplification. Apply only when they improve clarity.

## Universal Patterns

### Guard clauses (replace nested if-else)
```
# Before
def process(x):
    if x is not None:
        if x > 0:
            return x * 2
    return 0

# After
def process(x):
    if x is None or x <= 0:
        return 0
    return x * 2
```

### Extract repeated expressions
```
# Before
if items[idx].value > 0 and items[idx].active:
    total += items[idx].value

# After
item = items[idx]
if item.value > 0 and item.active:
    total += item.value
```

### Consolidate duplicate branches
```
# Before
if mode == "a":
    save(data)
    notify()
elif mode == "b":
    save(data)
    notify()

# After
if mode in ("a", "b"):
    save(data)
    notify()
```

### Remove dead code
- Unreachable code after return/raise/break
- Unused variables and imports
- Commented-out code blocks (not explanatory comments)

### Flatten unnecessary wrappers
```
# Before
def get_name(user):
    return user.name

name = get_name(user)

# After
name = user.name
```

## Python

### Comprehensions (when clearer than loop)
```
# Before
result = []
for item in items:
    if item.active:
        result.append(item.name)

# After
result = [item.name for item in items if item.active]
```

### Walrus operator (Python 3.8+, use sparingly)
```
# Before
match = pattern.search(text)
if match:
    process(match)

# After
if match := pattern.search(text):
    process(match)
```

### `any()`/`all()` instead of flag loops
```
# Before
found = False
for item in items:
    if item.valid:
        found = True
        break

# After
found = any(item.valid for item in items)
```

### f-strings over format/concatenation
```
# Before
msg = "Hello " + name + ", you have " + str(count) + " items"

# After
msg = f"Hello {name}, you have {count} items"
```

## TypeScript / JavaScript

### Optional chaining
```
// Before
const name = user && user.profile && user.profile.name;

// After
const name = user?.profile?.name;
```

### Nullish coalescing
```
// Before
const value = x !== null && x !== undefined ? x : defaultValue;

// After
const value = x ?? defaultValue;
```

### Destructuring
```
// Before
const name = props.name;
const age = props.age;

// After
const { name, age } = props;
```

### Template literals over concatenation
```
// Before
const url = baseUrl + "/api/" + version + "/users";

// After
const url = `${baseUrl}/api/${version}/users`;
```

### `Object.entries`/`Object.fromEntries` for object transforms
```
// Before
const result = {};
for (const key of Object.keys(obj)) {
    result[key] = obj[key] * 2;
}

// After
const result = Object.fromEntries(
    Object.entries(obj).map(([k, v]) => [k, v * 2])
);
```

## Go

### Named return for early returns with cleanup
```
// Before — deeply nested with defers
func process(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()
    data, err := io.ReadAll(f)
    if err != nil {
        return nil, err
    }
    return data, nil
}
```

### Table-driven tests over repeated test functions
### `errors.Is`/`errors.As` over string comparison
### `slices` package (Go 1.21+) over manual loops

## Rust

### `?` operator over match/unwrap chains
```
// Before
let file = match File::open(path) {
    Ok(f) => f,
    Err(e) => return Err(e),
};

// After
let file = File::open(path)?;
```

### `if let` / `let-else` over full match for single variants
### Iterator chains over manual loops (when clearer)
### Derive macros over manual trait implementations

## Swift

### Guard-let over nested if-let
```
// Before
func process(_ value: String?) {
    if let value = value {
        if value.count > 0 {
            doWork(value)
        }
    }
}

// After
func process(_ value: String?) {
    guard let value, !value.isEmpty else { return }
    doWork(value)
}
```

### Trailing closure syntax
### `map`/`compactMap`/`filter` over manual loops (when clearer)
### Property wrappers over repeated boilerplate

## Anti-patterns (DO NOT apply)

- Collapsing readable multi-line expressions into one-liners
- Replacing clear if-else with obscure ternary chains
- Abstracting code used in only one place
- Removing error handling for brevity
- Changing public APIs or function signatures
- Micro-optimising at the cost of readability
