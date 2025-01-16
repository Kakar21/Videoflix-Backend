from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import UserAccount
from apps.videos.models import Video, VideoProgress

def generate_test_video_file():
    """
    Creates a mock video file for testing purposes.
    """
    return SimpleUploadedFile(
        name='sample_video.mp4',
        content=b'Simulated video content',
        content_type='video/mp4',
    )

def generate_test_thumbnail():
    """
    Generates a mock thumbnail image for testing purposes.
    """
    return SimpleUploadedFile(
        name='sample_thumbnail.jpg',
        content=b'Simulated thumbnail content',
        content_type='image/jpeg',
    )

def create_sample_video():
    """
    Creates a video instance for testing.
    """
    video_file = generate_test_video_file()
    thumbnail = generate_test_thumbnail()

    return Video.objects.create(
        title='Sample Video',
        description='Test description for video model.',
        video_file=video_file,
        thumbnail=thumbnail,
        category='documentary'
    )

def create_test_user():
    """
    Creates a sample user instance for testing.
    """
    user = UserAccount.objects.create(email='testuser@example.com')
    user.set_password('secure_test_password')
    user.save()
    return user

def create_video_watch_progress(user, video):
    """
    Creates a test instance of video progress tracking.
    """
    return VideoProgress.objects.create(
        user=user,
        video=video,
        started=True,
        last_position=15.5,
        completed=False
    )
