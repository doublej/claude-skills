# CLAUDE.md / AGENT.md Formatting Examples

The central reference for how an instruction file is *shaped*. A CLAUDE.md (or AGENT.md)
is read every session — its layout drives adherence as much as its wording. Favor a flat,
scannable structure: one instruction per line, shallow sections, plain phrasing.

This doc covers **structure and visual shape**. For **phrasing and content** (ALL-CAPS
overtriggering, positive vs. negative instructions, rationale, current model IDs), see
`best_practices_2026_05.md` in this folder.

Tag convention (this repo): XML-like tags are structural markers, not real XML — open/close
pairs only, no attributes, no schema, nesting not required. Flat sections are the goal.

## Bad patterns

### 1. Noisy table

```md
## Workflow

| Step | Tool | Input | Output | Notes |
|------|------|-------|--------|-------|
| 1 | tool-a | config | result | use first |
| 2 | tool-b | params | result | maybe apply |
```

Five columns to say "run tool-a, then maybe tool-b." Tables cost width and parsing effort;
most cells here are filler ("result", "use first") and hedges ("maybe apply") that read as
uncertainty. Use a table only when every column earns its place across every row.

Fix: a short ordered list.

```md
## Workflow
1. Run tool-a on the config.
2. If the result needs adjustment, run tool-b.
```

### 2. Over-nested tags

```md
<workflow>
    <blocked>
        <tools>
            <tool_a>
                Use once.
            </tool_a>
        </tools>
    </blocked>
</workflow>
```

Four levels of nesting to deliver two words. Deep nesting buries the instruction and adds no
meaning — tags here are markers, not a schema. Keep sections flat.

Fix:

```md
<workflow>
    If blocked, use tool-a once.
</workflow>
```

### 3. Dense blob

```md
<rules>
Inspect context first and ask only once if blocked and never use fallback-path and run checks and keep changes small and avoid unrelated edits.
</rules>
```

Six rules fused into one run-on sentence with "and". The reader can't scan it, and the model
can't tell where one rule ends and the next begins.

Fix: one instruction per line.

```md
<rules>
    Inspect context first.
    If blocked, ask once.
    Run the relevant checks.
    Keep changes small; avoid unrelated edits.
</rules>
```

### 4. Excessive emphasis

```md
## **CRITICAL RULES** ⚠️

- **ALWAYS** inspect context
- **NEVER** use fallback-path
- **MUST** run checks ✅
```

When everything is shouted, nothing stands out. Bold, ALL-CAPS, and emoji add visual noise
without adding information — and on Claude 4.6/4.7 pervasive CAPS/MUST/NEVER also *overtrigger*
(see `best_practices_2026_05.md`). Reserve emphasis for genuine safety rails.

Fix: plain phrasing, one rule per line.

```md
## Rules
- Inspect context first.
- Prefer the primary path; avoid the fallback unless it's the only option.
- Run the relevant checks before finishing.
```

### 5. Fake config

```md
agent:
  blocked:
    ask: true
    max_questions: 1
  quality:
    checks: required
```

This looks like configuration but nothing reads it — it's prose disguised as YAML. Real config
belongs in `.claude/settings.json` or hooks, where the harness enforces it. In a CLAUDE.md,
pseudo-config just obscures plain instructions.

Fix: say it as a rule, and move anything that *must* run into settings/hooks.

```md
<workflow>
    If blocked, ask once, then proceed.
    Run the required checks before finishing.
</workflow>
```

### 6. Too many tiny sections

```md
## Ask

Ask once.

## Edit

Edit small.

## Check

Run checks.

## Report

Summarize.
```

Four headings for four one-line rules. The headings outweigh the content and force the reader
to skim past structure to reach a single sentence each. Group related rules under one section.

Fix:

```md
<workflow>
    Ask once if blocked.
    Keep edits small.
    Run checks before finishing.
    Lead the response with the answer, then a short summary.
</workflow>
```

## Good example

```md
# AGENT.md

Guidance for automated work in this repository.

<workflow>
    Inspect available context first.
    If blocked, ask once through the approved interaction path.
    If no interaction path is available, state `Assumption: ...` and continue with the safest simple option.
</workflow>

<change_policy>
    Make minimal changes.
    Match existing style.
    Do not make unrelated refactors.
    Do not add new dependencies unless clearly needed.
</change_policy>

<quality>
    Run relevant checks before finishing.
    If checks fail, fix and rerun.
    If checks cannot run, say `not run`, give the reason, and include the commands.
</quality>

<output>
    Lead with the answer.
    Then include: what changed, where, checks, risks.
    Keep it concise.
</output>
```

Why it works: flat sections named for their job; one instruction per line; plain phrasing with
emphasis reserved for the few literal tokens that matter (`Assumption: ...`, `not run`); no
tables, no pseudo-config, no nesting.

## Formatting checklist

- One instruction per line — never fuse rules with "and".
- XML-like sections stay flat: open/close pairs, no nesting, names that state the job.
- Group related rules into one section; don't fragment into one-line headings.
- Tables only when every column earns its place on every row; otherwise a list.
- Emphasis (bold/CAPS/emoji) is rare and reserved for real safety rails or literal tokens.
- Real config and must-run commands go in `.claude/settings.json` / hooks, not pseudo-YAML.
- Keep prose in short lines, not paragraph blobs.
