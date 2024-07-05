import bpy
bl_info = {
    "name": "Vertex Group doubles batch combine",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Data > Vertex Groups",
    "description": "using vertex mix modifier ->add all for every vertex groups doubles with .001 suffix",
}

# Get the active object
obj = bpy.context.active_object

# Create a list to store the vertex groups with .001 suffix
groups_with_suffix = []

# Create a list to store the modifiers created by the script
modifiers_created = []

# Find and delete the first VERTEX_WEIGHT_MIX modifier
for modifier in obj.modifiers:
    if modifier.type == 'VERTEX_WEIGHT_MIX':
        # Remove the first VERTEX_WEIGHT_MIX modifier found
        obj.modifiers.remove(modifier)
        break  # Exit the loop after removing the first modifier

# Iterate over all vertex groups in the object
for group in obj.vertex_groups:
    # Check if the vertex group name ends with .001
    if group.name.endswith('.001'):
        # Remove the suffix from the name
        original_name = group.name[:-4]
        
        # Add the original name to the vertexWeightMix modifier
        modifier = obj.modifiers.new(name="Vertex Weight Mix", type='VERTEX_WEIGHT_MIX')
        modifier.mix_mode = 'ADD'
        modifier.vertex_group_a = original_name
        modifier.vertex_group_b = group.name
        modifier.mix_set = 'ALL'  # Set Vertex Set to ALL
        modifier.normalize = True #fix if bugs
        # Store the vertex group with .001 suffix in the list
        groups_with_suffix.append(group)
        modifiers_created.append(modifier)

# Apply all the vertex weight mix modifiers that are enabled for viewport display
visible_objects = [obj for obj in bpy.context.view_layer.objects if obj.visible_get() and obj.select_get()]
for obj in visible_objects:
    if obj.type == "MESH":
        for modifier in obj.modifiers:
            if modifier.type == "VERTEX_WEIGHT_MIX" and modifier.show_viewport:
                # Apply the Vertex Weight Mix modifier if it is enabled for viewport display
                try:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
                except RuntimeError as e:
                    if "modifier is disabled, skipping apply" not in str(e):
                        raise e


#print("Vertex Weight Mix modifiers applied!")

# Delete the vertex groups with .001 suffix
for group in groups_with_suffix:
    if group.name in obj.vertex_groups:
        vertex_group = obj.vertex_groups[group.name]
        obj.vertex_groups.remove(vertex_group)

print("Script executed successfully!")
