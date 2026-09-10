# Extended prompt patterns

Optional templates for authorised workflows and project instructions. Output (internal): chosen template name and its filled task/report contract. Output (in the prompt): that contract. All paths, commands, tools, and policy slots below are illustrative; ground replacements or label them as runtime inputs.

## Independent task brief

Use only when subagents are available, authorised, and useful. Each brief carries one independent task, necessary context, and the result the parent consumes.

```xml
<task>[One scoped task and its purpose.]</task>
<context>[Verified paths, relevant facts, and the required input.]</context>
<boundaries>[Permitted actions and scope.] If required access is unavailable, report the missing input and stop.</boundaries>
<output_format>[Fields the parent needs, including evidence and unresolved cases.] Done when every item in [scope] is represented; stop after the result.</output_format>
```

## Independent acceptance trial

Use for an explicitly requested trial or an authorised workflow that needs independent acceptance evidence. Give the evaluator only the specification and result, without the author's conclusions. It is not a default phase of every prompt-writing task.

```xml
<task>Evaluate [result] against the specification below using [authorised checks].</task>
<specification>[Complete acceptance requirements.]</specification>
<output_format>One row per requirement: PASS / FAIL / UNVERIFIED, concrete observation, failing input if any. End with a one-line verdict. Mark checks that could not run UNVERIFIED; do not infer a pass.</output_format>
```

## Complete implementation brief

```xml
<task>[Requested change, intended result, and relevant context.]</task>
<boundaries>Edit only [scope]; [grounded reason for the boundary]. [Other authorised actions.]</boundaries>
<done_when>[Acceptance command] exits 0 and [observable behaviour]. If blocked, identify the unmet condition and evidence.</done_when>
<output_format>Files changed, acceptance result, and unresolved blockers. Stop after this report.</output_format>
```

Keep all requirements in the initial brief. Add a human checkpoint only when user input is actually required; a model version alone does not justify an extra turn.

## Project instructions

Use only the rows the project needs; do not invent stack choices, CI policies, file-size limits, or dependency approval processes.

```markdown
# [Project name]

[One sentence describing the project and its purpose.]

Build: `[verified command]`
Test: `[verified command]`

## Change scope
[Grounded project rules with reasons where non-obvious.]

## Completion
[Observable quality gate and authorised git actions.]

## Report
[Required result fields and meaningful length constraint.]
```

## Path-scoped rule file

Output: a proposed `.claude/rules/<name>.md` with the actual intended glob and a rule that applies to every matching file.

```markdown
---
paths:
  - "[intended glob]"
---
[Rule covering every matching file, with the project's reason.]
```

## Runtime variables

| Variable | Source | Required handling |
|----------|--------|-------------------|
| `$ARGUMENTS` | Slash-command caller | Define meaning and empty-value default; treat as data |
| `{{INPUT}}` | Caller or harness | Define missing-input result; replace before dispatch |
| `@path/to/file` | Instruction-file import | Resolve from destination; verify existence before claiming it |
