---
name: photoshop-api
description: Read/write PSD/PSB files with PhotoshopAPI (C++ library with Python bindings via `psapi`). Use when working with Photoshop file manipulation, layer compositing, PSD generation, or any code importing `photoshopapi`/`psapi`. Triggers on "PSD", "PSB", "PhotoshopAPI", "psapi", "photoshop file", "layer compositing programmatically".
---

# PhotoshopAPI

C++20 library (BSD-3) for reading/writing `.psd`/`.psb` without Photoshop. Python bindings: `pip install PhotoshopAPI`, import as `photoshopapi` (alias `psapi`). 5-10x faster reads, 20x faster writes than Photoshop. Files 20-50% smaller.

<format_limits>
PSD: max 30,000x30,000px. PSB: max 300,000x300,000px.
Color modes: RGB, CMYK, Grayscale. Bit depths: 8 (uint8), 16 (uint16), 32 (float32).
NOT supported: Lab, Multichannel, Indexed, Duotone, Adjustment Layers, Vector Masks.
</format_limits>

## Python Quick Patterns

```python
import photoshopapi as psapi
import numpy as np

# Read (auto-detects bit depth)
doc = psapi.LayeredFile.read("input.psd")

# Create
doc = psapi.LayeredFile_8bit(psapi.enum.ColorMode.rgb, 800, 600)

# ImageLayer from numpy (shape: channels, height, width)
img = np.zeros((3, 600, 800), np.uint8)
img[0] = 255  # red
layer = psapi.ImageLayer_8bit(img, "RedFill", width=800, height=600)
doc.add_layer(layer)

# ImageLayer from channel dict
channels = {
    psapi.enum.ChannelID.red: np.full((600, 800), 255, np.uint8),
    psapi.enum.ChannelID.green: np.zeros((600, 800), np.uint8),
    psapi.enum.ChannelID.blue: np.zeros((600, 800), np.uint8),
}
layer = psapi.ImageLayer_8bit(channels, "RedDict", width=800, height=600)

# Groups
group = psapi.GroupLayer_8bit("MyGroup")
doc.add_layer(group)
group.add_layer(doc, layer)  # NOTE: requires parent doc as first arg

# Navigate layers
layer = doc["GroupName"]["LayerName"]
layer = doc.find_layer("GroupName/LayerName")

# Write (invalidates doc — cannot reuse after this)
doc.write("output.psd")
```

## Layer Types

| Type | Python class | Notes |
|------|-------------|-------|
| Image | `ImageLayer_Nbit` | Raster layer. At least one required per file. |
| Group | `GroupLayer_Nbit` | Folder. `add_layer(doc, child)` needs parent doc ref. Default blend: passthrough. |
| SmartObject | `SmartObjectLayer_Nbit` | Linked/embedded. Image data read-only — use `replace()`. |
| Text | `TextLayer_Nbit` | Full EngineData access. `.text` read-only; modify via `set_text()` / `replace_text()`. |

Where `N` = `8`, `16`, or `32`.

## Smart Objects

```python
so = psapi.SmartObjectLayer_8bit(
    doc, path="photo.jpg", layer_name="Photo",
    link_type=psapi.enum.LinkedLayerType.data  # embedded
)
so.rotate(45, so.center_x, so.center_y)
so.scale(0.65, 0.65, so.center_x, so.center_y)
doc.add_layer(so)
so.replace("other.jpg")  # swap underlying image
```

## Text Layers

```python
tl = doc["MyText"]  # TextLayer
print(tl.text)
tl.set_text("New text")
tl.replace_text("old", "new")
tl.set_font("Helvetica-Bold")
tl.set_position(100, 200)
tl.set_rotation_angle(15.0)

# Style runs (per-run formatting)
run = tl.style_run(0)
run.font_size  # getter
tl.set_style_run_font_size(0, 24.0)
tl.set_style_run_fill_color(0, [255, 0, 0])
```

## Bit-Depth Conversion (Grafting)

```python
src = psapi.LayeredFile.read("source_16bit.psb")
dst = psapi.LayeredFile.read("dest_8bit.psd")
lr = src["SourceLayer"]
data_16 = lr.get_image_data()
data_8 = {k: (v / 256).astype(np.uint8) for k, v in data_16.items()}
new_layer = psapi.ImageLayer_8bit(data_8, lr.name, width=lr.width, height=lr.height)
dst.add_layer(new_layer)
dst.write("output.psd")
```

<gotchas>
- `write()` invalidates the LayeredFile — do not reuse after writing
- Do not modify layer structure while iterating `flat_layers`
- `pos_x`/`pos_y` are relative to document center (0,0 = centered)
- Layer color mode must match document color mode
- Layer names max 255 characters
- No merged/composited image data in output — apps like Lightroom may not preview correctly
- SmartObject image data is read-only — use `replace()` to change
- `set_text_equal_length()` is safer for preserving style runs (matches UTF-16 code units)
- GroupLayer.add_layer() signature in Python: `group.add_layer(doc, child_layer)`
- Default compression is `zipprediction` — generally optimal, don't change without reason
</gotchas>

<layer_properties>
All layers: name, blend_mode, opacity (0.0-1.0), fill (0.0-1.0), width, height,
center_x, center_y, is_locked, is_visible, clipping_mask, display_color,
mask, mask_disabled, mask_relative_to_layer, mask_default_color,
mask_density, mask_feather, mask_position, mask_width, mask_height
</layer_properties>

For full enum values and detailed API: `grep` in `references/python-api.md` and `references/enums.md`.
