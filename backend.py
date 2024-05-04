import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

class BrowseVideoFile(Operator, ImportHelper):
    bl_idname = "object.browse_video_file"
    bl_label = "Browse Video File"

    filename_ext = ".mp4"

    def execute(self, context):
        filepath = self.filepath
        print("Selected video file:", filepath)
        # You can perform further operations with the selected video file here
        return {'FINISHED'}

class SelectTemplateFile(Operator, ImportHelper):
    bl_idname = "object.select_template_file"
    bl_label = "Select Template File"

    filename_ext = ".blend"

    def execute(self, context):
        filepath = self.filepath
        print("Selected template file:", filepath)
        # You can perform further operations with the selected template file here
        return {'FINISHED'}

# Define the panel for the user interface
class PT_SimplePanel(bpy.types.Panel):
    bl_label = "Simple Video Editor"
    bl_idname = "PT_PT_SimplePanel"  # Add 'PT_PT_' prefix
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Browse video file button
        layout.operator("object.browse_video_file", text="Browse Video File")

        # Select template file button
        layout.operator("object.select_template_file", text="Select Template File")

# Register the classes
def register():
    bpy.utils.register_class(BrowseVideoFile)
    bpy.utils.register_class(SelectTemplateFile)
    bpy.utils.register_class(PT_SimplePanel)

def unregister():
    bpy.utils.unregister_class(BrowseVideoFile)
    bpy.utils.unregister_class(SelectTemplateFile)
    bpy.utils.unregister_class(PT_SimplePanel)

if __name__ == "__main__":
    register()

