# from flask import Flask, request, send_file
# from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips
# import os

# app = Flask(__name__)

# @app.route('/create_video', methods=['POST'])
# def create_video():
#     video_template = request.files['videoTemplate']
#     character_images = request.files.getlist('characterImages')
#     music_file = request.files['musicFile']

#     # Save uploaded files to the server
#     video_template.save('video_template.mp4')
#     for idx, character_image in enumerate(character_images, start=1):
#         character_image.save(f'character{idx}.jpg')
#     music_file.save('background_music.mp3')

#     # Load the video template
#     video_template = VideoFileClip("video_template.mp4")

#     # Load character images
#     character_image_files = [f'character{i}.jpg' for i in range(1, len(character_images) + 1)]

#     # Load music file
#     music_file = "background_music.mp3"

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
#     final_video = final_video.set_audio(music_file)

#     # Write the final video to a file
#     final_video.write_videofile("output.mp4")

#     # Send the generated video file back to the client
#     return send_file("output.mp4", as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, send_file
from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/create_video', methods=['POST'])
def create_video():
    # Get the uploaded files from the request
    video_template = request.files['videoTemplate']
    character_images = request.files.getlist('characterImages')
    music_file = request.files['musicFile']

    # Save uploaded files to the server (optional)
    video_template.save('video_template.mp4')
    for idx, character_image in enumerate(character_images, start=1):
        character_image.save(f'character{idx}.jpg')
    music_file.save('background_music.mp3')

    # Load the video template
    video_template = VideoFileClip("video_template.mp4")

    # Load character images
    character_image_files = [f'character{i}.jpg' for i in range(1, len(character_images) + 1)]

    # Load music file
    music_file = "background_music.mp3"

    # Create a list to hold the clips
    clips = []

    # Overlay character images onto the video template
    for character_image_file in character_image_files:
        character_clip = ImageSequenceClip([character_image_file], fps=24)
        overlay_clip = character_clip.set_position(("center", "center")).set_duration(video_template.duration)
        final_clip = concatenate_videoclips([video_template, overlay_clip])
        clips.append(final_clip)

    # Concatenate all clips together
    final_video = concatenate_videoclips(clips)

    # Add background music
    final_video = final_video.set_audio(music_file)

    # Write the final video to a file
    final_video.write_videofile("output.mp4", codec="libx264")

    # Send the generated video file back to the client
    return send_file("output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
