# from flask import Flask, render_template, request, send_file
# from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/create_video', methods=['POST'])
# def create_video():
#     if 'videoTemplate' not in request.files or 'characterImages' not in request.files or 'musicFile' not in request.files:
#         return 'Missing file(s)', 400

#     video_template = request.files['videoTemplate']
#     character_images = request.files.getlist('characterImages')
#     music_file = request.files['musicFile']

#     video_template_clip = VideoFileClip(video_template)

#     clips = []
#     for image in character_images:
#         character_clip = ImageSequenceClip([image], fps=24)
#         overlay_clip = character_clip.set_position(("center", "center")).set_duration(video_template_clip.duration)
#         final_clip = concatenate_videoclips([video_template_clip, overlay_clip])
#         clips.append(final_clip)

#     final_video = concatenate_videoclips(clips)
#     final_video = final_video.set_audio(music_file)

#     final_video.write_videofile('output.mp4')

#     return send_file('output.mp4', as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
# from flask import Flask, request, send_file
# from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/create_video', methods=['POST'])
# def create_video():
#     print("hello")
#     # Get the uploaded files from the request
#     video_template = request.files['videoTemplate']
#     character_images = request.files.getlist('characterImages')
#     music_file = request.files['musicFile']

#     # Save uploaded files to the server (optional)
#     video_template.save('video_template.mp4')
#     for idx, character_image in enumerate(character_images, start=1):
#         character_image.save(f'character{idx}.jpg')
#     music_file.save('background_music.mp3')

#     # Load the video template
#     video_template = VideoFileClip("video_template.mp4")

#     # Load character images
#     character_image_files = [f'character{i}.jpg' for i in range(1, len(character_images) + 1)]

#     # Load music file
#     music_file_path = "background_music.mp3"

#     # Create a list to hold the clips
#     clips = []

#     # Overlay character images onto the video template
#     for character_image_file in character_image_files:
#         character_clip = ImageSequenceClip([character_image_file], fps=24)
#         overlay_clip = character_clip.set_position(("center", "center")).set_duration(video_template.duration)
#         final_clip = concatenate_videoclips([video_template, overlay_clip])
#         clips.append(final_clip)

#     # Concatenate all clips together
#     final_video = concatenate_videoclips(clips)

#     # Add background music
#     final_video = final_video.set_audio(music_file_path)

#     # Write the final video to a file
#     final_video.write_videofile("output.mp4", codec="libx264")

#     # Send the generated video file back to the client
#     return send_file("output.mp4", as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, send_file
from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/create_video', methods=['POST'])
def create_video():
    # Get uploaded files from the request
    video_template = request.files['videoTemplate']
    character_images = request.files.getlist('characterImages')
    music_file = request.files['musicFile']

    # Save uploaded files to the server (optional)
    video_template.save('video_template.mp4')
    for idx, character_image in enumerate(character_images, start=1):
        character_image.save(f'character{idx}.jpg')
    music_file.save('background_music.mp3')

    # Load the video template
    video_template_clip = VideoFileClip("video_template.mp4")

    # Load character images
    character_clips = []
    for idx, character_image in enumerate(character_images, start=1):
        character_clip = ImageSequenceClip([f'character{idx}.jpg'], fps=24)
        character_clips.append(character_clip)

    # Overlay character images onto the video template
    final_clips = [video_template_clip] + character_clips
    final_video = concatenate_videoclips(final_clips)

    # Add background music
    final_video = final_video.set_audio("background_music.mp3")

    # Write the final video to a file
    final_video.write_videofile("output.mp4", codec="libx264")

    # Return the generated video file to the client
    return send_file("output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
