# Preset authoring — YAML schema and where to drop files

## Where presets live

- **Bundled** (this skill's defaults): `~/.claude/skills/teams/presets/<name>.yaml`
- **User overrides**: `~/.claude/team-presets/<name>.yaml`

On name collision the user override wins. `scripts/list-presets.sh` shows both sources and flags overrides. `scripts/spawn.py` resolves user first.

## Schema (authoritative)

See `presets/_schema.yaml` for the reference. Fields:

```yaml
name: string                          # must match filename (sans .yaml)
description: string                   # one-liner for /teams:list
default_team_name_prefix: string      # joined with ISO date for uniqueness
write_access: bool                    # true → spawn.py forces isolation=worktree on every member
forbid_main_branch: bool              # extra guard on top of preflight's default

lead_behavior: string                 # free-text: what the lead does post-spawn. Kept concise.

escalation:
  on_conflict: "consult-user-mcp"     # always this; field is future-proofing
  on_idle_stall_turns: int            # e.g. 3 — lead nudges, then escalates to user

members:                              # 1+ teammate specs
  - name: string                      # SendMessage address; also worktree branch suffix
    subagent_type: string             # one of: minimal-worker, read-only-reviewer,
                                      # write-implementer, adversarial-critic,
                                      # or any installed subagent
    model: string                     # claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5
    mode: string                      # plan | default | acceptEdits | dontAsk
    tools: [string]                   # additive to subagent_type's base tools; e.g. ["WebFetch"]
    isolation: "worktree" | "none"    # required "worktree" if write_access: true
    spawn_prompt: |                   # ≤10 lines; spawn.py may template-inject {team_name}
      Role: ...
      Goal: ...
      Stop condition: ...
    shutdown_on: idle | task_done | explicit

coordination:
  broadcast_rounds: int               # 0 = no forced broadcast phase
  task_dependency_chain: [string]     # ordered list of task-template ids lead creates upfront

hooks:
  teammate_idle: enforce_verdict | enforce_severity | none
  task_completed: require_clean_worktree | none
```

## Validation rules (enforced by spawn.py)

1. `name` matches filename.
2. `members` is non-empty; each name is unique within the preset.
3. If `write_access: true`: every member has `isolation: "worktree"` and a writable tool (Edit, Write, or NotebookEdit) in the effective allowlist.
4. If `write_access: false`: every member has `mode: "plan"` OR a read-only tool allowlist.
5. `model` is one of the accepted literals.
6. `coordination.task_dependency_chain` entries, if present, reference tasks the preset expects the lead to create — the preset's docs/lead_behavior should name them.

## Tips for a good preset

- **Name roles functionally, not by model.** `risk-auditor` not `opus-1`.
- **Keep spawn_prompt focused on the deliverable.** Everything else is handled by lead_behavior.
- **Pick the cheapest model that does the job.** Haiku for scribes, Sonnet for workers, Opus for judgment.
- **Read-only presets should stay read-only.** If you find yourself adding Edit to a reviewer, you probably want a different preset.
- **Coordinate via the shared task list, not SendMessage.** SendMessage is for prompts; tasks are for work units.

## Worked example — minimum viable preset

```yaml
# ~/.claude/team-presets/rubric-review.yaml
name: rubric-review
description: Review output against a user-supplied rubric. 2 graders + tiebreaker.
default_team_name_prefix: rubric-review
write_access: false
forbid_main_branch: false

lead_behavior: |
  Broadcast the artifact + rubric to grader-a and grader-b.
  Wait for verdicts. If they disagree, ask tiebreaker.
  Synthesize into a single report with score breakdown.

escalation:
  on_conflict: consult-user-mcp
  on_idle_stall_turns: 2

members:
  - name: grader-a
    subagent_type: read-only-reviewer
    model: claude-sonnet-4-6
    mode: plan
    tools: []
    isolation: none
    spawn_prompt: |
      Role: grader-a for {team_name}.
      Goal: score artifact against rubric; produce verdict + per-criterion notes.
      Stop: after posting verdict.
      Do NOT invoke skills or memory unless asked.
    shutdown_on: task_done

  - name: grader-b
    subagent_type: read-only-reviewer
    model: claude-sonnet-4-6
    mode: plan
    tools: []
    isolation: none
    spawn_prompt: |
      Role: grader-b for {team_name}. Independent second opinion.
      Goal: score artifact against rubric; produce verdict + notes.
      Stop: after posting verdict.
      Do NOT invoke skills or memory unless asked.
    shutdown_on: task_done

  - name: tiebreaker
    subagent_type: adversarial-critic
    model: claude-opus-4-7
    mode: plan
    tools: []
    isolation: none
    spawn_prompt: |
      Role: tiebreaker for {team_name}.
      Goal: resolve disagreements between graders with a reasoned verdict.
      Stop: after posting verdict. Skip silently if graders already agree.
      Do NOT invoke skills or memory unless asked.
    shutdown_on: task_done

coordination:
  broadcast_rounds: 0
  task_dependency_chain: []

hooks:
  teammate_idle: enforce_verdict
  task_completed: none
```

Drop this at `~/.claude/team-presets/rubric-review.yaml`, run `/teams:list` — it should appear alongside bundled presets, marked as `(user)`.

## Updating a bundled preset without forking

The override mechanism lets you patch a bundled preset by copying it to `~/.claude/team-presets/` and editing. Your edit wins on name collision. Easy path for one-off tuning.
