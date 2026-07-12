# Freeform Mode

Direct SVG authorship. The default mode: sketch geometric approaches mentally, commit to one, write clean paths by hand or via a small generator script. Shared rules (brief, banned elements, color strategy, typography, checklist) live in SKILL.md.

<canvas>

Default canvas: `viewBox="0 0 512 512"`.

</canvas>

<workflow>

1. **Brief** - Establish brand essence and type (see SKILL.md pre-flight)
2. **Sketch** - Describe 2-3 geometric approaches mentally
3. **Commit** - Pick ONE direction
4. **Execute** - Generate clean SVG
5. **Variants** - Provide icon + primary minimum
6. **Verify** - Run quality checklist

</workflow>

<python_generator>

## Python Generator Template

When the user prefers a script, use `~/.claude/skills/logo/scripts/generate-logo.py` as a starting point — it includes SVG primitive helpers (`svg_circle`, `svg_rect`, `svg_polygon`, `svg_path`, `svg_letterform`, `svg_wordmark`) plus the mathematical-mode construction toolkit. Customise `generate_elements()` for the brand.

Minimal inline template when a standalone one-off is enough:

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

</python_generator>

<output>

Deliver:
1. Logo brief (the thinking)
2. SVG code (primary version)
3. Icon variant SVG
4. Usage notes (2-3 lines max)

If user requests a Python script, provide the generator instead of raw SVG.

</output>
