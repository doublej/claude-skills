# Analysis Patterns

Detailed analysis checks for each dimension.

## Architecture Analysis

```text
Checks:
├── DDD Patterns (if enabled in PROJECT_RULES.md)
│   ├── Entities have identity comparison
│   ├── Value Objects are immutable
│   ├── Aggregates enforce invariants
│   ├── Repositories are interface-based
│   └── Domain events for state changes
│
├── Clean Architecture / Hexagonal
│   ├── Dependency direction (inward only)
│   ├── Domain has no external dependencies
│   ├── Ports defined as interfaces
│   └── Adapters implement ports
│
└── Directory Structure
    ├── Matches PROJECT_RULES.md layout
    ├── Separation of concerns
    └── No circular dependencies
```

## Code Quality Analysis

```text
Checks:
├── Naming Conventions
│   ├── Files match pattern (snake_case, kebab-case, etc.)
│   ├── Functions/methods follow convention
│   └── Constants are UPPER_SNAKE
│
├── Error Handling
│   ├── No ignored errors (_, err := ...)
│   ├── Errors wrapped with context
│   ├── No panic() for business logic
│   └── Custom error types for domain
│
├── Forbidden Practices
│   ├── No global mutable state
│   ├── No magic numbers/strings
│   ├── No commented-out code
│   ├── No TODO without issue reference
│   └── No `any` type (TypeScript)
│
└── Security
    ├── Input validation at boundaries
    ├── Parameterized queries (no SQL injection)
    ├── Sensitive data not logged
    └── Secrets not hardcoded
```

## Testing Analysis

```text
Checks:
├── Test Coverage
│   ├── Current coverage percentage
│   ├── Gap to minimum (80%)
│   └── Critical paths covered
│
├── Test Patterns
│   ├── Table-driven tests (Go)
│   ├── Arrange-Act-Assert structure
│   ├── Mocks for external dependencies
│   └── No test pollution (global state)
│
├── Test Naming
│   ├── Follows Test{Unit}_{Scenario}_{Expected}
│   └── Descriptive test names
│
└── Test Types
    ├── Unit tests exist
    ├── Integration tests exist
    └── Test fixtures/factories
```

## DevOps Analysis

```text
Checks:
├── Containerization
│   ├── Dockerfile exists
│   ├── Multi-stage build
│   ├── Non-root user
│   └── Health check defined
│
├── Local Development
│   ├── docker-compose.yml exists
│   ├── All services defined
│   └── Volumes for hot reload
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

## Agent Selection

Select the appropriate code analysis agent based on language detection:

| Language/Project Type | Code Analysis Agent |
|-----------------------|---------------------|
| Go (`go.mod` exists) | `ring-dev-team:backend-engineer-golang` |
| TypeScript Backend (express, fastify, nestjs) | `ring-dev-team:backend-engineer-typescript` |
| TypeScript Frontend (react, next) | `ring-dev-team:frontend-bff-engineer-typescript` |
| Frontend Design/CSS | `ring-dev-team:frontend-designer` |
| Mixed/Multiple | Dispatch multiple code agents in parallel |

## Parallel Analysis Dispatch

All agents MUST be dispatched in a SINGLE message with multiple Task tool calls.

Each agent will:
1. Read `docs/PROJECT_RULES.md` automatically
2. Load its Ring standards via WebFetch
3. Return dimension-specific findings

### Go Projects

```yaml
Task tool:
  subagent_type: "ring-dev-team:backend-engineer-golang"
  model: "opus"
  prompt: |
    **MODE: ANALYSIS ONLY** (do not implement, only report findings)

    Analyze this Go codebase for refactoring opportunities.

    Focus on:
    - Directory structure compliance with PROJECT_RULES.md
    - DDD patterns (Entities, Value Objects, Aggregates, Repositories)
    - Clean/Hexagonal Architecture (dependency direction)
    - Error handling patterns (no ignored errors, proper wrapping)
    - Naming conventions (files, functions, constants)
    - Anti-patterns and technical debt
    - Security issues (input validation, SQL injection, secrets)

    Return findings with severity (Critical/High/Medium/Low), location (file:line), issue, and recommendation.
```

### TypeScript Backend

```yaml
Task tool:
  subagent_type: "ring-dev-team:backend-engineer-typescript"
  model: "opus"
  prompt: |
    **MODE: ANALYSIS ONLY** (do not implement, only report findings)

    Focus on: Directory structure, Clean Architecture, type safety (no `any`),
    error handling, async/await patterns, security issues.
```

### TypeScript Frontend/BFF

```yaml
Task tool:
  subagent_type: "ring-dev-team:frontend-bff-engineer-typescript"
  model: "opus"
  prompt: |
    **MODE: ANALYSIS ONLY** (do not implement, only report findings)

    Focus on: Component structure, state management, API layer architecture,
    type safety, performance patterns.
```

### Testing (Always Included)

```yaml
Task tool:
  subagent_type: "ring-dev-team:qa-analyst"
  model: "opus"
  prompt: |
    **MODE: ANALYSIS ONLY**
    Check: Test coverage (min 80%), test patterns, TDD compliance,
    missing tests for critical paths, naming, mock usage.
```

### DevOps (Always Included)

```yaml
Task tool:
  subagent_type: "ring-dev-team:devops-engineer"
  model: "opus"
  prompt: |
    **MODE: ANALYSIS ONLY**
    Check: Dockerfile best practices, docker-compose config, .env.example.
```

### SRE (Always Included)

```yaml
Task tool:
  subagent_type: "ring-dev-team:sre"
  model: "opus"
  prompt: |
    **MODE: ANALYSIS ONLY**
    Check: Health endpoints, structured logging, tracing setup.
```
