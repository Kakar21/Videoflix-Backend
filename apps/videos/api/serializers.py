from rest_framework import serializers
from apps.videos.models import Video, VideoProgress


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail', 'category', 'created_at', 'new']


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