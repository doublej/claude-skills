---
name: adobe-photoshop
description: Automate local Adobe Photoshop on macOS via ExtendScript (.jsx) or UXP Scripts (.psjs), triggered from the terminal using osascript. Use when editing PSDs, batch processing images, manipulating layers, exporting files, or running Photoshop actions programmatically.
---

# Adobe Photoshop (Local Automation — macOS)

Automate your local Photoshop installation via scripts triggered from the terminal. No cloud API or licence needed.

## Bundled CLI (`tools/ps`)

A ready-to-use Python CLI is included. No dependencies — stdlib only.

### Setup (one-time)

```bash
# Make executable and optionally add to PATH
chmod +x ~/.claude/skills/adobe-photoshop/tools/ps
ln -s ~/.claude/skills/adobe-photoshop/tools/ps /usr/local/bin/ps-photoshop
```

### Commands

```bash
# Export PSD to JPG/PNG
ps export design.psd --format jpg --quality 85 --out ./exports

# Resize and save
ps resize design.psd 1920 1080 --out resized.psd

# Update a text layer
ps text design.psd "Headline" "New copy here" --out updated.psd

# Run a recorded Action
ps action design.psd "My Action" "My Set"

# Batch export all PSDs in a folder
ps batch ./designs --format png --out ./exports

# List all layers
ps layers design.psd

# Run any .jsx script
ps run my-script.jsx

# Target a specific Photoshop version
ps --app "Adobe Photoshop 2023" export design.psd
```

The app name is auto-detected from `/Applications` (latest version wins).

---

## Two Scripting Approaches

| Approach | File ext | PS version | Best for |
|----------|----------|-----------|----------|
| **ExtendScript** | `.jsx` | All versions | Reliable, widely supported, most examples online |
| **UXP Script** | `.psjs` | 22.5+ (2021+) | Modern API, async/await, better type safety |

## Triggering from Terminal (ExtendScript)

```bash
# Run a .jsx script in Photoshop
osascript -e 'tell application "Adobe Photoshop 2024" to do javascript file "/abs/path/to/script.jsx"'
```

From Python:
```python
import subprocess

def run_jsx(script_path: str, ps_version: str = "Adobe Photoshop 2024"):
    subprocess.run([
        "osascript", "-e",
        f'tell application "{ps_version}" to do javascript file "{script_path}"'
    ], check=True)
```

Find your installed version name:
```bash
ls /Applications | grep -i photoshop
```

## Triggering from Terminal (UXP Scripts)

UXP Scripts can't be reliably triggered via AppleScript. Use the **Scripts menu** inside Photoshop (`File → Scripts → Browse…`) or the UXP Developer Tool. For fully programmatic use, prefer ExtendScript.

## ExtendScript Patterns (.jsx)

### Open, edit, export

```javascript
// script.jsx
var doc = app.open(new File("/input/design.psd"));

// Rename a layer
doc.layers[0].name = "Background";

// Change text
var textLayer = doc.layers.getByName("Headline");
textLayer.textItem.contents = "New Headline";

// Export as JPEG
var opts = new ExportOptionsSaveForWeb();
opts.format = SaveDocumentType.JPEG;
opts.quality = 85;
doc.exportDocument(new File("/output/design.jpg"), ExportType.SAVEFORWEB, opts);

doc.close(SaveOptions.DONOTSAVECHANGES);
```

### Batch process a folder

```javascript
// batch.jsx
var folder = Folder.selectDialog("Pick folder");
var files = folder.getFiles("*.psd");

for (var i = 0; i < files.length; i++) {
    var doc = app.open(files[i]);

    // ... your edits here ...

    var outFile = new File(folder.fsName + "/out_" + files[i].name.replace(".psd", ".jpg"));
    var opts = new ExportOptionsSaveForWeb();
    opts.format = SaveDocumentType.JPEG;
    opts.quality = 85;
    doc.exportDocument(outFile, ExportType.SAVEFORWEB, opts);
    doc.close(SaveOptions.DONOTSAVECHANGES);
}
```

### Replace smart object content

```javascript
// smart_object.jsx
var doc = app.activeDocument;
var layer = doc.layers.getByName("Mockup");

// Select the smart object layer
doc.activeLayer = layer;

// Open embedded smart object
app.executeAction(app.charIDToTypeID("PlcP"), undefined, DialogModes.NO);

// Get the smart object doc, replace its content
var soDoc = app.activeDocument;
var placed = app.open(new File("/path/to/new-artwork.png"));
placed.selection.selectAll();
placed.selection.copy();
placed.close(SaveOptions.DONOTSAVECHANGES);

soDoc.paste();
soDoc.close(SaveOptions.SAVECHANGES); // saves back into smart object
```

### Layer visibility + export (batch variants)

```javascript
// variants.jsx — show one layer group at a time, export each
var doc = app.activeDocument;
var groups = ["Version A", "Version B", "Version C"];

for (var i = 0; i < groups.length; i++) {
    // Hide all groups
    for (var j = 0; j < groups.length; j++) {
        doc.layers.getByName(groups[j]).visible = false;
    }
    // Show current
    doc.layers.getByName(groups[i]).visible = true;

    var opts = new ExportOptionsSaveForWeb();
    opts.format = SaveDocumentType.PNG;
    opts.PNG8 = false;
    doc.exportDocument(
        new File("/output/" + groups[i] + ".png"),
        ExportType.SAVEFORWEB, opts
    );
}
```

## UXP Script Patterns (.psjs)

```javascript
// script.psjs — requires Photoshop 22.5+
const { app } = require('photoshop');
const { executeAsModal } = require('photoshop').core;

await executeAsModal(async () => {
    const doc = app.activeDocument;

    // Edit text layer
    const layer = doc.layers.find(l => l.name === "Headline");
    if (layer?.kind === "text") {
        layer.textItem.content = "Updated Text";
    }

    // Export PNG
    await doc.saveAs.png(
        require('uxp').storage.localFileSystem.getFileForSaving("output.png"),
        { compression: 6 }
    );
}, { commandName: "Update and Export" });
```

## Common Operations Reference

### Save / Export formats

```javascript
// Save as PSD
doc.saveAs(new File("/out/file.psd"), new PhotoshopSaveOptions(), true);

// Save as PNG
var pngOpts = new ExportOptionsSaveForWeb();
pngOpts.format = SaveDocumentType.PNG;
pngOpts.PNG8 = false; // PNG-24
doc.exportDocument(new File("/out/file.png"), ExportType.SAVEFORWEB, pngOpts);

// Save as JPEG
var jpgOpts = new ExportOptionsSaveForWeb();
jpgOpts.format = SaveDocumentType.JPEG;
jpgOpts.quality = 90;
doc.exportDocument(new File("/out/file.jpg"), ExportType.SAVEFORWEB, jpgOpts);
```

### Layer operations

```javascript
var doc = app.activeDocument;

doc.layers[0].visible = false;           // hide layer
doc.layers[0].opacity = 75;             // set opacity
doc.layers[0].name = "Renamed";         // rename

doc.mergeVisibleLayers();               // flatten visible
doc.flatten();                          // flatten all

// Create a new solid fill layer
var layer = doc.artLayers.add();
layer.kind = LayerKind.NORMAL;
```

### Resize / crop

```javascript
doc.resizeImage(1920, 1080, 72, ResampleMethod.BICUBIC);
doc.resizeCanvas(2000, 2000, AnchorPosition.MIDDLECENTER);
doc.crop([0, 0, 1920, 1080]); // [left, top, right, bottom]
```

### Run a recorded Action

```javascript
// Run an Action from the Actions panel
app.doAction("My Action", "My Action Set");
```

## Python Orchestration Pattern

```python
import subprocess
import tempfile
import os

def run_ps_script(jsx_code: str, ps_app: str = "Adobe Photoshop 2024") -> None:
    with tempfile.NamedTemporaryFile(suffix=".jsx", mode="w", delete=False) as f:
        f.write(jsx_code)
        tmp = f.name
    try:
        subprocess.run(
            ["osascript", "-e", f'tell application "{ps_app}" to do javascript file "{tmp}"'],
            check=True
        )
    finally:
        os.unlink(tmp)

# Usage
run_ps_script("""
var doc = app.activeDocument;
doc.layers[0].name = "Updated";
""")
```

## Notes

- Always use **absolute paths** in scripts — relative paths resolve against the PS app bundle, not your cwd
- `app.activeDocument` is the frontmost open document; open documents explicitly with `app.open(new File(...))`
- ExtendScript is synchronous — no `await` needed, but Photoshop blocks while running
- Test scripts interactively first via `File → Scripts → Browse…` before wiring to terminal
- For heavy batch jobs, run Photoshop headless via Actions + Batch (`File → Automate → Batch`) instead of custom scripts
- Photoshop app name varies by version — check with `ls /Applications | grep -i photoshop`
