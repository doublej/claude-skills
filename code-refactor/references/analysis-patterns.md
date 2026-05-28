# Analysis Patterns

Detailed analysis checks for each dimension.

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

## Parallel Analysis Dispatch

All agents MUST be dispatched in a SINGLE message with multiple Task tool calls.

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
