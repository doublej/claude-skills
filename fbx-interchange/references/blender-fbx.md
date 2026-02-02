# Blender FBX Export/Import Guide

## Contents
- [Export to Cinema 4D](#export-to-cinema-4d)
- [Import from Cinema 4D](#import-from-cinema-4d)
- [Armature/Rig Considerations](#armaturerig-considerations)
- [Animation Export](#animation-export)

## Export to Cinema 4D

### Operator Parameters (bpy.ops.export_scene.fbx)

```python
bpy.ops.export_scene.fbx(
    filepath="output.fbx",
    use_selection=False,          # Export selected only
    use_visible=False,            # Export visible only
    use_active_collection=False,  # Export active collection only
    global_scale=1.0,             # Scale factor
    apply_unit_scale=False,       # CRITICAL: Keep OFF for C4D
    apply_scale_options='FBX_SCALE_ALL',
    axis_forward='-Z',            # C4D expects -Z forward
    axis_up='Y',                  # C4D expects Y up
    object_types={'ARMATURE', 'MESH', 'OTHER'},
    use_mesh_modifiers=True,      # Apply modifiers
    use_mesh_modifiers_render=True,
    mesh_smooth_type='FACE',
    use_subsurf=False,            # Apply subdiv as mesh
    use_mesh_edges=False,
    use_tspace=True,              # Tangent space for normal maps
    use_triangles=False,          # Keep quads
    use_custom_props=False,
    add_leaf_bones=False,         # Avoid extra bones
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    use_armature_deform_only=False,
    armature_nodetype='NULL',
    bake_anim=True,
    bake_anim_use_all_bones=True,
    bake_anim_use_nla_strips=False,
    bake_anim_use_all_actions=False,
    bake_anim_force_startend_keying=True,
    bake_anim_step=1.0,
    bake_anim_simplify_factor=1.0,
    path_mode='AUTO',
    embed_textures=False,
    batch_mode='OFF',
)
```

### Scale Settings Explained

| Setting | Value | Effect |
|---------|-------|--------|
| `global_scale` | 1.0 | No scaling applied |
| `apply_unit_scale` | False | Preserves Blender's internal units |
| `apply_scale_options` | FBX_SCALE_ALL | Bakes object scale into mesh |

**Why `apply_unit_scale=False`?**
Blender uses meters internally. With `apply_unit_scale=True`, a 2m cube becomes 200 units in C4D (assuming C4D is set to cm). Keeping it OFF preserves the numeric values.

### Axis Conventions

```
Blender default:    Cinema 4D:
  +Z (up)             +Y (up)
   |                   |
   +-- +Y (forward)    +-- +Z (forward)
  /                   /
+X                  +X

Export with: -Z Forward, Y Up
```

## Import from Cinema 4D

### Operator Parameters (bpy.ops.import_scene.fbx)

```python
bpy.ops.import_scene.fbx(
    filepath="input.fbx",
    use_manual_orientation=False,
    global_scale=1.0,
    bake_space_transform=False,
    use_custom_normals=True,
    use_image_search=True,
    use_alpha_decals=False,
    decal_offset=0.0,
    use_anim=True,
    anim_offset=1.0,
    use_subsurf=False,
    use_custom_props=True,
    use_custom_props_enum_as_string=True,
    ignore_leaf_bones=True,       # Clean up hierarchy
    force_connect_children=True,  # Fix disconnected bones
    automatic_bone_orientation=True,
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    use_prepost_rot=True,
)
```

### Import Fixes

**Bones have wrong orientation:**
```python
# After import, select armature and run:
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
bpy.ops.object.mode_set(mode='OBJECT')
```

**Scale is wrong:**
- Try `global_scale=0.01` (C4D cm to Blender m)
- Or `global_scale=100.0` (opposite direction)

## Armature/Rig Considerations

### Bone Naming
FBX preserves bone names. Ensure names don't contain:
- Periods (`.`) - Blender uses these for hierarchy
- Colons (`:`) - Can cause namespace issues

### Weight Painting
- Vertex groups transfer via FBX
- Normalize weights before export: `bpy.ops.object.vertex_group_normalize_all()`

### Constraints
FBX does NOT transfer:
- IK constraints
- Copy rotation/location
- Drivers

**Solution:** Bake constrained motion to keyframes before export.

## Animation Export

### Baking Actions

```python
# Bake all actions to keyframes
for action in bpy.data.actions:
    # Set action as active
    obj.animation_data.action = action
    # Bake
    bpy.ops.nla.bake(
        frame_start=int(action.frame_range[0]),
        frame_end=int(action.frame_range[1]),
        only_selected=False,
        visual_keying=True,
        clear_constraints=False,
        bake_types={'POSE'}
    )
```

### Multiple Actions
To export multiple animations:
1. Use NLA strips (enable `bake_anim_use_nla_strips`)
2. Or export separate FBX files per action
3. Or use Takes in FBX (C4D can read these)

### Frame Rate
Match frame rates between applications:
- Check: `bpy.context.scene.render.fps`
- C4D default: 30 fps
- Set before export to avoid timing issues
