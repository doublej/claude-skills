---
name: pillow-drawing
description: "Professional graphics with Python Pillow: shapes, text, cards, badges, banners"
---

# Pillow Drawing

<overview>
Create professional-looking graphics programmatically. Requires `pillow` (`uv add pillow`).

For image manipulation, format conversion, and batch processing, see `references/image-operations.md`.
</overview>

<rules>
## Rule #1: Anti-Alias Everything

Pillow's `ImageDraw` has NO native anti-aliasing for shapes. Without it, everything looks jagged. **Always supersample**: draw at 2-4x, downscale with LANCZOS.

```python
from PIL import Image, ImageDraw

SCALE = 3  # 3x supersample — good balance of quality vs memory

def create_canvas(w, h, bg="#1a1a2e"):
    """Create a supersampled RGBA canvas."""
    return Image.new("RGBA", (w * SCALE, h * SCALE), bg)

def finalize(img, w, h):
    """Downscale to target size with anti-aliasing."""
    return img.resize((w, h), Image.Resampling.LANCZOS)

# Usage
W, H = 800, 600
canvas = create_canvas(W, H)
draw = ImageDraw.Draw(canvas)
# ... draw at SCALE'd coordinates ...
result = finalize(canvas, W, H)
result.save("output.png")
```

All coordinates and sizes must be multiplied by SCALE when drawing. Font sizes too.
</rules>

<how_to_use>
## Text That Doesn't Suck

### Always use a real font

```python
from PIL import ImageFont

# NEVER use the default bitmap font
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=48 * SCALE)

# Linux: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
# Bundled: include .ttf in assets/ and load from there
```

### Center text properly — use anchors

```python
# anchor="mm" = middle-middle (both axes centered on the point)
draw.text((400 * SCALE, 300 * SCALE), "Centered",
          font=font, fill="#e0e0e0", anchor="mm")
```

Anchor codes: horizontal `l`eft/`m`iddle/`r`ight + vertical `a`scender/`m`iddle/`d`escender/`b`aseline.

### Text with stroke (outline) for contrast on busy backgrounds

```python
draw.text((x, y), "Label", font=font, fill="white",
          stroke_width=2 * SCALE, stroke_fill="#1a1a2e", anchor="mm")
```

### Multiline text

```python
# anchor NOT supported for multiline — position manually
draw.multiline_text((x, y), "Line one\nLine two",
                    font=font, fill="#e0e0e0", spacing=8 * SCALE, align="center")

# Measure multiline bounds
bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=8 * SCALE)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
```

### Quick font size (v10.1+, no font object)

```python
draw.text((10, 10), "Quick", fill="black", font_size=24)  # no anti-alias control
```

## Color Palettes That Work

### The rules

- **Never use pure black `#000000` or pure white `#FFFFFF`** — harsh contrast looks amateur
- Use off-black (`#1a1a2e`, `#2d2d2d`) and off-white (`#e8e8e8`, `#f5f5f5`)
- **3-5 colors max** from a cohesive palette
- **60-30-10 rule**: 60% background, 30% secondary, 10% accent

### Ready-to-use palettes

```python
PALETTES = {
    "dark_tech": {
        "bg": "#0d1117", "surface": "#161b22", "border": "#30363d",
        "text": "#e6edf3", "accent": "#58a6ff", "success": "#39d353",
    },
    "warm_pro": {
        "bg": "#fff8f0", "surface": "#fff1e6", "border": "#e8d5c4",
        "text": "#2d2d2d", "accent": "#ff5a09", "muted": "#8b7355",
    },
    "soft_clean": {
        "bg": "#fafafa", "surface": "#ffffff", "border": "#e5e5e5",
        "text": "#393939", "accent": "#7a9d96", "muted": "#999999",
    },
    "midnight": {
        "bg": "#1a1a2e", "surface": "#16213e", "border": "#0f3460",
        "text": "#e0e0e0", "accent": "#e94560", "highlight": "#533483",
    },
}
```

### Programmatic color generation with HSL

```python
import colorsys

def hsl_to_rgb(h, s, l):
    """HSL (0-360, 0-100, 0-100) -> RGB hex string."""
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

# Harmonious colors: same saturation/lightness, rotate hue
base_hue = 210  # blue
colors = [hsl_to_rgb((base_hue + i * 30) % 360, 70, 55) for i in range(5)]
```

## Shapes

### Rounded rectangles

```python
draw.rounded_rectangle(
    [20 * SCALE, 20 * SCALE, 380 * SCALE, 280 * SCALE],
    radius=16 * SCALE, fill="#161b22", outline="#30363d", width=2 * SCALE
)
```

### Circles

```python
# Pillow v10.4+
draw.circle((200 * SCALE, 200 * SCALE), 50 * SCALE, fill="#58a6ff")

# Older versions — use ellipse with square bounding box
cx, cy, r = 200 * SCALE, 200 * SCALE, 50 * SCALE
draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#58a6ff")
```

### Lines and polygons

```python
draw.line([(50 * SCALE, 50 * SCALE), (350 * SCALE, 350 * SCALE)],
          fill="#e94560", width=3 * SCALE)
draw.polygon([(200 * SCALE, 50 * SCALE), (350 * SCALE, 300 * SCALE),
              (50 * SCALE, 300 * SCALE)], fill="#533483", outline="#e94560")
```

## Drop Shadows

Shadows add depth and make elements pop. Draw shadow shape -> blur -> composite content on top.

```python
from PIL import ImageFilter

def draw_card_with_shadow(w, h, palette, radius=16, shadow_blur=20, shadow_offset=(8, 8)):
    """Draw a card with a soft drop shadow."""
    pad = shadow_blur * 2 + max(abs(shadow_offset[0]), abs(shadow_offset[1]))
    canvas = Image.new("RGBA", ((w + pad * 2) * SCALE, (h + pad * 2) * SCALE), (0, 0, 0, 0))

    # Shadow layer
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sx = (pad + shadow_offset[0]) * SCALE
    sy = (pad + shadow_offset[1]) * SCALE
    sd.rounded_rectangle(
        [sx, sy, sx + w * SCALE, sy + h * SCALE],
        radius=radius * SCALE, fill=(0, 0, 0, 80)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur * SCALE))

    # Card on top
    cd = ImageDraw.Draw(shadow)
    cx, cy = pad * SCALE, pad * SCALE
    cd.rounded_rectangle(
        [cx, cy, cx + w * SCALE, cy + h * SCALE],
        radius=radius * SCALE, fill=palette["surface"], outline=palette["border"],
        width=1 * SCALE
    )
    return shadow  # finalize() this later
```

## Gradients

Pillow has no built-in color gradients. Use NumPy or per-row drawing.

### Linear gradient with NumPy

```python
import numpy as np

def linear_gradient(w, h, color1, color2, horizontal=False):
    """Create a smooth linear gradient image."""
    c1 = np.array(color1, dtype=np.float64)
    c2 = np.array(color2, dtype=np.float64)
    steps = w if horizontal else h
    grad = np.linspace(c1, c2, steps).astype(np.uint8)
    if horizontal:
        arr = np.tile(grad, (h, 1, 1))
    else:
        arr = np.tile(grad[:, np.newaxis, :], (1, w, 1))
    return Image.fromarray(arr, "RGB")

# Usage
bg = linear_gradient(800, 600, (13, 17, 23), (22, 33, 62))
```

### Gradient without NumPy (pure Pillow)

```python
def linear_gradient_pure(w, h, color1, color2):
    """Vertical gradient using Pillow only."""
    base = Image.new("RGB", (w, h), color1)
    top = Image.new("RGB", (w, h), color2)
    mask = Image.linear_gradient("L").resize((w, h), Image.Resampling.LANCZOS)
    return Image.composite(top, base, mask)
```

### Gradient as overlay mask

```python
# Apply gradient transparency over an image
gradient_mask = Image.linear_gradient("L").resize(img.size, Image.Resampling.LANCZOS)
img.putalpha(gradient_mask)  # fades from opaque top to transparent bottom
```

## Compositing

### Layer multiple elements (correct way)

```python
# ALWAYS use alpha_composite for RGBA blending — NOT paste()
# paste() ignores alpha and overwrites pixels
base = Image.new("RGBA", (800, 600), "#0d1117")
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
# ... draw on overlay ...
result = Image.alpha_composite(base, overlay)
```

### Opacity adjustment

```python
def set_opacity(img, opacity):
    """Scale alpha channel by opacity (0.0-1.0)."""
    r, g, b, a = img.convert("RGBA").split()
    a = a.point(lambda p: int(p * opacity))
    return Image.merge("RGBA", (r, g, b, a))
```

### Rounded corner mask

```python
def round_corners(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, *img.size], radius=radius, fill=255)
    img = img.convert("RGBA")
    img.putalpha(mask)
    return img
```

## Complete Example: Profile Card

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCALE = 3
W, H = 400, 200
P = PALETTES["dark_tech"]

# Canvas with gradient background
canvas = linear_gradient(W * SCALE, H * SCALE, (13, 17, 23), (22, 33, 62))
canvas = canvas.convert("RGBA")
draw = ImageDraw.Draw(canvas)

# Card background
margin = 20 * SCALE
draw.rounded_rectangle(
    [margin, margin, W * SCALE - margin, H * SCALE - margin],
    radius=12 * SCALE, fill=P["surface"], outline=P["border"], width=1 * SCALE
)

# Avatar circle
cx, cy = 80 * SCALE, 100 * SCALE
draw.circle((cx, cy), 30 * SCALE, fill=P["accent"])

# Name
name_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24 * SCALE)
draw.text((130 * SCALE, 75 * SCALE), "Jane Developer",
          font=name_font, fill=P["text"], anchor="lm")

# Role
role_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14 * SCALE)
draw.text((130 * SCALE, 110 * SCALE), "Senior Engineer",
          font=role_font, fill="#8b949e", anchor="lm")

# Accent bar
draw.rounded_rectangle(
    [margin + 8 * SCALE, H * SCALE - margin - 6 * SCALE,
     margin + 60 * SCALE, H * SCALE - margin - 2 * SCALE],
    radius=2 * SCALE, fill=P["accent"]
)

# Finalize
result = canvas.resize((W, H), Image.Resampling.LANCZOS)
result.save("card.png")
```

</how_to_use>

<quality_gates>

## Quality Checklist

Before saving final output:

1. **Anti-aliased?** — Drew at SCALE, downscaled with LANCZOS
2. **Real font loaded?** — `ImageFont.truetype()`, not default bitmap
3. **No pure black/white?** — Off-black bg, off-white text
4. **Margins/padding?** — At least 5% of canvas as breathing room
5. **3-5 colors max?** — From a cohesive palette
6. **Alpha compositing correct?** — `alpha_composite()`, not bare `paste()`
7. **JPEG quality?** — `quality=95` for graphics, never default 75
8. **Font sizes proportional?** — Calculated relative to canvas, not hardcoded
</quality_gates>
