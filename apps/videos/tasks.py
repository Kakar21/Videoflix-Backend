import os
import shutil
import subprocess
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip

def process_video(video_path, video_id, thumbnail_path):
    """
    Processes a video by compressing the thumbnail, 
    and converting it to different resolutions.
    """
    print(f"Processing video {video_path} for ID {video_id}")  # Debugging
    compress_and_resize_thumbnail(thumbnail_path, video_id)
    
    # 4 Auflösungen generieren
    convert_video(video_path, "120p", 160, 120, 400)
    convert_video(video_path, "360p", 640, 360, 1000)
    convert_video(video_path, "720p", 1280, 720, 3000)
    convert_video(video_path, "1080p", 1920, 1080, 5000)
    
    move_video_files(video_path, video_id)

def compress_and_resize_thumbnail(thumbnail_path, video_id):
    """
    Compresses and resizes the video thumbnail.
    """
    optimized_thumbnail_path = os.path.join('media', 'thumbnails', f"{video_id}.jpeg")

    with Image.open(thumbnail_path) as img:
        img = img.convert('RGB')
        img = img.resize((120, 214))
        img.save(thumbnail_path, format='JPEG', quality=85, optimize=True)

    shutil.copy(thumbnail_path, optimized_thumbnail_path)

def ensure_directory_exists(directory):
    """
    Ensures that the target directory exists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def move_video_files(video_path, video_id):
    """
    Moves all generated MP4 files to the correct directory.
    """
    directory, file_name = os.path.split(video_path)
    base_name, _ = os.path.splitext(file_name)
    target_directory = os.path.join('media', 'videos', str(video_id))

    ensure_directory_exists(target_directory)
    files_to_move = [
        f"{directory}/{base_name}_120p.mp4",
        f"{directory}/{base_name}_360p.mp4",
        f"{directory}/{base_name}_720p.mp4",
        f"{directory}/{base_name}_1080p.mp4"
    ]

    for file_path in files_to_move:
        if os.path.exists(file_path):
            target_path = os.path.join(target_directory, os.path.basename(file_path))
            shutil.move(file_path, target_path)
            print(f"Moved {file_path} to {target_path}")  # Debugging
        else:
            print(f"File not found: {file_path}")

def convert_video(video_path, resolution, width, height, bitrate):
    """
    Converts the video to a specific resolution and bitrate.
    """
    file_name, _ = os.path.splitext(video_path)
    target = f"{file_name}_{resolution}.mp4"

    print(f"Converting {video_path} to {resolution} ({width}x{height})...")  # Debugging

    cmd = (
        f'ffmpeg -i "{video_path}" -vf "scale={width}:{height}" '
        f'-c:v h264 -b:v {bitrate}k -c:a aac -b:a 128k "{target}"'
    )
    subprocess.run(cmd, capture_output=True, shell=True)

def remove_video_files(video_id):
    """
    Removes all video-related files.
    """
    remove_video_thumbnail(video_id)
    remove_videos(video_id)

def remove_video_thumbnail(video_id):
    """
    Deletes the thumbnail images.
    """
    thumbnail_path = os.path.join('media', 'thumbnails', f"{video_id}.jpeg")
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

def remove_videos(video_id):
    """
    Deletes all video files.
    """
    target_directory = os.path.join('media', 'videos', str(video_id))
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
