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

# Call the function to remove the vertex groups
remove_vertex_groups()
