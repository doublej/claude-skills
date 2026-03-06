# Rename Strategies Reference

Safe rename execution patterns, pitfalls, and rollback strategies.

## Execution Order

Always rename from leaves to roots — inner/private symbols first, public API last.

### Symbol Rename Order

1. **Local variables** — confined to a single function, zero external impact
2. **Private functions/methods** — internal to a module, low risk
3. **Internal (module-level)** — used within the module but not exported
4. **Exported symbols** — public API, highest risk
5. **File renames** — affects import paths everywhere

### Per-Symbol Rename Steps

For each symbol rename:
1. Read the file containing the definition
2. Use Grep to find all references across the codebase
3. Rename the definition
4. Rename all references (same file first, then other files)
5. Verify no broken references remain

## Safe Rename Patterns

### Functions / Methods

```
# Definition
old: def getData(self):
new: def get_data(self):

# All call sites
old: obj.getData()
new: obj.get_data()

# References in strings/decorators — manual review needed
old: @route("/data", methods=["GET"], endpoint="getData")
new: @route("/data", methods=["GET"], endpoint="get_data")  # CHECK: is this a public API?
```

### Classes / Types

```
# Definition
old: class dataProcessor:
new: class DataProcessor:

# Constructor calls
old: proc = dataProcessor()
new: proc = DataProcessor()

# Type annotations
old: def handle(proc: dataProcessor) -> None:
new: def handle(proc: DataProcessor) -> None:

# Inheritance
old: class SubProc(dataProcessor):
new: class SubProc(DataProcessor):
```

### Constants

```
# Definition
old: maxRetries = 3
new: MAX_RETRIES = 3

# All usages
old: for i in range(maxRetries):
new: for i in range(MAX_RETRIES):
```

### File Renames

```
# 1. Update all imports FIRST
old: from utils.getData import fetch
new: from utils.get_data import fetch

# 2. Then rename the file
mv utils/getData.py utils/get_data.py

# 3. Verify no broken imports
grep -r "getData" --include="*.py"
```

## Pitfalls

### String Literals

Symbol names in strings are NOT caught by simple search-replace:

```python
# These need manual review:
getattr(obj, "getData")           # dynamic attribute access
config["getData"]                  # dict key
endpoint="/getData"                # API endpoint
logging.info("getData called")    # log messages (usually OK to leave)
```

**Strategy:** After rename, grep for the old name in string literals. Flag for manual review.

### Dynamic Access / Reflection

```python
# Python
getattr(obj, name)          # name could be the old symbol
setattr(obj, name, value)
obj.__dict__[name]
vars(obj)[name]

# JavaScript/TypeScript
obj[key]                    # computed property access
eval("obj.oldName")         # eval — rare but dangerous
Reflect.get(obj, name)

# Go
reflect.ValueOf(obj).MethodByName("OldName")
```

**Strategy:** Grep for `getattr`, `setattr`, `__dict__`, bracket notation near old names. Flag for manual review.

### Decorators / Metadata

```python
# Python decorators may register names
@app.route("/api", endpoint="old_name")
@pytest.fixture(name="old_name")
@dataclass(frozen=True)  # field names matter

# TypeScript decorators
@Column({ name: "old_name" })
@ApiProperty({ description: "..." })
```

### Serialization / Database Fields

```python
# These names are part of the data contract — DO NOT rename:
class User(BaseModel):
    firstName: str    # JSON field name — renaming breaks API
    last_name: str    # Also a JSON field

# Unless using field aliases:
class User(BaseModel):
    first_name: str = Field(alias="firstName")  # safe — alias preserves API
```

**Strategy:** Flag serialized model fields. Only rename if aliases are in place.

### Re-exports / Index Files

```typescript
// index.ts re-exports — must update both sides
export { getData } from "./utils";  // old
export { get_data } from "./utils"; // new — but consumers still use getData!

// Barrel exports need careful coordination
```

### Test Assertions

```python
# Tests may assert on names
assert func.__name__ == "getData"     # breaks after rename
mock.assert_called_with("getData")    # breaks after rename
```

**Strategy:** Include test files in the rename scope. Grep for old name in assertions.

## Batch Ordering

When renaming multiple symbols in one batch:

1. **Group by file** — minimize file I/O
2. **Sort by line number descending** within each file — later renames don't shift earlier line numbers
3. **Rename definitions before references** — ensures Grep finds the old name at reference sites
4. Wait — actually: **rename references first, then definitions** — this way you can still search for the old definition name

Corrected order:
1. Group by file
2. For each file: rename references to the old name first
3. Then rename the definition
4. Cross-file references: rename in importing files, then in the defining file

## File Rename Strategy

1. Grep all files for imports of the old filename
2. Update import paths in all consuming files
3. `git mv old_file new_file` (preserves git history)
4. Verify: grep for old filename in all files

## Quality Gates Per Batch

After each batch of renames:

1. **Typecheck** — catches broken references in typed languages
   - Python: `mypy` or `pyright`
   - TypeScript: `tsc --noEmit`
   - Go: `go vet`
   - Rust: `cargo check`

2. **Test** — catches runtime reference failures
   - Run the project's test suite
   - Focus on tests touching renamed files

3. **Lint** — catches style violations
   - Ensures new names pass linting rules

**Fix cycle:** If checks fail, fix up to 3 times. If still failing, revert the batch:
```bash
git checkout HEAD -- .
git clean -fd
```

## Rollback Strategy

Each batch gets its own commit. To undo a batch:

```bash
# Revert the last batch commit
git revert HEAD --no-edit

# Or reset to before the batch (destructive)
git reset --hard HEAD~1
```

Branch strategy ensures the main branch is never affected:
```bash
git checkout -b taxonomy/YYYYMMDD-HHMMSS
# All renames happen on this branch
# User reviews and merges when satisfied
```

## Priority Classification

| Priority | Category | Risk | Example |
|----------|----------|------|---------|
| P1 | Public API symbols | High | Exported functions, class names in libraries |
| P2 | Internal exported | Medium | Module-level functions used across files |
| P3 | Private methods | Low | Methods prefixed with `_` |
| P4 | Local variables | Minimal | Function-scoped variables |
| P5 | File names | Medium | Affects import paths |

Default execution order: P4 → P3 → P2 → P1 → P5 (safest first).

## Verb Consolidation Renames

When the quality analysis detects inconsistent verb usage (e.g. mixed `get`/`fetch` for the same action), batch-rename the minority verb to the dominant one.

### Safety Checks

1. **Verify the verb difference is intentional or accidental:**
   - `get` (sync) vs `fetch` (async) may be a deliberate convention — do not rename
   - `find` (search/filter) vs `get` (by ID) may have different semantics
   - Ask for confirmation when the minority verb appears >5 times

2. **Rename all instances of the minority verb in one batch:**
   - Grep for `\bfetch_` or `\bfetch[A-Z]` to find all functions using that verb
   - Replace verb prefix only — keep the noun unchanged (`fetch_user` → `get_user`)
   - Include references (call sites, imports, tests)

3. **Check for name collisions:**
   - Before renaming `fetch_user` → `get_user`, verify `get_user` doesn't already exist
   - If collision detected, skip that rename and flag for manual review

### Execution Pattern

```
# 1. Collect all functions using the minority verb
grep -rn "\bfetch_\|fetch[A-Z]" --include="*.py" .

# 2. For each, verify the dominant-verb name doesn't exist
grep -rn "\bget_user\b" --include="*.py" .

# 3. Rename (same per-symbol steps as standard renames)
# Definition first, then references

# 4. Quality gate after the full verb batch
```

### When NOT to Consolidate

- The verb difference reflects a real semantic difference (sync/async, single/batch)
- The minority verb is used in an external/public API
- The codebase has documented conventions explaining the distinction
