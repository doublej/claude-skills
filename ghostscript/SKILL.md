---
name: ghostscript
description: Comprehensive Ghostscript command-line reference for PDF/PostScript manipulation. Covers PDF merging, splitting, compression, format conversion (PDF/PS/EPS/images), rasterization, and optimization. Use when working with PDF processing, converting between document formats, extracting images from PDFs, or batch document operations.
---

# Ghostscript Skill

Command-line reference for Ghostscript PDF and PostScript processing.

## When to Use

- Merging or splitting PDF files
- Compressing/optimizing PDFs for web or print
- Converting PDF to images (PNG, JPEG, TIFF)
- Converting between PDF, PostScript, and EPS
- Extracting pages from PDFs
- Batch document processing
- Rasterizing vector documents

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

Common flags:
- `-dBATCH` - Exit after processing (no interactive prompt)
- `-dNOPAUSE` - Don't pause between pages
- `-dQUIET` - Suppress output messages
- `-dSAFER` - Restrict file operations (security)

**Standard invocation pattern:**
```bash
gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=<device> -sOutputFile=<output> <input>
```

## Output Devices

| Device | Format | Use Case |
|--------|--------|----------|
| `pdfwrite` | PDF | Create/modify PDFs |
| `ps2write` | PostScript | Convert to PS |
| `eps2write` | EPS | Encapsulated PostScript |
| `png16m` | PNG (24-bit) | High-quality images |
| `pnggray` | PNG (grayscale) | B&W documents |
| `pngalpha` | PNG (alpha) | Transparent background |
| `jpeg` | JPEG | Compressed images |
| `jpeggray` | JPEG (grayscale) | B&W compressed |
| `tiff24nc` | TIFF (24-bit) | Print-quality images |
| `tiffgray` | TIFF (grayscale) | B&W print |
| `bmp16m` | BMP | Windows bitmap |
| `pcx24b` | PCX | Legacy format |
| `pdfimage8` | PDF (image) | Rasterized PDF |
| `txtwrite` | Text | Extract text content |
| `docxwrite` | DOCX | Microsoft Word |

## PDF Operations

### Merge PDFs

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=merged.pdf \
   file1.pdf file2.pdf file3.pdf
```

### Split PDF (Extract Pages)

Extract single page:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFirstPage=3 -dLastPage=3 \
   -sOutputFile=page3.pdf \
   input.pdf
```

Extract page range:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFirstPage=5 -dLastPage=10 \
   -sOutputFile=pages5-10.pdf \
   input.pdf
```

Split into individual pages:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=page_%03d.pdf \
   input.pdf
```

### Compress PDF

**Screen quality (72 dpi, smallest size):**
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/screen \
   -sOutputFile=compressed.pdf \
   input.pdf
```

**Ebook quality (150 dpi):**
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/ebook \
   -sOutputFile=compressed.pdf \
   input.pdf
```

**Print quality (300 dpi):**
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/printer \
   -sOutputFile=compressed.pdf \
   input.pdf
```

**Prepress quality (300 dpi, color preserving):**
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/prepress \
   -sOutputFile=compressed.pdf \
   input.pdf
```

### PDF Settings Comparison

| Setting | DPI | Image Quality | File Size | Use Case |
|---------|-----|---------------|-----------|----------|
| `/screen` | 72 | Low | Smallest | Web viewing |
| `/ebook` | 150 | Medium | Small | Digital reading |
| `/printer` | 300 | High | Medium | Office printing |
| `/prepress` | 300 | Highest | Large | Professional print |
| `/default` | - | Balanced | Medium | General use |

### Custom Compression Settings

Fine-grained control over image compression:
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

### Linearize PDF (Fast Web View)

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFastWebView=true \
   -sOutputFile=linearized.pdf \
   input.pdf
```

### Convert to PDF/A (Archival)

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dPDFA=2 \
   -dPDFACompatibilityPolicy=1 \
   -sOutputFile=archive.pdf \
   input.pdf
```

### Remove Metadata

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFastWebView=false \
   -sOutputFile=clean.pdf \
   -c "[/Title () /Author () /Subject () /Keywords () /Creator () /Producer () /DOCINFO pdfmark" \
   -f input.pdf
```

## Format Conversion

### PDF to PostScript

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=ps2write \
   -sOutputFile=output.ps \
   input.pdf
```

### PostScript to PDF

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=output.pdf \
   input.ps
```

Or use the wrapper script:
```bash
ps2pdf input.ps output.pdf
```

### PDF to EPS

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=eps2write \
   -sOutputFile=output.eps \
   input.pdf
```

### EPS to PDF

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dEPSCrop \
   -sOutputFile=output.pdf \
   input.eps
```

## Image Extraction / Rasterization

### PDF to PNG

Single page or all pages:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=png16m \
   -r300 \
   -sOutputFile=page_%03d.png \
   input.pdf
```

Specific page:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=png16m \
   -r300 \
   -dFirstPage=1 -dLastPage=1 \
   -sOutputFile=page1.png \
   input.pdf
```

With transparency:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pngalpha \
   -r300 \
   -sOutputFile=page_%03d.png \
   input.pdf
```

### PDF to JPEG

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=jpeg \
   -dJPEGQ=90 \
   -r300 \
   -sOutputFile=page_%03d.jpg \
   input.pdf
```

### PDF to TIFF

High-quality for print:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=tiff24nc \
   -r300 \
   -sOutputFile=page_%03d.tiff \
   input.pdf
```

Multi-page TIFF:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=tiff24nc \
   -r300 \
   -sOutputFile=output.tiff \
   input.pdf
```

### Resolution Guide

| Use Case | Resolution | Flag |
|----------|------------|------|
| Screen/Web | 72-96 dpi | `-r72` |
| Ebook/Preview | 150 dpi | `-r150` |
| Print quality | 300 dpi | `-r300` |
| High-res print | 600 dpi | `-r600` |

### Custom Page Size

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=png16m \
   -r300 \
   -g2550x3300 \
   -sOutputFile=output.png \
   input.pdf
```

Note: `-g` uses pixels (width x height at specified DPI)

### Resize/Scale Output

Fit to specific dimensions:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dFIXEDMEDIA \
   -dPDFFitPage \
   -dDEVICEWIDTHPOINTS=612 \
   -dDEVICEHEIGHTPOINTS=792 \
   -sOutputFile=resized.pdf \
   input.pdf
```

## Text Extraction

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=txtwrite \
   -sOutputFile=output.txt \
   input.pdf
```

## Grayscale Conversion

Convert color PDF to grayscale:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dColorConversionStrategy=/Gray \
   -dProcessColorModel=/DeviceGray \
   -sOutputFile=grayscale.pdf \
   input.pdf
```

## Password Protection

### Add Password

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOwnerPassword=owner123 \
   -sUserPassword=user456 \
   -dEncryptionR=3 \
   -sOutputFile=protected.pdf \
   input.pdf
```

### Remove Password (if you have it)

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sPDFPassword=thepassword \
   -sOutputFile=unlocked.pdf \
   input.pdf
```

## Page Manipulation

### Rotate Pages

Rotate all pages 90 degrees:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=rotated.pdf \
   -c "<</Orientation 1>> setpagedevice" \
   -f input.pdf
```

### N-up Printing (Multiple Pages Per Sheet)

2-up:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dNupXY="2x1" \
   -sOutputFile=2up.pdf \
   input.pdf
```

4-up:
```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dNupXY="2x2" \
   -sOutputFile=4up.pdf \
   input.pdf
```

## Batch Processing

### Process Multiple Files

```bash
for f in *.pdf; do
    gs -dBATCH -dNOPAUSE -dQUIET \
       -sDEVICE=pdfwrite \
       -dPDFSETTINGS=/ebook \
       -sOutputFile="compressed_${f}" \
       "$f"
done
```

### Convert Directory of Images to PDF

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=combined.pdf \
   image1.jpg image2.jpg image3.jpg
```

## Troubleshooting

### Common Issues

**"Unable to open initial device"**
- Check device name spelling
- Verify Ghostscript installation

**Output is blank**
- Add `-dSAFER` flag
- Check input file isn't corrupted

**Poor image quality**
- Increase resolution: `-r300`
- Use `/prepress` instead of `/screen`

**File size too large**
- Use lower `-dPDFSETTINGS`
- Reduce image resolution

### Verbose Output

For debugging, remove `-dQUIET`:
```bash
gs -dBATCH -dNOPAUSE \
   -sDEVICE=pdfwrite \
   -sOutputFile=output.pdf \
   input.pdf
```

### Check PDF Info

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=nullpage \
   -c "input.pdf (r) file runpdfbegin pdfpagecount = quit"
```

## Quick Reference

| Task | Command |
|------|---------|
| Merge PDFs | `gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=out.pdf a.pdf b.pdf` |
| Extract page | `gs ... -dFirstPage=N -dLastPage=N -sOutputFile=page.pdf input.pdf` |
| Compress (web) | `gs ... -dPDFSETTINGS=/screen -sOutputFile=small.pdf input.pdf` |
| Compress (print) | `gs ... -dPDFSETTINGS=/printer -sOutputFile=print.pdf input.pdf` |
| PDF to PNG | `gs ... -sDEVICE=png16m -r300 -sOutputFile=page_%03d.png input.pdf` |
| PDF to JPEG | `gs ... -sDEVICE=jpeg -dJPEGQ=90 -r300 -sOutputFile=out.jpg input.pdf` |
| Grayscale | `gs ... -dColorConversionStrategy=/Gray -sOutputFile=gray.pdf input.pdf` |
| PS to PDF | `gs ... -sDEVICE=pdfwrite -sOutputFile=out.pdf input.ps` |
| PDF to PS | `gs ... -sDEVICE=ps2write -sOutputFile=out.ps input.pdf` |

## Documentation

- [Ghostscript Documentation](https://ghostscript.readthedocs.io/en/latest/Use.html)
- [Official Website](https://ghostscript.com/)
- [Device List](https://ghostscript.com/docs/9.54.0/Devices.htm)
