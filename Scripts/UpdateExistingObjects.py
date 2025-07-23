import bpy

if bpy.context.active_object is None:
    print("No active object selected.")
else:
    selected_obj = bpy.context.active_object
    selected_name = selected_obj.name
    
    target_objects = [obj for obj in bpy.data.objects if selected_name in obj.name and obj != selected_obj]

    for target in target_objects:
        new_obj = selected_obj.copy()
        new_obj.data = selected_obj.data.copy()  
        
        new_obj.location = target.location
        new_obj.rotation_euler = target.rotation_euler
        new_obj.scale = target.scale
        
        for key in target.keys():
            if key not in "_RNA_UI":
                new_obj[key] = target[key]
        
        for col in target.users_collection:
            col.objects.link(new_obj)
        
        bpy.data.objects.remove(target, do_unlink=True)

    print(f"Replaced {len(target_objects)} object(s) with '{selected_name}'.")
