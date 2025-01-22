from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.videos.views import VideoListView, VideoProgressViewSet, VideoDetailView

router = DefaultRouter()
router.register(r'video-progress', VideoProgressViewSet, basename='video-progress')

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('', include(router.urls)),
]
