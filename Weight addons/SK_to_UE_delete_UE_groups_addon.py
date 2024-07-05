bl_info = {
    "name": "SK to UE delete UE groups",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Search > Delete UE Vertex Groups",
    "description": "Removes UE vertex groups from the selected mesh.",
    "category": "Mesh",
}

import bpy


def remove_vertex_groups():
    vertex_group_names = ["calf_r", "calf_l", "upperarm_r", "upperarm_l", "neck_01", "spine_03", "spine_05", "lowerarm_r", "lowerarm_l", "clavicle_l", "clavicle_r", "thigh_l", "thigh_r", "upperarm_twist_02_r", "upperarm_twist_02_l", "spine_04", "ball_l", "ball_r"]

    obj = bpy.context.active_object

    if obj is not None and obj.type == 'MESH':
        vertex_groups = obj.vertex_groups
        removed_count = 0

        for vertex_group_name in vertex_group_names:
            vertex_group = vertex_groups.get(vertex_group_name)
            if vertex_group is not None:
                vertex_groups.remove(vertex_group)
                removed_count += 1

        print(f"Removed {removed_count} vertex group(s).")
    else:
        print("No active mesh object found.")


class OBJECT_OT_remove_vertex_groups(bpy.types.Operator):
    bl_idname = "object.remove_ue_vertex_groups"
    bl_label = "Delete UE Vertex Groups"
    bl_description = "Removes UE vertex groups from the selected mesh."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        remove_vertex_groups()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_remove_vertex_groups.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_remove_vertex_groups)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_remove_vertex_groups)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
