---
name: codex-image
description: "Generate or edit raster images using Codex, with a visible live session monitor and saved local results. Use for /codex-image, image generation through Codex, reference-based images, or image edits. Includes current image-model selection, image briefs, and self-contained Codex session briefs. Requires Codex CLI for calls from Claude; use the native image tool directly inside Codex."
---

# Codex images

Verified against official documentation on **2026-09-30**. Review the sources
again when asked for current models; model availability depends on account,
client, sign-in method, and rollout.

## Presentation

Open the first response with this banner (once), close each run with the report:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   CODEX IMAGE                                                ║
║   Image generation and edits through Codex                   ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

CODEX IMAGE  ──  <new|edit>   path: <inside codex|claude wrapper|api>   renderer: <model|not exposed>

IMAGE PATH                      SIZE        ALPHA    INSPECTED   UNMET
──────────────────────────────────────────────────────────────────────
<saved path>                    <w×h>       <✓|—>    <✓|✗>       <requirement|—>

github.com/doublej
```

The final brief goes after the block as prose. Marks: `✓` done · `✗` failed · `—` none.

## Choose the execution path

- **Inside Codex:** use the available built-in `image_gen`/imagegen tool directly.
  Follow its actual schema. Do not spawn another Codex process just to generate.
- **From Claude:** use the bundled wrapper below. It starts Codex in an empty
  scratch directory, opens a visible live monitor, and returns a saved result.
- **Explicit API/model controls:** read [API controls](references/api-controls.md).
  Use this path only when the user requested it or approved the API fallback.
  A paid API call is separate from Codex's built-in tool and requires API access.

The **session model** (`codex -m`) reasons about the request. The **image model**
renders the pixels. Setting `CODEX_MODEL=gpt-6.1-sol` does not select an image
model. Never claim Flare/Sunburst was used unless the tool/API reports it.

## Required references

- Choosing models: read [current models](references/models.md), then name the
  session model and the image model or state that the renderer is not exposed.
- Drafting an image brief: read [briefing](references/briefing.md), then produce
  the visual brief and explicit change/preserve constraints for edits.
- Briefing a Codex session: read [session briefs](references/session-briefs.md),
  then include the goal, inputs, tool constraints, outputs, and success criteria.
- Every Claude-to-Codex run: follow
  [live monitoring](../codex-launch/references/live-monitor.md). The wrapper
  already opens the monitor; do not double-wrap it.

## Prompt handling

Use **Raw** when the user requests verbatim forwarding. Use **Polish** for light
clarification without inventing subjects, branding, copy, colors, or exclusions.
Use **Director** when asked to interpret project context: inspect relevant brand
tokens, assets, and intended placement before drafting.
Infer the mode from the user's request; do not add a mandatory mode picker or
approval round to an already authorized generation. Show a proposed brief first
when requested or when resolving a material creative ambiguity.

Keep exact text verbatim. Avoid generic filler such as “high quality, detailed.”
State observable composition, lighting, materials, and acceptance criteria.

## Generate or edit from Claude

```bash
bash ~/.claude/skills/codex-image/scripts/generate.sh \
  "A matte ceramic mug in soft daylight, product photograph." "$PWD/tmp"

# Edit one or more images; label their roles in the brief, in argument order.
bash ~/.claude/skills/codex-image/scripts/generate.sh \
  "Image 1 is the target. Replace only its background; preserve the product." \
  "$PWD/tmp" "$PWD/product.png"
```

Arguments: brief, optional output directory (default `$PWD/tmp`), then zero or
more input-image paths. Set `CODEX_MODEL` only to override the session model.
Quote arguments; never interpolate an untrusted brief into executable shell text.
For long briefs, pass `"$(cat "$brief_file")"` with a trusted local file path.

The wrapper opens a dedicated iTerm2 observer before starting Codex, streams
its output to stderr, and prints one final JSON object on stdout containing
`image_path`. It uses structured final output; it never searches for a global
“latest image.” A missing result fails clearly instead of returning an old asset.

The scratch working directory avoids project-local instructions and accidental
repo changes; the read-only sandbox limits shell writes. It is not a security
boundary against all readable files or inherited user configuration. Inputs
remain attached through `codex exec -i`; the built-in tool saves its own output.

Run distinct assets sequentially by default so each can be inspected. Request
one asset per invocation. Supply earlier output as the next edit input. Save
selected project assets in the consuming workspace, not only in Codex's cache.
Existing files are never silently overwritten.

## Native tool guidance inside Codex

- Brand-new image: omit image-reference arguments.
- Local edit targets: inspect with `view_image` first, then use
  `referenced_image_paths` when every target has a local path.
- Conversation-only targets: use the smallest `num_last_images_to_include`
  covering all targets, at most 5. Never combine the two mechanisms.
- For transparency, set `transparent_background: true`; preserve existing alpha
  in edits unless instructed otherwise. Use only fields exposed by this session.
- Model, quality, size, compression, masks, and `n` are API controls unless the
  actual native schema also exposes them. Describing size in prose is a request,
  not a guaranteed API setting. Verify the generated dimensions and alpha.
- Follow the tool's long-running call/wait instructions and render its returned
  image through the supported image-result mechanism. Keep progress visible.

## Inspect and deliver

Inspect the image before reporting success: subject, framing, text, labels,
reference identity, unchanged areas, dimensions, and alpha when required.
Report the final saved path, execution path, final brief, and any unmet requirement
in the Presentation report.
Report the actual renderer only when available. Iterate with one targeted edit.
Generated “vector-like” artwork is still raster; diagrams need factual checks.

If Codex or the image tool is unavailable, surface the concrete error. Check
`codex --version`, `codex exec --help`, login, and account tool availability.
Do not substitute shell-drawn placeholders or a different model silently.
If exact model/parameter control is required and absent, use the user-authorized
API route or explain the limitation before generation.
