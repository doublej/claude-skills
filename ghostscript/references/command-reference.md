# Ghostscript Command Reference

Detailed reference for Ghostscript commands, devices, and options.

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
| `txtwrite` | Text | Extract text content |
| `docxwrite` | DOCX | Microsoft Word |
| `nullpage` | None | Validation/info only |

## PDF Settings Comparison

| Setting | DPI | Image Quality | File Size | Use Case |
|---------|-----|---------------|-----------|----------|
| `/screen` | 72 | Low | Smallest | Web viewing |
| `/ebook` | 150 | Medium | Small | Digital reading |
| `/printer` | 300 | High | Medium | Office printing |
| `/prepress` | 300 | Highest | Large | Professional print |
| `/default` | - | Balanced | Medium | General use |

## Resolution Guide

| Use Case | Resolution | Flag |
|----------|------------|------|
| Screen/Web | 72-96 dpi | `-r72` |
| Ebook/Preview | 150 dpi | `-r150` |
| Print quality | 300 dpi | `-r300` |
| High-res print | 600 dpi | `-r600` |

## Custom Compression Settings

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

### Rotate Pages (90 degrees)

```bash
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sOutputFile=rotated.pdf \
   -c "<</Orientation 1>> setpagedevice" \
   -f input.pdf
```

### N-up Printing

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
