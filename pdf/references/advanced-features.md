# Ghostscript Advanced Features

## OCR (Optical Character Recognition)

Ghostscript can add invisible OCR text layers to scanned PDFs, making them searchable.

### OCR Devices

| Device | Description |
|--------|-------------|
| `pdfocr8` | PDF with OCR, 8-bit color |
| `pdfocr24` | PDF with OCR, 24-bit color |
| `pdfocr32` | PDF with OCR, 32-bit color |
| `ocr` | Plain UTF-8 text extraction via OCR |
| `hocr` | hOCR formatted output |

### Create Searchable PDF from Scanned Images

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfocr24 \
   -r300 \
   -sOutputFile=searchable.pdf \
   scanned.pdf
```

### OCR with pdfwrite

Use `-sUseOCR` to add OCR text during PDF processing:

```bash
# Always apply OCR
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sUseOCR=Always \
   -sOutputFile=searchable.pdf \
   scanned.pdf

# Only OCR pages without text
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sUseOCR=AsNeeded \
   -sOutputFile=searchable.pdf \
   mixed.pdf
```

Values: `Never` (default), `AsNeeded`, `Always`

### Extract Text via OCR

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=ocr \
   -sOutputFile=extracted.txt \
   scanned.pdf
```

## PDF/A (Archival PDF)

PDF/A ensures long-term preservation by embedding all resources and disabling features that hinder archival.

### Basic PDF/A Creation

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFA=2 \
   -dPDFACompatibilityPolicy=1 \
   -sColorConversionStrategy=RGB \
   -sOutputFile=archive.pdf \
   input.pdf
```

### PDF/A Versions

| Flag | Standard | Notes |
|------|----------|-------|
| `-dPDFA=1` | PDF/A-1b | Most compatible, PDF 1.4 based |
| `-dPDFA=2` | PDF/A-2b | Supports JPEG2000, transparency |
| `-dPDFA=3` | PDF/A-3b | Allows embedded files |

### PDF/A Compatibility Policy

| Value | Behavior |
|-------|----------|
| `0` | Include incompatible features (non-compliant) |
| `1` | Ignore/skip incompatible features |
| `2` | Abort on incompatible features |

### Full PDF/A with ICC Profile

For strict compliance, provide a PDFA definition file:

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFA=2 \
   -dPDFACompatibilityPolicy=1 \
   -sColorConversionStrategy=RGB \
   -dNoOutputFonts=false \
   -sOutputFile=archive.pdf \
   PDFA_def.ps \
   input.pdf
```

## PDF/X (Prepress PDF)

PDF/X is designed for reliable print production exchange.

### Basic PDF/X Creation

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFX=3 \
   -sColorConversionStrategy=CMYK \
   -sOutputFile=prepress.pdf \
   input.pdf
```

### PDF/X Versions

| Flag | Standard | Color Space |
|------|----------|-------------|
| `-dPDFX=1` | PDF/X-1a | CMYK + Spot only |
| `-dPDFX=3` | PDF/X-3 | CMYK + ICC profiles |
| `-dPDFX=4` | PDF/X-4 | CMYK + transparency |

**Note:** RGB is prohibited in PDF/X. Use `-sColorConversionStrategy=CMYK` or `Gray`.

## Font Embedding Control

### Convert All Text to Outlines

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dNoOutputFonts \
   -sOutputFile=outlined.pdf \
   input.pdf
```

### Control Font Compression

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dCompressFonts=true \
   -sOutputFile=output.pdf \
   input.pdf
```

### Embed Substitute Fonts

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dEmbedSubstituteFonts=true \
   -sOutputFile=output.pdf \
   input.pdf
```

### Specify Font Search Path

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sFONTPATH=/path/to/fonts \
   -sOutputFile=output.pdf \
   input.pdf
```

## Custom Image Resampling

Fine-grained control over how images are downsampled during PDF optimization.

### Bicubic Downsampling to Custom DPI

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=150 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=150 \
   -dMonoImageDownsampleType=/Bicubic \
   -dMonoImageResolution=300 \
   -sOutputFile=optimized.pdf \
   input.pdf
```

### Downsample Types

| Type | Quality | Speed |
|------|---------|-------|
| `/Subsample` | Low | Fast |
| `/Average` | Medium | Medium |
| `/Bicubic` | High (Mitchell filter) | Slow |

### Disable Downsampling

```bash
-dColorImageDownsampleType=/None \
-dGrayImageDownsampleType=/None \
-dMonoImageDownsampleType=/None
```

## PDF Compatibility Levels

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -sOutputFile=output.pdf \
   input.pdf
```

| Level | PDF Version | Key Feature |
|-------|-------------|-------------|
| `1.2` | Acrobat 3 | Baseline |
| `1.3` | Acrobat 4 | No transparency support |
| `1.4` | Acrobat 5 | Transparency, 128-bit encryption |
| `1.5` | Acrobat 6 | Object streams, JPEG2000 |
| `1.6` | Acrobat 7 | OpenType font embedding |
| `1.7` | Acrobat 8 | AES encryption |
| `2.0` | PDF 2.0 | Latest standard |

### Flatten Transparency for Older Viewers

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.3 \
   -dHaveTransparency=false \
   -sOutputFile=flat.pdf \
   input.pdf
```

## Linearization (Fast Web View)

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFastWebView=true \
   -sOutputFile=linearized.pdf \
   input.pdf
```

## Interpolation Control

```bash
# Fine-tune image scaling quality
# Value >1: only interpolate when scale factor exceeds value
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=png16m -r300 \
   -dInterpolateControl=4 \
   -sOutputFile=output.png \
   input.pdf
```

**Note:** `-dDOINTERPOLATE` and `-dNOINTERPOLATE` are deprecated; use `-dInterpolateControl` instead.
