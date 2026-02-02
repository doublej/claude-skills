# Cinema 4D FBX Export/Import Guide

## Contents
- [Export to Blender](#export-to-blender)
- [Import from Blender](#import-from-blender)
- [Python Scripting](#python-scripting)
- [Version Differences](#version-differences)

## Export to Blender

### Export Dialog Settings

```
File → Export → FBX (.fbx)

General:
├── FBX Version: 7.4 binary (recommended)
├── Coordinate System: Y-Up, Right-Handed
├── Scale Factor: 1.0
└── ASCII: OFF (binary is smaller/faster)

Include:
├── Geometry: ON
├── Materials: ON
├── Textures: Embed or Reference
├── Cameras: As needed
├── Lights: As needed
└── Animation: ON

Geometry:
├── Triangulate: OFF (preserve quads for Blender)
├── Save Normals: ON
├── Save Vertex Colors: ON
├── Save UVs: ON
└── SDS Subdivision Surfaces: OFF (export as mesh if needed)

Animation:
├── Animation: ON
├── Bake All Frames: ON (if using constraints/expressions)
├── Frame Start/End: Match your timeline
└── Sampling Rate: 1 (every frame)
```

### Joint/Skeleton Export

C4D joints map to Blender armature bones:
- Joint objects → Bones
- Skin deformer → Armature modifier with vertex groups
- Weight tags → Vertex weights

**Best practices:**
1. Freeze all transforms on joints before export
2. Ensure skin binding is in bind pose
3. Remove unused influence (weight optimization)

## Import from Blender

### Import Dialog Settings

```
File → Import → FBX (.fbx)

Coordinate System:
├── Detect: ON (auto-detect from file)
├── Or manually: Y-Up, -Z Forward
└── Scale: Auto or 1.0

Include:
├── Geometry: ON
├── Materials: ON
├── Animation: ON
├── Cameras/Lights: As needed
└── Merge Takes: OFF (keep animations separate)

Options:
├── Import Normals: ON
├── Import Materials: Create New
└── Create Unknown Nodes: OFF
```

### Post-Import Fixes

**Wrong scale:**
- Select all objects
- Scale uniformly: 0.01 or 100 depending on direction
- Freeze transforms

**Flipped normals:**
- Select mesh
- Mesh → Normals → Reverse Normals

**Missing textures:**
- Check texture paths in Material Manager
- Relink to correct texture files

## Python Scripting

### Export via Python (c4d module)

```python
import c4d
from c4d import documents

def export_fbx(doc, filepath):
    # Get FBX export plugin
    plug = c4d.plugins.FindPlugin(1026370, c4d.PLUGINTYPE_SCENESAVER)
    if not plug:
        return False

    # Get export settings container
    op = {}
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        fbxExport = op.get("imexporter")
        if fbxExport:
            # Configure settings
            fbxExport[c4d.FBXEXPORT_FBX_VERSION] = c4d.FBX_EXPORTVERSION_NATIVE
            fbxExport[c4d.FBXEXPORT_ASCII] = False
            fbxExport[c4d.FBXEXPORT_CAMERAS] = False
            fbxExport[c4d.FBXEXPORT_LIGHTS] = False
            fbxExport[c4d.FBXEXPORT_SPLINES] = False
            fbxExport[c4d.FBXEXPORT_ANIMATIONS] = True
            fbxExport[c4d.FBXEXPORT_BAKEFRAMES] = True
            fbxExport[c4d.FBXEXPORT_PLA_TO_VERTEXCACHE] = False
            fbxExport[c4d.FBXEXPORT_TRIANGULATE] = False
            fbxExport[c4d.FBXEXPORT_SAVE_NORMALS] = True
            fbxExport[c4d.FBXEXPORT_SAVE_VERTEX_COLORS] = True
            fbxExport[c4d.FBXEXPORT_SAVE_UV] = True

    # Export
    return c4d.documents.SaveDocument(
        doc, filepath,
        c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,
        1026370  # FBX exporter ID
    )
```

### Import via Python

```python
import c4d
from c4d import documents

def import_fbx(filepath):
    # Load FBX file
    doc = c4d.documents.LoadDocument(
        filepath,
        c4d.SCENEFILTER_OBJECTS |
        c4d.SCENEFILTER_MATERIALS |
        c4d.SCENEFILTER_ANIMATION
    )

    if doc:
        c4d.documents.InsertBaseDocument(doc)
        c4d.documents.SetActiveDocument(doc)
        return True
    return False
```

### Batch Export Selected

```python
import c4d
import os

def batch_export_selected(output_dir):
    doc = c4d.documents.GetActiveDocument()
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    for obj in selection:
        # Create temp doc with just this object
        temp_doc = c4d.documents.BaseDocument()
        clone = obj.GetClone()
        temp_doc.InsertObject(clone)

        # Export
        filepath = os.path.join(output_dir, f"{obj.GetName()}.fbx")
        c4d.documents.SaveDocument(
            temp_doc, filepath,
            c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,
            1026370
        )

        # Cleanup
        c4d.documents.KillDocument(temp_doc)
```

## Version Differences

### FBX Versions

| Version | Notes |
|---------|-------|
| FBX 7.4 | Best compatibility, recommended |
| FBX 7.5 | Better blend shapes support |
| FBX 2020 | Latest features, may have issues in older Blender |

### C4D Version Notes

**R23+:**
- Improved FBX 7.5 support
- Better joint orientation preservation

**R25+:**
- Scene Nodes not exported to FBX
- Convert to classic objects first

**2023+:**
- Enhanced weight map precision
- Better morph target support

### Blender Version Compatibility

| Blender | Best FBX Version | Notes |
|---------|------------------|-------|
| 2.8x | 7.4 | Most stable |
| 2.9x | 7.4 | Good support |
| 3.x | 7.4/7.5 | Improved importer |
| 4.x | 7.4/7.5 | Best compatibility yet |
