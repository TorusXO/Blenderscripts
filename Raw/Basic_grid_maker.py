import bpy

# Set the cursor location
bpy.context.scene.cursor.location = bpy.context.scene.cursor.location

# Add a plane to the cursor location
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=bpy.context.scene.cursor.location)

# Merge the plane
bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.merge(type='CENTER')

# Switch back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Get the selected object
selected_obj = bpy.context.active_object

# Add an array modifier to the duplicated object in x axis
array_modifier = selected_obj.modifiers.new(name="ArrayX", type='ARRAY')
array_modifier.use_constant_offset = True
array_modifier.use_relative_offset = False
array_modifier.use_object_offset = False
array_modifier.count = 3    # Number of copies in the array


array_modifier = selected_obj.modifiers.new(name="ArrayY", type='ARRAY')
array_modifier.use_constant_offset = True
array_modifier.use_relative_offset = False
array_modifier.use_object_offset = False
array_modifier.count = 3    # Number of copies in the array
bpy.context.object.modifiers["ArrayY"].constant_offset_displace[1] = 1
bpy.context.object.modifiers["ArrayY"].constant_offset_displace[0] = 0

# Apply all modifiers
modifiers = selected_obj.modifiers[:]
for modifier in modifiers:
    bpy.context.view_layer.objects.active = selected_obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)