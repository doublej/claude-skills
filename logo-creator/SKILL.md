---
name: logo-creator
description: Create distinctive, production-ready logos as SVG code. Use when user needs a logo, icon, wordmark, monogram, or visual identity. Generates geometric, scalable vector graphics with no external dependencies. Triggers on "create logo", "design logo", "make icon", "brand identity", "logomark", "wordmark".
---

# Logo Creator

You design logos with conviction. No committee. No "options." One direction, executed ruthlessly.

## Pre-Flight: Logo Brief

Before ANY code, produce this brief:

```
LOGO BRIEF
Brand: [name]
Essence: [one word - what feeling does this brand evoke?]
Type: [logomark | wordmark | lettermark | combination | emblem | abstract]
Shape Language: [geometric | organic | angular | rounded | mixed]
Signature Element: [the ONE thing that makes this memorable]
Palette: primary [hex], secondary [hex], accent [hex]
Typography: [none | see Typography Intent block below]
```

## Logo Types

| Type | When to Use | Example |
|------|-------------|---------|
| Wordmark | Brand name IS the identity, distinctive typography | Google, Coca-Cola |
| Lettermark | Long name, initials work better | IBM, HBO |
| Logomark | Symbol can stand alone, icon-friendly | Apple, Twitter |
| Combination | New brand, needs both recognition paths | Adidas, Burger King |
| Emblem | Traditional, badge-like, institutional | Starbucks, Harley-Davidson |
| Abstract | Concept over literal, tech/modern brands | Pepsi, Airbnb |

## Design Principles

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

## Banned Elements

These signal lazy design:
- Swooshes and swoops
- Generic globes
- Puzzle pieces
- Light bulbs (for "ideas")
- Handshake icons
- Generic people silhouettes
- Laurel wreaths (unless actually classical)
- Arrows pointing up/right (for "growth")
- Infinity symbols
- Generic gears

## SVG Output Format

Always use this structure:

```svg
<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <title>Brand Name Logo</title>
  <!-- Primary shape -->
  <!-- Secondary elements -->
  <!-- Wordmark paths if applicable -->
</svg>
```

Requirements:
- `viewBox` always (never fixed width/height)
- `xmlns` namespace required
- `<title>` for accessibility
- Clean, semantic grouping with `<g>` elements
- Hex colors only, no named colors
- No inline styles unless necessary

## Color Strategy

| Approach | When | Example |
|----------|------|---------|
| Monochrome | Maximum versatility, serious brands | Law firm, luxury |
| Duotone | Primary + accent, balanced presence | Tech, professional services |
| Triadic | Bold, playful, high energy | Consumer, entertainment |

Reserve gradients for hero usage only. Logo must work flat.

## Typography in Logos

Typography is optional. Default to pure geometry unless the brand name IS the identity (wordmark, lettermark, combination).

### Font Intent

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

**Never use `<text>` elements.** All letterforms must be `<path>` data — constructed or converted to outlines.

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

## Python Generator Template

When user prefers a script:

```python
#!/usr/bin/env python3
"""Generate [Brand] logo as SVG."""

def generate_logo(output_path: str = "logo.svg") -> None:
    width, height = 512, 512
    primary = "#1a1a1a"
    secondary = "#ffffff"

    # Build SVG elements
    elements = []

    # [Logo geometry here]

    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <title>Brand Logo</title>
  {"".join(elements)}
</svg>'''

    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Logo saved: {output_path}")

if __name__ == "__main__":
    generate_logo()
```

No external dependencies. Standard library only.

## Variants to Deliver

For complete logo system, provide:

1. **Primary** - Full logo, preferred usage
2. **Icon** - Logomark only, square format for favicons/avatars
3. **Horizontal** - Wide format for headers
4. **Monochrome** - Single color version
5. **Reversed** - For dark backgrounds

Minimum: Primary + Icon.

## Quality Checklist

Before delivery:
- [ ] Works at 16px (favicon)
- [ ] Works at 512px (hero)
- [ ] Readable in monochrome
- [ ] No orphaned paths or groups
- [ ] viewBox is correct
- [ ] Title element present
- [ ] Colors are hex, not named
- [ ] No `<text>` elements — all type is `<path>` geometry
- [ ] No external font dependencies

## Workflow

1. **Brief** - Establish brand essence and type
2. **Sketch** - Describe 2-3 geometric approaches mentally
3. **Commit** - Pick ONE direction
4. **Execute** - Generate clean SVG
5. **Variants** - Provide icon + primary minimum
6. **Verify** - Run quality checklist

## Output

Deliver:
1. Logo brief (the thinking)
2. SVG code (primary version)
3. Icon variant SVG
4. Usage notes (2-3 lines max)

If user requests Python script, provide generator instead of raw SVG.
