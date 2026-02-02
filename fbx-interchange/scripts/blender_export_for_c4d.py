"""
Blender FBX Export Script for Cinema 4D Compatibility

Run in Blender: Text Editor → Open → Run Script
Or via command line: blender -b file.blend -P blender_export_for_c4d.py

Exports selected objects (or all if none selected) with optimal
settings for Cinema 4D import.
"""

import bpy
import os


def export_fbx_for_c4d(
    filepath: str,
    selected_only: bool = False,
    include_animation: bool = True,
    apply_modifiers: bool = True,
):
    """
    Export FBX with Cinema 4D compatible settings.

    Args:
        filepath: Output .fbx file path
        selected_only: Export only selected objects
        include_animation: Include animation data
        apply_modifiers: Apply modifiers before export
    """
    # Ensure .fbx extension
    if not filepath.lower().endswith('.fbx'):
        filepath += '.fbx'

    # Apply transforms to selected objects
    if selected_only:
        objs = bpy.context.selected_objects
    else:
        objs = bpy.context.scene.objects

    # Store selection
    original_selection = bpy.context.selected_objects[:]
    original_active = bpy.context.view_layer.objects.active

    # Apply transforms
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        if obj.type in {'MESH', 'ARMATURE'}:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

    if bpy.context.selected_objects:
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # Restore selection
    bpy.ops.object.select_all(action='DESELECT')
    for obj in original_selection:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = original_active

    # Export with C4D-compatible settings
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=selected_only,
        use_visible=False,
        use_active_collection=False,
        # Scale - keep 1:1 for predictable results
        global_scale=1.0,
        apply_unit_scale=False,  # Critical for C4D compatibility
        apply_scale_options='FBX_SCALE_ALL',
        # Axis conversion for C4D
        axis_forward='-Z',
        axis_up='Y',
        # Object types
        object_types={'ARMATURE', 'MESH', 'EMPTY'},
        # Mesh settings
        use_mesh_modifiers=apply_modifiers,
        use_mesh_modifiers_render=apply_modifiers,
        mesh_smooth_type='FACE',
        use_subsurf=False,
        use_mesh_edges=False,
        use_tspace=True,  # Tangent space for normal maps
        use_triangles=False,  # Keep quads
        use_custom_props=False,
        # Armature settings
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        use_armature_deform_only=False,
        armature_nodetype='NULL',
        # Animation
        bake_anim=include_animation,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=False,
        bake_anim_force_startend_keying=True,
        bake_anim_step=1.0,
        bake_anim_simplify_factor=1.0,
        # Paths
        path_mode='AUTO',
        embed_textures=False,
        batch_mode='OFF',
    )

    print(f"Exported to: {filepath}")
    return filepath


def main():
    """Main entry point when running as script."""
    import sys

    # Default output path
    blend_path = bpy.data.filepath
    if blend_path:
        output_path = os.path.splitext(blend_path)[0] + '_c4d.fbx'
    else:
        output_path = '//export_c4d.fbx'

    # Check for command line args after '--'
    if '--' in sys.argv:
        args = sys.argv[sys.argv.index('--') + 1:]
        if args:
            output_path = args[0]

    # Export
    selected = len(bpy.context.selected_objects) > 0
    export_fbx_for_c4d(
        filepath=bpy.path.abspath(output_path),
        selected_only=selected,
        include_animation=True,
        apply_modifiers=True,
    )


if __name__ == '__main__':
    main()
