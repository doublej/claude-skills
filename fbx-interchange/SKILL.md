---
name: fbx-interchange
description: Expert guidance for FBX asset interchange between Blender and Cinema 4D with MCP integration. Use when transferring 3D models, rigs, or animations between Blender and C4D, troubleshooting FBX import/export issues, fixing scale/axis problems, or automating FBX workflows via Blender MCP.
---

# FBX Interchange: Blender ↔ Cinema 4D

Transfer 3D assets between Blender and Cinema 4D via FBX with correct scale, axes, and rig preservation.

## MCP Integration

When Blender MCP is available, automate exports directly:

### Export via MCP

```python
# Execute in Blender via MCP
mcp__blender__execute_blender_code(code="""
import bpy

# Apply transforms before export
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# Export with C4D-compatible settings
bpy.ops.export_scene.fbx(
    filepath="/path/to/output.fbx",
    use_selection=False,
    global_scale=1.0,
    apply_unit_scale=False,
    apply_scale_options='FBX_SCALE_ALL',
    axis_forward='-Z',
    axis_up='Y',
    add_leaf_bones=False,
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    bake_anim=True,
    bake_anim_use_nla_strips=False,
    mesh_smooth_type='FACE',
    use_tspace=True
)
""")
```

### Import via MCP

```python
# Import FBX from C4D into Blender
mcp__blender__execute_blender_code(code="""
import bpy

bpy.ops.import_scene.fbx(
    filepath="/path/to/from_c4d.fbx",
    global_scale=1.0,
    use_custom_normals=True,
    ignore_leaf_bones=True,
    force_connect_children=True,
    automatic_bone_orientation=True,
    primary_bone_axis='Y',
    secondary_bone_axis='X'
)
""")
```

### Scene Inspection

```python
# Check scene before export
mcp__blender__get_scene_info()

# Get object details
mcp__blender__get_object_info(object_name="Armature")

# Screenshot for verification
mcp__blender__get_viewport_screenshot(max_size=800)
```

## Quick Reference

| From | To | Key Settings |
|------|-----|--------------|
| Blender | C4D | Scale: 1.0, Apply Transform, -Z Forward, Y Up |
| C4D | Blender | FBX 7.4, Y-Up, Auto-detect scale |

## Blender → Cinema 4D

### Export Settings (Blender)

```
Export FBX (.fbx):
├── Scale: 1.0
├── Apply Scalings: FBX All
├── Forward: -Z Forward
├── Up: Y Up
├── Apply Unit: OFF (critical!)
├── Apply Transform: ON
├── Geometry:
│   ├── Smoothing: Face
│   └── Tangent Space: ON (if using normal maps)
├── Armature:
│   ├── Primary Bone Axis: Y
│   └── Secondary Bone Axis: X
└── Animation:
    ├── Bake Animation: ON
    └── NLA Strips: OFF (unless needed)
```

Run `scripts/blender_export_for_c4d.py` in Blender for automated export.

### Import in Cinema 4D

1. File → Import → FBX
2. Settings:
   - Coordinate System: Auto-detect
   - Scale: 1.0
   - Import Animation: ON
   - Merge Sequences: OFF

## Cinema 4D → Blender

### Export Settings (C4D)

```
Export FBX:
├── FBX Version: 7.4 binary (most compatible)
├── Coordinate System: Y-Up
├── Export:
│   ├── Geometry: ON
│   ├── Materials: ON
│   └── Animation: ON
└── Geometry:
    ├── Triangulate: OFF (preserve quads)
    └── Save Normals: ON
```

### Import in Blender

```
Import FBX:
├── Scale: 1.0
├── Apply Transform: ON
├── Ignore Leaf Bones: ON
├── Force Connect Children: ON
└── Automatic Bone Orientation: ON
```

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Model 100x too small/large | Unit mismatch | Set Scale to 0.01 or 100 |
| Model rotated -90° | Axis convention | Use -Z Forward, Y Up in Blender |
| Broken rig hierarchy | Bone axis mismatch | Use Primary Y, Secondary X |
| Missing animations | Not baked | Enable Bake Animation |
| Deformed mesh on import | Double transforms | Disable Apply Unit in Blender |

## Detailed Guides

- **[references/blender-fbx.md](references/blender-fbx.md)**: Blender export/import deep dive
- **[references/c4d-fbx.md](references/c4d-fbx.md)**: Cinema 4D export/import settings
- **[references/troubleshooting.md](references/troubleshooting.md)**: Extended problem-solving guide
