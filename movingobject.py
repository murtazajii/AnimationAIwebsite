import bpy
from mathutils import Vector

# Create a new scene if needed
if bpy.context.scene is None:
    bpy.ops.scene.new(type='NEW')

# Create a monkey object
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 0))
monkey = bpy.context.object

# Set initial location and rotation
monkey.location = (0, 0, 0)
monkey.rotation_euler = (0, 0, 0)  # Initial rotation (in radians)

# Define movement parameters
movement_speed = 0.1   # Speed of movement per frame

# Main loop
def main():
    frame_count = 0
    forward_direction = Vector((0, 1, 0))
    while frame_count < 200:  # Limiting the animation to 200 frames
        # Move the monkey forward
        monkey.location += movement_speed * forward_direction
        
        # Insert keyframe for location
        monkey.keyframe_insert(data_path="location", index=-1)
        
        # If monkey reaches a certain boundary, reverse direction
        if frame_count == 100:
            frame_count =0
            forward_direction *= -1
        # Advance one frame
        bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        frame_count += 1

# Call the main function
main()
