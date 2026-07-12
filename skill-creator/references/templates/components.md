# Reusable Components Library

Copy-paste snippets for consistent formatting across skills.

---

## Phase Headers

### Style 1: Bracket Notation (Recommended for most skills)

```markdown
[PHASE_NAME] Brief description of what's happening...
```

**Examples:**
```markdown
[SCAN] Searching for configuration files...
[ANALYZE] Evaluating dependencies...
[EXECUTE] Applying changes...
[VERIFY] Running tests...
```

---

### Style 2: Markdown Heading

```markdown
### Phase 1 — Name
Brief description of this phase...
```

**Examples:**
```markdown
### Phase 1 — Discovery
Scanning project structure and detecting configuration...

### Phase 2 — Analysis
Evaluating code quality and identifying improvements...
```

---

### Style 3: Step Notation

```markdown
Step N: Name
  Details about this step...
```

**Examples:**
```markdown
Step 1: Initialize
  Setting up environment and loading configuration...

Step 2: Process
  Analyzing 47 files for issues...
```

---

## Status Indicators

### Basic Symbols

```markdown
✓  Success / completed action
→  In progress / transitioning
⚠  Warning / attention needed
✗  Error / failed action
```

---

### Usage Patterns

**During scanning:**
```markdown
[SCAN] Searching for files...
  → Checking src/ directory
  → Checking test/ directory
  ✓ Found 47 files
```

**With results:**
```markdown
[ANALYZE] Checking code quality...
  ✓ 45 files passed
  ⚠ 2 files have warnings
  ✗ 1 file has errors
```

**Progressive states:**
```markdown
[PROCESS] Running operations...
  ✓ Step 1 complete
  → Step 2 in progress (45% done)
  - Step 3 pending
  - Step 4 pending
```

---

## Progress Tracking

### Simple Counter

```markdown
[PHASE] Processing files... (12/47 complete)
```

---

### Percentage

```markdown
[MIGRATE] 67% complete (20/30 items)
```

---

### Multi-worker

```markdown
[ANALYZE] Processing in parallel...
  Worker A: 23 files processed
  Worker B: 19 files processed
  Worker C: 5 files processed
```

---

### Time Estimate

```markdown
[DEPLOY] Deploying services...
  Progress: 45% (estimated 2 minutes remaining)
```

---

### Detailed Progress Bar (ASCII)

```markdown
[PROCESS] Progress: [===========·········] 55% (11/20)
```

---

## ASCII Boxes

### Light Border (Informational)

```markdown
┌─────────────────────────────────────┐
│ Content here                        │
└─────────────────────────────────────┘
```

**Use for:** General information, grouping related content

---

### Medium Border (Important)

```markdown
╔═════════════════════════════════════╗
║ Content here                        ║
╚═════════════════════════════════════╝
```

**Use for:** Important information, summaries

---

### Heavy Border (Critical)

```markdown
╔═══════════════════════════════════════╗
║                                       ║
║  ⚠️  CRITICAL DECISION POINT           ║
║                                       ║
╠═══════════════════════════════════════╣
║  This action will affect production  ║
║  and cannot be undone automatically. ║
║                                       ║
╚═══════════════════════════════════════╝
```

**Use for:** Warnings, destructive actions, critical approvals

---

### Nested Boxes

```markdown
╔═══════════════════════════════════════╗
║  Outer Context                        ║
╠═══════════════════════════════════════╣
║  ┌─────────────────────────────────┐ ║
║  │ Inner Detail                    │ ║
║  └─────────────────────────────────┘ ║
╚═══════════════════════════════════════╝
```

---

## Approval Gates

### Standard Approval

```markdown
⚡ Action required: [Brief description of what will happen]

Do you want to proceed?
```

---

### Approval with Summary

```markdown
╔═══════════════════════════════════════╗
║  Ready to [action]                    ║
╠═══════════════════════════════════════╣
║  Files to modify: 5                   ║
║  Files to create: 2                   ║
║  Files to delete: 1                   ║
╚═══════════════════════════════════════╝

Do you want to proceed?
```

---

### Critical Approval

```markdown
⚠️  WARNING: Destructive Operation

This will permanently:
  - Delete 3 database tables
  - Remove 127 files (2.3 MB)
  - Clear all caches

Type "CONFIRM DELETE" to proceed, or anything else to cancel.
```

---

### Approval with Options

```markdown
╔═══════════════════════════════════════╗
║  Multiple options available           ║
╚═══════════════════════════════════════╝

Choose an action:
  1. Apply changes and commit
  2. Apply changes only (no commit)
  3. Preview changes (dry run)
  4. Cancel

Enter option number (1-4):
```

---

## Tables

### Simple Reference

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value A  | Value B  | Value C  |
```

---

### With Alignment

```markdown
| Left-aligned | Centered | Right-aligned |
|:-------------|:--------:|--------------:|
| Text         | Text     | 123           |
| Text         | Text     | 456           |
```

---

### Status Table

```markdown
| File            | Status | Changes |
|-----------------|--------|---------|
| auth.ts         | ✓ OK   | 3       |
| database.ts     | ⚠ WARN | 12      |
| config.ts       | ✗ FAIL | -       |
```

---

### Comparison Table

```markdown
| Feature | Before | After |
|---------|--------|-------|
| Lines of code | 450 | 320 |
| Functions | 23 | 18 |
| Complexity | High | Medium |
```

---

### Command Reference Table

```markdown
| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize | `tool init --type=web` |
| `build` | Build project | `tool build --prod` |
| `test` | Run tests | `tool test --watch` |
```

---

## Lists and Hierarchies

### Simple List

```markdown
Items found:
  - Item 1
  - Item 2
  - Item 3
```

---

### Nested List

```markdown
Project structure:
  - src/
    - components/
    - utils/
  - test/
    - unit/
    - integration/
```

---

### Ordered List

```markdown
Steps to follow:
  1. Initialize environment
  2. Install dependencies
  3. Run build script
  4. Deploy to server
```

---

### Definition List

```markdown
**Term 1**
  Definition or explanation of term 1

**Term 2**
  Definition or explanation of term 2
```

---

## Code Blocks

### Basic Code Block

````markdown
```typescript
function example() {
  return "hello";
}
```
````

---

### With Language Highlighting

````markdown
```python
def process_data(items):
    return [item.upper() for item in items]
```
````

---

### Command Output

````markdown
```bash
$ npm install
added 347 packages in 12s
```
````

---

### Inline Code

```markdown
Use the `git status` command to check your working tree.
```

---

## Error Messages

### Simple Error

```markdown
✗ Error: Operation failed

Reason: File not found: config.json
```

---

### Error with Context

```markdown
✗ Build failed

Error: TypeScript compilation error in auth.ts:42

  Line 42: Cannot find name 'user'

  Did you mean 'User' (capitalized)?
```

---

### Error with Recovery Steps

```markdown
✗ Deployment failed: Connection timeout

What went wrong:
  Server did not respond within 30 seconds

Recovery steps:
  1. Check server status: curl https://api.example.com/health
  2. Verify credentials: echo $API_KEY
  3. Check network: ping api.example.com
  4. Retry deployment: run /deploy again

Need help? See docs/troubleshooting.md
```

---

## Warnings

### Simple Warning

```markdown
⚠ Warning: API rate limit approaching (80/100 requests)
```

---

### Warning with Recommendation

```markdown
⚠ Warning: Large file detected

File: data.json (15 MB)

Recommendation:
  Consider excluding large files from commits
  Add to .gitignore: echo "data.json" >> .gitignore
```

---

### Warning List

```markdown
⚠ Found 3 warnings:

  1. Deprecated function in auth.ts:23
     → Replace with: newAuthFunction()

  2. Unused variable in utils.ts:67
     → Remove or add underscore: _unusedVar

  3. Missing return type in api.ts:103
     → Add explicit return type
```

---

## Success Messages

### Simple Success

```markdown
✅ Done: Changes applied successfully
```

---

### Success with Summary

```markdown
✅ Deployment complete

Summary:
  - 5 files updated
  - 2 files created
  - 0 errors
  - Completed in 3.2 seconds
```

---

### Success with Next Steps

```markdown
✅ Setup complete

Next steps:
  1. Run `npm start` to start the development server
  2. Visit http://localhost:3000 in your browser
  3. Edit src/index.ts to start coding

Documentation: docs/getting-started.md
```

---

## Decision Trees (ASCII)

### Simple Tree

```markdown
Decision flow:
├─ Condition A?
│  ├─ YES → Action 1
│  └─ NO → Action 2
└─ Fallback → Action 3
```

---

### Complex Tree

```markdown
Project setup:
├─ Existing project?
│  ├─ YES → Detect configuration
│  │       ├─ Found package.json → Node.js project
│  │       ├─ Found Cargo.toml → Rust project
│  │       └─ None found → Ask user
│  └─ NO → Initialize new project
│          ├─ Choose template:
│          │   ├─ Web application
│          │   ├─ CLI tool
│          │   └─ Library
│          └─ Create structure
```

---

## Separators

### Section Separator

```markdown
---
```

---

### Visual Break

```markdown
═══════════════════════════════════════
```

---

### Light Separator

```markdown
───────────────────────────────────────
```

---

## Emojis (Use Sparingly)

```markdown
✅ Success
✗ Error
⚠️ Warning
⚡ Action required
🚀 Deployment
🔍 Scanning
🛠️ Building
📝 Writing
🧪 Testing
🐛 Debugging
💾 Saving
🔄 Syncing
```

**Note:** Use emojis consistently within a skill, and avoid overuse.

---

## Badges/Labels

### Status Badges

```markdown
[STABLE]
[BETA]
[DEPRECATED]
[EXPERIMENTAL]
```

---

### Priority Labels

```markdown
[HIGH PRIORITY]
[MEDIUM PRIORITY]
[LOW PRIORITY]
```

---

### Type Labels

```markdown
[BREAKING CHANGE]
[NEW FEATURE]
[BUG FIX]
[IMPROVEMENT]
```

---

## Timestamps

### Simple Timestamp

```markdown
[2025-02-05 14:30:22] Operation started
```

---

### Relative Time

```markdown
Started 3 minutes ago...
Estimated completion: 2 minutes remaining
```

---

### Duration

```markdown
Total time: 3m 42s
```

---

## Usage Tips

### 1. Pick Components That Match Your Skill

Not every skill needs every component. Choose what fits:
- Simple skill? Use basic status indicators
- Complex skill? Add phases and approval gates
- Reference skill? Focus on tables and lists

### 2. Stay Consistent Within a Skill

Once you pick a style (e.g., `[PHASE]` vs `### Phase`), use it throughout.

### 3. Don't Over-format

Clarity > visual complexity. If ASCII boxes make output harder to read, skip them.

### 4. Test Readability

After adding components:
- Can you skim and understand state?
- Are errors obvious?
- Is important information highlighted?

### 5. Adapt, Don't Copy Blindly

These are starting points. Adjust wording, structure, and style to match your skill's personality.

---

## See Also

- [OUTPUT_FRAMEWORK.md](../OUTPUT_FRAMEWORK.md) - Full framework documentation
- [simple-workflow.md](./simple-workflow.md) - Template for simple skills
- [multi-phase.md](./multi-phase.md) - Template for complex skills
- [reference.md](./reference.md) - Template for documentation skills
