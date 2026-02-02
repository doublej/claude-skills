---
name: icc-color-pdf
description: Manage ICC profiles and color spaces in PDF files. Covers RGB-to-CMYK conversion, ICC profile embedding/extraction, PDF/X and PDF/A output intents, color space analysis, ink coverage, preflight validation, and print-ready workflows using Ghostscript, pikepdf, Pillow/pyCMS, and Little-CMS.
---

# ICC Color & PDF Skill

Manage ICC color profiles and color spaces in PDF files for print and archival workflows.

## When to Use

- Converting PDF color spaces (RGB to CMYK, CMYK to gray, etc.)
- Embedding or extracting ICC profiles in PDFs
- Creating PDF/X prepress or PDF/A archival files with output intents
- Analyzing ink coverage or color spaces in a PDF
- Preflight validation of ICC profiles
- Building print-ready PDF pipelines

## Tools & Installation

```bash
# Core: Ghostscript (color conversion engine)
brew install ghostscript        # macOS
sudo apt install ghostscript    # Debian/Ubuntu

# Python: pikepdf (PDF structure), Pillow (image ICC), Little-CMS bindings
uv add pikepdf pillow
# or: pip install pikepdf pillow

# Little-CMS CLI utilities (transicc, jpgicc, tificc, linkicc)
brew install little-cms2        # macOS
sudo apt install liblcms2-utils # Debian/Ubuntu

# Validation
brew install verapdf            # PDF/A validation
# or download from https://verapdf.org
```

## Ghostscript Color Conversion

### RGB to CMYK

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sOutputFile=cmyk.pdf input.pdf
```

### RGB to CMYK with ICC Profile

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -dOverrideICC=true \
   -sOutputICCProfile=ISOcoated_v2_300_eci.icc \
   -sDefaultRGBProfile=sRGB.icc \
   -dRenderIntent=1 \
   -sOutputFile=cmyk_icc.pdf input.pdf
```

### CMYK to RGB

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=RGB \
   -dProcessColorModel=/DeviceRGB \
   -sOutputFile=rgb.pdf input.pdf
```

### To Grayscale

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=Gray \
   -dProcessColorModel=/DeviceGray \
   -sOutputFile=gray.pdf input.pdf
```

### Object-Type Color Management

Apply different ICC profiles per object type (text, images, vectors):

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sGraphicICCProfile=graphic.icc \
   -sImageICCProfile=image.icc \
   -sTextICCProfile=text.icc \
   -dGraphicIntent=1 \
   -dImageIntent=0 \
   -dTextIntent=1 \
   -sOutputFile=output.pdf input.pdf
```

Render intents: `0`=Perceptual, `1`=Relative Colorimetric, `2`=Saturation, `3`=Absolute Colorimetric.

## ICC Profile Parameters (Ghostscript)

| Parameter | Purpose |
|-----------|---------|
| `-sDefaultGrayProfile` | ICC for undefined gray spaces (default: `default_gray.icc`) |
| `-sDefaultRGBProfile` | ICC for undefined RGB spaces (default: `default_rgb.icc` = sRGB v2) |
| `-sDefaultCMYKProfile` | ICC for undefined CMYK spaces (default: `default_cmyk.icc`) |
| `-sOutputICCProfile` | ICC profile for the output device |
| `-sGraphicICCProfile` | ICC override for vector graphics |
| `-sImageICCProfile` | ICC override for images |
| `-sTextICCProfile` | ICC override for text |
| `-dOverrideICC` | Override document-embedded ICC profiles |
| `-dRenderIntent` | 0=Perceptual, 1=RelColorimetric, 2=Saturation, 3=AbsColorimetric |
| `-dDeviceGrayToK` | Map gray directly to K channel (avoids rich black) |
| `-dUseFastColor` | Non-ICC device-based conversion (fast but crude) |

## PDF/X Output with ICC

```bash
# PDF/X-3 with embedded output intent
gs -dPDFX -dBATCH -dNOPAUSE -dQUIET \
   -dProcessColorModel=/DeviceCMYK \
   -sColorConversionStrategy=CMYK \
   -sOutputICCProfile=ISOcoated_v2_300_eci.icc \
   -dRenderIntent=1 \
   -sDEVICE=pdfwrite \
   -sOutputFile=output_pdfx.pdf \
   PDFX_IntCmyk.ps input.pdf
```

The `PDFX_IntCmyk.ps` preamble file ships with Ghostscript (in `lib/`). It sets required PDF/X metadata.

## PDF/A with Output Intent

```bash
gs -dPDFA=2 -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=RGB \
   -sOutputICCProfile=srgb.icc \
   -sOutputFile=archive.pdf \
   PDFA_def.ps input.pdf
```

## Analysis & Preflight

### Ink Coverage

```bash
# Per-page CMYK ink percentages
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=inkcov input.pdf
```

Output: `C M Y K` percentages per page. Total >300% may cause print issues.

### Color Space Info

```bash
# List fonts, spot colors, metadata
gs -dBATCH -dNOPAUSE -dQUIET -dPDFINFO input.pdf
```

### veraPDF (PDF/A Validation)

```bash
# Validate PDF/A compliance including ICC profiles
verapdf --flavour 2b input.pdf

# Extract ICC profile info
verapdf --extract input.pdf
```

## Python: pikepdf

### Read Output Intent Profile

```python
import pikepdf

pdf = pikepdf.open("input.pdf")
for intent in pdf.Root.get("/OutputIntents", []):
    profile_stream = intent.get("/DestOutputProfile")
    if profile_stream:
        icc_data = bytes(profile_stream.read_bytes())
        with open("extracted_profile.icc", "wb") as f:
            f.write(icc_data)
```

### Add Output Intent (PDF/A or PDF/X)

```python
import pikepdf

pdf = pikepdf.open("input.pdf")
with open("sRGB.icc", "rb") as f:
    icc_data = f.read()

icc_stream = pdf.make_stream(icc_data)
icc_stream["/N"] = 3  # 3 for RGB, 4 for CMYK

output_intent = pikepdf.Dictionary({
    "/Type": pikepdf.Name("/OutputIntent"),
    "/S": pikepdf.Name("/GTS_PDFA1"),  # or /GTS_PDFX for PDF/X
    "/OutputConditionIdentifier": "sRGB IEC61966-2.1",
    "/DestOutputProfile": icc_stream,
})

if "/OutputIntents" not in pdf.Root:
    pdf.Root["/OutputIntents"] = pikepdf.Array()
pdf.Root["/OutputIntents"].append(output_intent)
pdf.save("output_with_intent.pdf")
```

### List Color Spaces per Page

```python
import pikepdf

pdf = pikepdf.open("input.pdf")
for i, page in enumerate(pdf.pages):
    resources = page.get("/Resources", {})
    cs = resources.get("/ColorSpace", {})
    print(f"Page {i+1}: {dict(cs)}")
```

## Python: Pillow + pyCMS

### Convert Image Color Space with ICC

```python
from PIL import Image, ImageCms

img = Image.open("photo.tiff")
srgb = ImageCms.createProfile("sRGB")
cmyk_profile = ImageCms.getOpenProfile("ISOcoated_v2_300_eci.icc")

transform = ImageCms.buildTransform(
    srgb, cmyk_profile, "RGB", "CMYK",
    renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
)
cmyk_img = ImageCms.applyTransform(img, transform)
cmyk_img.save("photo_cmyk.tiff")
```

### Read Embedded ICC Profile

```python
from PIL import Image

img = Image.open("photo.jpg")
icc = img.info.get("icc_profile")
if icc:
    with open("extracted.icc", "wb") as f:
        f.write(icc)
```

## Little-CMS CLI Tools

| Tool | Purpose |
|------|---------|
| `transicc` | Transform colors through ICC profile chains (text/CGATS input) |
| `jpgicc` | Apply ICC transforms to JPEG files |
| `tificc` | Apply ICC transforms to TIFF files |
| `linkicc` | Create device-link profiles from profile chains |
| `psicc` | Generate PostScript CRD from ICC profiles |

### Create Device Link Profile

```bash
# Chain source->destination into a single device link
linkicc -o devicelink.icc sRGB.icc ISOcoated_v2_300_eci.icc

# Use device link in Ghostscript
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sProofProfile=devicelink.icc \
   -sOutputFile=output.pdf input.pdf
```

### Transform Colors

```bash
# Interactive: type RGB values, get CMYK output
transicc -i sRGB.icc -o ISOcoated_v2_300_eci.icc

# From file
transicc -i sRGB.icc -o ISOcoated_v2_300_eci.icc < colors.txt
```

## Common ICC Profiles

| Profile | Color Space | Use Case |
|---------|-------------|----------|
| `sRGB IEC61966-2.1` | RGB | Web, general digital |
| `Adobe RGB (1998)` | RGB | Photography, wide gamut |
| `ISOcoated_v2_300_eci.icc` | CMYK | European coated paper (Fogra39) |
| `Fogra27L.icm` | CMYK | European uncoated paper |
| `USWebCoatedSWOP.icc` | CMYK | US web offset printing (SWOP) |
| `GRACoL2006_Coated1v2.icc` | CMYK | US commercial sheetfed |
| `JapanColor2001Coated.icc` | CMYK | Japanese coated paper |

ICC profile locations:
- macOS: `/Library/ColorSync/Profiles/` and `~/Library/ColorSync/Profiles/`
- Linux: `/usr/share/color/icc/` and `~/.local/share/icc/`
- Ghostscript built-in: run `gs -h` and check SearchPath entries, then look in `iccprofiles/`

## Reference Files

- [ghostscript-color-reference.md](references/ghostscript-color-reference.md) - Advanced Ghostscript ICC options, troubleshooting, known issues, PDF/X preamble details
- [python-color-workflows.md](references/python-color-workflows.md) - Full Python pipeline examples, batch processing, pikepdf advanced usage, img2pdf integration

### Grep Patterns for Reference Lookup

| Need | File | Pattern |
|------|------|---------|
| Black handling | ghostscript-color-reference.md | `black\|DeviceGrayToK\|rich black` |
| Spot colors | ghostscript-color-reference.md | `spot\|separation\|DeviceN` |
| PDF/X preamble | ghostscript-color-reference.md | `PDFX_Int\|preamble` |
| Troubleshooting | ghostscript-color-reference.md | `Troubleshoot\|washed\|pale` |
| Batch Python | python-color-workflows.md | `batch\|glob\|directory` |
| img2pdf | python-color-workflows.md | `img2pdf` |
| PDF/A Python | python-color-workflows.md | `PDF.A\|output.intent` |

## Documentation

- [Ghostscript Color Management](https://ghostscript.readthedocs.io/en/latest/GhostscriptColorManagement.html)
- [pikepdf Documentation](https://pikepdf.readthedocs.io/en/latest/)
- [Pillow ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html)
- [Little-CMS](https://www.littlecms.com/)
- [ICC Specification](https://www.color.org/specification/ICC.1-2022-05.pdf)
- [veraPDF](https://verapdf.org/)
