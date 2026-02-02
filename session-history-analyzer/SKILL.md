---
name: session-history-analyzer
description: "Analyze Claude Code session history for the CURRENT PROJECT to create summarized timelines. Use when (1) User asks to analyze their session history, (2) User wants a summary of what they worked on, (3) User needs clarified/rewritten prompts, (4) User wants to review their conversation timeline. Triggers on 'analyze session', 'summarize history', 'what did I work on', 'session timeline'."
---

# Session Analyzer

## Initialization

Display boot sequence:

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   SESSION ANALYZER v2.0                                          ║
║   Claude Code Project History Analysis                           ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   [LOAD] Project session scanner                                 ║
║   [LOAD] Message extraction engine                               ║
║   [LOAD] Haiku 4.5 subagent pool                                 ║
║   [LOAD] Timeline synthesis module                               ║
║                                                                  ║
║   System ready.                                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Phase 1: SCAN

Scan current project's history:

```bash
python3 {SKILL_DIR}/scripts/extract_session.py scan
```

Displays project-specific stats. Parse JSON output and present:

```
[SCAN] Project: <name>

   Sessions:        <N>
   User messages:   <N>
   Date range:      YYYY-MM-DD to YYYY-MM-DD
   Est. tokens:     <N>
```

Then ask how many recent messages to analyze:

```
How many recent messages would you like to analyze?
- 25 messages (~8K tokens)
- 50 messages (~16K tokens)
- All <N> messages (~<X>K tokens)
```

---

## Phase 2: EXTRACT

Extract the requested number of messages:

```bash
python3 {SKILL_DIR}/scripts/extract_session.py extract -n <limit> -o .history-analysis
```

Report:
```
[EXTRACT] Extracting <N> most recent user messages...
[EXTRACT] Messages: <N> | Tokens: ~<N> | Range: <date> to <date>
[EXTRACT] Output: .history-analysis/
```

Creates:
- `message_index.json` - References to source files (uuid, source_file, source_line)
- `user_messages.json` - Full message content for analysis

---

## Phase 3: ANALYZE (parallel)

Launch two Haiku subagents in parallel using Task tool with `model: haiku`:

```
[ANALYZE] Spawning Worker A: Message Categorizer
[ANALYZE] Spawning Worker B: Context Resolver
```

**Worker A - Message Categorizer**:
```
Read .history-analysis/user_messages.json. Categorize each message:
- TASK: Direct work requests ("create", "build", "fix", "add")
- QUESTION: Information queries ("how", "what", "where", "why")
- CORRECTION: Fixes/adjustments ("no", "wrong", "instead", "actually")
- FEEDBACK: Reactions ("good", "thanks", "perfect", interrupts)
- META: Commands, model switches, configuration

Write .history-analysis/categorized_messages.json:
[{timestamp, project, category, original, one_line_summary}]
```

**Worker B - Context Resolver**:
```
Read .history-analysis/user_messages.json. For messages with unresolved
references ("that", "it", "the thing", "this", "above"), infer what they
refer to based on timestamp proximity and project context.

Write .history-analysis/resolved_context.json:
[{uuid, timestamp, original, inferred_context, clarified_prompt}]
```

When complete:
```
[ANALYZE] Worker A: <N> messages categorized
[ANALYZE] Worker B: <N> references resolved
```

---

## Phase 4: SYNTHESIZE

Launch synthesizer subagent (haiku):

```
[SYNTHESIZE] Generating unified timeline...
```

**Worker C - Timeline Synthesizer**:
```
Read .history-analysis/categorized_messages.json
Read .history-analysis/resolved_context.json

Create .history-analysis/timeline_summary.md:

# Project Timeline: <project_name>
Period: <start_date> to <end_date>
Messages analyzed: <N>

## Executive Summary
2-3 sentences: main themes, accomplishments, patterns.

## Chronological Timeline
| Date | Original | Clarified | Category |
|------|----------|-----------|----------|
Key requests with clarified versions.

## Communication Patterns
- Common request types
- Prompting style observations
- Areas where context was often missing

## Suggested Prompt Improvements
Rewritten versions of ambiguous prompts.
```

---

## Phase 5: PRESENT

```
╔══════════════════════════════════════════════════════════════════╗
║   ANALYSIS COMPLETE                                              ║
╚══════════════════════════════════════════════════════════════════╝
```

Read and display `.history-analysis/timeline_summary.md`.

---

## Technical Reference

**Data storage:** `~/.claude/projects/<encoded-path>/<uuid>.jsonl`
- Scans only current project sessions
- Messages indexed with source_file + source_line references

**Filtered noise:**
- `<local-command-stdout>` - CLI output
- `<command-name>/*` - Slash commands
- `<system-reminder>` - System injections
- `[Request interrupted` - Interrupts
