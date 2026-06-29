---
name: codex-image
description: "Generate images via Codex CLI's built-in image_gen tool and return the local file path. Use when user wants to generate an image and get the result back into this Claude session. Triggers on '/codex-image', 'generate an image with codex', 'codex image'. Requires codex CLI installed."
---

# codex-generate-image

Generate images using Codex's built-in `image_gen` tool. Unlike `codex-launch`, this captures the result back — the generated image path is returned to the current Claude session.

<usage>

```
/codex-image <prompt>
```

Output lands in `CWD/tmp/` by default.

</usage>

<workflow>

1. Run the generate script:
   ```bash
   scripts/generate.sh "<prompt>" "<dest_dir>" "<input_image>"
   ```
   - `prompt` — the image description (required)
   - `dest_dir` — output directory (default: `$(pwd)/tmp`)
   - `input_image` — optional. Omit for **generate** mode (text→image). Pass a path for **edit** mode (image→image): the script forwards it to Codex via `codex exec -i`.

2. Script runs `codex exec` non-interactively with the image prompt.

3. Script locates the generated image in `~/.codex/generated_images/`, copies it to dest, and prints `IMAGE_RESULT: <path>`.

4. Report the final path to the user. Use `Read` to display the image inline if desired.

</workflow>

<batch_usage>

**Multi-image jobs must run sequentially — never in parallel.**

When `codex exec` doesn't echo the `IMAGE_PATH:` line, the script falls back to picking the most-recently-modified file in `~/.codex/generated_images/`. That fallback is process-global, so two concurrent invocations can cross-wire and copy each other's output. For a batch of N images, loop one call at a time:

```bash
for prompt in "${prompts[@]}"; do
  scripts/generate.sh "$prompt" "$dest"
done
```

Do not background the calls or fan them out across subagents.

</batch_usage>

<prompt_mode>

Before generating, determine how the user wants their prompt handled. Use `consult-user-mcp ask` with a pick dialog:

```
title: "Prompt mode"
body: "How should I handle your prompt?"
type: pick
choices:
  - "Raw — pass my prompt exactly as-is to Codex"
  - "Polish — light cleanup, add style/medium if missing"
  - "Director — full rewrite into an optimal gpt-image-2 prompt using project context"
descriptions:
  - "No interpretation. Your words, verbatim."
  - "Minor augmentation: style, quality, constraints. No invented content."
  - "I'll study the project (colors, brand, assets, purpose), then craft a detailed structured prompt. You review before I generate."
```

### Raw mode

Pass the user's prompt string directly to the script unchanged. No augmentation, no rewrites.

### Polish mode

Light-touch augmentation:
- Add style/medium if not specified (e.g., "digital illustration", "photograph")
- Add "high quality, detailed" if the prompt is bare
- Append "no watermark, no text" unless text was explicitly requested
- Keep augmentation minimal — don't invent content the user didn't ask for

### Director mode

Full prompt engineering pass. Before writing the prompt:

1. **Gather project context** — scan for: brand colors (CSS variables, design tokens, tailwind config), existing assets/logos, README/package.json for project purpose, any style guides or design system files.

2. **Craft a structured prompt** using the gpt-image-2 schema:
   ```
   Use case: <taxonomy slug from list below>
   Asset type: <where this image will be used>
   Primary request: <user's core intent, expanded>
   Scene/backdrop: <environment>
   Subject: <main subject with specifics>
   Style/medium: <photo/illustration/3D/vector-style/etc>
   Composition/framing: <layout, camera angle, spacing>
   Lighting/mood: <lighting + atmosphere>
   Color palette: <derived from project or user request>
   Constraints: <must-haves>
   Avoid: <negative constraints>
   ```

3. **Show the crafted prompt** to the user via `consult-user-mcp ask` (type: confirm) before generating. Let them approve or request changes.

Use-case taxonomy slugs: `photorealistic-natural`, `product-mockup`, `ui-mockup`, `infographic-diagram`, `logo-brand`, `illustration-story`, `stylized-concept`, `ads-marketing`, `scientific-educational`, `productivity-visual`, `historical-scene`.

</prompt_mode>

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
- `image` — input image(s) to edit. Pass via the script's third arg, which forwards it as `codex exec -i` (see workflow step 1).
- `mask` — mask for inpainting (white = edit area)

</gpt_image_2_parameters>

<error_handling>

- If `codex` is not installed: tell user to run `npm i -g @openai/codex`
- If image generation fails: surface the error from Codex output
- If image not found after exec: check `~/.codex/generated_images/` manually

</error_handling>
