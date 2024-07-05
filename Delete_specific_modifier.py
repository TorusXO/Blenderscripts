import bpy
from bpy.types import Operator, Menu

# bunch delete selected modifier from all selected objects

# Operator to delete selected modifiers
class DeleteSpecificModifier(Operator):
    bl_idname = "object.delete_specific_modifier"
    bl_label = "Delete Specific Modifier"
    bl_description = "Delete the selected modifier from all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    modifier_name: bpy.props.StringProperty(name="Modifier Name")

    def execute(self, context):
        for obj in context.selected_objects:
            if self.modifier_name in obj.modifiers:
                obj.modifiers.remove(obj.modifiers[self.modifier_name])
        return {'FINISHED'}

# Menu for the "Modifiers" panel
class OBJECT_PT_ModifiersMenu(Menu):
    bl_label = "Modifiers Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.delete_specific_modifier", text="Delete Weighted Normal").modifier_name = "Weighted Normal"
        layout.operator("object.delete_specific_modifier", text="Delete Auto Smooth").modifier_name = "Auto Smooth"

# Register the classes
def register():
    bpy.utils.register_class(DeleteSpecificModifier)
    bpy.utils.register_class(OBJECT_PT_ModifiersMenu)

    bpy.types.DATA_PT_modifiers.prepend(menu_func)

def unregister():
    bpy.utils.unregister_class(DeleteSpecificModifier)
    bpy.utils.unregister_class(OBJECT_PT_ModifiersMenu)

    bpy.types.DATA_PT_modifiers.remove(menu_func)

# Menu function
def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(OBJECT_PT_ModifiersMenu.bl_idname)

if __name__ == "__main__":
    register()


#working script for certain modifiers
import bpy

# List of modifier names to remove
modifiers_to_remove = ["Weighted Normal", "Auto Smooth"]

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Iterate through each object
for obj in selected_objects:
    # Check if the object has modifiers
    if obj.modifiers:
        # Iterate through the modifiers
        for modifier in obj.modifiers:
            # Check if the modifier name is in the list to remove
            if modifier.name in modifiers_to_remove:
                # Remove the modifier
                obj.modifiers.remove(modifier)
