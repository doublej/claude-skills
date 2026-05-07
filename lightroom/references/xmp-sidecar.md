# XMP Sidecar Editing

XMP (Extensible Metadata Platform) is Adobe's XML-based metadata standard. Lightroom (cloud + Classic) reads and writes XMP for develop settings, ratings, keywords, and EXIF/IPTC. For RAW formats Lightroom can't write into, edits land in a paired `<filename>.xmp` sidecar.

## When to use

- Bulk edits across thousands of files (faster than REST round-trips, no API quota).
- Offline workflows (no network, no Adobe Developer Console signup).
- Pre-import preparation: tag/rate/develop before Lightroom ever sees the file.
- Convert presets between tools (Capture One, darktable also speak crs:).

## File location

| Format | Where edits live |
|---|---|
| `.dng`, `.tif`, `.psd`, `.jpg`, `.png` | Embedded XMP in the file itself (and optionally a sidecar) |
| `.cr3`, `.cr2`, `.nef`, `.arw`, `.raf`, `.orf`, `.rw2`, etc. | Sidecar: same name as RAW with `.xmp` extension |

Lightroom looks for the sidecar with the **exact same basename** in the same directory:
```
photo.cr3
photo.xmp           ← ExifTool default
photo.cr3.xmp       ← Lightroom Classic sometimes writes this; cloud LR ignores it
```
Stick with `<basename>.xmp` (no extension chain) for cloud Lightroom compatibility.

## Namespaces

XMP attributes are namespaced. The ones Lightroom uses:

| Prefix | URI | Owns |
|---|---|---|
| `crs` | `http://ns.adobe.com/camera-raw-settings/1.0/` | Develop settings |
| `xmp` | `http://ns.adobe.com/xap/1.0/` | Rating, label, creator tool |
| `xmpMM` | `http://ns.adobe.com/xap/1.0/mm/` | Document/instance IDs, history |
| `dc` | `http://purl.org/dc/elements/1.1/` | Title, description, **subject (= keywords)**, creator |
| `exif` | `http://ns.adobe.com/exif/1.0/` | Camera EXIF |
| `tiff` | `http://ns.adobe.com/tiff/1.0/` | Camera/lens make/model |
| `photoshop` | `http://ns.adobe.com/photoshop/1.0/` | Headline, instructions, source |
| `Iptc4xmpCore` | `http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/` | Location, contact |
| `lr` | `http://ns.adobe.com/lightroom/1.0/` | Hierarchical subjects (LR only) |

## Common attributes

### Develop settings (crs:)
All keys from `develop-settings-keys.md` work as `crs:<KeyName>` attributes. Numeric values are quoted strings — the parser coerces. Format:
```xml
crs:Exposure2012="+0.50"
crs:Contrast2012="+20"
crs:Highlights2012="-30"
crs:Vibrance="+15"
crs:WhiteBalance="Daylight"
crs:Temperature="5500"
```

Plus / minus signs are required for some Lightroom versions. ExifTool prepends `+` automatically for positive numbers when writing crs: tags.

### Process version
```xml
crs:Version="15.4"           <!-- Camera Raw version that wrote this -->
crs:ProcessVersion="11.0"    <!-- Color science generation -->
```
- `6.7` = PV2012 (LR 4-LR Classic 7.3)
- `11.0` = PV4 (LR Classic 7.4 +, Lightroom desktop)
- `15.4` = PV5 (LR Classic 11+, Lightroom desktop 6+)

When generating XMP from scratch, set both. Newer Lightroom downgrades cleanly; older Lightroom may ignore unknown PVs.

### Rating + label
```xml
xmp:Rating="5"               <!-- 0-5 star -->
xmp:Label="Yellow"           <!-- Color label: Red, Yellow, Green, Blue, Purple -->
```

### Keywords (flat)
```xml
<dc:subject>
  <rdf:Bag>
    <rdf:li>portrait</rdf:li>
    <rdf:li>2026</rdf:li>
    <rdf:li>client-acme</rdf:li>
  </rdf:Bag>
</dc:subject>
```

### Hierarchical keywords (Lightroom only)
```xml
<lr:hierarchicalSubject>
  <rdf:Bag>
    <rdf:li>People|Family|Mom</rdf:li>
    <rdf:li>Places|Netherlands|Amsterdam</rdf:li>
  </rdf:Bag>
</lr:hierarchicalSubject>
```
Pipe-separated; each level gets a flat `dc:subject` entry too.

### Title + caption
```xml
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">Sunset over Amsterdam</rdf:li></rdf:Alt></dc:title>
<dc:description><rdf:Alt><rdf:li xml:lang="x-default">Long caption here</rdf:li></rdf:Alt></dc:description>
```

## Minimal sidecar template

For a fresh sidecar (no prior edits), this is the smallest valid file Lightroom accepts:
```xml
<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="3.6.0">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
      xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
      xmlns:xmp="http://ns.adobe.com/xap/1.0/"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      crs:Version="15.4"
      crs:ProcessVersion="11.0"
      xmp:Rating="0">
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>
```

The `<?xpacket?>` PIs and `id="W5M0MpCehiHzreSzNTczkc9d"` are required (Adobe XMP magic). Don't omit them.

## Tooling

### ExifTool (recommended for CLI / shell scripts)

Install: `brew install exiftool` (macOS) or `apt install libimage-exiftool-perl` (Linux).

Read all XMP from a file:
```bash
exiftool -xmp:all photo.xmp
exiftool -xmp:all photo.cr3        # reads embedded + sidecar, merged
```

Write a single develop key:
```bash
exiftool -xmp-crs:Exposure2012=+0.5 -overwrite_original photo.cr3
```

Write multiple keys in one call:
```bash
exiftool \
  -xmp-crs:Exposure2012=+0.5 \
  -xmp-crs:Contrast2012=+20 \
  -xmp-crs:Highlights2012=-30 \
  -xmp:Rating=5 \
  -xmp-dc:Subject="portrait" \
  -xmp-dc:Subject+="2026" \
  -overwrite_original photo.cr3
```
- `-xmp-dc:Subject="portrait"` replaces the keyword list.
- `-xmp-dc:Subject+="2026"` appends to the keyword list.
- `-xmp-dc:Subject-="old"` removes a keyword.

Copy ALL XMP from one file (e.g., a preset XMP) to many:
```bash
exiftool -tagsFromFile preset.xmp -xmp:all -overwrite_original /shoots/2026-05-06/*.CR3
```

Bulk-write from a CSV of filename + Exposure adjustments:
```bash
while IFS=, read -r f exp; do
  exiftool "-xmp-crs:Exposure2012=$exp" -overwrite_original "$f"
done < tweaks.csv
```

ExifTool gotchas:
- `-overwrite_original` skips creating a `.cr3_original` backup. Omit it if you want a backup.
- Without `-overwrite_original`, ExifTool writes the new file and renames the old to `<file>_original`. Disk-space-aware in big batches.
- For RAW formats, ExifTool writes the sidecar — original RAW bytes stay untouched.

### Python — python-xmp-toolkit

Install: `pip install python-xmp-toolkit` (depends on `exempi`: `brew install exempi` on macOS).

```python
from libxmp import XMPFiles, consts

xmpfile = XMPFiles(file_path="photo.xmp", open_forupdate=True)
xmp = xmpfile.get_xmp()

CRS = consts.XMP_NS_CameraRaw   # "http://ns.adobe.com/camera-raw-settings/1.0/"
xmp.set_property(CRS, "Exposure2012", "+0.5")
xmp.set_property(CRS, "Contrast2012", "+20")
xmp.set_property(consts.XMP_NS_XMP, "Rating", "5")

xmpfile.put_xmp(xmp)
xmpfile.close_file()
```

For batch jobs, `python-xmp-toolkit` is slower than ExifTool subprocess calls (~30 ms per file overhead from libexempi load). For >1000 files, prefer ExifTool with `-stay_open True` (long-lived ExifTool process).

### Python — lxml + string templating

For writing fresh sidecars (no prior content to merge), templating is simplest:
```python
from string import Template

XMP_TEMPLATE = Template("""<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="3.6.0">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
      xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
      xmlns:xmp="http://ns.adobe.com/xap/1.0/"
      crs:Version="15.4"
      crs:ProcessVersion="11.0"
      crs:Exposure2012="$exposure"
      crs:Contrast2012="$contrast"
      xmp:Rating="$rating">
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>""")

with open("photo.xmp", "w") as f:
    f.write(XMP_TEMPLATE.substitute(exposure="+0.5", contrast="+20", rating="5"))
```

Cheap, fast, no deps beyond stdlib. Good for batch generation from a database of edits.

## Round-trip with Lightroom (cloud / desktop)

Lightroom desktop does **not** auto-watch sidecars. After modifying XMP:

1. **Already in the catalog**: select the photos → **Photo → Read Metadata from File**. Lightroom merges XMP changes back. Conflicts: cloud version wins for fields the user has edited recently; XMP wins for fields untouched in the cloud.
2. **Not yet imported**: import normally. Sidecar is read at import time.

To **export** Lightroom-cloud edits to XMP (for backup, sharing, or feeding Path A):
- Lightroom desktop has no "Save Metadata to File" command (Classic does). Workaround: export with **Original + Settings** — produces source file + paired XMP.

<round_trip_traps>
- After Read Metadata from File, the cloud version of develop settings updates and syncs to mobile/web.
- Read Metadata is per-photo, not auto-watched. For pipelines, document a manual or AppleScript-driven trigger.
- If a photo was edited in Lightroom cloud after the XMP was written, those cloud edits will be **overwritten** by the XMP. Always read latest XMP from cloud before round-tripping.
</round_trip_traps>

## Export develop settings as a portable preset

A Lightroom preset is a `.xmp` file with **only** crs: develop settings (no Rating, no Subject, no document IDs). Strip everything except the crs: namespace and `crs:HasSettings="True"`:

```xml
<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="3.6.0">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
      xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
      crs:PresetType="Normal"
      crs:Cluster=""
      crs:UUID="<uuid4-hex>"
      crs:SupportsAmount="False"
      crs:SupportsColor="True"
      crs:SupportsMonochrome="True"
      crs:SupportsHighDynamicRange="True"
      crs:SupportsNormalDynamicRange="True"
      crs:SupportsSceneReferred="False"
      crs:SupportsOutputReferred="True"
      crs:CameraModelRestriction=""
      crs:Copyright=""
      crs:ContactInfo=""
      crs:Version="15.4"
      crs:ProcessVersion="11.0"
      crs:HasSettings="True"
      crs:Exposure2012="+0.50"
      crs:Contrast2012="+20"
      ...>
      <crs:Name><rdf:Alt><rdf:li xml:lang="x-default">My Preset</rdf:li></rdf:Alt></crs:Name>
      <crs:ShortName><rdf:Alt><rdf:li xml:lang="x-default">My Preset</rdf:li></rdf:Alt></crs:ShortName>
      <crs:SortName><rdf:Alt><rdf:li xml:lang="x-default">My Preset</rdf:li></rdf:Alt></crs:SortName>
      <crs:Group><rdf:Alt><rdf:li xml:lang="x-default">User Presets</rdf:li></rdf:Alt></crs:Group>
      <crs:Description><rdf:Alt><rdf:li xml:lang="x-default"></rdf:li></rdf:Alt></crs:Description>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>
```

Drop into the preset folder:
- macOS: `~/Library/Application Support/Adobe/CameraRaw/Settings/User Presets/<name>.xmp`
- Windows: `%APPDATA%\Adobe\CameraRaw\Settings\User Presets\<name>.xmp`

Restart Lightroom. Preset shows up in the Presets panel and syncs across devices.

## Anti-patterns

- **Don't write XMP for cloud-only photos** — photos imported from camera-roll on mobile have no local file. Use the REST API.
- **Don't omit `crs:Version` and `crs:ProcessVersion`** — Lightroom will treat the file as PV1 (oldest, 2003-era) and silently no-op modern keys.
- **Don't write `crs:HasSettings="False"`** if you want the preset to apply — that flag tells Lightroom to skip the preset's settings.
- **Don't write Lua-style booleans** (`true`/`false`) — XMP wants `"True"` / `"False"` strings.
- **Don't trust `Subject` to round-trip case** — Lightroom normalizes keyword case based on its own keyword library.
