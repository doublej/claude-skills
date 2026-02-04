# Skill Output Framework

## Purpose

This framework provides consistent formatting patterns for claude-skills output, helping maintain clarity and scannability across 60+ skills while preserving flexibility for skill-specific needs.

**Goals:**
- Standardize common output elements (phase headers, status indicators, progress tracking)
- Provide reusable templates for different skill types
- Enable users to quickly understand skill progress and state
- Maintain coherence without sacrificing personality

**Non-goals:**
- Mandate rigid output formats that reduce skill uniqueness
- Replace LLM-generated content with purely deterministic templates
- Force retrofitting of all existing skills

---

## Output Patterns

The framework identifies 7 distinct output patterns observed across existing skills. Choose the pattern that matches your skill's complexity and workflow.

### 1. Structured Multi-Phase ⭐ (Most Common)

**When to use:** Complex workflows with clear progression (scan → analyze → execute)

**Characteristics:**
- Explicit phase boundaries
- Progressive disclosure (show what's happening at each stage)
- Status updates within phases
- User approval gates at critical decision points

**Example:**
```
[SCAN] Searching for deprecated patterns...
  ✓ Found 12 files with old API usage
  ✓ Identified 3 migration candidates
  → Moving to analysis phase

[ANALYZE] Evaluating impact...
  → Checking dependencies for file1.ts
  → Checking dependencies for file2.ts
  ✓ Analysis complete: 2 files safe to migrate

[EXECUTE] Applying migrations...
  ✓ Updated file1.ts (3 changes)
  ✓ Updated file2.ts (1 change)
  ✓ Migration complete
```

**Best for:** Refactoring tools, analysis skills, deployment workflows

---

### 2. Simple/Minimal

**When to use:** Straightforward single-action skills

**Characteristics:**
- Command-first approach
- No elaborate phase structure
- Direct output with minimal formatting
- Gets to the point immediately

**Example:**
```
Running linter...

✓ No issues found in 47 files
```

**Best for:** Utility skills, quick checks, simple commands

---

### 3. Manifesto + Rules-Heavy

**When to use:** Skills with strong philosophical approach or complex constraints

**Characteristics:**
- Opens with guiding principles
- Lists rules/constraints before action
- Establishes context and expectations
- Action follows philosophy

**Example:**
```
# Code Simplification Philosophy

Principles:
- Preserve all functionality
- Reduce cognitive load
- Follow existing patterns
- No premature abstraction

Rules:
1. Never remove working code without equivalent replacement
2. Maintain test coverage
3. Keep changes atomic

[SIMPLIFY] Analyzing complexity...
```

**Best for:** Opinionated tools, code quality skills, architectural guides

---

### 4. Decision Tree/Flowchart

**When to use:** Skills with conditional branching logic

**Characteristics:**
- ASCII flowchart or decision tree
- Shows logic paths visually
- Highlights current path
- Makes branching explicit

**Example:**
```
Decision Flow:
├─ File exists?
│  ├─ YES → Check if writable
│  │       └─ Writable → Proceed with edit
│  └─ NO → Create new file
│          └─ Ask for template choice
│              ├─ TypeScript
│              ├─ Python
│              └─ Rust
```

**Best for:** Conditional workflows, project setup, environment detection

---

### 5. Reference Table

**When to use:** Documentation lookups, cross-reference tools

**Characteristics:**
- Structured data presentation
- Markdown tables
- Clear column headers
- Scannable format

**Example:**
```
## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize project | `skill init --type=web` |
| `build` | Compile project | `skill build --prod` |
| `test` | Run test suite | `skill test --watch` |
```

**Best for:** API reference skills, command lookups, configuration guides

---

### 6. Checklist + Decision Point

**When to use:** Multi-step tasks requiring user validation

**Characteristics:**
- Explicit checkbox-style progress
- Clear approval gates
- No automatic progression
- User maintains control

**Example:**
```
Pre-deployment Checklist:

✓ Tests passing
✓ Dependencies updated
✓ Environment variables set
⚠ Backup created (manual verification needed)

⚡ Ready to deploy to production.
   This action cannot be undone.

Do you want to proceed?
```

**Best for:** Deployment tools, destructive operations, critical workflows

---

### 7. Hierarchical Box/Border

**When to use:** Skills needing strong visual hierarchy or emphasis

**Characteristics:**
- ASCII art boxes/borders
- Visual weight for importance
- Nested structure
- Eye-catching output

**Example:**
```
╔═══════════════════════════════════════╗
║  🚀 DEPLOYMENT READY                  ║
╠═══════════════════════════════════════╣
║  Environment: production              ║
║  Version: v2.1.0                      ║
║  Targets: 3 servers                   ║
╚═══════════════════════════════════════╝

┌─────────────────────────────────────┐
│ Pre-flight checks                   │
├─────────────────────────────────────┤
│ ✓ Health checks passed              │
│ ✓ Database migrations ready         │
│ ✓ Rollback plan verified            │
└─────────────────────────────────────┘
```

**Best for:** Critical notifications, summary reports, final confirmations

---

## Reusable Components

Copy-paste these snippets into your skills for consistent formatting.

### Phase Headers

**Style 1: Bracket notation (most common)**
```
[PHASE_NAME] Brief description of what's happening...
```

**Style 2: Markdown heading**
```
### Phase 1 — Name
Brief description...
```

**Style 3: Step notation**
```
Step 1: Name
  Details about this step...
```

**Choose one style per skill and use consistently.**

---

### Status Indicators

**Standard symbols:**
```
[SCAN]    Currently scanning...
  ✓       Success / completed
  →       In progress / moving to next
  ⚠       Warning / attention needed
  ✗       Error / failed
```

**Usage example:**
```
[ANALYZE] Processing dependencies...
  ✓ Resolved 47 packages
  ⚠ 2 packages have security advisories
  → Checking for updates...
```

---

### Progress Trackers

**Simple counter:**
```
[PROCESS] Analyzing files... (12/47 complete)
```

**Multi-worker progress:**
```
[ANALYZE] Worker A: 23 files processed
[ANALYZE] Worker B: 19 files processed
[ANALYZE] Worker C: 5 files processed
```

**Percentage-based:**
```
[MIGRATE] 67% complete (20/30 files)
```

---

### ASCII Box Templates

**Light (informational):**
```
┌─────────────────────────────────────┐
│ Content here                        │
└─────────────────────────────────────┘
```

**Medium (important):**
```
╔═════════════════════════════════════╗
║ Content here                        ║
╚═════════════════════════════════════╝
```

**Heavy (critical/emphasis):**
```
╔═══════════════════════════════════════╗
║                                       ║
║  ⚠️  CRITICAL DECISION POINT           ║
║                                       ║
╠═══════════════════════════════════════╣
║  This action will delete production  ║
║  data. This cannot be undone.        ║
║                                       ║
╚═══════════════════════════════════════╝
```

---

### Approval Gates

**Standard pattern:**
```
⚡ Action required: [Brief description of what will happen]

Do you want to proceed?
```

**With context:**
```
╔═══════════════════════════════════════╗
║  Ready to commit changes              ║
╠═══════════════════════════════════════╣
║  Files changed: 5                     ║
║  Lines added: 127                     ║
║  Lines removed: 43                    ║
╚═══════════════════════════════════════╝

Commit message: "refactor: simplify auth logic"

Do you want to create this commit?
```

**Critical operations:**
```
⚠️ WARNING: Destructive Operation

This will permanently delete:
  - 3 database tables
  - 127 files (2.3 MB)
  - All backups older than 30 days

Type "CONFIRM DELETE" to proceed, or anything else to cancel.
```

---

### Table Formats

**Simple reference:**
```
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value A  | Value B  | Value C  |
```

**With alignment:**
```
| Left-aligned | Center | Right |
|:-------------|:------:|------:|
| Text         | Text   | 123   |
```

**Status table:**
```
| File            | Status | Changes |
|-----------------|--------|---------|
| auth.ts         | ✓ OK   | 3       |
| database.ts     | ⚠ WARN | 12      |
| config.ts       | ✗ FAIL | -       |
```

---

## Best Practices

### Consistency Within a Skill

**DO:**
- Pick one phase header style and use throughout
- Use the same status symbols consistently
- Maintain uniform indentation
- Keep tone/voice consistent

**DON'T:**
- Mix `[PHASE]` with `### Phase` headers in same skill
- Switch between `✓` and `✅` randomly
- Change visual hierarchy mid-execution

---

### Clarity and Scannability

**DO:**
- Use whitespace to separate phases
- Put the most important information at the top
- Use visual markers (`→`, `✓`, `⚠`) for quick scanning
- Show summaries before details

**DON'T:**
- Create walls of text without structure
- Hide errors in verbose output
- Use ASCII art excessively (reduces scannability)
- Bury critical decisions deep in output

**Example (scannable):**
```
[ANALYZE] Found 3 issues:

  ✗ TypeScript error in auth.ts:42
  ⚠ Deprecated API in database.ts:156
  ⚠ Missing type in config.ts:12

Most critical: TypeScript error blocks compilation
```

---

### Progressive Disclosure

Show information as it becomes relevant, not all at once.

**Good progression:**
```
[SCAN] Searching codebase...
  ✓ Found 47 files

[ANALYZE] Checking for issues...
  → Analyzing auth.ts
  → Analyzing database.ts
  ✓ Analysis complete

[RESULTS] 2 issues found:
  Issue 1: [details]
  Issue 2: [details]
```

**Too much upfront:**
```
[INITIALIZE] Starting analysis tool v2.1.3
Configuration loaded from ~/.config/tool.yaml
Plugins: eslint, typescript, prettier
Search paths: src/, lib/, test/
Exclusions: node_modules/, dist/, .git/
Cache enabled: true (last cleared 3 days ago)
...

[Now actually starting work]
```

---

### User Control and Approval

**When to ask for approval:**
- Destructive operations (delete, overwrite)
- External actions (API calls, commits, deployments)
- Expensive operations (long-running tasks)
- Ambiguous decisions (multiple valid paths)

**When NOT to ask:**
- Read-only operations
- Clearly safe actions
- Steps user explicitly requested

**Pattern:**
```
[READY] About to execute:
  - Delete 3 temporary files
  - Create 1 new migration file
  - Update 2 config files

Do you want to proceed?
```

---

### Error Communication

**Clear failure modes:**
```
✗ Migration failed: auth.ts

  Reason: Syntax error at line 42

  Fix: Correct the closing bracket on line 42

  Rollback: No changes were committed
```

**Recovery steps:**
```
⚠ Warning: API rate limit reached

Recovery options:
  1. Wait 60 seconds and retry
  2. Use cached data instead
  3. Cancel operation

What would you like to do?
```

---

### Length Considerations

**Terse (prefer for):**
- Simple operations
- Frequently-run skills
- Utility commands
- Progress updates

**Verbose (prefer for):**
- Complex workflows
- First-time setup
- Error explanations
- Critical decisions

**Balance example:**
```
# Too terse
Analyzing...
Done. 3 issues.

# Too verbose
[ANALYZE] Initiating comprehensive analysis workflow
[ANALYZE] Parsing abstract syntax tree for semantic understanding
[ANALYZE] Applying heuristic pattern matching algorithms
[ANALYZE] Cross-referencing with dependency graph
[ANALYZE] Finalizing analysis results
[ANALYZE] Analysis complete. Found 3 issues requiring attention.

# Just right
[ANALYZE] Checking code for issues...
  ✓ Scanned 47 files
  ✓ Found 3 issues
```

---

## Migration Guide

Applying this framework to existing skills is **optional**. Use this guide if you want to improve an existing skill's output.

### Step 1: Identify Current Pattern

Which of the 7 patterns does your skill most closely match?

1. Structured Multi-Phase
2. Simple/Minimal
3. Manifesto + Rules-Heavy
4. Decision Tree/Flowchart
5. Reference Table
6. Checklist + Decision Point
7. Hierarchical Box/Border

### Step 2: Assess Pattern Match

Does the current pattern match your skill's complexity?

- **Too simple** → Consider adding phase structure
- **Too complex** → Simplify to essential information
- **Just right** → Focus on consistency polish

### Step 3: Apply Components Incrementally

Don't rewrite everything at once. Pick one improvement:

1. **Standardize status symbols** (easiest)
   - Replace mixed symbols with `✓`, `→`, `⚠`, `✗`

2. **Add phase headers** (medium)
   - Pick header style and mark major transitions

3. **Improve approval gates** (medium)
   - Use consistent pattern before destructive actions

4. **Add progress tracking** (harder)
   - Show status during long operations

### Step 4: Test with Users

- Is the output easier to scan?
- Are errors more obvious?
- Do users know when to approve/wait?
- Is important information highlighted?

### Step 5: Iterate

The framework is living documentation. If you discover better patterns, document them and share.

---

## Examples: Good vs. Unclear

### Example 1: Phase Transitions

**Unclear:**
```
Looking at files
Found some issues
Making changes
Finished
```

**Clear:**
```
[SCAN] Searching codebase...
  ✓ Found 47 files

[ANALYZE] Checking for issues...
  ✓ Found 3 issues requiring changes

[EXECUTE] Applying fixes...
  ✓ Updated 3 files

✅ Complete
```

---

### Example 2: Error Messages

**Unclear:**
```
Error: failed
```

**Clear:**
```
✗ Deployment failed

Reason: Server rejected connection (timeout after 30s)

Recovery:
  1. Check server status: curl https://api.example.com/health
  2. Verify credentials: echo $API_KEY
  3. Retry deployment: run /deploy again

Need help? See docs/troubleshooting.md
```

---

### Example 3: Approval Gates

**Unclear:**
```
Ready to deploy
```

**Clear:**
```
╔═══════════════════════════════════════╗
║  Ready to deploy to production        ║
╠═══════════════════════════════════════╣
║  Environment: prod-us-east-1          ║
║  Version: v2.1.0                      ║
║  Affected services: 3                 ║
║  Estimated downtime: 30 seconds       ║
╚═══════════════════════════════════════╝

⚠️  This will restart production services

Do you want to proceed?
```

---

## Design Principles

### 1. Clarity Over Creativity

Users should instantly understand:
- What phase the skill is in
- What's happening right now
- What will happen next
- When they need to take action

Visual flair is good, but never at the expense of clarity.

---

### 2. Consistency Within, Flexibility Across

**Within a skill:** Pick a style and commit
- Use same phase header format throughout
- Use same status symbols throughout
- Maintain consistent visual hierarchy

**Across skills:** Allow variation
- Different skills can use different patterns
- Match pattern to skill complexity
- Preserve skill personality/voice

---

### 3. User Control

**Always show what will happen before doing it:**
```
[READY] About to:
  - Delete 12 files
  - Create 3 new files
  - Commit with message: "refactor: simplify"

Proceed?
```

**Never do risky things silently:**
```
✗ BAD: Deleting production database... (no warning!)
✓ GOOD: Confirm deletion of production database?
```

---

### 4. Scannability

Users should be able to **skim** and understand state without reading every word.

**Techniques:**
- Visual markers (`✓`, `→`, `⚠`, `✗`)
- Whitespace for separation
- Headers for sections
- Indentation for hierarchy
- Short lines (avoid wrapping)

---

### 5. Maintainability

Output patterns should be easy to update as skills evolve.

**Prefer:**
- Template strings with variables
- Reusable formatting functions
- Consistent conventions

**Avoid:**
- One-off formatting scattered throughout code
- Hardcoded strings with no structure
- Mixing formatting logic with business logic

---

## Quick Reference

### Choosing a Pattern

| Skill Type | Recommended Pattern |
|------------|-------------------|
| Multi-step workflow | Structured Multi-Phase |
| Simple utility | Simple/Minimal |
| Code quality tool | Manifesto + Rules-Heavy |
| Conditional setup | Decision Tree/Flowchart |
| Documentation lookup | Reference Table |
| Deployment tool | Checklist + Decision Point |
| Critical operation | Hierarchical Box/Border |

### Common Components

| Element | Symbol/Format |
|---------|---------------|
| Success | `✓` |
| In progress | `→` |
| Warning | `⚠` |
| Error | `✗` |
| Phase header | `[PHASE_NAME]` |
| Approval gate | `⚡ Action required:` |

---

## Version History

- 1.0 (2026-02-05) Initial framework based on analysis of 60+ skills

---

## Contributing

Found a better pattern? Discovered an improvement? Update this document and share with the community. The framework evolves through real-world use.
