from django.urls import path
from apps.videos.views import VideoListView

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
]
