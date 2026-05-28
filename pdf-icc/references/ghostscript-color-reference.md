# Ghostscript ICC Color Management - Advanced Reference

## Black Handling

### DeviceGrayToK

When converting RGB/Gray to CMYK, gray values can map to either pure K (black only) or rich black (C+M+Y+K mix). Control with:

```bash
# Map gray to K channel only (clean text, sharp lines)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -dDeviceGrayToK=true \
   -sOutputFile=output.pdf input.pdf
```

- `true` = gray maps to K only (preferred for text-heavy documents)
- `false` = gray goes through ICC transform (may produce rich black)

### Rich Black vs Pure K

Rich black (e.g., C:60 M:40 Y:40 K:100) gives deeper blacks in print but causes registration issues on text. Use `-dDeviceGrayToK=true` for documents with body text to ensure pure K black.

### Black Point Compensation

```bash
-dBlackPtComp=0    # Component (per-channel)
-dBlackPtComp=1    # None
-dBlackPtComp=2    # Use black point compensation (default)
```

Per object type:
```bash
-dGraphicBlackPt=2
-dImageBlackPt=0
-dTextBlackPt=2
```

## Spot Colors & Separations

### DeviceN and Separation Color Spaces

Ghostscript handles spot colors through DeviceN and Separation color spaces. When converting, spot colors can be:

1. **Preserved** (default when output supports them)
2. **Converted to process colors** (when `-sColorConversionStrategy=CMYK`)

```bash
# Preserve spot colors in output
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=LeaveColorUnchanged \
   -dProcessColorModel=/DeviceCMYK \
   -sOutputFile=output.pdf input.pdf
```

### ColorConversionStrategy Options

| Strategy | Behavior |
|----------|----------|
| `LeaveColorUnchanged` | No conversion; preserves all color spaces including spot |
| `CMYK` | Convert everything to CMYK process |
| `RGB` | Convert everything to RGB |
| `Gray` | Convert everything to grayscale |
| `UseDeviceIndependentColor` | Convert to CIE-based color (for PDF/X) |

## PDF/X Preamble Files

### PDFX_IntCmyk.ps

This PostScript preamble defines required PDF/X metadata. It ships with Ghostscript in the `lib/` directory. Key fields to customize:

```postscript
% Customize these in a copy of the preamble:
/ICCProfile (path/to/output_profile.icc)   % Output ICC profile path
/Title (Document Title)                      % PDF title
/OutputCondition (Commercial and specialty)  % Output condition text
/OutputConditionIdentifier (FOGRA39)         % Standard identifier
```

### Custom PDF/X Preamble

Create a custom preamble for your print workflow:

```postscript
% my_pdfx.ps - Custom PDF/X-3 preamble
[ /Title (My Document)
  /DOCINFO pdfmark

[ /OutputCondition (Coated paper, 300% ink limit)
  /OutputConditionIdentifier (FOGRA39)
  /RegistryName (http://www.color.org)
  /ICCProfile (/path/to/ISOcoated_v2_300_eci.icc)
  /OutputIntent pdfmark
```

Use with:
```bash
gs -dPDFX -dBATCH -dNOPAUSE \
   -sDEVICE=pdfwrite \
   -sOutputFile=output.pdf \
   my_pdfx.ps input.pdf
```

### PDFA_def.ps

Similar preamble for PDF/A. Key difference: uses `/GTS_PDFA1` instead of `/GTS_PDFX`.

```postscript
% PDFA_def.ps customization
/ICCProfile (srgb.icc) def
/OutputConditionIdentifier (sRGB IEC61966-2.1) def
```

## Overriding Embedded Profiles

### -dOverrideICC

When `true`, Ghostscript ignores ICC profiles embedded in the PDF and uses its default profiles (or those specified via `-sDefault*Profile`).

```bash
# Force all colors through your chosen profiles
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -dOverrideICC=true \
   -sDefaultRGBProfile=AdobeRGB1998.icc \
   -sDefaultCMYKProfile=ISOcoated_v2_300_eci.icc \
   -sOutputICCProfile=USWebCoatedSWOP.icc \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sOutputFile=output.pdf input.pdf
```

### When to Use OverrideICC

- Source PDF has incorrect/outdated embedded profiles
- Standardizing color across documents from different sources
- Converting for a specific press that requires a particular profile

## Troubleshooting

### Washed-Out or Pale Blacks

**Problem**: After RGB-to-CMYK conversion, blacks appear washed out or gray.

**Causes**:
1. Ghostscript versions 9.22-9.27 had regressions with certain ICC profiles
2. The ICC profile may clip black values

**Fixes**:
```bash
# Option 1: Force gray to K channel
-dDeviceGrayToK=true

# Option 2: Use absolute colorimetric intent
-dRenderIntent=3

# Option 3: Use device-independent color strategy
-sColorConversionStrategy=UseDeviceIndependentColor

# Option 4: Use -dUseFastColor for simple conversions (no ICC)
-dUseFastColor
```

### Colors Shift After Conversion

**Problem**: Colors look different after conversion.

**Check**:
1. Verify the correct ICC profiles are being loaded: run with `-dQUIET` removed to see profile loading messages
2. Ensure render intent matches your needs (perceptual for photos, relative colorimetric for logos)
3. Check if `-dOverrideICC` is overriding a correct embedded profile

### Ghostscript Can't Find ICC Profiles

```bash
# Check Ghostscript's search paths
gs -h 2>&1 | grep -A5 "Search path"

# Find Ghostscript's resource directory
gs -q -dBATCH -dNOPAUSE -c "currentglobal true setglobal /GenericResourceDir where {pop GenericResourceDir print} {(not found) print} ifelse quit"

# ICC profiles directory is usually:
# <resource_dir>/../iccprofiles/
```

**Fix**: Provide absolute paths to ICC profiles:
```bash
-sOutputICCProfile=/usr/share/color/icc/ISOcoated_v2_300_eci.icc
```

### Transparency Issues in PDF/X

PDF/X does not support transparency. Flatten first:

```bash
gs -dPDFX -dBATCH -dNOPAUSE \
   -dHaveTransparency=false \
   -sDEVICE=pdfwrite \
   -sOutputFile=pdfx.pdf \
   PDFX_IntCmyk.ps input.pdf
```

### Large File Size After Conversion

Color conversion re-encodes images. Control with:

```bash
# Downsample high-res images
-dDownsampleColorImages=true
-dColorImageResolution=300

# Set compression
-dAutoFilterColorImages=true
-dColorImageFilter=/DCTEncode   # JPEG for photos
# or
-dColorImageFilter=/FlateEncode  # Lossless for graphics
```

## Device Link Profiles

Device link profiles chain two or more profiles into a single transform, bypassing the Profile Connection Space (PCS). Advantages:

- Faster transforms (single lookup)
- More control over gamut mapping
- Can preserve K channel in CMYK-to-CMYK transforms

```bash
# Create with Little-CMS
linkicc -o cmyk2cmyk.icc source_cmyk.icc destination_cmyk.icc

# Use as Ghostscript device link
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sDeviceLinkProfile=cmyk2cmyk.icc \
   -sOutputFile=output.pdf input.pdf
```

### K-Channel Preservation

For CMYK-to-CMYK transforms where you want to preserve the black channel:

```bash
# linkicc with black preservation
linkicc -b -o cmyk2cmyk_kpreserve.icc source.icc dest.icc
# -b enables black point compensation
```

## Proofing

### Soft Proofing

```bash
# Simulate press output on screen (proof profile)
gs -dBATCH -dNOPAUSE -dQUIET \
   -sDEVICE=pdfwrite \
   -sProofProfile=press_profile.icc \
   -dDeviceLinkProfile= \
   -sOutputFile=proof.pdf input.pdf
```

## Resolution and Conversion Quality

Higher resolution produces more accurate color conversion for raster content:

```bash
# Default is 720 dpi; increase for quality-critical work
gs -r1200 -dBATCH -dNOPAUSE \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sOutputFile=output.pdf input.pdf
```

Note: higher `-r` values increase processing time significantly.
