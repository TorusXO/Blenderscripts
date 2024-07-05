import bpy
from mathutils import Vector

def move_pivot_to_xy_center():
    # Get the active object
    obj = bpy.context.active_object

    # Select the object and make it the active one
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Switch to Object mode if not already in it
    bpy.ops.object.mode_set(mode="OBJECT")
    
    # Calculate the center of the mesh bounding box
    bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
    
    # Store the current location of the object's origin
    origin_location = obj.location.copy()
    
    # Move the origin to the XY center of the mesh
    obj.location -= Vector((bbox_center.x, bbox_center.y, 0))
    
    # Reset the Z-coordinate of the origin back to the original location
    obj.location.z = origin_location.z
    
    # Set the 3D cursor location to the origin
    bpy.context.scene.cursor.location = (0, 0, 0)
    
    # Set the pivot point to the 3D cursor location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

move_pivot_to_xy_center()
