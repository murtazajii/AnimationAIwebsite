# import bpy

# # Filepath to the custom template file
# # custom_template_filepath = "/path/to/custom_template.blend"

# # # Load the custom template file
# # bpy.ops.wm.open_mainfile(filepath=custom_template_filepath)
# # Load the default startup file

# # Load the default startup file


# # Load the default startup file
# bpy.ops.wm.open_mainfile(filepath=bpy.app.tempdir + "startup.blend")




# # Now you can perform any additional operations you want with the loaded file
import bpy
bpy.ops.mesh.primitive_cube_add(size=4)
cube_obj=bpy.context.active_object
cube_obj.location.x=10

