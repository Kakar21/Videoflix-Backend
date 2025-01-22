from rest_framework import serializers
from apps.videos.models import Video, VideoProgress
import os


class VideoSerializer(serializers.ModelSerializer):
    video_120p = serializers.SerializerMethodField()
    video_360p = serializers.SerializerMethodField()
    video_720p = serializers.SerializerMethodField()
    video_1080p = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'category', 'thumbnail', 
                  'created_at', 'new', 'video_120p', 'video_360p', 'video_720p', 'video_1080p']

    def get_video_url(self, obj, quality):
        """
        Erstellt eine vollständige URL für das Video in der angegebenen Qualität.
        """
        request = self.context.get('request')
        if not obj.video_file:
            return None
        base_name = os.path.splitext(os.path.basename(obj.video_file.name))[0]
        video_path = f"/media/videos/{obj.id}/{base_name}_{quality}.mp4"
        return request.build_absolute_uri(video_path) if request else video_path

    def get_video_120p(self, obj):
        return self.get_video_url(obj, "120p")

    def get_video_360p(self, obj):
        return self.get_video_url(obj, "360p")

    def get_video_720p(self, obj):
        return self.get_video_url(obj, "720p")

    def get_video_1080p(self, obj):
        return self.get_video_url(obj, "1080p")


class VideoProgressSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    class Meta:
        model = VideoProgress
        fields = ['video', 'started', 'last_position', 'completed', 'updated_at']


class VideoProgressUpdateSerializer(serializers.Serializer):
    last_position = serializers.FloatField()

    def save_progress(self, user, video):
        """
        Save or update the progress of the video for the given user.
        """
        last_position = self.validated_data['last_position']
        
        video_progress, created = VideoProgress.objects.get_or_create(
            user=user,
            video=video,
            defaults={'last_position': last_position, 'started': True}
        )

        if not created:
            video_progress.last_position = last_position
            video_progress.started = True
            video_progress.save()

        return video_progress