# Brief the image model

Use the shared techniques in OpenAI's
[image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting),
verified **2026-09-30**. Labeled sections are useful scaffolding, not a special
model schema. A short paragraph is enough for a simple request.

## Build a visual brief

```text
Purpose: <where used, audience, what the image should communicate>
Subject and action: <visible subject, count, pose, gaze, interaction>
Scene: <setting and relevant surrounding objects>
Medium: <photograph, illustration, 3D render, raster logo exploration>
Composition: <framing, relative scale, placement, camera angle, negative space>
Light and materials: <direction, softness, surface texture, color behavior>
Palette: <specified colors or grounded project tokens>
Text, verbatim: "<exact copy>"; <position, typography, occurrence count>
References: <Image 1: target/subject; Image 2: style; Image 3: background>
Change: <for edits, the only intended changes>
Preserve: <identity, shape, label, crop, layout, lighting, other invariants>
Exclude: <only relevant unwanted details>
Pass criteria: <observable requirements to inspect>
```

Omit irrelevant sections. Never invent a brand, slogan, character, object, or
palette. If project context supplies one, include the concrete value in the
brief sent to Codex; it cannot infer Claude's unread conversation or files.

Keep model/quality/size/mask/output settings in a separate execution contract.
On a native tool without those fields, describe the desired visual dimensions
and verify the output rather than promising precise API control.

## Model-specific choices

- **Flare:** start with a clean, focused brief for fast iterations. Establish
  acceptable quality before optimizing latency. Use exact text and edit
  invariants just as with Sunburst; speed does not remove those requirements.
- **Sunburst:** start here for difficult edits or when Image 2/Flare fails an
  important quality requirement. Explicitly state reference roles, product
  geometry, facial identity, small text, and permitted changes. Use higher
  supported quality only when inspection demonstrates a need.
- **Image 2:** shared briefs apply; preserve validated baseline settings when
  comparing 2.5. Omit `input_fidelity`; high fidelity is automatic.
- **Image 1/1.5/mini:** shared briefs still apply. Use supported legacy size and
  fidelity controls from [API controls](api-controls.md), and plan migration
  before the shutdown dates in [models](models.md).

## Ready-to-adapt examples

### Photograph / website hero

```text
Purpose: homepage hero for a ceramics workshop.
Subject: one handmade cream ceramic mug on an oak workbench.
Medium: real product photograph; visible glaze texture and wood grain.
Composition: wide, eye-level, mug in the right third; calm negative space on
the left for separately rendered HTML copy. Entire handle visible.
Light: soft window daylight from the left; restrained, natural shadows.
Exclude: text, logos, extra mugs, heavy retouching.
Pass criteria: clear silhouette, natural material texture, usable copy space.
```

“Shot with a 50 mm lens” is an appearance cue, not a physical guarantee.
For people, specify full-body vs close-up framing, visible feet where needed,
gaze, and natural interaction with objects. Inspect hands and proportions.

### Exact copy / campaign

```text
Purpose: portrait campaign image for the supplied Thread brand brief.
Scene: a group of friends in a candid contemporary streetwear fashion shoot.
Composition: clear faces and relaxed poses; reserve the lower fifth for copy.
Text, verbatim: "Yours to Create." exactly once in legible bold sans serif.
Exclude: extra text, unrelated logos, watermarks.
Pass criteria: spelling, punctuation, occurrence count, and readable typography.
```

Supply the user's actual brand assets and palette when fidelity is required.
Spell unusual names letter by letter only when that clarifies ambiguous copy.
For contractual typography, generate the art and place approved text separately
when the user authorizes that workflow.

### Reference-based precise edit

```text
Image 1: the product photograph and edit target.
Image 2: reference for the new backdrop's color and texture only.
Change: replace only Image 1's backdrop with the backdrop treatment of Image 2.
Preserve: the product's geometry, proportions, label text, crop, highlights,
edge detail, and camera angle. Match the original lighting at the contact edge.
Exclude: any objects or text from Image 2.
Pass criteria: no product redesign; label unchanged; no edge halos.
```

Include every target/reference in the invocation, not only in prose. Restate
preservation constraints on each follow-up. If an edit drifts, return to the
last accepted input rather than accumulating unwanted changes.

### Transparent asset / logo exploration

```text
Create a single centered, simple geometric kingfisher mark for the supplied
brand. Flat vector-like shapes, strong silhouette, generous clear padding.
Fully transparent background with clean alpha edges; no scenery, shadow,
checkerboard, or additional copy. Preserve the supplied palette.
Pass criteria: readable at small size; genuine alpha; no fringe.
```

Use native `transparent_background: true` where exposed, or API
`background="transparent"` with PNG/WebP. “Vector-like” still produces a bitmap.
For an existing editable vector system, edit its vector assets directly.

### Diagram / educational image

Give the model the approved facts, exact labels, and relationships. Specify
reading order and arrow direction; do not rely on it to discover the mechanism.
Check factual relationships, units, spelling, and legibility in addition to
appearance. Prefer deterministic diagrams when editable, exact structure matters.

## Iterate and accept

Inspect first. Request one change and list what stays unchanged. Keep the same
references and settings when comparing models. Validate dimensions, text,
identity, geometry, local edit scope, alpha, and the actual intended placement.
Do not assume that more adjectives, more effort, or `max` fixes an unclear brief.
