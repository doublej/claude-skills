---
name: dev-refactor
description: Analyzes existing codebases against standards to identify gaps in architecture, code quality, testing, and DevOps. Auto-detects project language and generates refactoring tasks. Use when refactoring legacy projects, auditing codebases, or modernizing existing code.
---

# Dev Refactor

Analyses an existing codebase to identify gaps between current implementation and project standards, then generates a structured refactoring plan with actionable tasks.

## What This Skill Does

1. **Detects project language** from manifest files (go.mod, package.json, pyproject.toml, Cargo.toml, etc.)
2. **Reads project standards** from PROJECT_RULES.md, CLAUDE.md, or auto-detects conventions
3. **Generates structural map** using codebase-mapper (PageRank-ranked)
4. **Runs automated detection** using repomap-analyzer (deprecated, dead code, duplicates, conventions)
5. **Dispatches analysis agents** for deeper inspection across 4 dimensions
6. **Compiles findings** into structured analysis report with severity levels
7. **Generates tasks.md** with actionable refactoring tasks
8. **User approves** the plan before execution

## Analysis Dimensions

| Dimension | What It Checks |
|-----------|---------------|
| Architecture | Patterns, structure, dependency direction, separation of concerns |
| Code Quality | Standards compliance, naming, error handling, security |
| Testing | Coverage, test patterns, naming, missing tests |
| DevOps | Containerisation, CI/CD, environment config |

## Workflow

### Step 1: Detect Language and Standards

```text
Language detection:
├── go.mod           -> Go
├── Cargo.toml       -> Rust
├── package.json     -> TypeScript/JavaScript
├── pyproject.toml   -> Python
└── Multiple         -> Use all applicable standards

Standards (checked in order, first found wins):
├── docs/PROJECT_RULES.md
├── docs/STANDARDS.md
├── CLAUDE.md
└── Auto-detect from existing code patterns
```

If no standards file exists, proceed with language-default best practices and note it in the report.

### Step 2: Structural Map (codebase-mapper)

Generate a PageRank-ranked map to identify the most important files:

```bash
bash {CODEBASE_MAPPER_DIR}/scripts/repomap.sh . --root . --map-tokens 8192 --exclude-unranked
```

This reveals which files are most referenced/depended upon — refactoring these has the highest impact.

### Step 3: Automated Detection (repomap-analyzer)

Run automated detectors for quick wins:

```bash
python3 {REPOMAP_ANALYZER_DIR}/analyze.py . --output /tmp/auto-findings.md
```

This catches deprecated patterns, naming inconsistencies, dead code, and duplicates without manual inspection.

### Step 4: Deep Analysis (Parallel Agents)

Dispatch analysis agents in PARALLEL (single message, multiple Task tools):

- **Code analysis agent** — architecture, code quality, language-specific patterns
- **Testing agent** — coverage gaps, test quality, missing tests
- **DevOps agent** — container config, CI/CD, environment setup

Each agent operates in **analysis-only mode** (no implementation).

### Step 5: Compile and Prioritise

1. Merge automated findings + agent findings
2. Deduplicate overlapping issues
3. Categorise by dimension
4. Sort by severity (Critical > High > Medium > Low)
5. Group related issues into REFACTOR-XXX tasks by module and dependency order

### Step 6: Generate Artifacts

```text
docs/refactor/{timestamp}/
├── analysis-report.md     # Full findings with severity
├── tasks.md               # Actionable refactoring tasks
└── standards-used.md      # Standards referenced during analysis
```

### Step 7: User Approval

Present plan with options: Approve all, Approve with changes, Critical only, Cancel.

## Reference Files

- [Analysis Patterns](references/analysis-patterns.md) — detailed checks per dimension, agent prompts
- [Refactoring Strategies](references/refactoring-strategies.md) — compiling, prioritisation, task format
- [Common Rationalizations](references/common-rationalizations.md) — handling pressure to skip analysis

## Related Skills

| Skill | Relationship |
|-------|-------------|
| **codebase-mapper** | Generates PageRank structural map (Step 2) |
| **repomap-analyzer** | Runs automated code quality detection (Step 3) |
