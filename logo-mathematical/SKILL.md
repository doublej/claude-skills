---
name: logo-mathematical
description: "Logos from geometric first principles: grid systems, tangency, Bezier, SVG"
---

# Mathematical Logo Creator

<principles>
You construct logos from mathematical first principles. Every curve has a formula. Every proportion has a reason. The grid is law — but optical corrections keep it human.

**Do not over-rationalise.** The grid is a construction aid, not a post-hoc justification forced onto a finished shape.

**Show, don't compute.** Produce a rough SVG fast, preview it, then refine. Never spend extended reasoning on Bézier math without showing visual progress. For complex geometry, write a generator script instead of hand-computing coordinates.
</principles>

<preflight>

## Pre-Flight: Logo Brief

Before ANY code, produce this brief:

```
LOGO BRIEF
Brand: [name]
Essence: [one word]
Type: [logomark | wordmark | lettermark | combination | emblem | abstract]

VALUES (3-5, weights sum to 1.0)
v1: [value] (w=0.XX) → [visual objective] → [parameter handle]
v2: [value] (w=0.XX) → [visual objective] → [parameter handle]
v3: [value] (w=0.XX) → [visual objective] → [parameter handle]

CONSTRAINTS
Canvas: S=1000, module m=S/[N]
Smallest size: [16|24] px
Min stroke at S_min: [t_min] px
Min gap at S_min: [g_min] px
Complexity cap: C_max=[n] features
One-color required: [yes|no]

CONSTRUCTION
Family: [parametric curve | symmetry group | grid/tiling | superellipse]
Symmetry: [Cn|Dn|none], order n=[value]
Radii set: [e.g., {1m, 2m, 4m, 8m}]
Stroke: w=[value]m
Fillet radius: r=[value]m
Ratio system: [φ | √2 | 4:5 | none]
Overshoot: o=[value]%

Palette: primary [hex], secondary [hex], accent [hex]
Typography: [none | see Typography Intent]
```

</preflight>

<values_to_parameters>

## Values → Parameters

Map each brand value to 1-2 measurable visual metrics. This makes design decisions traceable.

| Metric | Symbol | What it measures |
|--------|--------|------------------|
| Symmetry order | `n` | Rotational/dihedral symmetry count |
| Curvature bound | `κ_max` | Maximum sharpness of turns |
| Complexity | `C` | Feature count (lobes, corners, control points) |
| Negative-space ratio | `NS` | Interior void / outer silhouette area |
| Stroke ratio | `SR` | Stroke width / mark diameter |
| Variance | `V` | Deviation from ideal shape (irregularity) |

Common value mappings (see `references/values-mapping.md` for worked example):

| Value | Direction | Parameters |
|-------|-----------|------------|
| Precision | ordered, exact | `n↑`, `V↓`, `C↓`, `κ_max↓` |
| Openness | breathable, inviting | `NS↑`, `g_min↑` |
| Resilience | robust, survives reproduction | `SR↑`, `t_min↑`, closed loops `L≥1` |
| Warmth | friendly, non-aggressive | `κ_max↓`, high-freq detail `HF↓` |
| Energy | dynamic, bold | `C↑`, asymmetry amplitude `a↑` |

</values_to_parameters>

<grid_module_system>

Canvas size `S` (default 1000). Grid resolution `N` (24, 32, 40, or 48).

```
m = S / N          (module size)
```

Quantize everything:
- **Positions**: multiples of `m/2` (or `m/4` if needed)
- **Radii**: small set, e.g. `{1m, 2m, 4m, 8m}`
- **Stroke widths**: pick 1-2 from `{1m, 1.5m, 2m}` and stick to them

**Grid snapping**: Do NOT hand-calculate snap offsets for every control point. Write a small script (Python/JS) that rounds coordinates to the nearest `m/2` and run it on the SVG. Visual verification beats analytical snapping.

</grid_module_system>

<construction_rules>

### Tangent fillet (rounded corner)

Two lines meeting at angle `θ`, desired radius `r`:
- Tangent distance from vertex: `t = r × cot(θ/2)`
- Center distance along bisector: `d = r / sin(θ/2)`

### Circle tangent to two circles

Circle of radius `r` tangent externally to `(C1,R1)` and `(C2,R2)`:
1. Inflate: `R1' = R1 + r`, `R2' = R2 + r`
2. Center lies at intersection of circles `(C1,R1')` and `(C2,R2')`
3. For internal tangency: `R' = |R - r|`

### Arc tangent to line + circle

- Offset the line by `r` (parallel)
- Inflate/deflate the circle by `r`
- Intersect to get center

### Bézier continuity

Two cubic segments meeting at `P`:
- **G1 (direction smooth)**: vectors `(P3-P2)` and `(Q1-Q0)` collinear, same direction
- **C1 (speed smooth)**: `Q1 = Q0 + (P3 - P2)` (mirror last handle into next)

Enforce G1 minimum at all joins. C1 where possible.

### Circle as Bézier

</construction_rules>

<circle_as_bezier>

Quarter-arc handle constant: `k = 4(√2 - 1) / 3 ≈ 0.55228475`

For quarter circle from (1,0) to (0,1): control points at `(1, k)` and `(k, 1)`.

See `references/construction-formulas.md` for full derivations and edge cases.

</circle_as_bezier>

<optical_corrections>

Apply as calculable parameters, not guesswork:

1. **Overshoot**: round shapes extend ~1-2% past flat baselines (`o = 0.015 × S` start)
2. **Optical centering**: geometric center + small offset toward visually lighter side (~1-2% of dimension)
3. **Horizontal stroke compensation**: `w_horizontal = 0.9 × w_vertical` (horizontals look heavier at equal thickness)

</optical_corrections>

<mathematical_families>

Choose based on target metrics:

| Family | Best for | Natural parameters |
|--------|----------|-------------------|
| Parametric curves (superellipse, epicycloid, polar Fourier) | Smooth iconic silhouettes | Lobe count, amplitude, curvature |
| Symmetry groups (Cn/Dn) | Precision, structure | Order, rotation, reflection |
| Grids/tilings | Modularity, system-ness | Cell count, gap, fill ratio |
| Superellipse `|x|^p + |y|^p = 1` | Tunable squircle | Exponent p (2=circle, ∞=square) |

Rule of thumb: need strong silhouette + small-size legibility → **parametric curves + symmetry first**.

Polar Fourier for rosette-style marks:
```
r(θ) = 1 + a × cos(n × θ)
x(θ) = r(θ) × cos(θ)
y(θ) = r(θ) × sin(θ)
```

</mathematical_families>

<ratio_systems>

Use a ratio `r` to scale key dimensions: `size_k = base × r^k`.

Options: `φ ≈ 1.618`, `√2 ≈ 1.414`, `4:5 = 1.25`, or none.

Golden ratio claims of inherent beauty are not evidence-based. Use it as a constraint, not a claim. Simpler ratios often work equally well.

</ratio_systems>

<typography>

## Typography in Logos

Typography is optional. Default to pure geometry unless the brand name IS the identity.

### Font Intent

If typography is used, justify the choice in the brief:

```
TYPOGRAPHY INTENT
Approach: [geometric construction | adapted from typeface family]
Why: [one sentence - what does this letterform style communicate?]
Character: [mono-width | proportional], [geometric | humanist | grotesque]
```

If you can't articulate why, the logo probably doesn't need type.

</typography>

<letterforms>

### Letterforms as Vector Geometry

**Never use `<text>` elements.** All letterforms must be `<path>` data.

1. Define a type grid: baseline, cap-height, x-height on the module grid
2. Build each letter using `<path>` with cubic/quadratic Béziers
3. Apply optical corrections (overshoot, stroke compensation)
4. Kern manually — measure gaps between path bounding boxes
5. Group the wordmark in a single `<g>`

</letterforms>

<banned_elements>

- Swooshes, swoops, generic globes, puzzle pieces, light bulbs
- Handshake icons, generic people, laurel wreaths (unless classical)
- Arrows pointing up/right, infinity symbols, generic gears
- Post-hoc grid overlays that don't match construction

</banned_elements>

<svg_output>

## SVG Output Format

```svg
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <title>Brand Name Logo</title>
  <!-- Construction grid reference (remove in production) -->
  <!-- Primary shape -->
  <!-- Secondary elements -->
  <!-- Wordmark paths if applicable -->
</svg>
```

- `viewBox` always (never fixed width/height). Default canvas: `0 0 1000 1000`
- `xmlns` namespace required, `<title>` for accessibility
- Hex colours only, no named colours
- Clean `<g>` grouping

</svg_output>

<color_strategy>

| Approach | When | Example |
|----------|------|---------|
| Monochrome | Maximum versatility, serious brands | Law firm, luxury |
| Duotone | Primary + accent, balanced | Tech, professional |
| Triadic | Bold, playful, high energy | Consumer, entertainment |

Logo must work flat. Reserve gradients for hero usage only.

</color_strategy>

<workflow>

**Core principle: show visuals early, refine with feedback.** Never spend more than one reasoning step computing coordinates without producing a viewable SVG.

1. **Brief** — values, constraints, math family, parameter targets
2. **Map** — values → metrics → parameter ranges
3. **Sketch** — produce a rough SVG in ≤30 seconds using simple shapes (circles, rects, arcs). Don't worry about G1 continuity, exact grid snap, or optical corrections yet. Write the SVG, preview it (see Preview below), and get user feedback on the overall direction before investing in math.
4. **Construct** — refine the sketch with proper curves and tangency. For anything beyond 2 arcs, **generate a script** (Python/JS) rather than hand-computing Bézier control points. Run the script to produce the SVG.
5. **Preview & iterate** — show the result after each major change. Use the preview template below. Make corrections based on what you see, not what you calculate.
6. **Correct** — apply overshoot, optical centering, stroke compensation. Verify visually — screenshot at 16px, 64px, and 1000px to confirm corrections work.
7. **Validate** — run validation checklist below
8. **Simplify** — reduce control points, remove tiny segments, enforce continuity
9. **Variants** — primary + icon minimum

</workflow>

<script_first>

### Script-first construction

For any logo with more than 2 arcs or 4 Bézier segments, write a generator script rather than hand-computing every coordinate. Benefits:
- Grid snapping is one `round(x / half_m) * half_m` call, not pages of arithmetic
- Parameter tweaks regenerate the entire SVG instantly
- Continuity constraints (G1/C1) are enforced programmatically
- Optical corrections (overshoot, stroke compensation) are applied consistently

Use `scripts/generate-logo.py` as a starting point or create a project-specific script.

</script_first>

<preview>

After writing an SVG, create a preview page and show it to verify the result visually. This is mandatory — never skip it.

Use the template at `templates/preview.html`. It shows the logo on light, dark, and 50% gray backgrounds with size variants (64px, 32px, 16px), plus interactive controls:
- **Grid overlay toggle** — shows the construction grid over the logo
- **Center lines toggle** — shows horizontal/vertical center crosshairs
- **Grid resolution selector** — switch between 24, 32, 40, 48 divisions

**Build the preview:**

```python
from pathlib import Path

def build_preview(svg_markup, brand_name, canvas=1000, grid_n=24, output="/tmp/logo-preview.html"):
    template = Path(__file__).parent.parent / "templates" / "preview.html"
    html = template.read_text()
    html = html.replace("{{SVG}}", svg_markup)
    html = html.replace("{{BRAND_NAME}}", brand_name)
    html = html.replace("{{CANVAS_SIZE}}", str(canvas))
    html = html.replace("{{GRID_N}}", str(grid_n))
    html = html.replace("{{MODULE_SIZE}}", f"{canvas / grid_n:.1f}")
    Path(output).write_text(html)
    return output
```

Or inline from a bash one-liner:

```bash
# Read SVG file and inject into template
SVG=$(cat logo.svg)
sed -e "s|{{SVG}}|$SVG|g" \
    -e "s|{{BRAND_NAME}}|BrandName|g" \
    -e "s|{{CANVAS_SIZE}}|1000|g" \
    -e "s|{{GRID_N}}|24|g" \
    -e "s|{{MODULE_SIZE}}|41.7|g" \
    templates/preview.html > /tmp/logo-preview.html
```

Open in the browser and screenshot to verify.

</preview>

<validation>

## Validation Checklist

- [ ] **Scalability**: recognisable at 16px, clean at 1000px
- [ ] **One-colour**: reads as solid shape without gradients
- [ ] **Reproduction**: satisfies `t_min` and `g_min` at `S_min`
- [ ] **Distinct silhouette**: identifiable from outline alone
- [ ] **Complexity**: feature count `C ≤ C_max`
- [ ] **Negative space**: internal voids don't collapse when downsampled
- [ ] **Parameter stability**: ±5% parameter change doesn't break legibility
- [ ] **Value traceability**: each value points to a measured parameter
- [ ] **Grid compliance**: all points snap to module grid
- [ ] **Continuity**: G1 minimum at all curve joins
- [ ] **No `<text>` elements**: all type is `<path>` geometry
- [ ] **No post-hoc grids**: grid was used for construction, not decoration

</validation>

<output>

Deliver:
1. Logo brief (values, parameters, construction decisions)
2. SVG code (primary version, canvas 1000×1000)
3. Icon variant SVG
4. Parameter sheet (the numbers that built it)

If user requests Python script, use `scripts/generate-logo.py` as base.

</output>
