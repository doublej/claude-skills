---
name: adobe-illustrator
description: "ExtendScript (.jsx) automation via osascript on macOS"
---

# Adobe Illustrator (Local Automation — macOS)

Automate your local Illustrator installation via scripts triggered from the terminal. No cloud API or licence needed.

<overview>
## Bundled CLI (`tools/ai`)

A ready-to-use Python CLI is included. No dependencies — stdlib only.
</overview>

<setup>
### Setup (one-time)

```bash
# Make executable and optionally add to PATH
chmod +x ~/.claude/skills/adobe-illustrator/tools/ai
ln -s ~/.claude/skills/adobe-illustrator/tools/ai /usr/local/bin/ai-illustrator
```
</setup>

<commands>
### Commands

```bash
# Export AI file to SVG/PDF/PNG/JPG
ai export design.ai --format svg --out ./exports

# Export a specific artboard by index (0-based)
ai export design.ai --format png --artboard 0 --out ./exports

# Resize the artboard
ai resize design.ai 1920 1080 --out resized.ai

# Update a text frame
ai text design.ai "Headline" "New copy here" --out updated.ai

# Run a recorded Action
ai action design.ai "My Action" "My Set"

# Batch export all AI files in a folder
ai batch ./designs --format svg --out ./exports

# List all layers
ai layers design.ai

# List all artboards
ai artboards design.ai

# Run any .jsx script
ai run my-script.jsx

# Target a specific Illustrator version
ai --app "Adobe Illustrator 2024" export design.ai
```

The app name is auto-detected from `/Applications` (latest version wins).
</commands>


<triggering>
## Triggering from Terminal

```bash
# Run a .jsx script in Illustrator
osascript -e 'tell application "Adobe Illustrator 2026" to do javascript file "/abs/path/to/script.jsx"'
```

From Python:
```python
import subprocess

def run_jsx(script_path: str, ai_version: str = "Adobe Illustrator 2026"):
    subprocess.run([
        "osascript", "-e",
        f'tell application "{ai_version}" to do javascript file "{script_path}"'
    ], check=True)
```

Find your installed version name:
```bash
ls /Applications | grep -i illustrator
```
</triggering>

<patterns>
## ExtendScript Patterns (.jsx)

### Open, edit, export

```javascript
var doc = app.open(new File("/input/design.ai"));

// Rename a layer
doc.layers[0].name = "Background";

// Add a text frame
var tf = doc.textFrames.add();
tf.contents = "Hello World";
tf.position = [100, 600]; // [x, y] from top-left in points

// Change text in existing frame
var headline = doc.textFrames.getByName("Headline");
headline.contents = "New Headline";

// Export as SVG
var svgOpts = new ExportOptionsSVG();
svgOpts.embedRasterImages = true;
svgOpts.fontSubsetting = SVGFontSubsetting.GLYPHSUSED;
doc.exportFile(new File("/output/design.svg"), ExportType.SVG, svgOpts);

doc.close(SaveOptions.DONOTSAVECHANGES);
```

### Batch process a folder

```javascript
var folder = new Folder("/path/to/designs");
var files = folder.getFiles("*.ai");

for (var i = 0; i < files.length; i++) {
    var doc = app.open(files[i]);

    // ... your edits here ...

    var outFile = new File(folder.fsName + "/out_" + files[i].name.replace(".ai", ".svg"));
    var opts = new ExportOptionsSVG();
    doc.exportFile(outFile, ExportType.SVG, opts);
    doc.close(SaveOptions.DONOTSAVECHANGES);
}
```

### Create paths programmatically

```javascript
var doc = app.activeDocument;
var layer = doc.layers[0];

// Rectangle via pathItems
var rect = layer.pathItems.rectangle(700, 100, 200, 150); // top, left, width, height
rect.fillColor = new RGBColor();
rect.fillColor.red = 255;
rect.fillColor.green = 100;
rect.fillColor.blue = 0;

// Ellipse
var ellipse = layer.pathItems.ellipse(500, 100, 200, 150);

// Freeform path
var line = layer.pathItems.add();
line.setEntirePath([[0, 0], [100, 200], [200, 100]]);
line.stroked = true;
line.strokeWidth = 2;
```

### Layer visibility + export (batch variants)

```javascript
var doc = app.activeDocument;
var names = ["Version A", "Version B", "Version C"];

for (var i = 0; i < names.length; i++) {
    // Hide all named layers
    for (var j = 0; j < names.length; j++) {
        doc.layers.getByName(names[j]).visible = false;
    }
    // Show current
    doc.layers.getByName(names[i]).visible = true;

    var opts = new ExportOptionsPNG24();
    opts.artBoardClipping = true;
    doc.exportFile(
        new File("/output/" + names[i] + ".png"),
        ExportType.PNG24, opts
    );
}
```

### Work with artboards

```javascript
var doc = app.activeDocument;

// List artboards
for (var i = 0; i < doc.artboards.length; i++) {
    var ab = doc.artboards[i];
    var rect = ab.artboardRect; // [left, top, right, bottom]
    $.writeln(ab.name + ": " + rect);
}

// Export each artboard separately
for (var i = 0; i < doc.artboards.length; i++) {
    doc.artboards.setActiveArtboardIndex(i);
    var opts = new ExportOptionsPNG24();
    opts.artBoardClipping = true;
    doc.exportFile(
        new File("/output/artboard_" + i + ".png"),
        ExportType.PNG24, opts
    );
}
```

### Place an external image

```javascript
var doc = app.activeDocument;
var placed = doc.placedItems.add();
placed.file = new File("/path/to/image.png");
placed.position = [100, 500];
placed.width = 300;
placed.height = 200;
```
</patterns>

<reference>
## Common Operations Reference

### Save / Export formats

```javascript
// Save as AI
doc.saveAs(new File("/out/file.ai"), new IllustratorSaveOptions());

// Save as PDF
var pdfOpts = new PDFSaveOptions();
pdfOpts.pDFPreset = "[Press Quality]";
doc.saveAs(new File("/out/file.pdf"), pdfOpts);

// Save as EPS
doc.saveAs(new File("/out/file.eps"), new EPSSaveOptions());

// Export as SVG
var svgOpts = new ExportOptionsSVG();
svgOpts.embedRasterImages = true;
doc.exportFile(new File("/out/file.svg"), ExportType.SVG, svgOpts);

// Export as PNG-24
var pngOpts = new ExportOptionsPNG24();
pngOpts.horizontalScale = 200; // 2x resolution
pngOpts.verticalScale = 200;
pngOpts.artBoardClipping = true;
doc.exportFile(new File("/out/file.png"), ExportType.PNG24, pngOpts);

// Export as JPEG
var jpgOpts = new ExportOptionsJPEG();
jpgOpts.qualitySetting = 90;
jpgOpts.artBoardClipping = true;
doc.exportFile(new File("/out/file.jpg"), ExportType.JPEG, jpgOpts);
```

### Layer operations

```javascript
var doc = app.activeDocument;

doc.layers[0].visible = false;           // hide layer
doc.layers[0].opacity = 75;             // set opacity
doc.layers[0].name = "Renamed";         // rename
doc.layers[0].locked = true;            // lock

// Create a new layer
var newLayer = doc.layers.add();
newLayer.name = "My Layer";

// Move layer to front
newLayer.zOrder(ZOrderMethod.BRINGTOFRONT);
```

### Colors

```javascript
// RGB
var rgb = new RGBColor();
rgb.red = 255; rgb.green = 128; rgb.blue = 0;

// CMYK
var cmyk = new CMYKColor();
cmyk.cyan = 0; cmyk.magenta = 100; cmyk.yellow = 100; cmyk.black = 0;

// Apply to path
var path = doc.pathItems[0];
path.fillColor = rgb;
path.strokeColor = cmyk;
path.strokeWidth = 2;
path.filled = true;
path.stroked = true;
```

### Text styling

```javascript
var tf = doc.textFrames[0];
var range = tf.textRange;
range.characterAttributes.size = 24;
range.characterAttributes.fillColor = rgb;

// Font
range.characterAttributes.textFont = app.textFonts.getByName("Helvetica-Bold");

// Paragraph
range.paragraphAttributes.justification = Justification.CENTER;
```

### Run a recorded Action

```javascript
app.doScript("My Action", "My Action Set");
```
</reference>

<orchestration>
## Python Orchestration Pattern

```python
import subprocess
import tempfile
import os

def run_ai_script(jsx_code: str, ai_app: str = "Adobe Illustrator 2026") -> None:
    with tempfile.NamedTemporaryFile(suffix=".jsx", mode="w", delete=False) as f:
        f.write(jsx_code)
        tmp = f.name
    try:
        subprocess.run(
            ["osascript", "-e", f'tell application "{ai_app}" to do javascript file "{tmp}"'],
            check=True
        )
    finally:
        os.unlink(tmp)

# Usage
run_ai_script("""
var doc = app.activeDocument;
doc.layers[0].name = "Updated";
""")
```
</orchestration>

<api_reference>
## API Reference

For comprehensive Illustrator DOM details (all object types, properties, methods, enumerations), see `references/api_reference.md`.
</api_reference>

<notes>
## Notes

- Always use **absolute paths** in scripts — relative paths resolve against the AI app bundle, not your cwd
- `app.activeDocument` is the frontmost open document; open documents explicitly with `app.open(new File(...))`
- ExtendScript is synchronous — no `await` needed, but Illustrator blocks while running
- Illustrator uses a **top-left origin** with Y increasing downward for `position`, but artboard rects use `[left, top, right, bottom]`
- Test scripts interactively first via `File > Scripts > Other Script…` before wiring to terminal
- Illustrator app name varies by version — check with `ls /Applications | grep -i illustrator`
- Actions in Illustrator use `app.doScript()` (not `app.doAction()` like Photoshop)
</notes>
