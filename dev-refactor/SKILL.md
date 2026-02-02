---
name: dev-refactor
description: Analyzes existing codebases against standards to identify gaps in architecture, code quality, testing, and DevOps. Auto-detects project language (Go, TypeScript, Frontend) and generates refactoring tasks. Use when refactoring legacy projects, auditing codebases, or modernizing existing code to follow standards.
---

# Dev Refactor Skill

Analyzes an existing codebase to identify gaps between current implementation and project standards, then generates a structured refactoring plan.

## What This Skill Does

1. **Detects project language** (Go, TypeScript, Python) from manifest files
2. **Reads PROJECT_RULES.md** (project-specific standards - MANDATORY)
3. **Dispatches specialized agents** that load Ring standards via WebFetch
4. **Compiles agent findings** into structured analysis report
5. **Generates tasks.md** in PM Team format
6. **User approves** the plan before execution via dev-cycle

## Core Principle

**Refactoring analysis is MANDATORY for codebases with technical debt.**

- **NEVER** skip analysis because "code works"
- **ALWAYS** analyze all 4 dimensions
- **DOCUMENT** all findings, not just critical
- Analysis now saves 10x effort later

## Prerequisites

1. **PROJECT_RULES.md exists** (MANDATORY - analysis cannot proceed without it)
2. **Project root identified**
3. **Language detectable** (go.mod, package.json, etc.)

If PROJECT_RULES.md is missing, STOP with blocker message.

## Analysis Dimensions - ALL REQUIRED

| Dimension | What It Checks | Skip Allowed? |
|-----------|---------------|---------------|
| Architecture | Patterns, structure, dependencies | NO |
| Code Quality | Standards compliance, complexity, naming | NO |
| Testing | Coverage, test quality, TDD compliance | NO |
| DevOps | Containerization, CI/CD, infrastructure | NO |

## Workflow Steps

### Step 0: Verify PROJECT_RULES.md (HARD GATE)

Check: `docs/PROJECT_RULES.md` or `docs/STANDARDS.md`
If missing: STOP - Cannot analyze without project standards.

### Step 1: Detect Project Language

```text
├── go.mod exists -> Go project
├── package.json exists
│   ├── Has react/next -> Frontend TypeScript
│   └── Has express/fastify/nestjs -> Backend TypeScript
└── Multiple languages -> Use all applicable standards
```

### Step 2: Read PROJECT_RULES.md

Load project-specific conventions and standards.

### Step 3: Scan Codebase

Dispatch specialized agents in PARALLEL (single message, multiple Task tools):
- Code analysis agent (language-specific)
- qa-analyst (testing)
- devops-engineer (infrastructure)
- sre (observability)

Each agent loads Ring standards via WebFetch automatically.

### Step 4: Compile Findings

Merge agent outputs into structured analysis report with severity levels.

### Step 5: Prioritize and Group

Group related issues into REFACTOR-XXX tasks by:
- Bounded context / module
- Dependency order
- Risk level

### Step 6: Generate tasks.md

Create refactoring tasks in PM Team format with acceptance criteria.

### Step 7: User Approval

Present plan with options: Approve all, Approve with changes, Critical only, Cancel.

### Step 8: Save Artifacts

```text
docs/refactor/{timestamp}/
├── analysis-report.md
├── tasks.md
└── project-rules-used.md
```

### Step 9: Handoff to dev-cycle

If approved: `/ring-dev-team:dev-cycle docs/refactor/{timestamp}/tasks.md`

## Example Usage

```bash
# Full project analysis
/ring-dev-team:dev-refactor

# Analyze specific directory
/ring-dev-team:dev-refactor src/domain

# Analysis only (no execution)
/ring-dev-team:dev-refactor --analyze-only
```

## Reference Files

- [Analysis Patterns](references/analysis-patterns.md) - Detailed checks, agent selection, prompts
- [Refactoring Strategies](references/refactoring-strategies.md) - Compiling, prioritization, task generation
- [Common Rationalizations](references/common-rationalizations.md) - Pressure resistance, red flags

## Related Skills

| Skill | Purpose |
|-------|---------|
| `ring-dev-team:dev-cycle` | Executes refactoring tasks through 6 gates |

## Key Principles

1. **Same workflow**: Refactoring uses the same dev-cycle as new features
2. **Standards-driven**: Combines PROJECT_RULES.md + Ring standards
3. **Traceable**: Every task links to specific issues found
4. **Incremental**: Can approve subset of tasks
5. **Reversible**: Original analysis preserved
