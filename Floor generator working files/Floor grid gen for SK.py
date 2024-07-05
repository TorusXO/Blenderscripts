import bpy


bl_info = {
    "name": "Floor grid Generation",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N menu",
    "description": "Generates a grid of vertexes on the cursor location",
    "category": "Add Mesh"
}


def add_floor_object(context):
    # Add a plane to the cursor location
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=bpy.context.scene.cursor.location)

    # Merge the plane
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.merge(type='CENTER')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Get the selected object
    selected_obj = bpy.context.active_object
    
    # Add an array modifier to the duplicated object in x axis
    array_modifier = selected_obj.modifiers.new(name="ArrayX", type='ARRAY')
    array_modifier.use_constant_offset = True
    array_modifier.use_relative_offset = False
    array_modifier.use_object_offset = False
    array_modifier.count = context.scene.floor_grid_gen_x   # Number of copies in the array

    array_modifier = selected_obj.modifiers.new(name="ArrayY", type='ARRAY')
    array_modifier.use_constant_offset = True
    array_modifier.use_relative_offset = False
    array_modifier.use_object_offset = False
    array_modifier.count = context.scene.floor_grid_gen_y   # Number of copies in the array
    bpy.context.object.modifiers["ArrayY"].constant_offset_displace[1] = 1
    bpy.context.object.modifiers["ArrayY"].constant_offset_displace[0] = 0
    
    # Apply all modifiers
    modifiers = selected_obj.modifiers[:]
    for modifier in modifiers:
        bpy.context.view_layer.objects.active = selected_obj
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    # Select the generated floor objects
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
        obj.select_set(True)

    # Separate by loose parts
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')


class VIEW3D_PT_floor_grid_gen(bpy.types.Panel):
    bl_label = "Floor Generation"
    bl_idname = "VIEW3D_PT_floor_grid_gen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Floor gen"

    # UI layout
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # ArrayX
        layout.prop(scene, "floor_grid_gen_x", text="ArrayX")

        # ArrayY
        layout.prop(scene, "floor_grid_gen_y", text="ArrayY")

        # Generate floor button
        layout.operator("object.floor_grid_gen", text="Generate Floor")


def register():
    bpy.types.Scene.floor_grid_gen_x = bpy.props.IntProperty(
        name="ArrayX",
        default=3,
        min=1,
        description="Number of copies in X-axis"
    )
    bpy.types.Scene.floor_grid_gen_y = bpy.props.IntProperty(
        name="ArrayY",
        default=3,
        min=1,
        description="Number of copies in Y-axis"
    )
    
    bpy.utils.register_class(VIEW3D_PT_floor_grid_gen)
    bpy.utils.register_class(OBJECT_OT_floor_grid_gen)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_floor_grid_gen)
    bpy.utils.unregister_class(OBJECT_OT_floor_grid_gen)


class OBJECT_OT_floor_grid_gen(bpy.types.Operator):
    bl_idname = "object.floor_grid_gen"
    bl_label = "Generate Floor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        add_floor_object(context)
        return {'FINISHED'}


if __name__ == "__main__":
    register()
