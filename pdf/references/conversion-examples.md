# Ghostscript Conversion Examples

Detailed recipes for PDF processing and format conversion.

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

All pages:
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

Single pages:
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
