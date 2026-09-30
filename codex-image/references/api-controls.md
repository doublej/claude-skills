# API controls and Codex tool boundaries

Verified **2026-09-30** against the official
[image generation guide](https://developers.openai.com/api/docs/guides/image-generation),
[prompting guide](https://developers.openai.com/api/docs/guides/image-prompting),
and [Images API reference](https://developers.openai.com/api/reference/resources/images).
These are API fields, not flags supported by `generate.sh` or implied native
tool arguments. Inspect the actual schema of the chosen surface.

## Models and parameters

| Control | Image 2.5 Flare / Sunburst | Image 2 | Image 1 / 1.5 |
| --- | --- | --- | --- |
| `model` | Exact image ID or documented snapshot | `gpt-image-2` or snapshot | Exact legacy model ID |
| `quality` | `auto`, `low`, `medium`, `high`, `xhigh`, `max` | `auto`, `low`, `medium`, `high` | `auto`, `low`, `medium`, `high` |
| `size` | `auto` or valid `WIDTHxHEIGHT` | Same flexible constraints | `auto`, `1024x1024`, `1536x1024`, `1024x1536` |
| `background` | `auto`, `opaque`, `transparent` | Transparency documented in preview | Transparency supported |
| `input_fidelity` | Do not inherit legacy settings; check current endpoint schema | Omit; always high | `low`/`high` where supported |
| `output_format` | `png`, `jpeg`, `webp` | Same | Same |
| `output_compression` | 0–100, JPEG/WebP only | Same | Same |

Use `n` on the Image API for variations of **one prompt**; distinct assets need
distinct prompts. Check the endpoint's documented range (currently 1–10 for
GPT Image). Responses tool calls have a different schema. `moderation` may be
`auto` or `low` on supported endpoints; leave defaults unless the task requires
a supported change. It does not disable safety rules.

Flexible size constraints for Image 2/2.5:

- Each edge at most **3840 pixels**, each divisible by **16**.
- Long-to-short edge ratio at most **3:1**.
- Total pixels between **655,360** and **8,294,400**.
- Above **3,686,400** pixels (`2560x1440`) is experimental.

Common choices: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`,
`2048x1152`, `3840x2160`, `2160x3840`. A panoramic request wider than 3:1
needs an agreed alternate composition or an explicit later crop; do not
invent unsupported dimensions. Verify the returned image's size.

Choose the model first. Use `low` for drafts; compare `medium`/`high` for final
assets and small text. Test `xhigh`/`max` only for an unmet quality requirement
within the latency budget. Do not confuse these renderer settings with the
Codex agent's reasoning effort. Higher quality is not always a better result.

## Editing and transparency

Use the edits endpoint for edits. Supply image inputs in stable order and label
each reference's purpose in the prompt. Check count/format/50 MB limits in the
chosen endpoint. A mask applies to the **first** input image. Its transparent
alpha areas mark where editing is allowed; “white = edit” is incorrect without
an explicit mask-conversion convention. Image and mask must match format and
dimensions and the mask needs an alpha channel. Masks guide the model; they
do not guarantee pixel-exact preservation outside the region.

For transparent assets, set `background="transparent"` and use PNG or WebP.
Inspect actual alpha and fine edges, hair, glass, and shadows. A checkerboard
painted into RGB is not transparency. Preserve returned alpha; JPEG cannot.
Image 2 transparency is preview; 2.5 supports it without the legacy downgrade.

When pixel-identical preservation is required, prompting alone is insufficient.
Use a user-authorized compositing workflow and validate the unchanged region.

## Select an exact model

The Image API is simplest for one-shot generation/editing. This is illustrative
API code, not an instruction to switch an ordinary native-tool request to API:

```python
import base64
from pathlib import Path
from openai import OpenAI

result = OpenAI().images.generate(
    model="gpt-image-2.5-flare",
    prompt="A centered ceramic mug, soft daylight, no text.",
    size="1536x1024",
    quality="medium",
    background="transparent",
    output_format="png",
    n=1,
)
Path("mug.png").write_bytes(base64.b64decode(result.data[0].b64_json))
```

For Sunburst use `model="gpt-image-2.5-sunburst"` with the same baseline settings.
For an edit use `images.edit(image=[...], prompt=..., model=...)` and optional
`mask`; quote exact text and repeat preservation constraints.

In Responses, the top-level model is a supported reasoning model; the image
model goes in the tool configuration:

```python
response = OpenAI().responses.create(
    model="gpt-6.1-sol",
    input="Create a centered ceramic mug product photograph.",
    tools=[{"type": "image_generation", "model": "gpt-image-2.5-flare"}],
    tool_choice={"type": "image_generation"},
)
```

Decode the `result` of `image_generation_call` output items. Retain the call ID
or response ID for iterative edits; inspect any `revised_prompt`. Check the
chosen top-level model's image-tool support rather than assuming all providers
or session models can call it. Tool `action` supports `auto`, `generate`, `edit`
where documented; an image attachment by itself does not specify edit intent.

## Existing bundled fallback CLI

Codex's system imagegen skill has `scripts/image_gen.py`; inspect its `--help`
and validation before using a new model or quality value. The installed copy
at review time still describes Image 2 as default and has stale transparency
guidance. Do not claim it supports 2.5/`xhigh`/`max` without checking its code.
Do not patch vendor skills or bypass their explicit CLI opt-in requirement.
For a user-requested API integration, use the supported SDK/API schema above.

API calls require `OPENAI_API_KEY`, network access, and model entitlement;
organization verification may be required. Codex built-in generation uses its
own authentication and does not require asking for an API key. Never print keys.
Verify current [pricing](https://developers.openai.com/api/docs/pricing) if cost
is part of the request; do not infer per-image cost from a quality label.
