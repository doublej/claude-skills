---
name: blender
description: Comprehensive Blender 4.x+ assistance including MCP integration, Python scripting (bpy), and modeling workflows. Use when working with Blender scenes, automating tasks, or integrating with asset libraries (PolyHaven, Sketchfab, Hyper3D, Hunyuan3D).
---

# Blender Skill

Assistance for Blender 4.x workflows, Python scripting, asset integration, and MCP operations.

## When to Use

- Inspecting or modifying Blender scenes via MCP
- Writing Python scripts for Blender automation (bpy)
- Importing assets from PolyHaven, Sketchfab, Hyper3D, or Hunyuan3D
- Modeling, materials, rendering, and scene composition

## Version Info

- **Latest Stable**: Blender 5.0 (Nov 2025)
- **Latest LTS**: Blender 4.5 LTS (Jul 2025)
- **Recommended**: Blender 4.3+

## MCP Quick Start

```python
# Scene inspection
mcp__blender__get_scene_info()
mcp__blender__get_object_info(object_name="Cube")
mcp__blender__get_viewport_screenshot(max_size=800)

# Execute code
mcp__blender__execute_blender_code(code="""
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
""")
```

## Python Scripting (bpy)

### Core Modules

```python
import bpy

bpy.context    # Current state (active scene, mode)
bpy.data       # All data in .blend
bpy.ops        # Operators (create undo steps)
```

**Prefer `bpy.data` over `bpy.ops`** - faster, no undo overhead.

### Common Patterns

```python
# Create object directly
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.scene.collection.objects.link(obj)
obj.location = (1, 2, 3)

# Material with Principled BSDF
mat = bpy.data.materials.new(name="PBR")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.8, 0.2, 0.1, 1.0)
obj.data.materials.append(mat)

# Delete object
bpy.data.objects.remove(obj, do_unlink=True)
```

## Workflow Guidelines

### Scene Organization
- Use collections to group related objects
- Name objects descriptively
- Apply transforms before exporting

### Materials & Textures
- Always use Principled BSDF for PBR
- Pack textures into .blend for portability
- Bake complex materials for game engines

### Rendering
- Render to image sequence, not video directly
- Use OpenEXR for professional VFX work
- Preview in final viewport shading first

## Quick Reference

| Task | Method |
|------|--------|
| Add cube | `bpy.ops.mesh.primitive_cube_add()` |
| Delete object | `bpy.data.objects.remove(obj, do_unlink=True)` |
| Add modifier | `obj.modifiers.new(name="Subsurf", type='SUBSURF')` |
| Export glTF | `bpy.ops.export_scene.gltf(filepath="/path/file.glb")` |
| Export FBX | `bpy.ops.export_scene.fbx(filepath="/path/file.fbx")` |
| Render frame | `bpy.ops.render.render(write_still=True)` |
| Render animation | `bpy.ops.render.render(animation=True)` |

## Output Formats

| Use Case | Format |
|----------|--------|
| Web/Preview | PNG 8-bit |
| High Quality | OpenEXR 16/32-bit |
| 3D Printing | STL |
| Game Engines | glTF/FBX |

## Reference Files

- [bpy Scripting](references/bpy-scripting.md) - Detailed Python patterns
- [Async Patterns](references/async-patterns.md) - Avoiding UI freeze
- [MCP Integration](references/mcp-integration.md) - Asset libraries, AI generation

## Blender 4.3+ Changes

### New Python API Features
- `ID.rename()` - Sophisticated renaming
- `bpy.app.handlers.blend_import_pre/post` - Import hooks
- `Curves.remove_curves()`, `resize_curves()`

### Breaking Changes
- Grease Pencil API completely rewritten
- `AttributeGroup` split into specialized types
- Legacy EEVEE shadow properties removed

## Documentation

- [Official Blender Python API](https://docs.blender.org/api/current/)
- [Blender Manual](https://docs.blender.org/manual/en/latest/)
- [Release Notes](https://developer.blender.org/docs/release_notes/)
