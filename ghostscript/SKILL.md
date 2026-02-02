---
name: ghostscript
description: Comprehensive Ghostscript command-line reference for PDF/PostScript manipulation. Covers PDF merging, splitting, compression, format conversion (PDF/PS/EPS/images), rasterization, OCR, PDF/A archival, and optimization. Use when working with PDF processing, converting between document formats, extracting images from PDFs, or batch document operations.
---

# Ghostscript Skill

Command-line reference for Ghostscript PDF and PostScript processing.

## When to Use

- Merging or splitting PDF files
- Compressing/optimizing PDFs for web or print
- Converting PDF to images (PNG, JPEG, TIFF, PSD)
- Converting between PDF, PostScript, and EPS
- Extracting pages or text from PDFs
- Creating PDF/A archival or PDF/X prepress files
- Adding OCR text layers to scanned PDFs
- Batch document processing
- Ink coverage analysis for print jobs

## Installation

```bash
# macOS
brew install ghostscript

# Ubuntu/Debian
sudo apt install ghostscript

# Check version
gs --version
```

## Basic Syntax

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

## Common Tasks

### Merge PDFs

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=merged.pdf \
   file1.pdf file2.pdf file3.pdf
```

### Extract Pages

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

### Compress PDF

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

### PDF to Images

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

### Convert to Grayscale

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dColorConversionStrategy=/Gray \
   -dProcessColorModel=/DeviceGray \
   -sOutputFile=grayscale.pdf input.pdf
```

### Extract Text

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=txtwrite \
   -sOutputFile=output.txt input.pdf
```

### PDF Info & Diagnostics

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

## Quick Reference Tables

### PDF Settings

| Setting | DPI | Use Case |
|---------|-----|----------|
| `/screen` | 72 | Web viewing |
| `/ebook` | 150 | Digital reading |
| `/printer` | 300 | Office printing |
| `/prepress` | 300 | Professional print |
| `/default` | - | Balanced |

### Key Devices

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
| `bbox` | — | Bounding box info |
| `inkcov` | — | Ink coverage % |
| `pdfocr24` | PDF+OCR | OCR text layer |
| `nullpage` | — | Validation only |

## Reference Files

For advanced usage, consult the reference files:

- [command-reference.md](references/command-reference.md) - Password protection, page rotation, N-up printing, custom compression, batch processing, resize/scale, troubleshooting
- [conversion-examples.md](references/conversion-examples.md) - Format conversion recipes (PDF↔PS, PDF↔EPS, PDF/A, PDF/X, linearization, metadata removal)
- [advanced-features.md](references/advanced-features.md) - OCR, PDF/A & PDF/X creation, font embedding control, custom image resampling, compatibility levels

### Grep patterns for reference lookup

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

## Documentation

- [Ghostscript Docs](https://ghostscript.readthedocs.io/en/latest/Use.html)
- [pdfwrite Device](https://ghostscript.readthedocs.io/en/latest/VectorDevices.html)
- [Output Devices](https://ghostscript.readthedocs.io/en/latest/Devices.html)
