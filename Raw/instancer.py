bl_info = {
    "name": "Object Copy",
    "blender": (2, 93, 0),
    "category": "Object",
}

import bpy

class OBJECT_OT_copy_objects(bpy.types.Operator):
    bl_idname = "object.copy_objects"
    bl_label = "Copy Objects"
    bl_options = {'REGISTER', 'UNDO'}

    copies: bpy.props.IntProperty(
        name="Number of Copies (N)",
        default=1,
        min=1,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for i in range(self.copies):
            bpy.ops.object.duplicate(linked=True)

        return {'FINISHED'}

def draw_menu(self, context):
    layout = self.layout
    layout.operator("object.copy_objects", text="Create Linked Copies")

classes = (
    OBJECT_OT_copy_objects,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(draw_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_object.remove(draw_menu)

if __name__ == "__main__":
    register()
