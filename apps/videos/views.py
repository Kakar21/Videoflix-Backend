from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.videos.models import Video
from apps.videos.api.serializers import VideoSerializer

class VideoListView(generics.ListAPIView):
    """
    API view to list all videos
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]