bl_info = {
    "name": "Mesh Cleanup",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Object > Mesh Cleanup",
    "description": "Cleans up mesh objects by joining them, removing doubles, and saving the file. Needed for batch preparing for the export to fbx to UE",
    "category": "Object"
}

import bpy
import os

def cleanup_mesh_objects():
    # Get the directory of the opened file
    directory = bpy.path.abspath('//')

    # Skip selection and joining if objects amount == 1
    if len(bpy.context.scene.objects) > 1:
        # Save and reset state of selection
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object
        for obj in selected_objects:
            obj.select_set(False)

        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH':
                ob.select_set(True)
                bpy.context.view_layer.objects.active = ob
            else:
                ob.select_set(False)
        bpy.ops.object.join()

        if bpy.context.selected_objects != []:
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    print(obj.name)
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.object.editmode_toggle()

    # Save the file with changes
    filename = bpy.path.basename(bpy.data.filepath)
    filepath = os.path.join(directory, filename)
    bpy.ops.wm.save_as_mainfile(filepath=filepath)

def menu_func(self, context):
    self.layout.operator("object.cleanup_mesh_objects", icon="PLUGIN")

def register():
    bpy.utils.register_class(CleanupMeshObjectsOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CleanupMeshObjectsOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

class CleanupMeshObjectsOperator(bpy.types.Operator):
    bl_idname = "object.cleanup_mesh_objects"
    bl_label = "Cleanup Mesh Objects"
    bl_description = "Cleans up mesh objects by joining them, removing doubles, and saving the file."

    def execute(self, context):
        cleanup_mesh_objects()
        return {'FINISHED'}

if __name__ == "__main__":
    register()