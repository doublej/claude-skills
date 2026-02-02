"""
Cinema 4D FBX Export Script for Blender Compatibility

Run in Cinema 4D: Script → User Scripts → Run Script
Or via Script Manager

Exports scene or selection with optimal settings for Blender import.
"""

import c4d
from c4d import documents, gui
import os


# FBX exporter plugin ID
FBX_EXPORTER_ID = 1026370


def configure_fbx_settings(fbx_export):
    """Configure FBX export settings for Blender compatibility."""
    # FBX version - 7.4 binary is most compatible
    fbx_export[c4d.FBXEXPORT_FBX_VERSION] = c4d.FBX_EXPORTVERSION_NATIVE

    # Format
    fbx_export[c4d.FBXEXPORT_ASCII] = False  # Binary is smaller/faster

    # Geometry
    fbx_export[c4d.FBXEXPORT_TRIANGULATE] = False  # Keep quads
    fbx_export[c4d.FBXEXPORT_SAVE_NORMALS] = True
    fbx_export[c4d.FBXEXPORT_SAVE_VERTEX_COLORS] = True
    fbx_export[c4d.FBXEXPORT_SAVE_UV] = True

    # Objects
    fbx_export[c4d.FBXEXPORT_CAMERAS] = False
    fbx_export[c4d.FBXEXPORT_LIGHTS] = False
    fbx_export[c4d.FBXEXPORT_SPLINES] = False

    # Animation
    fbx_export[c4d.FBXEXPORT_ANIMATIONS] = True
    fbx_export[c4d.FBXEXPORT_BAKEFRAMES] = True
    fbx_export[c4d.FBXEXPORT_PLA_TO_VERTEXCACHE] = False

    # Materials & Textures
    fbx_export[c4d.FBXEXPORT_MATERIALS] = True
    fbx_export[c4d.FBXEXPORT_TEXTURES] = True
    fbx_export[c4d.FBXEXPORT_EMBED_TEXTURES] = False

    return fbx_export


def export_fbx_for_blender(filepath, selected_only=False):
    """
    Export FBX with Blender-compatible settings.

    Args:
        filepath: Output .fbx file path
        selected_only: Export only selected objects

    Returns:
        True if export succeeded, False otherwise
    """
    doc = documents.GetActiveDocument()
    if not doc:
        gui.MessageDialog("No active document")
        return False

    # Ensure .fbx extension
    if not filepath.lower().endswith('.fbx'):
        filepath += '.fbx'

    # Get FBX exporter plugin
    plug = c4d.plugins.FindPlugin(FBX_EXPORTER_ID, c4d.PLUGINTYPE_SCENESAVER)
    if not plug:
        gui.MessageDialog("FBX exporter not found")
        return False

    # Get export settings container
    op = {}
    if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        gui.MessageDialog("Could not retrieve FBX settings")
        return False

    fbx_export = op.get("imexporter")
    if not fbx_export:
        gui.MessageDialog("Could not get FBX imexporter")
        return False

    # Configure settings
    configure_fbx_settings(fbx_export)

    # Handle selection-only export
    export_doc = doc
    if selected_only:
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not selection:
            gui.MessageDialog("No objects selected")
            return False

        # Create temp document with selection
        export_doc = documents.BaseDocument()
        for obj in selection:
            clone = obj.GetClone()
            export_doc.InsertObject(clone)

    # Export
    result = documents.SaveDocument(
        export_doc,
        filepath,
        c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,
        FBX_EXPORTER_ID
    )

    # Clean up temp doc
    if selected_only:
        documents.KillDocument(export_doc)

    if result:
        print(f"Exported to: {filepath}")
    else:
        gui.MessageDialog(f"Export failed: {filepath}")

    return result


def main():
    """Main entry point."""
    doc = documents.GetActiveDocument()
    if not doc:
        return

    # Default output path
    doc_path = doc.GetDocumentPath()
    doc_name = doc.GetDocumentName()

    if doc_path and doc_name:
        base_name = os.path.splitext(doc_name)[0]
        default_path = os.path.join(doc_path, f"{base_name}_blender.fbx")
    else:
        default_path = ""

    # Show save dialog
    filepath = c4d.storage.SaveDialog(
        title="Export FBX for Blender",
        def_path=default_path,
        def_file="",
        type="fbx"
    )

    if not filepath:
        return

    # Check if there's a selection
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    selected_only = False

    if selection:
        result = gui.QuestionDialog("Export selected objects only?")
        selected_only = result

    # Export
    export_fbx_for_blender(filepath, selected_only)


if __name__ == '__main__':
    main()
