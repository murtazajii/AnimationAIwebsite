# # import bpy
# # from bpy_extras.io_utils import ImportHelper
# # from bpy.types


# # class BrowseVideoFile(Operator, ImportHelper):
# #     bl_idname = "object.browse_video_file"
# #     bl_label = "Browse Video File"

# #     filename_ext = ".mp4"

# #     def execute(self, context):
# #         filepath = self.filepath
# #         print("Selected video file:", filepath)
# #         # You can perform further operations with the selected video file here
# #         return {'FINISHED'}

# # class SelectTemplateFile(Operator, ImportHelper):
# #     bl_idname = "object.select_template_file"
# #     bl_label = "Select Template File"

# #     filename_ext = ".blend"

# #     def execute(self, context):
# #         filepath = self.filepath
# #         print("Selected template file:", filepath)
# #         # You can perform further operations with the selected template file here
# #         return {'FINISHED'}

# # # Define the panel for the user interface
# # class PT_SimplePanel(bpy.types.Panel):
# #     bl_label = "Simple Video Editor"
# #     bl_idname = "PT_PT_SimplePanel"  # Add 'PT_PT_' prefix
# #     bl_space_type = 'VIEW_3D'
# #     bl_region_type = 'UI'
# #     bl_category = 'Tool'

# #     def draw(self, context):
# #         layout = self.layout

# #         # Browse video file button
# #         layout.operator("object.browse_video_file", text="Browse Video File")

# #         # Select template file button
# #         layout.operator("object.select_template_file", text="Select Template File")

# # # Register the classes
# # def register():
# #     bpy.utils.register_class(BrowseVideoFile)
# #     bpy.utils.register_class(SelectTemplateFile)
# #     bpy.utils.register_class(PT_SimplePanel)

# # def unregister():
# #     bpy.utils.unregister_class(BrowseVideoFile)
# #     bpy.utils.unregister_class(SelectTemplateFile)
# #     bpy.utils.unregister_class(PT_SimplePanel)

# # if __name__ == "__main__":
# #     register()

# from flask import Flask, request, jsonify
# import os
# import subprocess

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/edit-video', methods=['POST'])
# def edit_video():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video file provided'}), 400
    
#     video_file = request.files['video']
#     video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
#     video_file.save(video_path)

#     edited_video_path = edit_video_backend(video_path)
    
#     return jsonify({'edited_video_path': edited_video_path}), 200

# def edit_video_backend(input_path):
#     edited_video_path = os.path.splitext(input_path)[0] + '_edited.mp4'

#     # Perform video editing using Blender
#     # For demonstration, let's assume we're using FFmpeg for simplicity
#     subprocess.run(['blender', '--background', '--python', 'video_editing_script.py', '--', input_path, edited_video_path], check=True)

#     return edited_video_path

# if __name__ == "__main__":
#     app.run(debug=True)
import bpy
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to apply brightness and contrast adjustments
def apply_brightness_contrast(image, brightness, contrast):
    pixels = image.pixels[:]
    for i in range(0, len(pixels), 4):
        for j in range(3):
            pixels[i+j] = min(max(pixels[i+j] * contrast + brightness, 0.0), 1.0)
    image.pixels[:] = pixels

# Function to apply color adjustments
def apply_color_adjustments(image, saturation_factor, hue_shift):
    bpy.context.view_layer.objects.active = None  # Deselect active object
    bpy.ops.image.sample()  # Sample the image
    bpy.context.scene.tool_settings.image_sample_shade = 'VALUE'
    bpy.context.scene.tool_settings.image_sample_brightness = 1.0
    bpy.context.scene.tool_settings.image_sample_saturation = saturation_factor
    bpy.context.scene.tool_settings.image_sample_value = 1.0
    bpy.context.scene.tool_settings.image_sample_hue_shift = hue_shift
    bpy.ops.image.sample()

# Function to apply sharpening
def apply_sharpening(image, amount):
    bpy.context.view_layer.objects.active = None  # Deselect active object
    bpy.context.view_layer.objects.active = bpy.data.objects["Image"]
    bpy.ops.image.filter(type='SHARPEN', filter_blur=amount)

# Function to apply dodging
def apply_dodge(image, amount):
    bpy.context.view_layer.objects.active = None  # Deselect active object
    bpy.context.view_layer.objects.active = bpy.data.objects["Image"]
    bpy.ops.image.filter(type='DODGE', filter_value=amount)

# Function to apply burning
def apply_burn(image, amount):
    bpy.context.view_layer.objects.active = None  # Deselect active object
    bpy.context.view_layer.objects.active = bpy.data.objects["Image"]
    bpy.ops.image.filter(type='BURN', filter_value=amount)

# Function to apply all editing functions
def apply_image_editing(image_path, editing_params):
    # Load the image
    image = bpy.data.images.load(image_path)

    # Apply brightness and contrast adjustments
    apply_brightness_contrast(image, editing_params['brightness'], editing_params['contrast'])

    # Apply color adjustments
    apply_color_adjustments(image, editing_params['saturation_factor'], editing_params['hue_shift'])

    # Apply sharpening
    apply_sharpening(image, editing_params['sharpen_amount'])

    # Apply dodging
    apply_dodge(image, editing_params['dodge_amount'])

    # Apply burning
    apply_burn(image, editing_params['burn_amount'])

    # Save the edited image
    image.save_render('/path/to/save/edited_image.png')

# Endpoint for uploading image and applying editing
@app.route('/edit-image', methods=['POST'])
def edit_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected image'})

    # Save the uploaded image
    image_path = '/path/to/save/uploaded_image.png'
    image_file.save(image_path)

    # Get editing parameters from request
    editing_params = {
        'brightness': float(request.form['brightness']),
        'contrast': float(request.form['contrast']),
        'saturation_factor': float(request.form['saturation_factor']),
        'hue_shift': float(request.form['hue_shift']),
        'sharpen_amount': float(request.form['sharpen_amount']),
        'dodge_amount': float(request.form['dodge_amount']),
        'burn_amount': float(request.form['burn_amount']),
    }

    # Apply image editing
    apply_image_editing(image_path, editing_params)

    return jsonify({'message': 'Image editing applied successfully'})

if __name__ == '__main__':
    app.run(debug=True)



# Clear existing VSE data
def clear_vse():
    bpy.ops.sequencer.select_all(action='SELECT')
    bpy.ops.sequencer.delete()

# Function to add video clips to VSE
def add_video_clips(video_files):
    for i, video_file in enumerate(video_files):
        bpy.ops.sequencer.movie_strip_add(filepath=video_file, frame_start=i*100, channel=i)

# Function to add transition effects between clips
def add_transition_effects(num_clips):
    for i in range(num_clips - 1):
        bpy.ops.sequencer.effect_strip_add(type='TRANSITION', frame_start=(i+1)*100, frame_end=(i+1)*100 + 25, channel=i, overlap=25)

# Function to apply color effects to clips
def apply_color_effects():
    for strip in bpy.context.scene.sequence_editor.sequences:
        if strip.type == 'MOVIE':
            color_effect = strip.effects.new(type='COLOR')
            color_effect.color_saturation = 1.5
            color_effect.color_brightness = 0.5
            color_effect.color_contrast = 1.2

# Function to render the final video
def render_video(output_path):
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(animation=True)

@app.route('/edit-videos', methods=['POST'])
def edit_videos():
    # Clear existing VSE data
    clear_vse()

    # Get video files from request
    video_files = request.files.getlist('videos')

    # Save video files to temporary location
    temp_dir = "/tmp/videos/"
    os.makedirs(temp_dir, exist_ok=True)
    video_paths = []
    for video_file in video_files:
        video_path = os.path.join(temp_dir, video_file.filename)
        video_file.save(video_path)
        video_paths.append(video_path)

    # Add video clips to VSE
    add_video_clips(video_paths)

    # Add transition effects between clips
    add_transition_effects(len(video_files))

    # Apply color effects to clips
    apply_color_effects()

    # Render the final video
    output_path = "/path/to/render/output/final_video.mp4"
    render_video(output_path)

    return jsonify({'message': 'Video editing applied successfully'})

if __name__ == '__main__':
    app.run(debug=True)

import bpy
from flask import Flask, request, jsonify

app = Flask(__name__)

def edit_video(video_files, output_path):
    # Clear existing VSE data
    bpy.ops.sequencer.select_all(action='SELECT')
    bpy.ops.sequencer.delete()

    # Add video clips to VSE
    for i, video_file in enumerate(video_files):
        bpy.ops.sequencer.movie_strip_add(filepath=video_file, frame_start=i*100, channel=i)

    # Add transition effects between clips
    for i in range(len(video_files) - 1):
        bpy.ops.sequencer.effect_strip_add(type='TRANSITION', frame_start=(i+1)*100, frame_end=(i+1)*100 + 25, channel=i, overlap=25)

    # Apply color effects to clips
    for strip in bpy.context.scene.sequence_editor.sequences:
        if strip.type == 'MOVIE':
            color_effect = strip.effects.new(type='COLOR')
            color_effect.color_saturation = 1.5
            color_effect.color_brightness = 0.5
            color_effect.color_contrast = 1.2

    # Set render output path
    bpy.context.scene.render.filepath = output_path

    # Render the final video
    bpy.ops.render.render(animation=True)

@app.route('/edit-videos', methods=['POST'])
def edit_videos():
    video_files = request.files.getlist('videos')
    output_path = request.form['outputPath']

    # Save video files to temporary location
    temp_dir = "/tmp/videos/"
    os.makedirs(temp_dir, exist_ok=True)
    video_paths = []
    for video_file in video_files:
        video_path = os.path.join(temp_dir, video_file.filename)
        video_file.save(video_path)
        video_paths.append(video_path)

    # Edit and render the video
    edit_video(video_paths, output_path)

    return jsonify({'message': 'Video editing applied successfully'})

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)

# Function to clear existing VSE data
def clear_vse():
    bpy.ops.sequencer.select_all(action='SELECT')
    bpy.ops.sequencer.delete()

# Function to add a video clip to VSE
def add_video_clip(video_file, frame_start, channel):
    bpy.ops.sequencer.movie_strip_add(filepath=video_file, frame_start=frame_start, channel=channel)

# Function to delete a clip from VSE
def delete_clip(strip):
    bpy.context.scene.sequence_editor.sequences.remove(strip)

@app.route('/manage-clips', methods=['POST'])
def manage_clips():
    # Clear existing VSE data
    clear_vse()

    # Get data from request
    data = request.json

    # Add video clips to VSE
    for clip_data in data['clips']:
        add_video_clip(clip_data['video_file'], clip_data['frame_start'], clip_data['channel'])

    # Delete clips from VSE
    for clip_id in data.get('delete_clips', []):
        strip = bpy.context.scene.sequence_editor.sequences[clip_id]
        delete_clip(strip)

    return jsonify({'message': 'Clips managed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
# Function to adjust brightness, contrast, and saturation
def adjust_color_effects(saturation, brightness, contrast):
    for strip in bpy.context.scene.sequence_editor.sequences:
        if strip.type == 'MOVIE':
            color_effect = strip.effects.new(type='COLOR')
            color_effect.color_saturation = saturation
            color_effect.color_brightness = brightness
            color_effect.color_contrast = contrast

@app.route('/edit-color-effects', methods=['POST'])
def edit_color_effects():
    data = request.json
    saturation = data.get('saturation', 1.0)
    brightness = data.get('brightness', 0.0)
    contrast = data.get('contrast', 1.0)

    adjust_color_effects(saturation, brightness, contrast)

    return jsonify({'message': 'Color effects applied successfully'})

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)

# Function to add a transition effect between clips
def add_transition_effect(frame_start, frame_end, channel, overlap):
    bpy.ops.sequencer.effect_strip_add(type='TRANSITION', frame_start=frame_start, frame_end=frame_end, channel=channel, overlap=overlap)

@app.route('/add-transition-effect', methods=['POST'])
def add_transition():
    data = request.json
    frame_start = data.get('frame_start')
    frame_end = data.get('frame_end')
    channel = data.get('channel')
    overlap = data.get('overlap', 25)  # Default overlap

    add_transition_effect(frame_start, frame_end, channel, overlap)

    return jsonify({'message': 'Transition effect added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)

# Function to apply color effects to video clips
def apply_color_effects(saturation, brightness, contrast):
    for strip in bpy.context.scene.sequence_editor.sequences:
        if strip.type == 'MOVIE':
            color_effect = strip.effects.new(type='COLOR')
            color_effect.color_saturation = saturation
            color_effect.color_brightness = brightness
            color_effect.color_contrast = contrast

@app.route('/apply-color-effects', methods=['POST'])
def apply_color():
    data = request.json
    saturation = data.get('saturation', 1.0)
    brightness = data.get('brightness', 0.0)
    contrast = data.get('contrast', 1.0)

    apply_color_effects(saturation, brightness, contrast)

    return jsonify({'message': 'Color effects applied successfully'})

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)

# Function to add text to video clips
def add_text(text, frame_start, frame_end, channel, font_size=30, color=(1.0, 1.0, 1.0)):
    bpy.ops.object.text_add(enter_editmode=False, location=(0, 0, 0))
    bpy.ops.object.editmode_toggle()
    bpy.ops.font.delete(type='ALL')
    bpy.ops.font.text_insert(text=text)
    bpy.ops.object.editmode_toggle()
    
    text_obj = bpy.context.object
    text_obj.data.size = font_size
    
    text_strip = bpy.context.scene.sequence_editor.sequences.new_effect(name="Text", type='TEXT', channel=channel, frame_start=frame_start, frame_end=frame_end, seq1=text_obj)
    text_strip.text = text
    text_strip.font_size = font_size
    text_strip.color = color

@app.route('/add-text', methods=['POST'])
def add_text_route():
    data = request.json
    text = data.get('text')
    frame_start = data.get('frame_start')
    frame_end = data.get('frame_end')
    channel = data.get('channel')
    font_size = data.get('font_size', 30)
    color = data.get('color', [1.0, 1.0, 1.0])

    add_text(text, frame_start, frame_end, channel, font_size, color)

    return jsonify({'message': 'Text added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)

# Function to add keyframes and animation to video strips
def add_keyframes(channel, frame, property_name, value):
    for strip in bpy.context.scene.sequence_editor.sequences:
        if strip.channel == channel and strip.frame_final_start <= frame <= strip.frame_final_end:
            strip.keyframe_insert(data_path=property_name, frame=frame)
            setattr(strip, property_name, value)

@app.route('/add-keyframes', methods=['POST'])
def add_keyframes_route():
    data = request.json
    channel = data.get('channel')
    frame = data.get('frame')
    property_name = data.get('property_name')
    value = data.get('value')

    add_keyframes(channel, frame, property_name, value)

    return jsonify({'message': 'Keyframes added successfully'})

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)

# Function to add audio to video clips
def add_audio(audio_file, frame_start, channel):
    bpy.ops.sequencer.sound_strip_add(filepath=audio_file, frame_start=frame_start, channel=channel)

@app.route('/add-audio', methods=['POST'])
def add_audio_route():
    data = request.json
    audio_file = data.get('audio_file')
    frame_start = data.get('frame_start')
    channel = data.get('channel')

    add_audio(audio_file, frame_start, channel)

    return jsonify({'message': 'Audio added successfully'})

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)

# Function to render and export video
def render_and_export(output_path, resolution_x, resolution_y, frame_start, frame_end, fps):
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.context.scene.render.fps = fps
    bpy.ops.render.render(animation=True)

@app.route('/render-export', methods=['POST'])
def render_export_route():
    data = request.json
    output_path = data.get('output_path')
    resolution_x = data.get('resolution_x')
    resolution_y = data.get('resolution_y')
    frame_start = data.get('frame_start')
    frame_end = data.get('frame_end')
    fps = data.get('fps')

    render_and_export(output_path, resolution_x, resolution_y, frame_start, frame_end, fps)

    return jsonify({'message': 'Video rendered and exported successfully'})

if __name__ == '__main__':
    app.run(debug=True)
import os
import bpy
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to perform video editing
@app.route('/edit-video', methods=['POST'])
def edit_video():
    # Your video editing code here
    return jsonify({'message': 'Video editing applied successfully'})

# Function to manage video clips in the Video Sequence Editor
@app.route('/manage-clips', methods=['POST'])
def manage_clips():
    # Your clip management code here
    return jsonify({'message': 'Clips managed successfully'})

# Function to apply color effects to video clips
@app.route('/apply-color-effects', methods=['POST'])
def apply_color_effects():
    # Your color effects code here
    return jsonify({'message': 'Color effects applied successfully'})

# Function to add transition effects between video clips
@app.route('/add-transition-effect', methods=['POST'])
def add_transition():
    # Your transition effect code here
    return jsonify({'message': 'Transition effect added successfully'})

# Function to add text to video clips
@app.route('/add-text', methods=['POST'])
def add_text_route():
    # Your text adding code here
    return jsonify({'message': 'Text added successfully'})

# Function to add keyframes and animation to video strips
@app.route('/add-keyframes', methods=['POST'])
def add_keyframes_route():
    # Your keyframes adding code here
    return jsonify({'message': 'Keyframes added successfully'})

# Function to add audio to video clips
@app.route('/add-audio', methods=['POST'])
def add_audio_route():
    # Your audio adding code here
    return jsonify({'message': 'Audio added successfully'})

# Function to render and export video
@app.route('/render-export', methods=['POST'])
def render_export_route():
    # Your rendering and exporting code here
    return jsonify({'message': 'Video rendered and exported successfully'})

if __name__ == '__main__':
    app.run(debug=True)
