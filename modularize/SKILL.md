---
name: modularize
description: Intelligently split oversized files into focused, single-responsibility modules. Use when files exceed ~150 lines, have mixed responsibilities, or need structural cleanup.
---

# Modularize

Split oversized files into focused modules by analyzing responsibility boundaries, dependency graphs, and consumer imports.

## Scripts

All scripts are in `~/.claude/skills/modularize/scripts/`.

### Scan

```bash
python3 ~/.claude/skills/modularize/scripts/scan_files.py /path/to/file_or_dir              # human summary
python3 ~/.claude/skills/modularize/scripts/scan_files.py /path/to/file_or_dir --json        # structured JSON
python3 ~/.claude/skills/modularize/scripts/scan_files.py /path/to/dir --threshold 200       # custom threshold
```

Detects: files over threshold, function/class boundaries, symbol lengths, imports, and consumer relationships.

## Workflow

### Phase 1 — Scan

Run the scan script to find candidates:

```bash
python3 ~/.claude/skills/modularize/scripts/scan_files.py <target-path> --json
```

Parse the JSON output. If scanning a single file, pass the file path directly. If scanning a directory, all files over threshold are returned. Default threshold: 150 lines.

### Phase 2 — Analyze

For each candidate file, read the full file content and determine:

**Responsibility clusters** — group symbols by:
- Shared naming prefixes (e.g., `validate_email`, `validate_phone` → validation group)
- Shared parameter types or return types
- Shared callers (functions called from the same consumers)
- Logical domain (parsing, formatting, IO, business logic)

**Dependency classification:**
- **Leaf symbols**: not imported by other symbols in the same file → easy to extract
- **Hub symbols**: imported by many symbols in the file → should stay in place
- **Circular clusters**: symbols that reference each other → must move together
- **Shared types/constants**: used across multiple clusters → extract first into a types/constants module

**Split inhibitors** — do NOT split when:
- File has a single coherent responsibility (long but focused)
- Most symbols are tightly coupled (splitting would create circular imports)
- File is generated or auto-maintained
- Resulting modules would have <2 exported symbols each
- File is a test file (split tests with their source, not separately)

### Phase 3 — Plan

Present the split proposal to the user using `consult-user-mcp`. Format:

```
FILE: src/utils.ts (287 lines, 14 functions)

PROPOSED SPLITS:
1. src/validation.ts — 5 functions (~60 lines)
   - validateEmail, validatePhone, validateUrl, isRequired, sanitizeInput
2. src/formatting.ts — 4 functions (~55 lines)
   - formatDate, formatCurrency, formatPhone, truncateText
3. src/utils.ts — 5 functions (~80 lines) [STAYS]
   - debounce, throttle, deepMerge, uniqueId, sleep

SHARED TYPES: None needed (no cross-cluster type dependencies)

IMPORT UPDATES: 3 files need updated imports
  - src/components/Form.tsx (validateEmail, isRequired → from validation)
  - src/pages/Profile.tsx (formatDate, formatPhone → from formatting)
  - src/api/client.ts (sanitizeInput → from validation)
```

Wait for user confirmation. Adjust if requested.

**Naming rules for new modules:**
- Name by responsibility, never by structure (`validation.ts`, not `utils2.ts`)
- Never use: `helpers`, `misc`, `common`, `shared`, `extra`
- Match existing project naming conventions (kebab-case, snake_case, etc.)

### Phase 4 — Execute

Execute splits in this order:

**Step 1: Extract shared types/constants** (if any cross-cluster dependencies exist)
- Create the types/constants module first
- Move shared types, interfaces, constants, enums
- Update imports in the original file

**Step 2: Create new modules**

For each new module, handle language-specific patterns:

| Language | Export pattern | Import pattern |
|----------|---------------|----------------|
| TypeScript/JS | `export function`, `export const` | `import { x } from './module'` |
| Python | Top-level definitions (auto-exported) | `from .module import x` or `from module import x` |
| Go | Capitalized names (auto-exported) | Same package, no import needed; or `import "pkg/module"` |
| Rust | `pub fn`, `pub struct` | `use crate::module::x` or `mod module` |
| Swift | `public`/`internal` access | `import Module` or same-module access |

**Step 3: Update the original file**
- Remove extracted symbols
- Add imports from new modules where the original file still uses them
- Do NOT add backward-compat re-exports (consumers get updated instead)

**Step 4: Update all consumer imports**
- Find every file that imports from the original module
- Update import paths to point to the new module locations
- For Python packages: update `__init__.py` if using explicit re-exports

**Circular dependency resolution:**
If extraction would create a circular import:
1. Identify the shared dependency causing the cycle
2. Extract it into a separate module first
3. Have both modules import from the shared module

### Phase 5 — Verify

Run the project's existing checks to confirm nothing broke:

1. **Type checker** (tsc, mypy, pyright) — catches import errors
2. **Tests** (pytest, vitest, go test) — catches behavioral regressions
3. **Build** (if applicable) — catches module resolution issues

If checks fail, fix import issues (most common cause) and re-run. Up to 3 fix cycles, then reassess the split strategy.

## Decision Framework

**When to use this skill:**
- File exceeds 150 lines with multiple responsibilities
- Functions from different domains live in the same file
- User asks to "break up", "split", "modularize", or "reorganize" a file
- During refactoring when a file has grown organically

**When NOT to use:**
- File is large but has a single responsibility (e.g., a parser, a migration)
- File is auto-generated
- User wants to restructure the entire project architecture (that's a broader refactor)
- File is under 100 lines even if it has mixed concerns (not worth the churn)
