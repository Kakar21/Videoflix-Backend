from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from apps.videos.models import Video, VideoProgress
from apps.videos.api.serializers import VideoSerializer, VideoProgressSerializer, VideoProgressUpdateSerializer
from rest_framework.generics import RetrieveAPIView
import os
from urllib.parse import unquote

class VideoListView(generics.ListAPIView):
    """
    API view to list all videos
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class VideoDetailView(RetrieveAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.all()
    
    def get_object(self):
        """
        Retrieves the video based on the file name, ignoring the path.
        """
        queryset = self.get_queryset()
        raw_path = self.kwargs.get("video_file")

        if not raw_path:
            raise NotFound("Invalid video path.")

        decoded_path = unquote(raw_path)
        filename = os.path.basename(decoded_path)

        video = queryset.filter(video_file__endswith=filename).first()

        if not video:
            raise NotFound(f"Video '{filename}' not found")

        return video


class VideoProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle video progress-related endpoints
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """
        Returns a list of videos the user has started watching but not completed
        """
        user = request.user
        in_progress_videos = VideoProgress.objects.filter(user=user, started=True, completed=False).select_related('video')
        serializer = VideoProgressSerializer(in_progress_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def save_progress(self, request, pk=None):
        """
        Saves the progress of a video
        """
        serializer = VideoProgressUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = self._get_video_or_404(pk)
        serializer.save_progress(user=request.user, video=video)
        return Response({'message': 'Progress saved successfully.'}, status=status.HTTP_200_OK)

    def _get_video_or_404(self, pk):
        """
        Helper method to retrieve a video or raise a NotFound error
        """
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound('Video not found.')
