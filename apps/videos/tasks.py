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
    move_thumbnail(thumbnail_path)

    # 4 Auflösungen generieren
    convert_video(video_path, "120p", 160, 120, 400)
    convert_video(video_path, "360p", 640, 360, 1000)
    convert_video(video_path, "720p", 1280, 720, 3000)
    convert_video(video_path, "1080p", 1920, 1080, 5000)

    move_video_files(video_path, video_id)


def move_thumbnail(thumbnail_path):
    """
    Moves the thumbnail to /media/thumbnails/ without modifying it.
    """
    target_directory = os.path.join('media', 'thumbnails')
    ensure_directory_exists(target_directory)

    target_path = os.path.join(
        target_directory, os.path.basename(thumbnail_path))

    shutil.move(thumbnail_path, target_path)
    print(f"Moved thumbnail to {target_path}")  # Debugging


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
            target_path = os.path.join(
                target_directory, os.path.basename(file_path))
            shutil.move(file_path, target_path)
            print(f"Moved {file_path} to {target_path}")  # Debugging
        else:
            print(f"File not found: {file_path}")


def convert_video(video_path, resolution, width, height, bitrate):
    file_name, _ = os.path.splitext(video_path)
    target = f"{file_name}_{resolution}.mp4"

    # Dynamische Audio-Bitrate je nach Auflösung
    if resolution == "120p":
        audio_bitrate = 64
    elif resolution == "360p":
        audio_bitrate = 96
    elif resolution == "720p":
        audio_bitrate = 160
    elif resolution == "1080p":
        audio_bitrate = 256
    else:
        audio_bitrate = 128  # fallback, falls was schiefgeht

    print(f"Converting {video_path} to {resolution} ({width}x{height}) with audio {audio_bitrate}k...")

    cmd = (
        f'ffmpeg -i "{video_path}" -vf "scale={width}:{height}" '
        f'-c:v h264 -b:v {bitrate}k -c:a aac -b:a {audio_bitrate}k "{target}"'
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
    target_directory = os.path.join('media', 'thumbnails')
    if os.path.exists(target_directory):
        print(f"Removing thumbnails for video {video_id}")
        for file in os.listdir(target_directory):
            if file.startswith(f"{video_id}_"):
                os.remove(os.path.join(target_directory, file))


def remove_videos(video_id):
    """
    Deletes all video files.
    """
    target_directory = os.path.join('media', 'videos', str(video_id))
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
