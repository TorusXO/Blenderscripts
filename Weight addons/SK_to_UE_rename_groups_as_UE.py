bl_info = {
    "name": "Replace SK Vertex Group Names with UEs",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class ReplaceVertexGroupName(bpy.types.Operator):
    bl_idname = "object.replace_vertex_group_name"
    bl_label = "Replace SK Vertex Group Names"
    bl_description = "Replace SK vertex group names with UEs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        old_names = ["Bip01 R Calf", "Bip01 L Calf", "Bip01 R UpperArm", "Bip01 L UpperArm", "Bip01 Head", "Bip01 Pelvis", "Bip01 Spine1", "Bip01 R Hand", "Bip01 L Hand", "Bip01 L Clavicle", "Bip01 R Clavicle", "Bip01 L Thigh", "Bip01 R Thigh", "Bip01 R Forearm", "Bip01 L Forearm", "Bip01 Spine", "Bip01 L Foot", "Bip01 Foot", "Left ankle", "Right ankle", "Left knee", "Right knee", "Left leg", "Right leg", "Neck" , "Left elbow", "Right elbow", "Left arm", "Right arm", "Left shoulder", "Right shoulder", "Right wrist", "Left wrist", "Chest", "Spine", "Hips"]
        new_names = ["calf_r", "calf_l", "upperarm_r", "upperarm_l", "neck_01", "spine_03", "spine_05", "hand_r", "hand_l", "clavicle_l", "clavicle_r", "thigh_l", "thigh_r", "lowerarm_r", "lowerarm_l", "spine_04", "ball_l", "ball_r", "calf_l", "calf_r", "calf_l", "calf_r", "thigh_l", "thigh_r", "neck_01", "lowerarm_l", "lowerarm_r", "upperarm_l", "upperarm_r", "clavicle_l", "clavicle_r", "hand_r", "hand_l", "spine_05", "spine_03", "spine_01"]

        obj = context.active_object

        if obj is not None and obj.type == 'MESH':
            for vg in obj.vertex_groups:
                for old_name, new_name in zip(old_names, new_names):
                    if vg.name == old_name:
                        vg.name = new_name
                        self.report({'INFO'}, f"Vertex group name '{old_name}' replaced with '{new_name}'.")
                        break
            else:
                self.report({'INFO'}, "No vertex group names found to replace.")
        else:
            self.report({'INFO'}, "No active mesh object found.")

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ReplaceVertexGroupName.bl_idname)


def register():
    bpy.utils.register_class(ReplaceVertexGroupName)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ReplaceVertexGroupName)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()