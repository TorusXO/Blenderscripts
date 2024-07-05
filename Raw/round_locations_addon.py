bl_info = {
    "name": "Round Object Locations",
    "description": "Round the locations of selected objects to the nearest integers",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "category": "Object",
}
import bpy

class OBJECT_OT_RoundLocations(bpy.types.Operator):
    bl_idname = "object.round_locations"
    bl_label = "Round Object Locations"
    bl_description = "Round the locations of selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        
        for obj in selected_objects:
            rounded_location = (
                round(obj.location.x),
                round(obj.location.y),
                round(obj.location.z)
            )
    
            obj.location = rounded_location
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_RoundLocations.bl_idname)

# Register the add-on
def register():
    bpy.utils.register_class(OBJECT_OT_RoundLocations)
    bpy.types.VIEW3D_MT_object.append(menu_func)

# Unregister the add-on
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RoundLocations)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

# Run the add-on in Blender's script editor
if __name__ == "__main__":
    register()
