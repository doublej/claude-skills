---
name: logo
description: "Create logos, icons, wordmarks, monograms, and brand marks as production-ready SVG, via three construction modes: freeform (direct SVG design), mathematical (geometric first principles — grids, tangency, Bezier), and grid (constrained JSON cell maps, 3x3-9x9). The single entry point for logo work — no sibling logo skills exist. Triggers on 'create logo', 'design logo', 'make icon', 'logo for', 'brand mark', 'logomark', 'wordmark', 'monogram', 'brand identity', 'grid logo', 'geometric logo'."
---

# Logo

You design logos with conviction. No committee. No "options." One direction, executed ruthlessly.

<mode_selection>

## Pick a Construction Mode

Three modes share the brief, rules, and checklist below. Deep per-mode guidance lives in `references/`.

| Mode | How it works | Choose when | Reference |
|------|--------------|-------------|-----------|
| **Freeform** | Direct SVG authorship — sketch geometry, write paths | Default. Organic or mixed shape language, wordmarks, fast turnaround, no explicit system demanded | `references/freeform.md` |
| **Mathematical** | Geometric first principles — module grids, tangency, Bézier continuity, parametric curves, values→parameters mapping | Brand values must be traceable to measurable parameters; precision/system-driven marks; rosettes, superellipses, Cn/Dn symmetry; user says "mathematical", "constructed", "golden ratio", "grid system" | `references/mathematical.md` |
| **Grid** | Constrained JSON cell maps (3x3–9x9) converted to SVG by script | Ultra-bold iconic marks, favicons/app icons, pixel-art-adjacent aesthetics; forcing alignment beats freeform drift; user says "grid logo", "blocky", "modular cells" | `references/grid.md` |

Cues, not laws: if the user names a mode, use it. Otherwise pick ONE from the brief's shape language and commit — don't present mode options.

</mode_selection>

<preflight>

## Pre-Flight: Logo Brief

Before ANY code, produce this brief:

```
LOGO BRIEF
Brand: [name]
Essence: [one word - what feeling does this brand evoke?]
Mode: [freeform | mathematical | grid]
Type: [logomark | wordmark | lettermark | combination | emblem | abstract]
Shape Language: [geometric | organic | angular | rounded | mixed]
Signature Element: [the ONE thing that makes this memorable]
Aesthetic Thesis: [one sentence — the WHY behind your visual direction]
Palette: primary [hex], secondary [hex], accent [hex]
Typography: [none | see Typography Intent block below]
```

The aesthetic thesis is your conviction. "Modern and clean" is not a thesis. "Brutalist geometry that refuses decoration" is.

Mode-specific brief extensions (add these blocks when the mode applies):
- **Mathematical**: VALUES (weighted, mapped to parameters), CONSTRAINTS (canvas, module, min stroke/gap), CONSTRUCTION (family, symmetry, radii set, ratio system) — see `references/mathematical.md`
- **Grid**: Grid size [3-9, default 5] — see `references/grid.md`

</preflight>

<logo_types>

| Type | When to Use | Example |
|------|-------------|---------|
| Wordmark | Brand name IS the identity, distinctive typography | Google, Coca-Cola |
| Lettermark | Long name, initials work better | IBM, HBO |
| Logomark | Symbol can stand alone, icon-friendly | Apple, Twitter |
| Combination | New brand, needs both recognition paths | Adidas, Burger King |
| Emblem | Traditional, badge-like, institutional | Starbucks, Harley-Davidson |
| Abstract | Concept over literal, tech/modern brands | Pepsi, Airbnb |

</logo_types>

<design_principles>

### Simplicity
- Reduce to essential forms
- Must work at 16x16 favicon size
- Silhouette test: recognizable as solid shape?

### Memorability
- One distinctive element, not five clever ones
- Avoid generic: circles, swooshes, globes, generic people icons
- If you've seen it before, kill it

### Scalability
- Vector only (SVG)
- No gradients that break at small sizes
- No fine details that disappear

### Versatility
- Works on light and dark backgrounds
- Works in single color (black or white)
- Works with and without text

</design_principles>

<banned_elements>

These signal lazy design:
- Swooshes, swoops, curves that "suggest motion"
- Generic globes
- Puzzle pieces
- Light bulbs (for "ideas")
- Handshake icons
- Generic people silhouettes
- Laurel wreaths (unless actually classical)
- Arrows pointing up/right (for "growth")
- Infinity symbols
- Generic gears
- Post-hoc grid overlays that don't match construction

### Banned Words

Never use these in briefs or descriptions — they signal slop:
- "Sleek", "synergy", "innovative", "cutting-edge"
- "Elevate", "leverage", "holistic", "dynamic"
- "Premium feel", "modern aesthetic", "clean lines"

Say what you actually mean instead.

</banned_elements>

<color_strategy>

| Approach | When | Palette | Example |
|----------|------|---------|---------|
| Monochrome | Maximum versatility/impact, serious brands | 1 colour + background | Law firm, luxury |
| Duotone | Primary + accent, balanced presence | 2 colours | Tech, professional services |
| Triadic | Bold, playful, high energy | 3 colours (use sparingly) | Consumer, entertainment |

Logo must work flat. Reserve gradients for hero usage only.
One colour should dominate (60%+), one accent (10-30%), one optional detail.

</color_strategy>

<svg_output>

## SVG Output Format

```svg
<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <title>Brand Name Logo</title>
  <!-- Primary shape -->
  <!-- Secondary elements -->
  <!-- Wordmark paths if applicable -->
</svg>
```

Requirements:
- `viewBox` always (never fixed width/height). Default canvas 512 freeform, 1000 mathematical, grid-computed for grid mode
- `xmlns` namespace required
- `<title>` for accessibility
- Clean, semantic grouping with `<g>` elements
- Hex colors only, no named colors
- No inline styles unless necessary

</svg_output>

<typography_intent>

Typography is optional. Default to pure geometry unless the brand name IS the identity (wordmark, lettermark, combination).

If typography is used, justify the choice in the brief:

```
TYPOGRAPHY INTENT
Approach: [geometric construction | adapted from typeface family]
Why: [one sentence - what does this letterform style communicate?]
Character: [mono-width | proportional], [geometric | humanist | grotesque]
```

Examples of justified choices:
- Geometric mono-width for a code tool (precision, technical)
- Rounded grotesque for a children's app (friendly, approachable)
- High-contrast serif for a luxury brand (elegance, tradition)

If you can't articulate why, the logo probably doesn't need type.

### Letterforms as Vector Geometry

**Never use `<text>` elements** (exception: grid mode's off-grid text block, which uses restricted system fonts — see `references/grid.md`). All letterforms must be `<path>` data — constructed or converted to outlines.

Why:
- `<text>` depends on installed fonts — renders differently everywhere
- Paths are measurable: you know exact widths, heights, and whitespace
- Paths fit the logo grid — letters align to the same coordinate system as the mark

Construction approach:
1. Define a type grid: baseline, cap-height, x-height, ascender/descender lines
2. Build each letter on this grid using `<path>` with cubic/quadratic beziers
3. Ensure consistent stroke widths and optical corrections (round shapes extend ~2% past flat baselines)
4. Kern manually — measure gaps between path bounding boxes, not guesswork
5. Group the wordmark in a single `<g>` so it scales as one unit

</typography_intent>

<variants>

## Variants to Deliver

For a complete logo system, provide:

1. **Primary** - Full logo, preferred usage
2. **Icon** - Logomark only, square format for favicons/avatars
3. **Horizontal** - Wide format for headers
4. **Monochrome** - Single color version
5. **Reversed** - For dark backgrounds

Minimum: Primary + Icon.

</variants>

<workflow>

## Workflow

1. **Brief** - Establish brand essence, mode, and type
2. **Sketch** - Describe 2-3 geometric approaches mentally; produce a rough visual fast
3. **Commit** - Pick ONE direction
4. **Execute** - Follow the mode reference (`references/freeform.md`, `references/mathematical.md`, or `references/grid.md`)
5. **Variants** - Provide icon + primary minimum
6. **Verify** - Run quality checklist

**Show, don't compute.** Produce a rough SVG fast, preview it, then refine. Never spend extended reasoning on geometry without showing visual progress. For complex geometry, write a generator script instead of hand-computing coordinates.

</workflow>

<quality_checklist>

## Quality Checklist

Before delivery:
- [ ] Works at 16px (favicon)
- [ ] Works at 512px (hero)
- [ ] Readable in monochrome
- [ ] No orphaned paths or groups
- [ ] viewBox is correct
- [ ] `<title>` element present
- [ ] Colors are hex, not named
- [ ] No `<text>` elements — all type is `<path>` geometry (grid-mode text block excepted)
- [ ] No external font dependencies

Mode-specific extensions: mathematical adds a validation checklist (grid compliance, G1 continuity, parameter stability — see `references/mathematical.md`); grid adds bounds/palette/ASCII checks (see `references/grid.md`).

</quality_checklist>

<output>

## Output

Deliver:
1. Logo brief (the thinking)
2. SVG code (primary version)
3. Icon variant SVG
4. Usage notes (2-3 lines max)

Mode extras: mathematical adds a parameter sheet (the numbers that built it); grid adds the ASCII preview + JSON grid definition.

If user requests a Python script, use `~/.claude/skills/logo/scripts/generate-logo.py` as base (see mode references).

</output>
