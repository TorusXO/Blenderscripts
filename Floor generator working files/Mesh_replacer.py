bl_info = {
    "name": "Mesh Replacer",
    "author": "Torusxo",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "N Panel > Floor gen > Mesh Replacer",
    "description": "Replace selected objects with random objects from a target collection",
    "category": "Object",
}
# you need to put all the needed meshes in the collection and then select this collection
# then select the objects you want to replace
# note that rotation isnt copied from the source object
import bpy
import random
from bpy.types import Operator, Panel
from bpy.props import EnumProperty


# Operator class to perform the replacement operation
class MeshReplacerOperator(Operator):
    bl_idname = "object.mesh_replacer"
    bl_label = "Replace Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        target_collection = bpy.context.scene.target_collection
        if target_collection is None:
            self.report({'ERROR_INVALID_INPUT'}, "No target collection selected.")
            return {'CANCELLED'}

        replacers = bpy.data.collections[target_collection].objects[:]  # Get objects from the target collection

        for obj in bpy.context.selected_objects:
            replacer_object = random.choice(replacers)
            obj.data = replacer_object.data
            obj.name = replacer_object.name # Change the name of the resulting mesh to match the source mesh

        return {'FINISHED'}


# Panel class to display the UI in the N panel
class MeshReplacerPanel(Panel):
    bl_idname = "VIEW3D_PT_mesh_replacer"
    bl_label = "Mesh Replacer"
    bl_category = "Floor gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Select target collection:")

        layout.prop(scene, "target_collection", text="")

        layout.operator("object.mesh_replacer", text="Replace Meshes")


# Registration
classes = (
    MeshReplacerOperator,
    MeshReplacerPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Populate the target_collection EnumProperty with existing collections
    bpy.types.Scene.target_collection = EnumProperty(
        items=get_collection_items,
        name="Target Collection",
        description="Select target collection",
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.target_collection


# Helper function to populate target_collection EnumProperty with existing collections
def get_collection_items(self, context):
    items = []

    collections = bpy.data.collections
    for collection in collections:
        items.append((collection.name, collection.name, ""))

    return items


if __name__ == "__main__":
    register()
