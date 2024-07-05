bl_info = {
    "name": "SK to UE delete SK groups",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Search > Delete SK Vertex Groups",
    "description": "Deletes Empty sk/airbees groups from the selected mesh.",
    "category": "Mesh",
}

import bpy


def remove_vertex_groups():
    vertex_group_names = ["Bip01 R Hand Adjust", "bone_weapon_r", "Bip01 L Hand Adjust", "bone_weapon_l", "bone_shield", "Bip01 Neck", "Bip01 Head Adjust", "bone_helmet", "bone_shield_away", "pivot_liftobject", "bone_liftobject", "Root", "Right arm", "Right elbow", "Right wrist", "Thumb1_R", "Thumb2_R", "Thumb3_R", "Thumb3_R_end", "wing_r_talon32", "wing_r_talon31", "wing_r_talon23", "wing_r_talon22", "wing_r_talon21", "wing_r_talon1", "wing_l_talon32", "wing_l_talon31", "wing_l_talon23", "wing_l_talon22", "wing_l_talon21", "wing_l_talon1", "mesh_dragonwings", "wing_r_forearm", "wing_r_bicep", "wing_l_forearm", "wing_l_bicep", "root_wings", "MiddleFinger3_L.002", "MiddleFinger2_L.002", "RingFinger1_L.002", "MiddleFinger3_L.001", "MiddleFinger2_L.001", "IndexFinger1_L.001", "Thumb0_L", "MiddleFinger3_L.005", "MiddleFinger2_L.005", "RingFinger1_L.003", "MiddleFinger3_R.001", "MiddleFinger3_R.001", "MiddleFinger2_R.002", "Thumb0_R", "Left ankle", "Left knee", "Left leg", "Right ankle", "Right knee", "Right leg", "Head", "Left elbow", "Right elbow", "Neck", "LittleFinger3_L_end", "LittleFinger3_L", "LittleFinger2_L", "LittleFinger1_L", "RingFinger3_L_end", "RingFinger3_L", "RingFinger2_L", "RingFinger1_L", "IndexFinger3_L_end", "IndexFinger3_L", "IndexFinger2_L", "IndexFinger1_L", "MiddleFinger3_L_end", "MiddleFinger3_L", "MiddleFinger2_L", "MiddleFinger1_L", "Thumb3_L_end", "Thumb3_L", "Thumb2_L", "Thumb1_L", "LittleFinger3_R_end", "LittleFinger3_R", "LittleFinger2_R", "LittleFinger1_R", "RingFinger3_R_end", "RingFinger3_R" "RingFinger2_R", "RingFinger1_R", "IndexFinger3_R_end", "IndexFinger3_R", "IndexFinger2_R", "IndexFinger1_R", "MiddleFinger3_R_end", "MiddleFinger3_R", "MiddleFinger2_R", "MiddleFinger1_R", "neutral_bone"]
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
    #else:
        #print("No active mesh object found.")


class OBJECT_OT_remove_vertex_groups(bpy.types.Operator):
    bl_idname = "object.remove_sk_vertex_groups"
    bl_label = "Delete SK unused Vertex Groups"
    bl_description = "Removes SK unused vertex groups from the selected mesh."
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
