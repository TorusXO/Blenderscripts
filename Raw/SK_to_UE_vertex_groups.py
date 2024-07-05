import bpy

def replace_vertex_group_name():
    old_names = ["Bip01 R Calf", "Bip01 L Calf", "Bip01 R UpperArm", "Bip01 L UpperArm", "Bip01 Head", "Bip01 Pelvis", "Bip01 Spine1", "Bip01 R Hand", "Bip01 L Hand", "Bip01 L Clavicle", "Bip01 R Clavicle", "Bip01 L Thigh", "Bip01 R Thigh", "Bip01 R Forearm", "Bip01 L Forearm", "Bip01 Spine", "Bip01 L Foot", "Bip01  Foot"]
    new_names = ["calf_r", "calf_l", "upperarm_r", "upperarm_l", "neck_01", "spine_03", "spine_05", "lowerarm_r", "lowerarm_l", "clavicle_l", "clavicle_r", "thigh_l", "thigh_r", "upperarm_twist_02_r", "upperarm_twist_02_l", "spine_04", "ball_l", "ball_r"]

    obj = bpy.context.active_object

    if obj is not None and obj.type == 'MESH':
        for vg in obj.vertex_groups:
            for old_name, new_name in zip(old_names, new_names):
                if vg.name == old_name:
                    vg.name = new_name
                    print(f"Vertex group name '{old_name}' replaced with '{new_name}'.")
                    break
        else:
            print(f"No vertex group names found to replace.")
    else:
        print("No active mesh object found.")

replace_vertex_group_name()
#then apply skeleton as Armature Deform. 