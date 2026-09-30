# Current models and selection

Verified **2026-09-30**. This catalog separates documented API image models
from Codex session models. A published API model is not proof that Codex's
built-in image tool exposes a selector for it.

## Image models

| Model ID | Role and when to use | How to brief and operate |
| --- | --- | --- |
| `gpt-image-2.5-flare` | Small, speed-oriented model; fast everyday generation, drafts, variants, existing Image 2 workflows that already meet quality needs | State subject, composition, medium, exact text, references, and exclusions. Start with a representative brief; tune quality only after checking the result. Both generation and editing are supported. |
| `gpt-image-2.5-sunburst` | Base, quality-oriented model; demanding final assets, precise edits, complex reference preservation | Explicitly identify each reference's role and each edit invariant. Give difficult text, geometry, and edge requirements; inspect them after each edit. Test Flare against the same brief once Sunburst passes if latency matters. |
| `gpt-image-2` | Previous generation; keep for validated existing workflows or an explicit user choice | Shared briefing techniques apply. Flexible dimensions; automatic high input fidelity. Transparent output is now documented in preview; do not repeat the old “unsupported” claim. Test preview support in the chosen endpoint. |
| `gpt-image-1.5` | Previous image model; existing integrations, not the default for new work | Shared briefs; use `input_fidelity=high` for identity/label preservation when needed. Restricted size presets. Deprecated; shuts down **2026-12-01**. |
| `gpt-image-1` | Legacy generation/editing integrations | Clear briefs and masks where useful; high input fidelity can preserve references at higher input cost. Restricted sizes. Deprecated; shuts down **2026-10-23**. |
| `gpt-image-1-mini` | Legacy, lower-cost Image 1 variant for established draft workflows | Keep briefs focused; inspect exact text and identity carefully. Restricted sizes; verify fidelity support against its endpoint before setting it. Deprecated; shuts down **2026-12-01**. |
| `chatgpt-image-latest` | Alias for a previous ChatGPT image model, not a Codex agent model | Check the model page for the current alias target and endpoint support. Do not assume it tracks Image 2.5. Deprecated; shuts down **2026-12-01**. |

`dall-e-2` and `dall-e-3` shut down on **2026-05-12**; do not recommend them.
Pinned snapshots for reproducible 2.5 API evaluations are
`gpt-image-2.5-flare-2026-09-08` and `gpt-image-2.5-sunburst-2026-09-08`.
Model snapshots do not make sampling deterministic.

For new model-selectable workflows, start with Flare for speed or Sunburst for
demanding quality. Preserve an explicit user choice. Compare the same brief,
reference images, size, and supported explicit quality setting; measure actual
latency, accepted quality, failures, and cost. Equal quality labels and equal
token prices do not imply equal results or per-image costs.

## Codex session models

The installed **Codex CLI 0.159.2** account catalog was inspected on the same date.
The visible IDs below are an account snapshot, not universal entitlement.
Official model guidance documents the current family and rollout; the local
catalog supplies the precise visible IDs and supported efforts.

| Session model ID | Best use | Briefing guidance |
| --- | --- | --- |
| `gpt-6.1-sol` | Recommended workhorse when available; complex, repeated, long-running work at lower cost than Astra | Give the end-to-end goal, relevant files/references, constraints, and verifiable completion criteria. Let it choose routine steps. |
| `gpt-6-astra` | Hardest workflows needing sustained reasoning and judgment | Supply sources, tradeoffs, invariants, and acceptance checks; specify decisions it may make independently. Start with Light/`low`. |
| `gpt-6-sol` | Previous-generation workhorse; existing Sol workflows | Same complete task contract as 6.1 Sol. Compare results before changing a validated model configuration. |
| `gpt-6-luna` | Focused, repeatable, high-volume tasks; routine image-tool forwarding | Use a narrow goal, ordered inputs, explicit tool call requirements, and a precise output contract. Start with `high` per current model guidance. |
| `gpt-5.6-sol` | Older workhorse retained during rollout | Self-contained brief with outcome, scope, and checks. Prefer current Sol for new workflows when available. |
| `gpt-5.6-terra` | Older balanced model for straightforward tasks | Keep the task bounded; state permitted edits, exact inputs, and expected output. |
| `gpt-5.6-luna` | Older efficient model for clear tasks | Explicit inputs and output format; minimize ambiguity and unrelated context. |
| `gpt-5.5` | Legacy model still available at review time | Maintain only when deliberately selected; retires from ChatGPT-sign-in Codex **2026-10-14**. API retirement is separate. |

Current local effort values: `low`, `medium`, `high`, `xhigh`, `max`, `ultra` for
Sol/Astra/5.6 Terra; Luna models stop at `max`; 5.5 stops at `xhigh`.
Start with the session default unless task-specific guidance or the user says
otherwise. Increase effort for unresolved reasoning needs, not automatically
for a prettier image: session reasoning does not set renderer quality.
`ultra` can delegate to subagents; use only when delegation is authorized.

Hidden local catalog entries `gpt-reserve` and `codex-auto-review` are internal
reserve/approval-review roles, not ordinary user-selectable recommendations.
Retired/deprecated ChatGPT-sign-in Codex IDs include `gpt-5.3-codex-spark`
(retired 2026-09-14), `gpt-5.4`, `gpt-5.4-mini` (retired 2026-08-31),
`gpt-5.2`, and `gpt-5.3-codex`. API-key/provider catalogs differ. A gateway must
support Codex's Responses API, streaming, and tools; an arbitrary API model
listing or local-provider flag does not guarantee the image tool works.

## How to select and refresh

Use `/model` in an interactive Codex session, or `codex exec -m <session-id>`.
The image wrapper accepts `CODEX_MODEL` for this purpose. For a session override:

```bash
CODEX_MODEL=gpt-6.1-sol bash ~/.claude/skills/codex-image/scripts/generate.sh \
  "A small ceramic mug, studio product photograph." "$PWD/tmp"

# General captured task; pick effort supported by the selected session model.
bash ~/.claude/skills/codex-launch/scripts/run_monitored.sh "Codex task" \
  codex exec -C "$PWD" -s read-only -m gpt-6-luna \
  -c 'model_reasoning_effort="high"' --json -- "<self-contained task brief>"
```

Image-model selection is separate: use the Image API `model` field or the
Responses API image-generation tool's `model` field. Inspect the native tool
schema before promising a built-in model selector. If absent, report
“renderer not exposed” and use the authorized API route for an exact model.

For an update, fetch the official sources below, inspect `codex --version` and
`codex exec --help`, and check the current account's `/model` list. If reading
`$CODEX_HOME/models_cache.json`, extract only model IDs/descriptions/efforts;
the cache is internal, can be stale, and is not proof of successful access.
Do not override account/workspace restrictions or silently switch a requested model.

## Sources

- [Image prompting and model selection](https://developers.openai.com/api/docs/guides/image-prompting)
- [Image generation and endpoint controls](https://developers.openai.com/api/docs/guides/image-generation)
- [Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare) and [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)
- [API model catalog](https://developers.openai.com/api/docs/models) and [deprecations](https://developers.openai.com/api/docs/deprecations)
- [Codex models, rollout, effort, and retirements](https://learn.chatgpt.com/docs/models)
