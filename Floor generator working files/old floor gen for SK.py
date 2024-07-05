bl_info = {
    "name": "SK floor generator",
    "description": "Copy objects with randomize transform then stick to the grid and selects overlapping parts",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Floor gen",
    "category": "3D View",
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

    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        for i in range(self.copies):
            bpy.ops.object.duplicate(linked=True)
        
        return {'FINISHED'}


class OBJECT_PT_copy_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_copy_panel"
    bl_label = "Object Copy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floor gen'
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        layout.operator("object.copy_objects", text="Create Linked Copies")
        
        row = layout.row()
        row.prop(obj, "copies", text="Number of Copies")
    
        layout.operator("object.randomize_transform", text="randomize transform")
        layout.operator("object.round_locations", text="round object locations")
        layout.operator("object.check_locations", text="check overlaps and select them")
        
def check_object_locations():
    selected_objects = bpy.context.selected_objects
    unique_locations = set()
    
    # Get the unique point of origin locations
    for obj in selected_objects:
        location = tuple(obj.location)
        if location not in unique_locations:
            unique_locations.add(location)
    
    # Select objects with shared point of origin location, except one
    for location in unique_locations:
        objects_at_location = [obj for obj in selected_objects if tuple(obj.location) == location]
        
        if len(objects_at_location) > 1:
            objects_to_deselect = objects_at_location[1:]
            for obj in objects_to_deselect:
                obj.select_set(False)
                
class OBJECT_OT_CheckLocations(bpy.types.Operator):
    bl_idname = "object.check_locations"
    bl_label = "Check Object Locations"
    bl_description = "Check and deselect objects with shared locations"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        check_object_locations()
        return {'FINISHED'}


def menu_func(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_CheckLocations.bl_idname)


def round_object_locations():
    selected_objects = bpy.context.selected_objects
    
    for obj in selected_objects:
        rounded_location = (
            round(obj.location.x),
            round(obj.location.y),
            round(obj.location.z)
        )
        
        obj.location = rounded_location


class OBJECT_OT_RoundLocations(bpy.types.Operator):
    bl_idname = "object.round_locations"
    bl_label = "Round Object Locations"
    bl_description = "Round the locations of selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        round_object_locations()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_RoundLocations.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_copy_objects)
    bpy.utils.register_class(OBJECT_PT_copy_panel)
    bpy.utils.register_class(OBJECT_OT_RoundLocations)
    bpy.utils.register_class(OBJECT_OT_CheckLocations)
    bpy.types.Object.copies = bpy.props.IntProperty(name="Number of Copies", default=1, min=1)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_copy_objects)
    bpy.utils.unregister_class(OBJECT_PT_copy_panel)
    bpy.utils.unregister_class(OBJECT_OT_RoundLocations)
    bpy.utils.unregister_class(OBJECT_OT_CheckLocations)
    del bpy.types.Object.copies

    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.types.VIEW3D_MT_select_object.remove(menu_func)

if __name__ == "__main__":
    register()