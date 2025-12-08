---
name: blender
description: Comprehensive Blender 4.x+ assistance including MCP integration, Python scripting (bpy), and modeling workflows. Use when working with Blender scenes, automating tasks, or integrating with asset libraries (PolyHaven, Sketchfab, Hyper3D, Hunyuan3D).
---

# Blender Skill

Comprehensive assistance for Blender 4.x workflows, Python scripting, asset integration, and MCP operations.

## When to Use

- Inspecting or modifying Blender scenes via MCP
- Writing Python scripts for Blender automation (bpy)
- Importing assets from PolyHaven, Sketchfab, Hyper3D, or Hunyuan3D
- Modeling, materials, rendering, and scene composition
- Rendering and output configuration

## Current Version Info

- **Latest Stable**: Blender 5.0 (Nov 2025)
- **Latest LTS**: Blender 4.5 LTS (Jul 2025, supported until Jul 2027)
- **Recommended**: Blender 4.3+ for latest API features

## MCP Integration

### Scene Inspection

```python
# Get scene overview
mcp__blender__get_scene_info()

# Get specific object details
mcp__blender__get_object_info(object_name="Cube")

# Take viewport screenshot
mcp__blender__get_viewport_screenshot(max_size=800)
```

### Executing Python Code

Use `mcp__blender__execute_blender_code` for direct bpy operations:

```python
# Always break into small chunks
mcp__blender__execute_blender_code(code="""
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
""")
```

### Asset Libraries

**PolyHaven** (HDRIs, textures, models):
```python
# Check status
mcp__blender__get_polyhaven_status()

# Search assets
mcp__blender__search_polyhaven_assets(asset_type="hdris", categories="outdoor")

# Download and apply
mcp__blender__download_polyhaven_asset(asset_id="autumn_field", asset_type="hdris", resolution="2k")
mcp__blender__set_texture(object_name="Ground", texture_id="brick_wall")
```

**Sketchfab** (3D models):
```python
mcp__blender__get_sketchfab_status()
mcp__blender__search_sketchfab_models(query="chair", downloadable=True, count=10)
mcp__blender__download_sketchfab_model(uid="abc123")
```

**AI Generation** (Hyper3D Rodin):
```python
mcp__blender__get_hyper3d_status()

# Generate from text
mcp__blender__generate_hyper3d_model_via_text(text_prompt="wooden chair")

# Poll until done
mcp__blender__poll_rodin_job_status(subscription_key="...")

# Import result
mcp__blender__import_generated_asset(name="Chair", task_uuid="...")
```

**AI Generation** (Hunyuan3D):
```python
mcp__blender__get_hunyuan3d_status()
mcp__blender__generate_hunyuan3d_model(text_prompt="red sports car")
mcp__blender__poll_hunyuan_job_status(job_id="job_xxx")
mcp__blender__import_generated_asset_hunyuan(name="Car", zip_file_url="...")
```

## Python Scripting (bpy)

### API Best Practices

**Prefer `bpy.data` over `bpy.ops`:**
- `bpy.data` - Direct data access (faster, no undo overhead)
- `bpy.ops` - Context-dependent operators (create undo steps)

```python
# GOOD: Direct data manipulation
obj.location = (1, 2, 3)

# AVOID IN LOOPS: Creates undo steps
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
```

### Core Modules

```python
import bpy

bpy.context    # Current state (active scene, selected objects, mode)
bpy.data       # All data in .blend (objects, materials, meshes)
bpy.ops        # Operators (file I/O, vertex operations)
bpy.types      # Data type definitions
bpy.app        # Application-level (version, handlers)
bpy.msgbus     # Event system for property changes
```

### Common Patterns

**Object Creation (Direct):**
```python
# Create mesh and object
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.scene.collection.objects.link(obj)

# Position and scale
obj.location = (1, 2, 3)
obj.rotation_euler = (0, 0, 1.57)  # Radians
obj.scale = (2, 2, 2)
obj.name = "MyCube"
```

**Object Creation (Operators):**
```python
# Only use for specific cases (no direct data equivalent)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3, 0, 0))
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2)

obj = bpy.context.active_object
```

**Materials with Principled BSDF:**
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

**Collections:**
```python
# Create collection
col = bpy.data.collections.new("MyCollection")
bpy.context.scene.collection.children.link(col)

# Link/unlink objects
col.objects.link(obj)
bpy.context.scene.collection.objects.unlink(obj)  # Unlink before relinking

# Get all objects in collection
objects = col.objects
```

**Selection & Context:**
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

**Delete Objects:**
```python
# Direct deletion (preferred)
bpy.data.objects.remove(obj, do_unlink=True)

# Operator (use if data method unavailable)
bpy.ops.object.delete()
```

### Edit Mode Operations

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

### Modifiers

```python
# Add modifier
mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
mod.levels = 2
mod.render_levels = 3

# Apply modifier
bpy.ops.object.modifier_apply(modifier="Subsurf")
```

### Animation

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

### Rendering & Output

**Render Engines:**
```python
# EEVEE (real-time, fast, rasterization-based)
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Cycles (path tracing, physically accurate)
bpy.context.scene.render.engine = 'CYCLES'
```

**Render Settings:**
```python
# Resolution
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120

# Output format and path
bpy.context.scene.render.filepath = "/path/to/output"
bpy.context.scene.render.image_settings.file_format = 'PNG'  # or 'JPEG', 'OPEN_EXR'
bpy.context.scene.render.image_settings.color_depth = '16'  # 8, 16, or 32 bit

# Render animation as image sequence (safe, resumable)
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = "/path/frame_####.png"
bpy.ops.render.render(animation=True)

# Or single frame
bpy.ops.render.render(write_still=True)
```

**Output Format Recommendations:**
| Use Case | Format | Notes |
|----------|--------|-------|
| Web/Preview | PNG 8-bit | Lossless, widely compatible |
| High Quality | OpenEXR 16/32-bit | HDR, professional |
| Video/Web | MP4 via FFmpeg | Use image sequence first |
| 3D Printing | STL | Via export |
| Game Engines | glTF/FBX | Optimized formats |

### File Operations

```python
# Save file
bpy.ops.wm.save_as_mainfile(filepath="/path/to/file.blend")

# Load file
bpy.ops.wm.open_mainfile(filepath="/path/to/file.blend")

# Append/Link from another file
bpy.ops.wm.append(filepath="/path/file.blend/Object/ObjectName")
bpy.ops.wm.link(filepath="/path/file.blend/Material/MaterialName")

# Export to formats
bpy.ops.export_scene.gltf(filepath="/path/file.glb")
bpy.ops.export_scene.fbx(filepath="/path/file.fbx")
bpy.ops.wm.usd_export(filepath="/path/file.usd")
```

### Avoiding UI Freeze

**Problem:** Long scripts freeze Blender UI

**Rule of thumb:** Don't block main thread > 16ms (60fps)

#### 1. Modal Operator with Timer (Recommended for <10s work)

Break operations into small chunks per frame:

```python
import bpy

class MODAL_OT_process_data(bpy.types.Operator):
    bl_idname = "wm.modal_process"
    bl_label = "Process Data"

    _timer = None
    _index = 0
    _items = list(range(1000))

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._index < len(self._items):
                # Process small batch per frame
                batch_size = 10
                for i in range(batch_size):
                    if self._index < len(self._items):
                        self.process_item(self._items[self._index])
                        self._index += 1
                return {'RUNNING_MODAL'}
            else:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                return {'FINISHED'}

        elif event.type == 'ESC':
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def process_item(self, item):
        # Do work here
        pass

# Run it
bpy.ops.wm.modal_process('INVOKE_DEFAULT')
```

#### 2. Frame Change Handler (For <5s animations)

Let Blender's frame loop drive work:

```python
import bpy

class ProcessState:
    def __init__(self, items):
        self.index = 0
        self.items = items

    def process_frame(self, scene):
        """Called each rendered frame"""
        if self.index < len(self.items):
            self.process_item(self.items[self.index])
            self.index += 1
            print(f"Progress: {self.index}/{len(self.items)}")
        else:
            bpy.app.handlers.frame_change_post.remove(self.process_frame)

    def process_item(self, item):
        pass

# Set up
state = ProcessState(list(range(1000)))
bpy.app.handlers.frame_change_post.append(state.process_frame)

# Trigger by playing animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 1000
bpy.ops.screen.animation_play()
```

#### 3. Background Thread (For CPU-heavy work, no Blender data modifications)

```python
import bpy
import threading
from queue import Queue

result_queue = Queue()

def background_compute(items):
    """Runs in background - don't modify Blender here!"""
    for item in items:
        result = expensive_calculation(item)
        result_queue.put(result)

def expensive_calculation(x):
    # Simulate heavy work
    return sum(i**2 for i in range(100000))

# Start background thread
items = list(range(100))
thread = threading.Thread(target=background_compute, args=(items,))
thread.daemon = True
thread.start()

# Collect results in modal operator (safe in main thread)
class MODAL_OT_collect(bpy.types.Operator):
    bl_idname = "wm.collect_results"
    bl_label = "Collect Results"
    _timer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            # Collect available results
            while not result_queue.empty():
                result = result_queue.get()
                self.apply_result(result)

            # Check if thread done
            if not thread.is_alive() and result_queue.empty():
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def apply_result(self, result):
        # Modify Blender here (safe in main thread)
        print(f"Result: {result}")
```

#### 4. Disable Updates During Batch Operations

If you must work synchronously:

```python
import bpy

# Disable viewport updates
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'SOLID'  # Fastest viewport
                space.overlay.show_wireframes = False

# Batch operations without undo (faster)
with bpy.context.temp_override(use_undo=False):
    for i in range(1000):
        create_object(i)

# Force viewport redraw
for area in bpy.context.screen.areas:
    if area.type in ['VIEW_3D', 'PROPERTIES']:
        area.tag_redraw()
```

#### Quick Selection Guide

| Time | Method | Use Case |
|------|--------|----------|
| < 100ms | Direct execution | Simple operations |
| 100ms-1s | Modal operator + timer | Batch object creation |
| 1-10s | Modal + frame handler | Complex mesh operations |
| 10s+ | Background thread + queue | Simulation, rendering prep |

## Workflow Guidelines

### Scene Organization
- Use collections to group related objects (UI, props, characters, etc.)
- Name objects descriptively (not "Cube.001")
- Apply transforms before exporting (`Ctrl+A` in UI → Scale)
- Keep origin points consistent

### Asset Management
- Mark reusable objects as assets (`obj.asset_mark()`)
- Use **Link** for repeated instances (memory efficient)
- Use **Append** for unique editable copies
- Create asset bundles (`_bundle.blend`) with packed textures

### Performance
- Use instances for repeated geometry
- Limit viewport subdivision levels
- Use proxy objects for heavy assets
- Decimate high-poly imports before rigging

### Materials & Textures
- Always use Principled BSDF for PBR
- Organize nodes with frames
- Use texture atlases when possible
- Bake complex materials for game engines
- Pack textures into .blend for portability

### Modeling Best Practices
- Maintain quad topology for smooth subdivision
- Check normals (`N` → Viewport Shading → Face Orientation)
- Remove doubles (`M` → Merge by Distance)
- Keep mesh manifold (watertight) for 3D printing
- Use non-destructive modifiers during design

### Rendering
- Render to image sequence, not video directly (safer)
- Use OpenEXR for professional VFX work
- Enable adaptive sampling in Cycles for faster converge
- Always preview in final viewport shading before rendering

## Blender 4.3+ Changes

### New Python API Features
- `ID.rename()` - Sophisticated renaming beyond property
- `bpy.app.handlers.blend_import_pre/post` - Import hooks
- `Curves.remove_curves()`, `resize_curves()` - Curve operations

### Breaking Changes
- Grease Pencil API completely rewritten
- `AttributeGroup` split into specialized types
- Embedded ID pointer assignment now raises error
- Legacy EEVEE shadow properties removed

## Quick Reference

| Task | Method |
|------|--------|
| Add cube | `bpy.ops.mesh.primitive_cube_add()` |
| Delete object | `bpy.data.objects.remove(obj, do_unlink=True)` |
| Duplicate | `bpy.ops.object.duplicate()` |
| Join objects | `bpy.ops.object.join()` |
| Apply transforms | `bpy.ops.object.transform_apply(scale=True, location=True, rotation=True)` |
| Smooth shading | `bpy.ops.object.shade_smooth()` |
| Add subdivision | `obj.modifiers.new(name="Subsurf", type='SUBSURF')` |
| Export glTF | `bpy.ops.export_scene.gltf(filepath="/path/file.glb")` |
| Export FBX | `bpy.ops.export_scene.fbx(filepath="/path/file.fbx")` |
| Render frame | `bpy.ops.render.render(write_still=True)` |
| Render animation | `bpy.ops.render.render(animation=True)` |

## Documentation Links

- [Official Blender Python API](https://docs.blender.org/api/current/)
- [Blender 4.5 Manual](https://docs.blender.org/manual/en/latest/)
- [Release Notes](https://developer.blender.org/docs/release_notes/)
- [Asset Browser Guide](https://docs.blender.org/manual/en/latest/editors/asset_browser.html)
- [Geometry Nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html)
