# FBX Interchange Troubleshooting Guide

## Contents
- [Scale Issues](#scale-issues)
- [Rotation/Axis Problems](#rotationaxis-problems)
- [Rig/Skeleton Issues](#rigskeleton-issues)
- [Animation Problems](#animation-problems)
- [Materials/Textures](#materialstextures)
- [Performance](#performance)

## Scale Issues

### Model is 100x too large/small

**Symptom:** Object appears microscopic or fills entire viewport.

**Cause:** Unit system mismatch. Blender uses meters, C4D defaults to centimeters.

**Solutions:**

1. **On export (Blender):**
   ```python
   apply_unit_scale=False  # Keep this OFF
   global_scale=1.0
   ```

2. **On import:** Scale by 0.01 or 100:
   - Blender → C4D: Usually works at 1:1
   - C4D → Blender: May need `global_scale=0.01`

3. **Post-import fix:**
   ```python
   # Blender: Scale all imported objects
   import bpy
   for obj in bpy.context.selected_objects:
       obj.scale *= 0.01
   bpy.ops.object.transform_apply(scale=True)
   ```

### Scale changes on each export cycle

**Cause:** Cumulative scale from `apply_unit_scale=True`.

**Fix:** Always use `apply_unit_scale=False` and apply scale before export:
```python
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
```

## Rotation/Axis Problems

### Model rotated -90 degrees on X

**Symptom:** Model lies flat or faces wrong direction.

**Cause:** Y-up vs Z-up coordinate systems.

**Blender export fix:**
```
axis_forward='-Z'
axis_up='Y'
```

**Post-import fix (Blender):**
```python
import bpy
from mathutils import Matrix

# Rotate -90 on X to fix
for obj in bpy.context.selected_objects:
    obj.matrix_world = Matrix.Rotation(-1.5708, 4, 'X') @ obj.matrix_world
    bpy.ops.object.transform_apply(rotation=True)
```

### Objects offset from origin

**Cause:** World origin differences or object pivot points.

**Blender pre-export:**
```python
# Center all origins
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
# Clear location
bpy.ops.object.location_clear()
```

## Rig/Skeleton Issues

### Bones have wrong orientation after import

**Symptom:** Bones point in wrong direction, rig looks broken.

**Blender import fix:**
```python
automatic_bone_orientation=True
primary_bone_axis='Y'
secondary_bone_axis='X'
```

**Manual fix in Blender:**
```python
import bpy
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.select_all(action='SELECT')
bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
bpy.ops.object.mode_set(mode='OBJECT')
```

### Extra leaf bones appear

**Cause:** FBX adds end bones by default.

**Blender export:** `add_leaf_bones=False`

**Blender import:** `ignore_leaf_bones=True`

### Disconnected bone chains

**Symptom:** Bones don't connect head-to-tail.

**Blender import:** `force_connect_children=True`

### Skinning weights missing

**Causes:**
1. Vertex groups not named same as bones
2. Zero weights not exported

**Pre-export checklist:**
1. Vertex group names match bone names exactly
2. Normalize weights: `bpy.ops.object.vertex_group_normalize_all()`
3. Remove zero-weight vertices: `bpy.ops.object.vertex_group_clean()`

## Animation Problems

### No animation after import

**Causes:**
1. Animation not baked
2. NLA strips not exported

**Blender export:**
```python
bake_anim=True
bake_anim_use_nla_strips=False
bake_anim_use_all_actions=True
```

### Animation timing is off

**Cause:** Frame rate mismatch.

**Check frame rates:**
- Blender: `bpy.context.scene.render.fps`
- C4D: Project Settings → Frame Rate

**Set matching frame rate before export.**

### Constraints not working

**Issue:** IK, copy rotation, etc. don't transfer via FBX.

**Solution:** Bake constrained motion to keyframes:
```python
import bpy

bpy.ops.nla.bake(
    frame_start=1,
    frame_end=250,
    only_selected=False,
    visual_keying=True,
    clear_constraints=True,
    bake_types={'POSE'}
)
```

### Animation plays on wrong object

**Cause:** Object/armature naming conflicts.

**Fix:** Ensure unique names before export:
```python
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        obj.name = f"ARM_{obj.name}"
```

## Materials/Textures

### Materials missing

**Cause:** Incompatible shader nodes.

**Fix:** Use only Principled BSDF or basic nodes:
- Base Color
- Metallic
- Roughness
- Normal Map
- Emission

Complex node setups don't transfer. Bake to textures first.

### Textures not found

**Causes:**
1. Embedded textures disabled
2. Path references broken

**Blender export options:**
- `path_mode='COPY'` - Copy textures to export folder
- `embed_textures=True` - Embed in FBX file (larger file)

### UV maps missing

**Cause:** Multiple UV maps not all exported.

**Blender:** FBX exports all UV maps, but only active UV layer is primary.

**Pre-export:** Set correct UV map as active:
```python
mesh = bpy.context.object.data
mesh.uv_layers["UVMap"].active = True
```

## Performance

### FBX file is huge

**Causes:**
1. Embedded textures
2. High-poly geometry
3. Unnecessary data

**Reduce size:**
```python
# Blender export
embed_textures=False
use_mesh_edges=False
use_custom_props=False
```

### Import takes forever

**Causes:**
1. Complex hierarchy
2. Many materials
3. High vertex count

**Speed up:**
1. Import without animation first
2. Decimate before export
3. Merge materials where possible

### Blender crashes on import

**Possible fixes:**
1. Import without materials: uncheck "Import Materials"
2. Import in smaller chunks
3. Update Blender to latest version
4. Try ASCII FBX instead of binary (for debugging)
