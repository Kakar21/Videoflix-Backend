from apps.videos.tasks import process_video_for_hls, remove_video_files
from apps.videos.models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def handle_video_creation(sender, instance, created, **kwargs):
    """
    Handles video processing after a new video is uploaded.
    """
    if created and instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(process_video_for_hls, instance.video_file.path, instance.id, instance.thumbnail.path)

@receiver(post_delete, sender=Video)
def handle_video_deletion(sender, instance, **kwargs):
    """
    Ensures that all associated files of a deleted video are removed.
    """
    if instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(remove_video_files, instance.id)
