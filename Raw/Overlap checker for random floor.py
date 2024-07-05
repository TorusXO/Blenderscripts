import bpy

def check_object_locations():
    selected_objects = bpy.context.selected_objects
    unique_locations = set()

    # Get the unique point of origin locations
    for obj in selected_objects:
        location = tuple(obj.location)
        if location not in unique_locations:
            unique_locations.add(location)

    # Select objects with shared point of origin location, except one
    for location in unique_locations:
        objects_at_location = [obj for obj in selected_objects if tuple(obj.location) == location]
        if len(objects_at_location) > 1:
            objects_to_deselect = objects_at_location[1:]
            for obj in objects_to_deselect:
                obj.select_set(False)


# Run the checker function
check_object_locations()
