# Adobe Illustrator ExtendScript API Reference

## Core Object Hierarchy

```
Application (app)
├── documents[]  →  Document
│   ├── layers[]  →  Layer
│   │   ├── pathItems[]  →  PathItem
│   │   ├── compoundPathItems[]  →  CompoundPathItem
│   │   ├── textFrames[]  →  TextFrame
│   │   ├── placedItems[]  →  PlacedItem
│   │   ├── rasterItems[]  →  RasterItem
│   │   ├── meshItems[]  →  MeshItem
│   │   ├── pluginItems[]  →  PluginItem
│   │   ├── graphItems[]  →  GraphItem
│   │   ├── symbolItems[]  →  SymbolItem
│   │   ├── groupItems[]  →  GroupItem (contains nested items)
│   │   └── pageItems[]  →  PageItem (all items)
│   ├── artboards[]  →  Artboard
│   ├── swatches[]  →  Swatch
│   ├── symbols[]  →  Symbol
│   ├── brushes[]  →  Brush
│   ├── graphicStyles[]  →  GraphicStyle
│   ├── spots[]  →  Spot
│   ├── gradients[]  →  Gradient
│   ├── patterns[]  →  Pattern
│   └── views[]  →  View
├── textFonts[]  →  TextFont
└── printerList[]  →  Printer
```

## Application

| Property / Method | Description |
|---|---|
| `app.activeDocument` | Currently active document |
| `app.documents` | All open documents |
| `app.documents.add(type?, width?, height?)` | Create new document. Type: `DocumentColorSpace.RGB` or `.CMYK` |
| `app.open(fileRef)` | Open a file. `fileRef = new File("/path")` |
| `app.textFonts` | All available fonts |
| `app.textFonts.getByName("Helvetica")` | Get font by PostScript name |
| `app.doScript(action, set, dialogs?)` | Run an Action. `dialogs`: `DialogModes.NO` |
| `app.executeMenuCommand(cmd)` | Run menu command by ID string |
| `app.redraw()` | Force screen redraw |
| `app.userInteractionLevel` | `UserInteractionLevel.DONTDISPLAYALERTS` to suppress dialogs |

## Document

| Property / Method | Description |
|---|---|
| `doc.name` | File name |
| `doc.fullName` | Full File object |
| `doc.path` | Folder containing the file |
| `doc.width` / `doc.height` | Artboard dimensions (points) |
| `doc.documentColorSpace` | `DocumentColorSpace.RGB` or `.CMYK` |
| `doc.rulerOrigin` | `[x, y]` ruler origin |
| `doc.layers` | Layer collection |
| `doc.artboards` | Artboard collection |
| `doc.pathItems` | All PathItems across all layers |
| `doc.textFrames` | All TextFrames across all layers |
| `doc.groupItems` | All GroupItems |
| `doc.compoundPathItems` | All CompoundPathItems |
| `doc.placedItems` | All PlacedItems |
| `doc.rasterItems` | All RasterItems |
| `doc.symbolItems` | All SymbolItems |
| `doc.meshItems` | All MeshItems |
| `doc.pageItems` | All items (union) |
| `doc.selection` | Currently selected items (array) |
| `doc.swatches` | Swatch collection |
| `doc.symbols` | Symbol collection |
| `doc.spots` | Spot color collection |
| `doc.gradients` | Gradient collection |
| `doc.close(saveOpts?)` | `SaveOptions.SAVECHANGES`, `.DONOTSAVECHANGES`, `.PROMPTTOSAVECHANGES` |
| `doc.saveAs(file, opts)` | Save with format options |
| `doc.exportFile(file, type, opts)` | Export to file |
| `doc.fitArtboardToSelectedArt(idx?)` | Resize artboard to fit selection |
| `doc.rearrangeArtboards()` | Auto-arrange artboards |
| `doc.selectObjectsOnActiveArtboard()` | Select all on active artboard |

## Artboard

| Property / Method | Description |
|---|---|
| `artboard.name` | Artboard name |
| `artboard.artboardRect` | `[left, top, right, bottom]` in points |
| `doc.artboards.add(rect)` | Add new artboard |
| `doc.artboards.remove(index)` | Remove artboard |
| `doc.artboards.setActiveArtboardIndex(i)` | Set active artboard |
| `doc.artboards.getActiveArtboardIndex()` | Get active artboard index |

## Layer

| Property / Method | Description |
|---|---|
| `layer.name` | Layer name |
| `layer.visible` | Show/hide |
| `layer.locked` | Lock/unlock |
| `layer.opacity` | 0–100 |
| `layer.color` | Layer highlight color |
| `layer.printable` | Include in print |
| `layer.isIsolated` | Isolation mode |
| `layer.blendingMode` | `BlendModes.NORMAL`, `.MULTIPLY`, `.SCREEN`, etc. |
| `layer.zOrder(method)` | `ZOrderMethod.BRINGTOFRONT`, `.SENDTOBACK`, `.BRINGFORWARD`, `.SENDBACKWARD` |
| `layer.hasSelectedArtwork` | Whether selection exists |
| `layer.pathItems` / `.textFrames` / etc. | Items on this layer |
| `doc.layers.add()` | Create new layer |
| `doc.layers.getByName("name")` | Get layer by name |

## PathItem

| Property / Method | Description |
|---|---|
| `path.pathPoints` | Array of PathPoint objects |
| `path.setEntirePath([[x,y], ...])` | Set all anchor points |
| `path.closed` | Whether path is closed |
| `path.area` | Enclosed area (closed paths) |
| `path.length` | Path length |
| `path.filled` / `path.fillColor` | Fill state and color |
| `path.stroked` / `path.strokeColor` | Stroke state and color |
| `path.strokeWidth` | Stroke width (points) |
| `path.strokeCap` | `StrokeCap.BUTTENDCAP`, `.ROUNDENDCAP`, `.PROJECTINGENDCAP` |
| `path.strokeJoin` | `StrokeJoin.MITERENDJOIN`, `.ROUNDENDJOIN`, `.BEVELENDJOIN` |
| `path.strokeDashes` | Dash pattern array `[dash, gap, ...]` |
| `path.opacity` | 0–100 |
| `path.blendingMode` | Blending mode |
| `path.clipping` | Whether this is a clipping path |
| `path.position` | `[x, y]` top-left corner |
| `path.width` / `path.height` | Bounding box dimensions |
| `path.selected` | Selection state |
| `path.remove()` | Delete the item |
| `path.duplicate()` | Duplicate the item |
| `path.translate(dx, dy)` | Move |
| `path.resize(sx, sy)` | Scale (percentages) |
| `path.rotate(angle)` | Rotate (degrees) |

### Shape shortcuts (on `layer.pathItems`)

```javascript
pathItems.rectangle(top, left, width, height, reversed?)
pathItems.roundedRectangle(top, left, width, height, hRadius, vRadius, reversed?)
pathItems.ellipse(top, left, width, height, reversed?)
pathItems.polygon(centerX, centerY, radius, sides, reversed?)
pathItems.star(centerX, centerY, radius, innerRadius, points, reversed?)
```

## TextFrame

| Property / Method | Description |
|---|---|
| `tf.contents` | Plain text content |
| `tf.kind` | `TextType.POINTTEXT`, `.AREATEXT`, `.PATHTEXT` |
| `tf.position` | `[x, y]` |
| `tf.textRange` | Full text range for styling |
| `tf.characters` | Character collection |
| `tf.words` | Word collection |
| `tf.lines` | Line collection |
| `tf.paragraphs` | Paragraph collection |
| `tf.name` | Frame name (for `getByName`) |
| `tf.orientation` | `TextOrientation.HORIZONTAL` or `.VERTICAL` |
| `doc.textFrames.add()` | Add point text |
| `doc.textFrames.areaText(pathItem)` | Add area text inside a path |
| `doc.textFrames.pathText(pathItem)` | Add text on a path |
| `doc.textFrames.getByName("name")` | Get by name |

### Text Styling

```javascript
var attrs = tf.textRange.characterAttributes;
attrs.size = 24;                    // font size (points)
attrs.textFont = app.textFonts.getByName("Helvetica-Bold");
attrs.fillColor = rgbColor;         // RGBColor / CMYKColor
attrs.tracking = 50;                // letter spacing
attrs.leading = 28;                 // line height
attrs.baselineShift = 0;
attrs.horizontalScale = 100;        // percentage
attrs.verticalScale = 100;
attrs.rotation = 0;

var para = tf.textRange.paragraphAttributes;
para.justification = Justification.CENTER;  // LEFT, RIGHT, CENTER, FULLJUSTIFY
para.spaceAfter = 12;
para.spaceBefore = 0;
para.firstLineIndent = 0;
```

## PlacedItem

| Property / Method | Description |
|---|---|
| `placed.file` | File reference to linked file |
| `placed.position` | `[x, y]` |
| `placed.width` / `placed.height` | Dimensions |
| `placed.embed()` | Embed linked file |
| `placed.relink(fileRef)` | Relink to different file |
| `doc.placedItems.add()` | Place new item |

## GroupItem

| Property / Method | Description |
|---|---|
| `group.pageItems` | All items in the group |
| `group.pathItems` | Path items in the group |
| `group.textFrames` | Text frames in the group |
| `group.clipped` | Whether group is a clipping mask |
| `doc.groupItems.add()` | Create empty group |

## SymbolItem

```javascript
// Place existing symbol
var sym = doc.symbols.getByName("MySymbol");
var instance = doc.symbolItems.add(sym);
instance.position = [100, 500];

// Create symbol from selection
var sel = doc.selection[0];
var newSym = doc.symbols.add(sel);
```

## Color Objects

```javascript
// RGB
var c = new RGBColor();
c.red = 255; c.green = 128; c.blue = 0;

// CMYK
var c = new CMYKColor();
c.cyan = 0; c.magenta = 100; c.yellow = 100; c.black = 0;

// Grayscale
var c = new GrayColor();
c.gray = 50; // 0–100

// Spot color
var spot = doc.spots.add();
spot.name = "My Spot";
spot.color = rgbColor; // base color
var c = new SpotColor();
c.spot = spot;
c.tint = 100;

// No color (transparent)
var c = new NoColor();

// Gradient
var grad = doc.gradients.add();
grad.type = GradientType.LINEAR; // or RADIAL
grad.gradientStops[0].color = rgbColor;
grad.gradientStops[0].rampPoint = 0;
grad.gradientStops[1].color = rgbColor2;
grad.gradientStops[1].rampPoint = 100;

var c = new GradientColor();
c.gradient = grad;
c.angle = 45;
```

## Export Types & Options

### SVG
```javascript
var opts = new ExportOptionsSVG();
opts.embedRasterImages = true;
opts.fontSubsetting = SVGFontSubsetting.GLYPHSUSED;
opts.fontType = SVGFontType.OUTLINEFONT;
opts.coordinatePrecision = 3;
opts.DTD = SVGDTDVersion.SVG1_1;
opts.cssProperties = SVGCSSPropertyLocation.STYLEATTRIBUTES;
doc.exportFile(new File("/out.svg"), ExportType.SVG, opts);
```

### PNG-24
```javascript
var opts = new ExportOptionsPNG24();
opts.artBoardClipping = true;
opts.horizontalScale = 200;   // 2x
opts.verticalScale = 200;
opts.transparency = true;
opts.antiAliasing = true;
doc.exportFile(new File("/out.png"), ExportType.PNG24, opts);
```

### PNG-8
```javascript
var opts = new ExportOptionsPNG8();
opts.colorCount = 256;
opts.transparency = true;
opts.artBoardClipping = true;
doc.exportFile(new File("/out.png"), ExportType.PNG8, opts);
```

### JPEG
```javascript
var opts = new ExportOptionsJPEG();
opts.qualitySetting = 90;
opts.artBoardClipping = true;
opts.horizontalScale = 100;
opts.verticalScale = 100;
opts.antiAliasing = true;
doc.exportFile(new File("/out.jpg"), ExportType.JPEG, opts);
```

### PDF (save)
```javascript
var opts = new PDFSaveOptions();
opts.pDFPreset = "[Press Quality]";
opts.compatibility = PDFCompatibility.ACROBAT7;
opts.preserveEditability = true;
opts.viewAfterSaving = false;
doc.saveAs(new File("/out.pdf"), opts);
```

### EPS (save)
```javascript
var opts = new EPSSaveOptions();
opts.compatibility = Compatibility.ILLUSTRATOR17;
opts.preview = EPSPreview.COLORTIFF;
opts.embedLinkedFiles = true;
doc.saveAs(new File("/out.eps"), opts);
```

### Illustrator (save)
```javascript
var opts = new IllustratorSaveOptions();
opts.compatibility = Compatibility.ILLUSTRATOR17;
opts.flattenOutput = OutputFlattening.PRESERVEAPPEARANCE;
opts.embedICCProfile = true;
doc.saveAs(new File("/out.ai"), opts);
```

## Enumerations (commonly used)

| Enum | Values |
|---|---|
| `DocumentColorSpace` | `RGB`, `CMYK` |
| `SaveOptions` | `SAVECHANGES`, `DONOTSAVECHANGES`, `PROMPTTOSAVECHANGES` |
| `ExportType` | `SVG`, `PNG8`, `PNG24`, `JPEG`, `GIF`, `FLASH`, `PHOTOSHOP`, `TIFF`, `AutoCAD`, `WOSVG` |
| `BlendModes` | `NORMAL`, `MULTIPLY`, `SCREEN`, `OVERLAY`, `DARKEN`, `LIGHTEN`, `COLORDODGE`, `COLORBURN`, `HARDLIGHT`, `SOFTLIGHT`, `DIFFERENCE`, `EXCLUSION`, `HUE`, `SATURATION`, `COLOR`, `LUMINOSITY` |
| `Justification` | `LEFT`, `CENTER`, `RIGHT`, `FULLJUSTIFY`, `FULLJUSTIFYLASTLINELEFT`, `FULLJUSTIFYLASTLINECENTER`, `FULLJUSTIFYLASTLINERIGHT` |
| `StrokeCap` | `BUTTENDCAP`, `ROUNDENDCAP`, `PROJECTINGENDCAP` |
| `StrokeJoin` | `MITERENDJOIN`, `ROUNDENDJOIN`, `BEVELENDJOIN` |
| `ZOrderMethod` | `BRINGTOFRONT`, `BRINGFORWARD`, `SENDTOBACK`, `SENDBACKWARD` |
| `TextType` | `POINTTEXT`, `AREATEXT`, `PATHTEXT` |
| `Transformation` | `DOCUMENTORIGIN`, `TOPLEFT`, `LEFT`, `BOTTOMLEFT`, `BOTTOM`, `BOTTOMRIGHT`, `RIGHT`, `TOPRIGHT`, `TOP`, `CENTER` |
| `RulerUnits` | `Points`, `Picas`, `Inches`, `Millimeters`, `Centimeters`, `Pixels`, `Qs` |
