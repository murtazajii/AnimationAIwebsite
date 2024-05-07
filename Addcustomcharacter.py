import bpy
import math

# Add a monkey head to the scene
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 0))
monkey_obj = bpy.context.active_object

# Set up animation
total_frames = 100
rotation_amount = 2 * math.pi  # Full rotation in radians

# Set keyframes for animation
for frame in range(0, total_frames + 1):
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.objects.active = monkey_obj
    monkey_obj.rotation_euler = (0, 0, frame / total_frames * rotation_amount)
    monkey_obj.keyframe_insert(data_path="rotation_euler", index=-1)

# Set end frame
bpy.context.scene.frame_end = total_frames
