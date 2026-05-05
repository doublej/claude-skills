---
name: codex-generate-image
description: "Generate images via Codex CLI's built-in image_gen tool and return the local file path. Use when user wants to generate an image and get the result back into this Claude session. Triggers on '/codex-generate-image', 'generate an image with codex', 'codex image'. Requires codex CLI installed."
---

# codex-generate-image

Generate images using Codex's built-in `image_gen` tool. Unlike `codex-launch`, this captures the result back — the generated image path is returned to the current Claude session.

<usage>

```
/codex-generate-image <prompt>
```

Output lands in `CWD/tmp/` by default.

</usage>

<workflow>

1. Run the generate script:
   ```bash
   scripts/generate.sh "<prompt>" "<dest_dir>"
   ```
   - `prompt` — the image description (required)
   - `dest_dir` — output directory (default: `$(pwd)/tmp`)

2. Script runs `codex exec` non-interactively with the image prompt.

3. Script locates the generated image in `~/.codex/generated_images/`, copies it to dest, and prints `IMAGE_RESULT: <path>`.

4. Report the final path to the user. Use `Read` to display the image inline if desired.

</workflow>

<prompt_shaping>

Before passing the user's prompt to the script, augment it lightly:
- Add style/medium if not specified (e.g., "digital illustration", "photograph")
- Add "high quality, detailed" if the prompt is bare
- Keep augmentation minimal — don't invent content the user didn't ask for

</prompt_shaping>

<gpt_image_2_parameters>

Parameters accepted by gpt-image-2 (passed via prompt instructions to Codex):

| Parameter | Values | Notes |
|-----------|--------|-------|
| `prompt` | string (required) | Image description |
| `n` | 1–10 | Number of images to generate |
| `size` | `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`, or custom WxH | Max edge ≤ 3840px, both edges multiples of 16px, ratio ≤ 3:1, total pixels 655,360–8,294,400 |
| `quality` | `low`, `medium`, `high`, `auto` | `low` = fast drafts; `high` = final assets |
| `output_format` | `png`, `webp`, `jpeg` | PNG for transparency-ready; webp for smaller size |
| `output_compression` | 0–100 | Percentage, only for webp/jpeg |
| `moderation` | `auto`, `low` | Content filter strictness |

**Not supported on gpt-image-2:**
- `background` (transparent) — gpt-image-1.5 only
- `input_fidelity` — always high fidelity for image inputs

**Edit-specific parameters** (when modifying existing images):
- `image` — input image(s) to edit
- `mask` — mask for inpainting (white = edit area)

</gpt_image_2_parameters>

<error_handling>

- If `codex` is not installed: tell user to run `npm i -g @openai/codex`
- If image generation fails: surface the error from Codex output
- If image not found after exec: check `~/.codex/generated_images/` manually

</error_handling>
