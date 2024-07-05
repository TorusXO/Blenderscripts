bl_info = {
    "name": "Texture Name Checker",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Object > Texture Name Checker",
    "description": "Checks and modifies texture names",
    "category": "Object"
}

import bpy


class TextureNameCheckerOperator(bpy.types.Operator):
    bl_idname = "object.texture_name_checker"
    bl_label = "Texture Name Checker"
    bl_description = "Check and modify texture names"

    def execute(self, context):
        # Get all objects in the scene
        objects = bpy.context.scene.objects

        # Iterate through each object
        for obj in objects:
            # Check if the object is a mesh
            if obj.type == 'MESH':
                # Set the object as active
                bpy.context.view_layer.objects.active = obj

                # Get all materials assigned to the object
                materials = obj.data.materials

                # Iterate through each material
                for material_slot_index, material_slot in enumerate(materials):
                    # Check if the material has nodes
                    if material_slot.node_tree:
                        # Get the material's node tree
                        node_tree = material_slot.node_tree

                        # Iterate through each node in the node tree
                        for node in node_tree.nodes:
                            # Check if the node is a texture node
                            if isinstance(node, bpy.types.ShaderNodeTexImage):
                                # Get the active texture from the texture node
                                texture = node.image

                                # Get the texture name
                                texture_name = texture.name

                                # Check if the texture name ends with .001 or .002
                                if texture_name.endswith('.001') or texture_name.endswith('.002'):
                                    # Remove the last 4 characters from the texture name
                                    new_texture_name = texture_name[:-4]

                                    # Update the texture name
                                    texture.name = new_texture_name

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(TextureNameCheckerOperator.bl_idname)


def register():
    bpy.utils.register_class(TextureNameCheckerOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(TextureNameCheckerOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
