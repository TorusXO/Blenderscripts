bl_info = {
    "name": "Object Copy with Randomize Transform",
    "blender": (2, 93, 0),
    "category": "Object",
}

import bpy

class OBJECT_OT_copy_objects(bpy.types.Operator):
    bl_idname = "object.copy_objects"
    bl_label = "Copy Objects"
    bl_options = {'REGISTER', 'UNDO'}

    copies: bpy.props.IntProperty(
        name="Number of Copies",
        default=1,
        min=1,
    )

    randomize: bpy.props.BoolProperty(
        name="Randomize Transform",
        default=False,
    )
    
    loc_x: bpy.props.FloatProperty(
        name="Location X",
        default=0.0,
    )
    
    loc_y: bpy.props.FloatProperty(
        name="Location Y",
        default=0.0,
    )
    
    loc_z: bpy.props.FloatProperty(
        name="Location Z",
        default=0.0,
    )
    
    random_seed: bpy.props.IntProperty(
        name="Random Seed",
        default=0,
        min=0,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for i in range(self.copies):
            bpy.ops.object.duplicate(linked=True)
        
        if self.randomize:
            bpy.ops.object.randomize_transform(random_seed=self.random_seed, loc=(self.loc_x, self.loc_y, self.loc_z))
        
        return {'FINISHED'}

class OBJECT_PT_copy_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_copy_panel"
    bl_label = "Object Copy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'N'

    def draw(self, context):
        layout = self.layout
        
        obj = context.object

        layout.operator("object.copy_objects", text="Create Linked Copies")

        row = layout.row()
        row.prop(obj, "copies", text="Number of Copies")
        
        split = layout.split(factor=0.5)
        col = split.column()
        col.prop(obj, "randomize", text="Randomize Transform")
        
        row = col.row(align=True)
        row.prop(obj, "loc_x", text="Loc X")
        row.prop(obj, "loc_y", text="Loc Y")
        row.prop(obj, "loc_z", text="Loc Z")
        
        col.prop(obj, "random_seed", text="Random Seed")

def register():
    bpy.utils.register_class(OBJECT_OT_copy_objects)
    bpy.utils.register_class(OBJECT_PT_copy_panel)
    bpy.types.Object.copies = bpy.props.IntProperty(name="Number of Copies", default=1, min=1)
    bpy.types.Object.randomize = bpy.props.BoolProperty(name="Randomize Transform", default=False)
    bpy.types.Object.loc_x = bpy.props.FloatProperty(name="Location X", default=0.0)
    bpy.types.Object.loc_y = bpy.props.FloatProperty(name="Location Y", default=0.0)
    bpy.types.Object.loc_z = bpy.props.FloatProperty(name="Location Z", default=0.0)
    bpy.types.Object.random_seed = bpy.props.IntProperty(name="Random Seed", default=0, min=0)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_copy_objects)
    bpy.utils.unregister_class(OBJECT_PT_copy_panel)
    del bpy.types.Object.copies
    del bpy.types.Object.randomize
    del bpy.types.Object.loc_x
    del bpy.types.Object.loc_y
    del bpy.types.Object.loc_z
    del bpy.types.Object.random_seed

if __name__ == "__main__":
    register()