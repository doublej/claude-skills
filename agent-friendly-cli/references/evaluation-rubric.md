# Agent-Friendly CLI Evaluation Rubric

Score each category 0-2: 0=missing, 1=partial, 2=complete.

## Checklist

### Self-Description (0-2)
- [ ] Machine-readable guide/help command exists
- [ ] Returns capabilities, examples, error codes in structured format
- [ ] Agent can bootstrap without external docs

### Intent Routing (0-2)
- [ ] Common actions work without memorizing subcommand trees
- [ ] Argument shape implies intent (ID → inspect, string → search)
- [ ] Explicit subcommands available as escape hatches

### Structured Output (0-2)
- [ ] JSON/JSONL output available for all commands
- [ ] Field projection supported (`--fields`)
- [ ] Stable schemas across versions
- [ ] Verbosity tiers (brief/standard/full)

### Error Model (0-2)
- [ ] Errors return structured JSON with code, message, hint
- [ ] Errors indicate retryability
- [ ] Suggestions for correction included
- [ ] Categories distinguish user/transient/upstream/internal

### State & References (0-2)
- [ ] Results include stable IDs
- [ ] IDs from output can be passed to subsequent commands
- [ ] Config file for persistent defaults
- [ ] Ephemeral references for recent context (@1, @last)

### Infrastructure Shielding (0-2)
- [ ] Built-in rate limiting/throttling
- [ ] Transparent caching with override flags
- [ ] Auto-retry for transient failures
- [ ] Session management handled internally

### Batch Operations (0-2)
- [ ] Multi-item inspect/query in single call
- [ ] Search grid / matrix operations
- [ ] Compare/diff primitives
- [ ] Bulk export

### Workflow Completeness (0-2)
- [ ] discover → inspect → refine → export lifecycle
- [ ] No external tool needed for common workflows
- [ ] Resume/continue support for long operations

## Scoring

| Score | Rating |
|-------|--------|
| 0-4   | Poor — agent will struggle significantly |
| 5-8   | Basic — usable but with friction |
| 9-12  | Good — most agent workflows supported |
| 13-16 | Excellent — fully agent-native |

## Priority Order for Improvements

1. Structured output (biggest immediate impact)
2. Error model (reduces repair loops)
3. Self-description (reduces bootstrapping cost)
4. Batch operations (reduces token waste)
5. State/references (enables composition)
6. Intent routing (reduces memorization)
7. Infrastructure shielding (reduces boilerplate)
8. Workflow completeness (enables autonomy)
