import os
import shutil
import subprocess
import glob
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip

def process_video_for_hls(video_path, video_id, thumbnail_path):
    """
    Processes a video for HLS playback, generates a preview, compresses the thumbnail, 
    and creates multiple resolution formats.
    """
    generate_video_preview(video_path, video_id)
    compress_and_resize_thumbnail(thumbnail_path, video_id)
    create_hls_master_playlist(video_path)
    convert_to_hls_1080p(video_path)
    convert_to_hls_720p(video_path)
    convert_to_hls_480p(video_path)
    move_video_files(video_path, video_id)

def generate_video_preview(video_path, video_id):
    """
    Generates a 3-second preview of the video.
    """
    target_directory = os.path.join('media', 'previews', str(video_id))
    ensure_directory_exists(target_directory)
    preview_path = os.path.join(target_directory, 'preview.mp4')

    with VideoFileClip(video_path) as video:
        preview = video.subclip(0, 3)
        preview.write_videofile(preview_path, codec='libx264', audio_codec='aac', fps=24)

def compress_and_resize_thumbnail(thumbnail_path, video_id):
    """
    Compresses and resizes the video thumbnail to improve performance and reduce file size.
    """
    target_directory = os.path.join('media', 'thumbnails', str(video_id))
    ensure_directory_exists(target_directory)
    optimized_thumbnail_path = os.path.join(target_directory, 'thumbnail.jpeg')

    with Image.open(thumbnail_path) as img:
        img = img.convert('RGB')
        img = img.resize((120, 214))
        img.save(thumbnail_path, format='JPEG', quality=85, optimize=True)

    shutil.move(thumbnail_path, optimized_thumbnail_path)

def ensure_directory_exists(directory):
    """
    Ensures that the target directory exists; if not, it creates it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def move_video_files(video_path, video_id):
    """
    Moves all generated HLS files to the correct directory.
    """
    base_name, _ = os.path.splitext(video_path)
    directory, _ = os.path.split(video_path)
    target_directory = os.path.join('media', 'videos', str(video_id))

    ensure_directory_exists(target_directory)
    files_to_move = collect_files_to_move(directory, base_name)

    for file_path in files_to_move:
        if os.path.exists(file_path):
            target_path = os.path.join(target_directory, os.path.basename(file_path))
            shutil.move(file_path, target_path)
        else:
            print(f"File not found: {file_path}")

def collect_files_to_move(directory, base_name):
    """
    Collects a list of files to be moved to the appropriate directory.
    """
    files_to_move = [
        f"{directory}/master.m3u8",
        f"{base_name}.mp4",
        f"{base_name}_1080p.m3u8",
        f"{base_name}_720p.m3u8",
        f"{base_name}_480p.m3u8"
    ]

    for quality in ['1080p', '720p', '480p']:
        segment_pattern = f"{base_name}_{quality}_*.ts"
        segment_files = glob.glob(segment_pattern)
        files_to_move.extend(segment_files)

    return files_to_move

def create_hls_master_playlist(video_path):
    """
    Generates the master playlist file for HLS streaming.
    """
    file_name_no_url = os.path.basename(video_path).split('.')[0]
    master_playlist_path = os.path.join(os.path.dirname(video_path), 'master.m3u8')

    with open(master_playlist_path, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\n")
        f.write(f"{file_name_no_url}_1080p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720\n")
        f.write(f"{file_name_no_url}_720p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=854x480\n")
        f.write(f"{file_name_no_url}_480p.m3u8\n")

def convert_to_hls_1080p(video_path):
    """
    Converts the video to 1080p resolution for HLS streaming.
    """
    file_name, _ = os.path.splitext(video_path)
    target = f"{file_name}_1080p.m3u8"
    segment_filename = f"{file_name}_1080p_%03d.ts"

    cmd = f'ffmpeg -i "{video_path}" -vf scale=-2:1080 -c:v h264 -b:v 5000k -c:a aac -b:a 128k -hls_time 6 -hls_playlist_type vod -hls_segment_filename "{segment_filename}" "{target}"'
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_to_hls_720p(video_path):
    """
    Converts the video to 720p resolution for HLS streaming.
    """
    file_name, _ = os.path.splitext(video_path)
    target = f"{file_name}_720p.m3u8"
    segment_filename = f"{file_name}_720p_%03d.ts"

    cmd = f'ffmpeg -i "{video_path}" -vf scale=-2:720 -c:v h264 -b:v 3000k -c:a aac -b:a 128k -hls_time 6 -hls_playlist_type vod -hls_segment_filename "{segment_filename}" "{target}"'
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_to_hls_480p(video_path):
    """
    Converts the video to 480p resolution for HLS streaming.
    """
    file_name, _ = os.path.splitext(video_path)
    target = f"{file_name}_480p.m3u8"
    segment_filename = f"{file_name}_480p_%03d.ts"

    cmd = f'ffmpeg -i "{video_path}" -vf scale=-2:480 -c:v h264 -b:v 1000k -c:a aac -b:a 128k -hls_time 6 -hls_playlist_type vod -hls_segment_filename "{segment_filename}" "{target}"'
    subprocess.run(cmd, capture_output=True, shell=True)

def remove_video_files(video_id):
    """
    Removes all video-related files from storage.
    """
    remove_video_preview(video_id)
    remove_video_thumbnail(video_id)
    remove_hls_segments(video_id)

def remove_video_preview(video_id):
    """
    Deletes the preview video files.
    """
    target_directory = os.path.join('media', 'previews', str(video_id))
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

def remove_video_thumbnail(video_id):
    """
    Deletes the thumbnail images.
    """
    target_directory = os.path.join('media', 'thumbnails', str(video_id))
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

def remove_hls_segments(video_id):
    """
    Deletes all HLS video segment files.
    """
    target_directory = os.path.join('media', 'videos', str(video_id))
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
