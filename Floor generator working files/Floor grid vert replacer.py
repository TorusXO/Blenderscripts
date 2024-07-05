bl_info = {
    "name": "Floor Generator",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D",
    "description": "Generates a floor grid by merging selected vertices",
    "category": "Mesh"
}

import bpy

class VIEW3D_PT_floor_gen(bpy.types.Panel):
    bl_label = "Vert replace selected"
    bl_idname = "VIEW3D_PT_floor_gen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floor gen'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Display a button to run the vertex merging operation
        layout.operator("object.vert_grid_replace", text="Replace meshes")

def register():
    bpy.utils.register_class(VIEW3D_PT_floor_gen)
    bpy.utils.register_class(VertGridReplaceOperator)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_floor_gen)
    bpy.utils.unregister_class(VertGridReplaceOperator)

class VertGridReplaceOperator(bpy.types.Operator):
    bl_label = "Merge Vertices"
    bl_idname = "object.vert_grid_replace"

    def execute(self, context):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects

        # Iterate over each selected object
        for obj in selected_objects:
            # Check if the object is a mesh
            if obj.type == 'MESH':
                # Select the object
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.merge(type='CENTER')
                bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(VertGridReplaceOperator.bl_idname)

def register():
    bpy.utils.register_class(VIEW3D_PT_floor_gen)
    bpy.utils.register_class(VertGridReplaceOperator)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_floor_gen)
    bpy.utils.unregister_class(VertGridReplaceOperator)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)

if __name__ == "__main__":
    register()