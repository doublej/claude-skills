# Multi-Phase Workflow Template

Use this template for complex skills with multiple decision points, approval gates, and branching logic.

---

## Template Structure

```markdown
---
name: your-skill-name
description: Brief description of what your skill does and when to use it
allowed-tools:
  - Read
  - Bash(command*)
  - Edit
---

# Your Skill Name

[Detailed explanation of what this skill does and when to use it]

## Workflow

This skill follows a structured approach:

### Phase 1 — Discovery
[What gets discovered and how]

### Phase 2 — Analysis
[What gets analyzed and how]

### Phase 3 — Planning
[How decisions are made]

### Phase 4 — Execution
[What actions are taken]

### Phase 5 — Verification
[How results are validated]

---

## Phase 1 — Discovery

[DISCOVER] Scanning project structure...
  → Checking file system
  → Reading configuration
  → Detecting dependencies
  ✓ Discovery complete

Found:
  - [Category 1]: N items
  - [Category 2]: M items
  - [Category 3]: P items

---

## Phase 2 — Analysis

[ANALYZE] Evaluating findings...
  → Analyzing [aspect 1]
  → Analyzing [aspect 2]
  → Checking [constraint 1]
  ✓ Analysis complete

Results:
  ✓ [Positive finding 1]
  ⚠ [Warning 1]
  ✗ [Issue 1]

---

## Phase 3 — Planning

[PLAN] Creating execution strategy...

Proposed changes:
  1. [Change description 1]
     - Affects: [files/resources]
     - Risk: [low/medium/high]

  2. [Change description 2]
     - Affects: [files/resources]
     - Risk: [low/medium/high]

╔═══════════════════════════════════════╗
║  Ready to proceed with N changes      ║
╠═══════════════════════════════════════╣
║  Files to modify: X                   ║
║  Files to create: Y                   ║
║  Files to delete: Z                   ║
╚═══════════════════════════════════════╝

⚡ Action required: Review plan above

Do you want to proceed with these changes?
```

[Wait for user approval]

---

## Phase 4 — Execution

[EXECUTE] Applying changes...
  ✓ Step 1: [description]
  ✓ Step 2: [description]
  → Step 3: [description] (in progress)

Progress: (3/10 steps complete)
```

---

## Phase 5 — Verification

[VERIFY] Checking results...
  → Running tests
  → Validating changes
  ✓ Verification complete

Results:
  ✓ All tests passing
  ✓ No regressions detected
  ✓ Changes working as expected

✅ Done: [Summary of what was accomplished]

---

## Rollback (if needed)

If something went wrong:
```
⚠ Issue detected during [phase]

Rolling back changes:
  ✓ Reverted [change 1]
  ✓ Reverted [change 2]
  ✓ Rollback complete

No permanent changes were made.
```
```

---

## Key Elements

### 1. Phase Structure
Clear phase boundaries with numbering:
```markdown
## Phase 1 — Discovery
[DISCOVER] ...

## Phase 2 — Analysis
[ANALYZE] ...
```

### 2. Progressive Detail
Start with overview, then drill down:
```markdown
## Workflow Overview
1. Discovery → 2. Analysis → 3. Planning → 4. Execution → 5. Verification

[Then show each phase in detail]
```

### 3. Approval Gates
Explicit user control before risky actions:
```markdown
╔═══════════════════════════════════════╗
║  About to [action]                    ║
╠═══════════════════════════════════════╣
║  [Key details]                        ║
╚═══════════════════════════════════════╝

⚡ Action required: [What user needs to decide]

Do you want to proceed?
```

### 4. Status Tracking
Show progress during long phases:
```markdown
[EXECUTE] Applying migrations... (5/12 complete)
  ✓ Migration 1: AddUserTable
  ✓ Migration 2: AddIndexes
  ✓ Migration 3: UpdateSchema
  → Migration 4: MigrateData (running)
  - Migration 5: CleanupOldData
  ...
```

### 5. Error Recovery
Clear failure modes with recovery steps:
```markdown
✗ Phase 3 failed: [Reason]

What went wrong:
  [Explanation]

Recovery options:
  1. [Option 1]: [What it does]
  2. [Option 2]: [What it does]
  3. [Option 3]: [What it does]

What would you like to do?
```

---

## Example: Database Migration Skill

```markdown
---
name: database-migrator
description: Apply database migrations with safety checks and rollback support
allowed-tools:
  - Read
  - Bash(npm*, psql*)
---

# Database Migrator

Safely applies database migrations with pre-flight checks, user approval, and automatic rollback on failure.

## Workflow

### Phase 1 — Discovery
Scan for pending migrations and check database status

### Phase 2 — Analysis
Validate migrations and assess impact

### Phase 3 — Planning
Create execution plan with rollback strategy

### Phase 4 — Execution
Apply migrations with progress tracking

### Phase 5 — Verification
Validate schema and run sanity tests

---

## Phase 1 — Discovery

[DISCOVER] Scanning for migrations...
  → Checking migrations/ directory
  → Connecting to database
  → Querying migration history
  ✓ Discovery complete

Found:
  - Pending migrations: 3
  - Applied migrations: 47
  - Database: PostgreSQL 15.2

Pending:
  1. 20250201_add_user_roles.sql
  2. 20250202_create_indexes.sql
  3. 20250203_migrate_legacy_data.sql

---

## Phase 2 — Analysis

[ANALYZE] Validating migrations...
  → Checking SQL syntax
  → Analyzing schema changes
  → Estimating execution time
  ✓ Analysis complete

Assessment:
  ✓ All migrations valid
  ✓ No conflicting changes
  ⚠ Migration 3 will take ~30 seconds (table has 100K rows)

Impact:
  - Tables affected: 3
  - Indexes created: 5
  - Data rows to migrate: 100,000

---

## Phase 3 — Planning

[PLAN] Creating execution strategy...

Execution order:
  1. Begin transaction
  2. Apply migration 1: add_user_roles (est. 1s)
  3. Apply migration 2: create_indexes (est. 5s)
  4. Apply migration 3: migrate_legacy_data (est. 30s)
  5. Commit transaction

Rollback plan:
  - Automatic rollback on any error
  - Transaction isolation ensures atomicity
  - Backup available: backup_20250205_120000.sql

╔═══════════════════════════════════════╗
║  Ready to apply 3 migrations          ║
╠═══════════════════════════════════════╣
║  Estimated time: 36 seconds           ║
║  Rollback: Automatic on failure       ║
║  Backup: Available                    ║
╚═══════════════════════════════════════╝

⚡ Action required: Review migration plan

Do you want to apply these migrations?

---

## Phase 4 — Execution

[EXECUTE] Applying migrations...

  ✓ Transaction started
  ✓ Migration 1: add_user_roles (0.8s)
  ✓ Migration 2: create_indexes (4.2s)
  → Migration 3: migrate_legacy_data (in progress, 18s elapsed)

Progress: 65% (65,000/100,000 rows)

  ✓ Migration 3: migrate_legacy_data (28.5s)
  ✓ Transaction committed

Total time: 34.1 seconds

---

## Phase 5 — Verification

[VERIFY] Validating changes...
  → Running schema checks
  → Testing indexes
  → Verifying data integrity
  ✓ Verification complete

Results:
  ✓ Schema matches expected state
  ✓ All indexes created successfully
  ✓ Data migration completed (100,000 rows)
  ✓ Foreign key constraints valid

✅ Done: 3 migrations applied successfully

Migration history updated:
  - 20250201_add_user_roles.sql ✓
  - 20250202_create_indexes.sql ✓
  - 20250203_migrate_legacy_data.sql ✓
```

---

## Customization Tips

### Add Conditional Branching
Show different paths based on findings:

```markdown
[ANALYZE] Checking environment...

Environment: development
  → Using fast mode (no backup required)

[Alternative for production]
Environment: production
  → Creating backup first (required for prod)
  ✓ Backup complete: backup_20250205.sql
```

### Add Dry Run Mode
Let users preview without executing:

```markdown
[DRY RUN] Simulating changes...
  → Would update 5 files
  → Would create 2 files
  → Would delete 1 file

No actual changes made.

Run with --apply to execute changes.
```

### Add Checkpoints
For very long operations, add resumable checkpoints:

```markdown
[CHECKPOINT] Saved progress: 5/10 steps complete
If interrupted, restart with: skill resume --checkpoint=5
```

---

## When to Use This Template

**Good fit:**
- Database migrations
- Deployment workflows
- Large-scale refactoring
- Multi-step setup processes
- Operations with rollback needs

**Not a good fit:**
- Simple linear tasks → use `simple-workflow.md`
- Read-only operations → use `reference.md`
- Single-decision tools → consider simpler pattern

---

## See Also

- [OUTPUT_FRAMEWORK.md](../OUTPUT_FRAMEWORK.md) - Full framework documentation
- [simple-workflow.md](./simple-workflow.md) - Template for simpler workflows
- [components.md](./components.md) - Reusable formatting snippets
