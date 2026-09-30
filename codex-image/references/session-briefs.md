# Brief the Codex session

Codex sees only its own prompt, attached inputs, and accessible instructions.
The image brief tells the renderer what to draw. The session brief tells Codex
which tool to use, what inputs matter, what it may change, and how to deliver.

## Claude-to-Codex contract

Prepare a self-contained brief with:

- Goal and intended use; final visual brief, with exact user copy.
- Inputs in stable order, each with a role; include actual attachments.
- Execution path: native image tool, or an explicitly authorized API path.
- Desired model/settings plus a truthful limitation if the native schema cannot
  select them. Session `-m` is not the image renderer's model.
- Boundaries: allowed files/actions, preservation constraints, no unrelated
  changes, no silent fallback, iteration budget if one was supplied.
- Outputs and pass criteria: final asset path, inspection, what to report when
  blocked, and any requested structured result.

From Claude, open the actual session's live monitor using
[the shared workflow](../../codex-launch/references/live-monitor.md). This is
Claude's launch responsibility, not a request for Codex to run another monitor.
Give JJ the observer/log and session ID when exposed.

## Native session template

```text
Goal: Generate one raster homepage hero for the ceramics workshop.
Use the built-in image generation tool available in this session.
Do not substitute SVG, HTML, shell drawing, or an API call.

Visual brief:
<paste the final visual brief, including exact text and reference roles>

Inputs: <list attached images in order, or "none">
Requested output: wide composition, suitable for the stated hero placement.
Use genuine transparency only if required; preserve existing alpha on edits.
Inspect local edit targets with view_image before invoking the image tool.
Follow the actual image-tool schema for references and long-running waits.
If a requested model or setting is unavailable, report that limitation;
do not claim the setting was applied or silently switch execution paths.

Inspect the result against <concrete pass criteria>.
Save the selected final asset to <requested project destination> without
overwriting an existing file unless replacement was requested.
Report the final path, final visual brief, execution path, actual renderer
when exposed, and any requirement that could not be met.
```

When using `generate.sh`, the wrapper supplies scratch/read-only boundaries,
structured result output, and image copying. Pass the **visual brief** as its
first argument; do not contradict its output contract by asking for Markdown.

## Precise edit template

```text
Goal: Edit the attached product photo; return one raster asset.
Image 1 is the edit target. Image 2 supplies backdrop texture only.
Use the built-in image tool. Change only the backdrop as described below.
Preserve product geometry, label text, crop, lighting, and edge detail.
<paste the exact visual brief>
Inspect before and after. If an invariant cannot be maintained, report it.
No API fallback or substitute drawing. Do not overwrite the original.
Return the saved asset and the result of each acceptance check.
```

For follow-ups, attach the last accepted output and repeat the invariants.
“Same as Claude discussed” is insufficient: include the actual requirements.

## Exact image model / authorized API template

```text
Goal: Use the OpenAI Image API for one approved image generation.
Image model: gpt-image-2.5-sunburst.
Parameters: size=1536x1024, quality=high, output_format=png, n=1.
<paste the exact visual brief>
Use the existing approved API environment and current SDK schema.
Do not print API credentials. Do not substitute another model or endpoint.
Write <new asset path>, preserve returned bytes/alpha, inspect the pass criteria,
and report actual model, settings, saved path, and any unmet requirement.
If credentials, entitlement, or a required parameter are unavailable, report
the error and stop the dependent operation.
```

Choose Flare instead when speed is the agreed priority; start from the same
supported baseline quality/inputs when comparing. The API example is a brief,
not implicit permission to incur API usage for ordinary native requests.

## Session model adjustments

Use [models](models.md) for available session IDs and supported effort values.
For Luna, use a narrow, explicit contract. For Sol/Astra, provide outcomes,
sources, tradeoffs, and checks while leaving routine execution choices open.
Keep reasoning effort at the default unless the user requests it or the task
demonstrates a need. Renderer quality is a separate control.

For general coding handoffs, use the same structure: goal, verified working
directory, grounded inputs, permitted edits, constraints, checks, and output.
Use current flags from `codex --help`; `-q`, `-a suggest`, `-a auto-edit`, and
`-a full-auto` are obsolete. Sandbox and approval policy are separate controls.
