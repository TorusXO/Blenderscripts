bl_info = {
    "name": "FBX Bunch Export",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "File &gt; Export &gt; FBX Bunch Export",
    "description": "Batch export .blend files as .fbx in the directory of opened file",
    "category": "Import-Export"
}

import bpy
import os


class FBXBunchExportOperator(bpy.types.Operator):
    bl_idname = "export.fbx_bunch"
    bl_label = "FBX Bunch Export"
    
    def execute(self, context):
        directory = bpy.path.abspath("//")  # Set the directory to the selected folder
        output_format = ".fbx"  # Desired output format

        # Get a list of all .blend files in the directory
        blend_files = [file for file in os.listdir(directory) if file.endswith(".blend")]

        # Iterate through each .blend file
        for blend_file in blend_files:
            # Construct the full file paths
            blend_file_path = os.path.join(directory, blend_file)
            output_file_path = os.path.splitext(blend_file_path)[0] + output_format

            # Open the .blend file
            bpy.ops.wm.open_mainfile(filepath=blend_file_path)

            # Export as .fbx with the name of the original file
            bpy.ops.export_scene.fbx(filepath=output_file_path)

            print(f"Exported {blend_file} as {output_file_path}")

        print("Export complete!")

        return {'FINISHED'}


def menu_func_export(self, context):
    self.layout.operator(FBXBunchExportOperator.bl_idname, text="FBX Bunch Export")


classes = (
    FBXBunchExportOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()