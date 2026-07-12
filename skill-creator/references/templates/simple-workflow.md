# Simple Workflow Template

Use this template for straightforward skills with linear progression: scan → analyze → execute.

---

## Template Structure

```markdown
---
name: your-skill-name
description: Brief description of what your skill does and when to use it
---

# Your Skill Name

[Brief explanation of what this skill does]

## Usage

When user requests [specific action], this skill will:
1. Scan [what to scan]
2. Analyze [what to analyze]
3. Execute [what to execute]

---

[SCAN] Searching for [target]...
  → Checking [location 1]
  → Checking [location 2]
  ✓ Found N [items]

[ANALYZE] Evaluating [criteria]...
  → Assessing [item 1]
  → Assessing [item 2]
  ✓ Analysis complete: [summary]

[EXECUTE] Applying [changes]...
  ✓ Updated [item 1]
  ✓ Updated [item 2]
  ✓ [Action] complete

✅ Done: [Final summary]
```

---

## Key Elements

### 1. Phase Headers
Use `[PHASE]` format for consistency:
- `[SCAN]` - Finding/discovering things
- `[ANALYZE]` - Evaluating/processing
- `[EXECUTE]` - Taking action

### 2. Status Indicators
- `→` In progress / currently working
- `✓` Success / completed
- `⚠` Warning / needs attention
- `✗` Error / failed

### 3. Progressive Disclosure
Show information as it becomes relevant:
1. Start with what you're doing
2. Show progress during work
3. Summarize results at end

### 4. Final Summary
Always end with clear outcome:
- `✅ Done: [what was accomplished]`
- List key changes or results
- Point to next steps if applicable

---

## Example: Code Formatter Skill

```markdown
---
name: code-formatter
description: Format code files using project's style configuration
---

# Code Formatter

Formats code files according to project configuration (Prettier, Black, rustfmt, etc.)

## Usage

When user requests code formatting, this skill will:
1. Scan for project configuration
2. Identify files to format
3. Apply formatting

---

[SCAN] Detecting configuration...
  → Checking for .prettierrc
  → Checking for pyproject.toml
  ✓ Found Prettier config

[SCAN] Finding files to format...
  → Searching src/ directory
  → Searching test/ directory
  ✓ Found 23 files

[EXECUTE] Formatting files...
  ✓ Formatted src/index.ts
  ✓ Formatted src/utils.ts
  ✓ Formatted test/main.test.ts
  ...
  ✓ Formatted 23 files

✅ Done: All files formatted according to .prettierrc
```

---

## Customization Tips

### Add Approval Gate (Optional)
If your skill makes changes, add confirmation:

```markdown
[READY] About to format 23 files using Prettier

Do you want to proceed?
```

Wait for user confirmation before `[EXECUTE]` phase.

### Add Error Handling
Show clear errors with recovery steps:

```markdown
✗ Formatting failed: src/broken.ts

  Reason: Syntax error at line 42

  Fix: Correct the code and try again

  Files formatted so far: 12/23
```

### Add Progress for Long Operations
For operations >5 seconds, show progress:

```markdown
[EXECUTE] Formatting files... (12/23 complete)
```

---

## When to Use This Template

**Good fit:**
- File processing tools
- Code transformation skills
- Cleanup/maintenance utilities
- Simple refactoring tasks

**Not a good fit:**
- Complex multi-decision workflows → use `multi-phase.md`
- Documentation lookups → use `reference.md`
- Highly conditional logic → consider decision tree pattern

---

## See Also

- [OUTPUT_FRAMEWORK.md](../OUTPUT_FRAMEWORK.md) - Full framework documentation
- [multi-phase.md](./multi-phase.md) - Template for complex workflows
- [components.md](./components.md) - Reusable formatting snippets
