---
name: pdf
description: >
  Unified PDF skill. Use when:
  (1) generating PDFs programmatically with ReportLab — Canvas API, Platypus layouts, tables, charts, fonts, images;
  (2) managing ICC color profiles and color spaces — RGB-to-CMYK conversion, profile embedding/extraction, PDF/X and PDF/A output intents, ink coverage, preflight;
  (3) processing PDFs with Ghostscript CLI — merging, splitting, compression, format conversion, rasterization, OCR, batch operations.
  Replaces reportlab-pdf, icc-color-pdf, ghostscript.
---

# PDF Skill

Three branches. Pick the right one, or combine.

## Which Branch?

| Task | Branch |
|------|--------|
| Create PDFs from Python — reports, invoices, charts, vector graphics | [ReportLab](#reportlab) |
| Color management — ICC profiles, RGB/CMYK conversion, output intents, preflight | [Color](#color) |
| CLI PDF processing — merge, split, compress, rasterize, convert formats, OCR | [Ghostscript](#ghostscript) |

---

## ReportLab

Generate PDFs with ReportLab 4.x in Python.

### When to Use

- Creating PDFs programmatically from Python
- Building reports with tables, charts, and formatted text
- Generating invoices, certificates, or data-driven documents
- Drawing vector graphics and shapes
- Complex multi-page layouts with headers/footers

### Version & Installation

```bash
uv add reportlab
# or
pip install reportlab
```

- Latest: ReportLab 4.4.5
- Python: 3.9 - 3.13

### Architecture Overview

| API | Level | Use Case |
|-----|-------|----------|
| **Canvas** | Low-level | Direct PDF drawing, absolute positioning |
| **Platypus** | High-level | Document templates, flowable content |

**Rule of thumb:** Use Platypus for documents, Canvas for custom graphics.

### Canvas Quick Start

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=A4)
width, height = A4  # 595.27, 841.89 points

c.setFont("Helvetica", 12)
c.drawString(100, 750, "Hello, ReportLab!")

c.showPage()
c.save()
```

### Platypus Quick Start

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("This is a heading", styles['Heading1']))
story.append(Spacer(1, 12))
story.append(Paragraph("This is body text. " * 50, styles['Normal']))

doc.build(story)
```

### Basic Table

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ['Name', 'Age', 'City'],
    ['Alice', '30', 'New York'],
    ['Bob', '25', 'Los Angeles'],
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(table)
```

### Quick Reference

| Task | Method |
|------|--------|
| Create PDF | `canvas.Canvas("file.pdf")` |
| Draw text | `c.drawString(x, y, "text")` |
| Draw line | `c.line(x1, y1, x2, y2)` |
| Draw rectangle | `c.rect(x, y, w, h)` |
| Set font | `c.setFont("Helvetica", 12)` |
| Set color | `c.setFillColor(colors.red)` |
| New page | `c.showPage()` |
| Save PDF | `c.save()` |
| Simple doc | `SimpleDocTemplate("file.pdf")` |
| Add paragraph | `story.append(Paragraph(text, style))` |
| Add table | `story.append(Table(data))` |
| Build doc | `doc.build(story)` |

### Reference Files

- [Canvas API](references/canvas-api.md) - Text, shapes, colors, images, state management
- [Platypus Guide](references/platypus-guide.md) - Flowables, styles, tables, page templates
- [Charts & Patterns](references/charts-patterns.md) - Graphics, charts, invoice template

---

## Color

Manage ICC color profiles and color spaces in PDF files for print and archival workflows.

### When to Use

- Converting PDF color spaces (RGB to CMYK, CMYK to gray, etc.)
- Embedding or extracting ICC profiles in PDFs
- Creating PDF/X prepress or PDF/A archival files with output intents
- Analyzing ink coverage or color spaces in a PDF
- Preflight validation of ICC profiles
- Building print-ready PDF pipelines

### Tools & Installation

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

### Ghostscript Color Conversion

#### RGB to CMYK

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sOutputFile=cmyk.pdf input.pdf
```

#### RGB to CMYK with ICC Profile

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

#### CMYK to RGB

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=RGB \
   -dProcessColorModel=/DeviceRGB \
   -sOutputFile=rgb.pdf input.pdf
```

#### To Grayscale

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=Gray \
   -dProcessColorModel=/DeviceGray \
   -sOutputFile=gray.pdf input.pdf
```

#### Object-Type Color Management

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

### ICC Profile Parameters (Ghostscript)

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

### ColorConversionStrategy Options

| Strategy | Behavior |
|----------|----------|
| `LeaveColorUnchanged` | No conversion; preserves all color spaces including spot |
| `CMYK` | Convert everything to CMYK process |
| `RGB` | Convert everything to RGB |
| `Gray` | Convert everything to grayscale |
| `UseDeviceIndependentColor` | Convert to CIE-based color (for PDF/X) |

### PDF/X Output with ICC

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

### PDF/A with Output Intent

```bash
gs -dPDFA=2 -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=RGB \
   -sOutputICCProfile=srgb.icc \
   -sOutputFile=archive.pdf \
   PDFA_def.ps input.pdf
```

### Analysis & Preflight

#### Ink Coverage

```bash
# Per-page CMYK ink percentages
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=inkcov input.pdf
```

Output: `C M Y K` percentages per page. Total >300% may cause print issues.

#### Color Space Info

```bash
# List fonts, spot colors, metadata
gs -dBATCH -dNOPAUSE -dQUIET -dPDFINFO input.pdf
```

#### veraPDF (PDF/A Validation)

```bash
# Validate PDF/A compliance including ICC profiles
verapdf --flavour 2b input.pdf

# Extract ICC profile info
verapdf --extract input.pdf
```

### Python: pikepdf

#### Read Output Intent Profile

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

#### Add Output Intent (PDF/A or PDF/X)

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

#### List Color Spaces per Page

```python
import pikepdf

pdf = pikepdf.open("input.pdf")
for i, page in enumerate(pdf.pages):
    resources = page.get("/Resources", {})
    cs = resources.get("/ColorSpace", {})
    print(f"Page {i+1}: {dict(cs)}")
```

### Python: Pillow + pyCMS

#### Convert Image Color Space with ICC

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

#### Read Embedded ICC Profile

```python
from PIL import Image

img = Image.open("photo.jpg")
icc = img.info.get("icc_profile")
if icc:
    with open("extracted.icc", "wb") as f:
        f.write(icc)
```

### Little-CMS CLI Tools

| Tool | Purpose |
|------|---------|
| `transicc` | Transform colors through ICC profile chains (text/CGATS input) |
| `jpgicc` | Apply ICC transforms to JPEG files |
| `tificc` | Apply ICC transforms to TIFF files |
| `linkicc` | Create device-link profiles from profile chains |
| `psicc` | Generate PostScript CRD from ICC profiles |

#### Create Device Link Profile

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

#### Transform Colors

```bash
# Interactive: type RGB values, get CMYK output
transicc -i sRGB.icc -o ISOcoated_v2_300_eci.icc

# From file
transicc -i sRGB.icc -o ISOcoated_v2_300_eci.icc < colors.txt
```

### Common ICC Profiles

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

### Reference Files

- [Ghostscript Color Reference](references/ghostscript-color-reference.md) - Advanced Ghostscript ICC options, troubleshooting, known issues, PDF/X preamble details
- [Python Color Workflows](references/python-color-workflows.md) - Full Python pipeline examples, batch processing, pikepdf advanced usage, img2pdf integration

#### Grep Patterns for Color Reference Lookup

| Need | File | Pattern |
|------|------|---------|
| Black handling | ghostscript-color-reference.md | `black\|DeviceGrayToK\|rich black` |
| Spot colors | ghostscript-color-reference.md | `spot\|separation\|DeviceN` |
| PDF/X preamble | ghostscript-color-reference.md | `PDFX_Int\|preamble` |
| Troubleshooting | ghostscript-color-reference.md | `Troubleshoot\|washed\|pale` |
| Batch Python | python-color-workflows.md | `batch\|glob\|directory` |
| img2pdf | python-color-workflows.md | `img2pdf` |
| PDF/A Python | python-color-workflows.md | `PDF.A\|output.intent` |

---

## Ghostscript

Command-line reference for Ghostscript PDF and PostScript processing.

### When to Use

- Merging or splitting PDF files
- Compressing/optimizing PDFs for web or print
- Converting PDF to images (PNG, JPEG, TIFF, PSD)
- Converting between PDF, PostScript, and EPS
- Extracting pages or text from PDFs
- Creating PDF/A archival or PDF/X prepress files
- Adding OCR text layers to scanned PDFs
- Batch document processing

### Installation

```bash
# macOS
brew install ghostscript

# Ubuntu/Debian
sudo apt install ghostscript

# Check version
gs --version
```

### Basic Syntax

```bash
gs [options] [files]
```

Core flags:
- `-dBATCH` - Exit after processing (no interactive prompt)
- `-dNOPAUSE` - Don't pause between pages
- `-dQUIET` - Suppress output messages
- `-dSAFER` - Restrict file operations (security)
- `-o output` - Shorthand for `-dBATCH -dNOPAUSE -sOutputFile=output`

**Standard invocation pattern:**
```bash
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=<device> -sOutputFile=<output> <input>

# Equivalent shorthand:
gs -dQUIET -sDEVICE=<device> -o <output> <input>
```

### Common Tasks

#### Merge PDFs

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=merged.pdf \
   file1.pdf file2.pdf file3.pdf
```

#### Extract Pages

```bash
# Single page
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFirstPage=3 -dLastPage=3 \
   -sOutputFile=page3.pdf input.pdf

# Range
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFirstPage=5 -dLastPage=10 \
   -sOutputFile=pages5-10.pdf input.pdf

# Complex page selection (even/odd, ranges)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sPageList="1,3,5-10,even" \
   -sOutputFile=selected.pdf input.pdf

# Split into individual pages
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=page_%03d.pdf input.pdf
```

#### Compress PDF

```bash
# Web quality (72 dpi, smallest)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/screen \
   -sOutputFile=compressed.pdf input.pdf

# Print quality (300 dpi)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/printer \
   -sOutputFile=compressed.pdf input.pdf
```

#### PDF to Images

```bash
# PNG (24-bit, 300 dpi)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=png16m -r300 \
   -sOutputFile=page_%03d.png input.pdf

# PNG with transparency
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pngalpha -r300 \
   -sOutputFile=page_%03d.png input.pdf

# JPEG (quality 90)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=jpeg -dJPEGQ=90 -r300 \
   -sOutputFile=page_%03d.jpg input.pdf

# TIFF
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=tiff24nc -r300 \
   -sOutputFile=page_%03d.tiff input.pdf

# PSD (Photoshop)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=psdcmyk -r300 \
   -sOutputFile=page_%03d.psd input.pdf
```

#### Extract Text

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=txtwrite \
   -sOutputFile=output.txt input.pdf
```

#### PDF Info & Diagnostics

```bash
# Page count
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=nullpage \
   -c "input.pdf (r) file runpdfbegin pdfpagecount = quit"

# File metadata, fonts, spot colors
gs -dBATCH -dNOPAUSE -dQUIET -dPDFINFO input.pdf

# Bounding box detection
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=bbox input.pdf

# Ink coverage analysis (per page CMYK percentages)
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=inkcov input.pdf
```

### Quick Reference Tables

#### PDF Settings

| Setting | DPI | Use Case |
|---------|-----|----------|
| `/screen` | 72 | Web viewing |
| `/ebook` | 150 | Digital reading |
| `/printer` | 300 | Office printing |
| `/prepress` | 300 | Professional print |
| `/default` | - | Balanced |

#### Key Devices

| Device | Format | Notes |
|--------|--------|-------|
| `pdfwrite` | PDF | Create/modify PDFs |
| `ps2write` | PostScript | Level 2 PS |
| `eps2write` | EPS | Encapsulated PS |
| `png16m` | PNG 24-bit | Standard raster |
| `pngalpha` | PNG transparent | Alpha channel |
| `pnggray` | PNG grayscale | B&W |
| `jpeg` / `jpeggray` | JPEG | Lossy raster |
| `tiff24nc` / `tiffgray` | TIFF | Print-quality |
| `psdcmyk` / `psdrgb` | PSD | Photoshop format |
| `txtwrite` | Text | Text extraction |
| `bbox` | -- | Bounding box info |
| `inkcov` | -- | Ink coverage % |
| `pdfocr24` | PDF+OCR | OCR text layer |
| `nullpage` | -- | Validation only |

### Reference Files

- [Command Reference](references/command-reference.md) - Password protection, page rotation, N-up printing, custom compression, batch processing, resize/scale, troubleshooting
- [Conversion Examples](references/conversion-examples.md) - Format conversion recipes (PDF<>PS, PDF<>EPS, PDF/A, PDF/X, linearization, metadata removal)
- [Advanced Features](references/advanced-features.md) - OCR, PDF/A & PDF/X creation, font embedding control, custom image resampling, compatibility levels

#### Grep Patterns for Ghostscript Reference Lookup

| Need | File | Pattern |
|------|------|---------|
| Password | command-reference.md | `Password` |
| Rotation | command-reference.md | `Rotate` |
| N-up | command-reference.md | `N-up\|NupXY` |
| Batch processing | command-reference.md | `Batch` |
| PDF/A archival | advanced-features.md | `PDF/A` |
| PDF/X prepress | advanced-features.md | `PDF/X` |
| OCR | advanced-features.md | `OCR` |
| Font embedding | advanced-features.md | `Font` |
| Image resampling | advanced-features.md | `Resamp\|Downsample` |

---

## Reference Files

All reference files live in `references/`:

### ReportLab

- `references/canvas-api.md` -- Coordinate system, text, fonts, colors, shapes, paths, images, state management
- `references/platypus-guide.md` -- Flowables, paragraph styles, tables, headers/footers, multi-column layout
- `references/charts-patterns.md` -- Drawing objects, bar/pie/line charts, invoice template, report patterns

### Color

- `references/ghostscript-color-reference.md` -- Black handling, spot colors, PDF/X preambles, overriding ICC, troubleshooting, device link profiles, proofing
- `references/python-color-workflows.md` -- Batch conversion, pikepdf advanced (extract/audit/replace profiles), img2pdf, PDF/A compliance, Pillow batch workflows

### Ghostscript

- `references/command-reference.md` -- Output devices, PDF settings, resolution, compression, passwords, rotation, N-up, resize, batch processing, troubleshooting
- `references/conversion-examples.md` -- Merge, split, compress, linearize, PDF/A, metadata removal, PDF/PS/EPS conversion, rasterization, text extraction, grayscale
- `references/advanced-features.md` -- OCR devices, PDF/A versions & compliance, PDF/X versions, font embedding, image resampling, compatibility levels, transparency flattening

## Documentation

### ReportLab
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Official Documentation](https://docs.reportlab.com/)
- [PyPI Package](https://pypi.org/project/reportlab/)

### Color Management
- [Ghostscript Color Management](https://ghostscript.readthedocs.io/en/latest/GhostscriptColorManagement.html)
- [pikepdf Documentation](https://pikepdf.readthedocs.io/en/latest/)
- [Pillow ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html)
- [Little-CMS](https://www.littlecms.com/)
- [ICC Specification](https://www.color.org/specification/ICC.1-2022-05.pdf)
- [veraPDF](https://verapdf.org/)

### Ghostscript
- [Ghostscript Docs](https://ghostscript.readthedocs.io/en/latest/Use.html)
- [pdfwrite Device](https://ghostscript.readthedocs.io/en/latest/VectorDevices.html)
- [Output Devices](https://ghostscript.readthedocs.io/en/latest/Devices.html)
