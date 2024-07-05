import bpy
import random
#to use the script you need a replace source collection with meshes in it, then select what needs to be replaced, then apply script
# the source must have rotations applied, otherwise it wont be saved.
replacers = bpy.data.collections["replace_source"].objects[:] #uses replace_source collection's meshes

for obj in bpy.context.selected_objects:
    obj.data = random.choice(replacers).data