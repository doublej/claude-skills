# PhotoshopAPI — Python API Reference

## Installation

```bash
pip install PhotoshopAPI
```

Python 3.8-3.14. Wheels: Windows x86-64, Linux x86-64, macOS ARM64 (>=3.10).

```python
import photoshopapi as psapi
```

## LayeredFile

Classes: `LayeredFile_8bit`, `LayeredFile_16bit`, `LayeredFile_32bit`.
Auto-detect: `psapi.LayeredFile.read(path)` returns correct variant.

### Constructor

```python
doc = psapi.LayeredFile_8bit(color_mode, width, height)
```

### Properties

| Property | Type | Access |
|----------|------|--------|
| `icc` | numpy.ndarray | R/W |
| `compression` | psapi.enum.Compression | W |
| `num_channels` | int | R |
| `bit_depth` | psapi.enum.BitDepth | R |
| `layers` | list[Layer] | R |
| `flat_layers` | list[Layer] | R |
| `dpi` | int | R/W |
| `width` | int | R/W |
| `height` | int | R/W |

### Methods

- `read(path)` — static, returns typed instance
- `write(path, force_overwrite=True)` — saves; invalidates instance
- `add_layer(layer)` / `remove_layer(layer_or_name)` / `move_layer(child, parent=None)`
- `find_layer(path_string)` / `is_layer_in_document(layer)`
- `invalidate_text_cache()` — forces PS to re-render text on open
- `__getitem__(name)` — dict-style layer access

## ImageLayer

Classes: `ImageLayer_8bit`, `ImageLayer_16bit`, `ImageLayer_32bit`.

### Constructor

```python
psapi.ImageLayer_8bit(
    image_data,          # np.ndarray (C,H,W) or dict
    layer_name,          # str, max 255 chars
    layer_mask=None,     # np.ndarray (H,W)
    width=0, height=0,
    blend_mode=psapi.enum.BlendMode.normal,
    pos_x=0, pos_y=0,   # relative to doc center
    opacity=1.0,
    compression=psapi.enum.Compression.zipprediction,
    color_mode=psapi.enum.ColorMode.rgb,
    is_visible=True,
    is_locked=False
)
```

Image data accepts three forms:
1. `np.ndarray` shape `(channels, height, width)` — alpha as last channel
2. `dict[int, np.ndarray]` — int index keys
3. `dict[psapi.enum.ChannelID, np.ndarray]` — enum keys

### Data Access

- `layer.image_data` / `layer.get_image_data()` — dict of channel index → numpy array
- `layer.get_channel_by_id(channel_id)` / `layer.get_channel_by_index(index)`
- `layer[index]` — get channel; `layer[index] = array` — set channel
- `layer.channels` — list of available channel indices
- `layer.num_channels` — count
- `layer.mask` — get/set mask array; `layer.has_mask()`

## GroupLayer

Classes: `GroupLayer_8bit`, `GroupLayer_16bit`, `GroupLayer_32bit`.

```python
group = psapi.GroupLayer_8bit("GroupName")
doc.add_layer(group)
group.add_layer(doc, child_layer)  # parent doc required as first arg
```

Default blend mode: `passthrough`.

## SmartObjectLayer

Classes: `SmartObjectLayer_8bit`, `SmartObjectLayer_16bit`, `SmartObjectLayer_32bit`.

### Constructor

```python
psapi.SmartObjectLayer_8bit(
    layered_file,        # parent LayeredFile
    path="image.jpg",    # file to embed/link
    layer_name="name",
    link_type=psapi.enum.LinkedLayerType.data,  # .data=embedded, .external=linked
    warp=None,
    # + standard layer params (blend_mode, opacity, etc.)
)
```

### Methods

- `replace(path, link_externally=False)` — swap underlying image
- `hash()` / `filename()` / `filepath()`
- `get_original_image_data()`
- `original_width()` / `original_height()`
- `move(x, y)` / `rotate(angle, cx, cy)` / `scale(sx, sy, cx, cy)`
- `transform(matrix_3x3)` / `reset_warp()` / `reset_transform()`

Image data is read-only. Use `replace()` to change. Warp accessible via `.warp`.

## TextLayer

Classes: `TextLayer_8bit`, `TextLayer_16bit`, `TextLayer_32bit`.

### Text Content

- `layer.text` — read-only string
- `set_text(value)` / `replace_text(old, new, replace_all=True)`
- `set_text_equal_length(value)` / `replace_text_equal_length(old, new)` — safer for preserving style runs

### Font Management

- `font_count` / `font_postscript_name(idx)` / `font_name(idx)`
- `add_font(name)` / `find_font_index(name)`
- `set_font(postscript_name)` — sets across all runs
- `primary_font_name` / `used_font_names()`

### Style Runs

Access: `layer.style_run(idx)` returns proxy object.

Properties per run: `font_size`, `leading`, `auto_leading`, `kerning`, `fill_color`, `stroke_color`, `font`, `faux_bold`, `faux_italic`, `horizontal_scale`, `vertical_scale`, `tracking`, `baseline_shift`, `auto_kern`, `underline`, `strikethrough`, `ligatures`, `old_style`, `proportional_metrics`, `font_caps`, `font_baseline`, `no_break`

Getters: `style_run_font_size(idx)`, setters: `set_style_run_font_size(idx, val)`.

### Paragraph Runs

Access: `layer.paragraph_run(idx)` returns proxy.

Properties: `justification`, `auto_hyphenate`, `word_spacing`, `letter_spacing`, `glyph_spacing`, `first_line_indent`, `start_indent`, `end_indent`, `space_before`, `space_after`

### Transform

- `transform()` → `[xx, xy, yx, yy, tx, ty]` / `set_transform(values)`
- `rotation_angle` / `set_rotation_angle(degrees)`
- `scale_x` / `scale_y` / `set_scale(sx, sy)`
- `position()` → `(x, y)` / `set_position(x, y)`
- `reset_transform()`

### Warp

- `has_warp` / `warp_style` / `warp_value`
- `set_warp_style(style)` / `set_warp_value(val)`

## Geometry Module

```python
psapi.geometry.Point2D(x, y)        # 2D point with arithmetic
psapi.geometry.create_quad(w, h)    # corner quad
psapi.geometry.create_homography(src_quad, dst_quad)  # 3x3 projective matrix
```

## Low-Level: PhotoshopFile

For binary-level access. Sections: File Header, Color Mode Data, Image Resources, Layer and Mask Information, Additional Layer Info, Image Data.

- `PhotoshopFile.find_bitdepth(path)` — detect bit depth without full parse

## C++ Differences

Python uses `_Nbit` suffix instead of `<bppN_t>` template parameter.
Properties instead of getter/setter methods.
Image data as numpy arrays instead of `std::vector`.
`LayeredFile.read()` auto-detection is Python-only.
Progress callbacks are C++ only.
