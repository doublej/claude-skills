# Refactoring Strategies

Compiling findings, prioritization, and task generation.

## Compile Findings

Collect outputs from all dispatched agents and merge into structured report:

1. **Collect** all agent outputs (backend-engineer-*, qa-analyst, devops-engineer, sre)
2. **Parse** findings from each output (severity, location, issue, recommendation)
3. **Deduplicate** overlapping findings
4. **Categorize** by dimension (Architecture, Code Quality, Testing, DevOps)
5. **Sort** by severity (Critical -> High -> Medium -> Low)

### Analysis Report Template

```markdown
# Analysis Report: {project-name}

**Generated:** {date}
**Standards:** {path to PROJECT_RULES.md used}
**Scope:** {directories analyzed}

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

## Prioritize and Group

Group related issues into logical refactoring tasks:

```text
Grouping Strategy:
1. By bounded context / module
2. By dependency order (fix dependencies first)
3. By risk (critical security first)

Example grouping:
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
└── REFACTOR-004: Containerization improvements
    ├── DEVOPS-001: Add multi-stage Dockerfile
    └── DEVOPS-002: Create docker-compose.yml
```

## Generate tasks.md

Create refactoring tasks in PM Team format:

```markdown
# Refactoring Tasks: {project-name}

**Source:** Analysis Report {date}
**Total Tasks:** {count}
**Estimated Effort:** {total hours}

---

## REFACTOR-001: Fix domain layer isolation

**Type:** backend
**Effort:** 4h
**Priority:** Critical
**Dependencies:** none

### Description
Remove infrastructure dependencies from domain layer and establish proper
port/adapter boundaries following hexagonal architecture.

### Acceptance Criteria
- [ ] AC-1: Domain package has zero imports from infrastructure
- [ ] AC-2: Repository interfaces defined in domain layer
- [ ] AC-3: All domain entities use dependency injection
- [ ] AC-4: Existing tests still pass

### Technical Notes
- Files to modify: src/domain/*.go
- Pattern: See PROJECT_RULES.md -> Hexagonal Architecture section
- Related issues: ARCH-001, ARCH-003, ARCH-005

### Issues Addressed
| ID | Description | Location |
|----|-------------|----------|
| ARCH-001 | Domain imports database | src/domain/user.go:15 |
| ARCH-003 | No repository interface | src/domain/ |
| ARCH-005 | Events in wrong layer | src/infrastructure/events.go |
```

## User Approval

Present the generated plan using AskUserQuestion:

```yaml
AskUserQuestion:
  questions:
    - question: "Review the refactoring plan. How do you want to proceed?"
      header: "Approval"
      multiSelect: false
      options:
        - label: "Approve all"
          description: "Save tasks.md, proceed to dev-cycle execution"
        - label: "Approve with changes"
          description: "Let user edit tasks.md first, then proceed"
        - label: "Critical only"
          description: "Filter to only Critical/High priority tasks"
        - label: "Cancel"
          description: "Abort execution, keep analysis report only"
```

## Save Artifacts

```text
docs/refactor/{timestamp}/
├── analysis-report.md    # Full analysis with all findings
├── tasks.md              # Approved refactoring tasks
└── project-rules-used.md # Copy of PROJECT_RULES.md at time of analysis
```

## Output Schema

```yaml
output_schema:
  format: "markdown"
  artifacts:
    - name: "analysis-report.md"
      location: "docs/refactor/{timestamp}/"
      required: true
    - name: "tasks.md"
      location: "docs/refactor/{timestamp}/"
      required: true
  required_sections:
    - name: "Summary"
      pattern: "^## Summary"
    - name: "Critical Issues"
      pattern: "^## Critical Issues"
    - name: "Tasks Generated"
      pattern: "^## REFACTOR-"
```

## Handoff to dev-cycle

If approved:

```bash
/ring-dev-team:dev-cycle docs/refactor/{timestamp}/tasks.md
```

Executes each task through the standard 6-gate process:
- Gate 0: Implementation (TDD)
- Gate 1: DevOps Setup
- Gate 2: SRE (Observability)
- Gate 3: Testing
- Gate 4: Review (3 parallel reviewers)
- Gate 5: Validation (user approval)
