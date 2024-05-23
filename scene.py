import bpy

# def create_scene_from_user_data():
#     # Check if the user data exists in the scene
#     if 'music_preferences' not in bpy.context.scene or \
#        'custom_characters' not in bpy.context.scene or \
#        'movie_templates' not in bpy.context.scene:
#         print("User data not found. Please run the operators to collect data first.")
#         return
    
#     # Clear existing scene data
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.ops.object.select_by_type(type='MESH')
#     bpy.ops.object.delete()

#     # Create objects based on user data
#     music_preferences = bpy.context.scene['music_preferences'].split(',')
#     custom_characters = bpy.context.scene['custom_characters'].split(',')
#     movie_templates = bpy.context.scene['movie_templates'].split(',')

#     # Create music objects
#     for genre in music_preferences:
#         bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
#         cube = bpy.context.active_object
#         cube.name = f"Music_{genre.strip()}"

#     # Create character objects
#     for character in custom_characters:
#         bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
#         sphere = bpy.context.active_object
#         sphere.name = f"Character_{character.strip()}"

#     # Create movie template objects
#     for template in movie_templates:
#         bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 0))
#         cylinder = bpy.context.active_object
#         cylinder.name = f"Template_{template.strip()}"

#     print("Scene created successfully.")

# create_scene_from_user_data()import bpy

# Set the path to your Blender file

blend_file_path = r"C:\Users\MURTAZAY\Downloads\rain_v2.4 (1)\rain_rig.blend"

# Load the blend file
with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
    # List all the objects in the Blender file
    print("Objects in the Blender file:")
    for obj_name in data_from.objects:
        print(obj_name)

