---
name: agent-friendly-cli
description: "Design CLIs optimized for LLM/agent consumption and parsing"
  or auditing a CLI's agent-friendliness.
---

# Agent-Friendly CLI

Build CLIs that minimize agent memory burden, token usage, and repair loops.

## Core Properties

An agent-friendly CLI is:

1. **Self-describing** — one command returns a complete machine-readable guide
2. **Intent-oriented** — commands match goals, not memorized syntax
3. **Structured** — outputs and errors are machine-parseable
4. **Recoverable** — failures include actionable repair hints
5. **State-aware** — prior results and defaults are reusable
6. **Infrastructure-buffered** — rate limits, cache, sessions internalized
7. **Batch-capable** — one command replaces repetitive loops
8. **Workflow-complete** — full task lifecycle inside the CLI

## Workflow

Determine the task type:

**Building a new CLI:**
1. Gather requirements (what agents will do with this CLI)
2. Design the command surface using the design template below
3. Implement with structured output, error model, and state management
4. Audit with `references/evaluation-rubric.md`

**Refactoring existing CLI for agents:**
1. Audit current CLI against `references/evaluation-rubric.md`
2. Identify gaps (usually: structured output, error model, self-description)
3. Add agent-friendly layers without breaking human UX
4. Re-audit

**Auditing a CLI:**
1. Run through `references/evaluation-rubric.md` checklist
2. Report findings with priority ranking

## Design Template

When designing a CLI, address each layer:

### 1. Entry Surface
- Natural invocation (argument shape implies intent)
- Explicit subcommands as escape hatches
- `guide` or `prime` command for machine-readable self-description

### 2. Data Contract
- `--format json|jsonl|table|csv` (default: json when piped, table when TTY)
- `--fields` for field projection
- `--verbose` / `--brief` verbosity tiers
- Stable schemas — breaking changes require version bump

### 3. State Model
- Ephemeral IDs (short, recent-context references like `@1`, `@last`)
- Persistent references for cross-command reuse
- Config file for defaults (`~/.config/<tool>/config.toml`)

### 4. Execution Model
- Built-in throttling for API-backed commands
- Transparent caching with `--no-cache` / `--refresh` overrides
- Auto-retry with backoff for transient failures
- `--dry-run` for destructive operations

### 5. Error Model

```json
{
  "error": {
    "code": "INVALID_DATE_FORMAT",
    "message": "Cannot parse '2025-13-01' as a date",
    "hint": "Use ISO 8601 format: YYYY-MM-DD",
    "retryable": false,
    "suggestion": "mytool search --date 2025-01-13"
  }
}
```

Categories: `user_error`, `transient`, `upstream`, `internal`

### 6. Composition Model
- IDs from output pass directly into next command
- Batch operations: `mytool inspect @1 @2 @3` or `mytool search --grid "a,b" "x,y"`
- Compare primitives: `mytool diff @1 @2`

### 7. Workflow Model
- discover → inspect → refine → export → resume
- Full lifecycle without leaving the CLI

## Intent-First Routing Examples

```
mytool ABC123          # identifier → inspect
mytool "search term"   # string → search
mytool file.json       # file → import/process
mytool @1 @2           # refs → compare
mytool                 # no args → interactive/status
```

## Self-Description Command

Every CLI should have a `guide` (or `prime`) command that returns:

```json
{
  "name": "mytool",
  "version": "1.0.0",
  "purpose": "One-sentence description",
  "commands": [],
  "workflows": [],
  "examples": [],
  "error_codes": [],
  "config": { "path": "~/.config/mytool/config.toml", "keys": [] }
}
```

## Input Normalization

Accept flexibly, emit strictly:
- Dates: `2025-01-13`, `jan 13 2025`, `13/01/2025` → always output ISO 8601
- IDs: case-insensitive input → canonical case output
- Amounts: `1000`, `1,000`, `1k` → normalized number

## Key Anti-Patterns

- Prose-only output with no structured option
- Opaque error messages ("Something went wrong")
- Requiring docs lookup to use basic features
- Agent must manage sleep/retry/cache externally
- No way to reference previous results
- N identical calls where one batch call suffices
