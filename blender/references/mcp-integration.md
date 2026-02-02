# Blender MCP Integration

Using MCP tools to control Blender remotely.

## Scene Inspection

```python
# Get scene overview
mcp__blender__get_scene_info()

# Get specific object details
mcp__blender__get_object_info(object_name="Cube")

# Take viewport screenshot
mcp__blender__get_viewport_screenshot(max_size=800)
```

## Executing Python Code

```python
# Always break into small chunks
mcp__blender__execute_blender_code(code="""
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
""")
```

## PolyHaven (HDRIs, textures, models)

```python
# Check status
mcp__blender__get_polyhaven_status()

# Search assets
mcp__blender__search_polyhaven_assets(
    asset_type="hdris",
    categories="outdoor"
)

# Download and apply
mcp__blender__download_polyhaven_asset(
    asset_id="autumn_field",
    asset_type="hdris",
    resolution="2k"
)

mcp__blender__set_texture(
    object_name="Ground",
    texture_id="brick_wall"
)
```

## Sketchfab (3D models)

```python
# Check status
mcp__blender__get_sketchfab_status()

# Search models
mcp__blender__search_sketchfab_models(
    query="chair",
    downloadable=True,
    count=10
)

# Download
mcp__blender__download_sketchfab_model(uid="abc123")
```

## Hyper3D Rodin (AI Generation from text)

```python
# Check status
mcp__blender__get_hyper3d_status()

# Generate from text
mcp__blender__generate_hyper3d_model_via_text(
    text_prompt="wooden chair"
)

# Poll until done
mcp__blender__poll_rodin_job_status(subscription_key="...")

# Import result
mcp__blender__import_generated_asset(
    name="Chair",
    task_uuid="..."
)
```

## Hunyuan3D (AI Generation)

```python
# Check status
mcp__blender__get_hunyuan3d_status()

# Generate model
mcp__blender__generate_hunyuan3d_model(
    text_prompt="red sports car"
)

# Poll status
mcp__blender__poll_hunyuan_job_status(job_id="job_xxx")

# Import
mcp__blender__import_generated_asset_hunyuan(
    name="Car",
    zip_file_url="..."
)
```
