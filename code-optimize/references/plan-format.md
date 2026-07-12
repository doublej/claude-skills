# Plan Format — Standards, Checklists, and Task Plans

How to turn scan findings into an approved, actionable plan.

<standards_detection>

```text
Language detection:
├── go.mod           -> Go
├── Cargo.toml       -> Rust
├── package.json     -> TypeScript/JavaScript
├── pyproject.toml   -> Python
├── Package.swift    -> Swift
└── Multiple         -> Use all applicable standards

Standards (checked in order, first found wins):
├── docs/PROJECT_RULES.md
├── docs/STANDARDS.md
├── CLAUDE.md
└── Auto-detect from existing code patterns
```

If no standards file exists, proceed with language-default best practices and
note it in the report.

</standards_detection>

<analysis_checklists>

Detailed checks per analysis dimension.

## Architecture Analysis

```text
Checks:
├── Dependency Direction
│   ├── Domain has no external dependencies
│   ├── Dependencies point inward only
│   └── No circular dependencies between modules
│
├── Structure
│   ├── Matches standards/conventions (if documented)
│   ├── Clear separation of concerns
│   ├── Ports defined as interfaces (if applicable)
│   └── Adapters implement ports (if applicable)
│
└── Directory Layout
    ├── Logical grouping by feature or layer
    ├── Consistent file naming
    └── No mixed responsibilities in modules
```

## Code Quality Analysis

```text
Checks:
├── Naming Conventions
│   ├── Files match project pattern
│   ├── Functions/methods follow convention
│   └── Constants use appropriate casing
│
├── Error Handling
│   ├── No silently ignored errors
│   ├── Errors include context
│   ├── No panic/throw for business logic
│   └── Boundary validation present
│
├── Forbidden Practices
│   ├── No global mutable state
│   ├── No magic numbers/strings
│   ├── No commented-out code
│   ├── No TODO without issue reference
│   └── No untyped escape hatches (any, Object, etc.)
│
└── Security
    ├── Input validation at boundaries
    ├── Parameterised queries
    ├── Sensitive data not logged
    └── Secrets not hardcoded
```

## Testing Analysis

```text
Checks:
├── Coverage
│   ├── Current coverage percentage
│   ├── Critical paths covered
│   └── Gap to project minimum
│
├── Patterns
│   ├── Consistent test structure (Arrange-Act-Assert / Given-When-Then)
│   ├── Mocks for external dependencies
│   └── No test pollution (global state)
│
├── Naming
│   ├── Descriptive test names
│   └── Follows project convention
│
└── Types
    ├── Unit tests exist
    ├── Integration tests exist
    └── Test fixtures/factories where appropriate
```

## DevOps Analysis

```text
Checks:
├── Containerisation
│   ├── Dockerfile exists (if applicable)
│   ├── Multi-stage build
│   ├── Non-root user
│   └── Health check defined
│
├── Local Development
│   ├── docker-compose.yml or equivalent
│   ├── All services defined
│   └── Hot reload configured
│
├── Environment
│   ├── .env.example exists
│   ├── All env vars documented
│   └── No secrets in repo
│
└── CI/CD
    ├── Pipeline exists
    ├── Tests run in CI
    └── Linting enforced
```

</analysis_checklists>

<parallel_dispatch>

All analysis agents MUST be dispatched in a SINGLE message with multiple Task
tool calls.

Each agent should:
1. Read project standards (PROJECT_RULES.md, CLAUDE.md, or auto-detected)
2. Analyse only — do NOT implement changes
3. Return findings with: severity, location (file:line), issue, recommendation

### Code Analysis Agent

```yaml
Task tool:
  subagent_type: "general-purpose"
  model: "sonnet"
  prompt: |
    **MODE: ANALYSIS ONLY** (do not implement, only report findings)

    Analyze this {language} codebase for refactoring opportunities.

    Read any standards file (PROJECT_RULES.md, CLAUDE.md) first.

    Focus on:
    - Directory structure and architecture patterns
    - Dependency direction and separation of concerns
    - Error handling patterns
    - Naming conventions
    - Anti-patterns and technical debt
    - Security issues

    Return findings with severity (Critical/High/Medium/Low), location (file:line), issue, and recommendation.
```

### Testing Agent

```yaml
Task tool:
  subagent_type: "general-purpose"
  model: "sonnet"
  prompt: |
    **MODE: ANALYSIS ONLY**

    Analyze test coverage and quality.

    Check: test coverage, test patterns, naming, missing tests for critical paths,
    mock usage, test isolation.

    Return findings with severity, location, issue, and recommendation.
```

### DevOps Agent

```yaml
Task tool:
  subagent_type: "general-purpose"
  model: "sonnet"
  prompt: |
    **MODE: ANALYSIS ONLY**

    Check: Dockerfile best practices, docker-compose config, .env.example,
    CI/CD pipeline, health endpoints, structured logging.

    Return findings with severity, location, issue, and recommendation.
```

</parallel_dispatch>

<compile_findings>

Collect outputs from all sources and merge into a structured report:

1. **Collect** automated findings (scan scripts, code-audit) + agent outputs
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

</compile_findings>

<prioritise_and_group>

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

</prioritise_and_group>

<tasks_format>

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

</tasks_format>

<user_approval>

Present the generated plan with options:

| Option | Behaviour |
|--------|-----------|
| Approve all | Save tasks.md, start execution |
| Approve with changes | User edits tasks.md first |
| Critical only | Filter to Critical/High priority tasks |
| Cancel | Keep analysis report only |

If the user cancels at the approval step:

1. Ask why (briefly)
2. Save reason to `docs/refactor/{timestamp}/cancelled-reason.md`
3. Preserve partial analysis artifacts

</user_approval>

<save_artifacts>

```text
docs/refactor/{timestamp}/
├── analysis-report.md     # Full analysis with all findings
├── tasks.md               # Approved refactoring tasks
└── standards-used.md      # Standards referenced during analysis
```

</save_artifacts>

<pressure_resistance>

How to handle pressure to skip or reduce analysis scope.

| Excuse | Reality |
|--------|---------|
| "Code works fine" | Working != maintainable. Analysis reveals hidden debt. |
| "Too time-consuming" | Cost of analysis < cost of compounding debt. |
| "Standards don't fit us" | Document YOUR standards, then analyse against those. |
| "Only critical matters" | Today's medium = tomorrow's critical. Document all. |
| "Legacy gets a pass" | Legacy needs analysis most — it sets precedent. |

All dimensions should be covered unless the user explicitly scopes down:

| Deliverable | Required | Purpose |
|-------------|----------|---------|
| analysis-report.md | Yes | Document findings |
| tasks.md | Yes | Convert findings to actionable tasks |
| User approval | Yes | Get explicit decision on execution |

</pressure_resistance>
