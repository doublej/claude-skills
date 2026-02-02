# Blender Python Scripting (bpy)

Detailed patterns for Python scripting in Blender.

## API Best Practices

**Prefer `bpy.data` over `bpy.ops`:**
- `bpy.data` - Direct data access (faster, no undo overhead)
- `bpy.ops` - Context-dependent operators (create undo steps)

```python
# GOOD: Direct data manipulation
obj.location = (1, 2, 3)

# AVOID IN LOOPS: Creates undo steps
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
```

## Core Modules

```python
import bpy

bpy.context    # Current state (active scene, selected objects, mode)
bpy.data       # All data in .blend (objects, materials, meshes)
bpy.ops        # Operators (file I/O, vertex operations)
bpy.types      # Data type definitions
bpy.app        # Application-level (version, handlers)
bpy.msgbus     # Event system for property changes
```

## Object Creation

### Direct Method (Preferred)

```python
# Create mesh and object
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.scene.collection.objects.link(obj)

# Position and scale
obj.location = (1, 2, 3)
obj.rotation_euler = (0, 0, 1.57)  # Radians
obj.scale = (2, 2, 2)
```

### Operators (When Needed)

```python
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3, 0, 0))
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2)

obj = bpy.context.active_object
```

## Materials with Principled BSDF

```python
# Create material with nodes
mat = bpy.data.materials.new(name="PBRMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes

# Get or create Principled BSDF
bsdf = nodes.get("Principled BSDF")
if not bsdf:
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')

# Set PBR properties
bsdf.inputs["Base Color"].default_value = (0.8, 0.2, 0.1, 1.0)  # RGBA
bsdf.inputs["Metallic"].default_value = 0.5
bsdf.inputs["Roughness"].default_value = 0.3

# Assign to object
obj.data.materials.append(mat)
```

## Collections

```python
# Create collection
col = bpy.data.collections.new("MyCollection")
bpy.context.scene.collection.children.link(col)

# Link/unlink objects
col.objects.link(obj)
bpy.context.scene.collection.objects.unlink(obj)

# Get all objects in collection
objects = col.objects
```

## Selection & Context

```python
# Deselect all
bpy.ops.object.select_all(action='DESELECT')

# Select specific object
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Get all selected
selected = bpy.context.selected_objects

# Check mode
if bpy.context.mode == 'OBJECT':
    pass  # Object mode operations
elif bpy.context.mode == 'EDIT_MESH':
    pass  # Edit mode operations
```

## Delete Objects

```python
# Direct deletion (preferred)
bpy.data.objects.remove(obj, do_unlink=True)

# Operator
bpy.ops.object.delete()
```

## Edit Mode Operations

```python
import bmesh

# Enter edit mode
bpy.ops.object.mode_set(mode='EDIT')

# Get bmesh
bm = bmesh.from_edit_mesh(obj.data)

# Operations
bm.faces.ensure_lookup_table()
for face in bm.faces:
    face.select = True

# Update mesh
bmesh.update_edit_mesh(obj.data)

# Return to object mode
bpy.ops.object.mode_set(mode='OBJECT')
```

## Modifiers

```python
# Add modifier
mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
mod.levels = 2
mod.render_levels = 3

# Apply modifier
bpy.ops.object.modifier_apply(modifier="Subsurf")
```

## Animation

```python
# Set keyframe
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)

obj.location = (5, 0, 0)
obj.keyframe_insert(data_path="location", frame=60)

# Set frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60
```

## Rendering

```python
# Engine selection
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Fast
bpy.context.scene.render.engine = 'CYCLES'  # Accurate

# Resolution
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Output
bpy.context.scene.render.filepath = "/path/to/output"
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Render
bpy.ops.render.render(write_still=True)  # Single frame
bpy.ops.render.render(animation=True)  # Animation
```

## File Operations

```python
# Save/Load
bpy.ops.wm.save_as_mainfile(filepath="/path/to/file.blend")
bpy.ops.wm.open_mainfile(filepath="/path/to/file.blend")

# Append/Link from another file
bpy.ops.wm.append(filepath="/path/file.blend/Object/ObjectName")
bpy.ops.wm.link(filepath="/path/file.blend/Material/MaterialName")

# Export
bpy.ops.export_scene.gltf(filepath="/path/file.glb")
bpy.ops.export_scene.fbx(filepath="/path/file.fbx")
```
