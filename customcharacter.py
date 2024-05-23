import bpy
# Function to load a character model based on user selection
def load_character(character_name):
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Load the selected character model
    bpy.ops.import_scene.obj(filepath=f"path/to/characters/{character_name}.obj")

    # Set the newly imported object as the active object
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

# Function to edit the character model based on user input
def edit_character(scale_factor):
    selected_object = bpy.context.object
    
    # Check if the selected object is a mesh
    if selected_object.type == 'MESH':
        # Access the mesh data of the selected object
        mesh = selected_object.data
        
        # Modify the mesh geometry (e.g., scale the mesh)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))  # Scale the mesh
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Selected object is not a mesh.")

# Main function to handle user interaction
def main():
    # User selects a character
    selected_character = input("Enter the name of the character you want to load: ")
    load_character(selected_character)
    
    # User edits the character
    scale_factor = float(input("Enter the scale factor (e.g., 1.2 for 20% increase): "))
    edit_character(scale_factor)

# Run the main function
if __name__ == "__main__":
    main()
