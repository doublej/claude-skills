# Refactoring Strategies

Compiling findings, prioritisation, and task generation.

## Compile Findings

Collect outputs from all sources and merge into structured report:

1. **Collect** automated findings (repomap-analyzer) + agent outputs
2. **Parse** findings from each source (severity, location, issue, recommendation)
3. **Deduplicate** overlapping findings
4. **Categorise** by dimension (Architecture, Code Quality, Testing, DevOps)
5. **Sort** by severity (Critical > High > Medium > Low)

### Analysis Report Template

```markdown
# Analysis Report: {project-name}

**Generated:** {date}
**Standards:** {path to standards file used, or "auto-detected"}
**Scope:** {directories analysed}

## Summary

| Dimension    | Issues | Critical | High | Medium | Low |
|--------------|--------|----------|------|--------|-----|
| Architecture | 12     | 2        | 4    | 4      | 2   |
| Code Quality | 23     | 1        | 8    | 10     | 4   |
| Testing      | 8      | 3        | 3    | 2      | 0   |
| DevOps       | 5      | 0        | 2    | 2      | 1   |
| **Total**    | **48** | **6**    | **17**| **18**| **7**|

## Critical Issues (Fix Immediately)

### ARCH-001: Domain depends on infrastructure
**Location:** `src/domain/user.go:15`
**Issue:** Domain entity imports database package
**Standard:** Domain layer must have zero external dependencies
**Fix:** Extract repository interface, inject via constructor
```

## Prioritise and Group

Group related issues into logical refactoring tasks:

```text
Grouping Strategy:
1. By module / bounded context
2. By dependency order (fix dependencies first)
3. By risk (critical security first)

Example:
├── REFACTOR-001: Fix domain layer isolation
│   ├── ARCH-001: Remove infra imports from domain
│   ├── ARCH-003: Extract repository interfaces
│   └── ARCH-005: Move domain events to domain layer
│
├── REFACTOR-002: Implement proper error handling
│   ├── CODE-002: Wrap errors with context (15 locations)
│   ├── CODE-007: Replace panic with error returns
│   └── CODE-012: Add custom domain error types
│
├── REFACTOR-003: Add missing test coverage
│   ├── TEST-001: User service unit tests
│   ├── TEST-002: Order handler tests
│   └── TEST-003: Repository integration tests
│
└── REFACTOR-004: Containerisation improvements
    ├── DEVOPS-001: Add multi-stage Dockerfile
    └── DEVOPS-002: Create docker-compose.yml
```

## Generate tasks.md

Create refactoring tasks with acceptance criteria:

```markdown
# Refactoring Tasks: {project-name}

**Source:** Analysis Report {date}
**Total Tasks:** {count}

---

## REFACTOR-001: Fix domain layer isolation

**Priority:** Critical
**Dependencies:** none

### Description
Remove infrastructure dependencies from domain layer and establish proper
port/adapter boundaries.

### Acceptance Criteria
- [ ] Domain package has zero imports from infrastructure
- [ ] Repository interfaces defined in domain layer
- [ ] All domain entities use dependency injection
- [ ] Existing tests still pass

### Technical Notes
- Files to modify: src/domain/*.go
- Related issues: ARCH-001, ARCH-003, ARCH-005
```

## User Approval

Present the generated plan with options:

| Option | Behaviour |
|--------|-----------|
| Approve all | Save tasks.md, start execution |
| Approve with changes | User edits tasks.md first |
| Critical only | Filter to Critical/High priority tasks |
| Cancel | Keep analysis report only |

## Save Artifacts

```text
docs/refactor/{timestamp}/
├── analysis-report.md     # Full analysis with all findings
├── tasks.md               # Approved refactoring tasks
└── standards-used.md      # Standards referenced during analysis
```
