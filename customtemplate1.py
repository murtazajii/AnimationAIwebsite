import bpy

# Function to list available templates
def list_templates():
    print("Available Templates:")
    for index, template in enumerate(templates):
        print(f"{index + 1}. {template}")

# Function to load a template based on user selection
def load_template(template_index):
    template_name = templates[template_index - 1]  # Adjusting index for 0-based list
    # Load the selected template
    bpy.ops.wm.open_mainfile(filepath=f"path/to/templates/{template_name}.blend")

# Main function to handle user interaction
def main():
    # List available templates
    list_templates()
    # Ask user to select a template
    template_index = int(input("Enter the index of the template you want to load: "))
    # Load the selected template
    load_template(template_index)
    print("Template loaded successfully.")

# List of available templates (replace with your actual template names)
templates = ["template1", "template2", "template3"]

# Run the main function
if __name__ == "__main__":
    main()
