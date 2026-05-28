# Image Operations Reference

General Pillow operations for manipulation, format conversion, batch processing.

## Resize

```python
from PIL import Image

# Exact size (may distort)
resized = img.resize((800, 600), Image.Resampling.LANCZOS)

# Thumbnail (preserves aspect, modifies in-place)
img.thumbnail((800, 800), Image.Resampling.LANCZOS)

# Resize to width, preserve aspect
ratio = 800 / img.width
resized = img.resize((800, int(img.height * ratio)), Image.Resampling.LANCZOS)
```

## Crop

```python
cropped = img.crop((100, 100, 500, 400))  # (left, upper, right, lower)

# Center crop to square
s = min(img.size)
left = (img.width - s) // 2
top = (img.height - s) // 2
square = img.crop((left, top, left + s, top + s))
```

## Rotate & Flip

```python
rotated = img.rotate(45, expand=True, fillcolor="white")
flipped_h = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
flipped_v = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
```

## Filters

```python
from PIL import ImageFilter

blurred = img.filter(ImageFilter.GaussianBlur(radius=5))
sharp = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
edges = img.filter(ImageFilter.FIND_EDGES)
```

## Brightness / Contrast / Color

```python
from PIL import ImageEnhance

ImageEnhance.Brightness(img).enhance(1.3)
ImageEnhance.Contrast(img).enhance(1.5)
ImageEnhance.Color(img).enhance(0.0)       # 0 = grayscale
ImageEnhance.Sharpness(img).enhance(2.0)
```

## Format Conversion

```python
img.save("output.jpg", quality=95, optimize=True, progressive=True)
img.save("output.webp", quality=80, method=6)
img.save("output.png", optimize=True)
img.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
```

### Mode conversion

```python
rgba = img.convert("RGBA")
rgb = img.convert("RGB")
gray = img.convert("L")

# RGBA -> RGB with custom background
bg = Image.new("RGB", img.size, (255, 255, 255))
bg.paste(img, mask=img.split()[3])
```

## Batch Processing

```python
from pathlib import Path

def batch_convert(src_dir, dst_dir, fmt="webp", **save_kwargs):
    dst = Path(dst_dir)
    dst.mkdir(parents=True, exist_ok=True)
    for f in Path(src_dir).iterdir():
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}:
            img = Image.open(f)
            if img.mode == "RGBA" and fmt == "jpeg":
                img = img.convert("RGB")
            img.save(dst / f"{f.stem}.{fmt}", **save_kwargs)
```

## Color Management

```python
from PIL import ImageCms

srgb = ImageCms.createProfile("sRGB")
target = ImageCms.getOpenProfile("AdobeRGB1998.icc")
transform = ImageCms.buildTransform(srgb, target, "RGB", "RGB")
converted = ImageCms.applyTransform(img, transform)
```

For print workflows (CMYK, PDF/X), use the **pdf-icc** skill.

## Gotchas

- `Image.open()` is lazy -- call `.load()` or `.copy()` before closing the file
- `thumbnail()` modifies in-place; `resize()` returns a new image
- Saving RGBA as JPEG fails -- convert to RGB first
- `paste()` without mask ignores source alpha -- always pass `mask=overlay`
- `putpixel()` is slow -- use NumPy for bulk pixel ops
- Default `Image.Resampling.NEAREST` looks blocky -- use `LANCZOS` for photos
- macOS fonts: `/System/Library/Fonts/` and `/Library/Fonts/`
