from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import UserAccount
from apps.videos.models import Video, VideoProgress
from rest_framework_simplejwt.tokens import RefreshToken


class VideoModelTests(TestCase):
    """
    Tests for the Video and VideoProgress models.
    """

    def setUp(self):
        """
        Prepare sample data for model tests.
        """
        self.user = UserAccount.objects.create_user(email="testuser@mail.com", password="password123")
        self.video = Video.objects.create(
            title="Sample Video",
            description="This is a test video.",
            category="documentary",
            video_file="videos/sample.mp4",
            thumbnail="thumbnails/sample.jpg"
        )
        self.video_progress = VideoProgress.objects.create(
            user=self.user,
            video=self.video,
            last_position=0
        )

    def test_video_model_representation(self):
        """
        Verify the string representation of the Video model.
        """
        self.assertEqual(str(self.video), "Sample Video")

    def test_video_progress_model_representation(self):
        """
        Verify the string representation of the VideoProgress model.
        """
        self.assertEqual(
            str(self.video_progress),
            f"{self.user.email} - {self.video.title} - {self.video_progress.last_position}"
        )

    def test_video_fields(self):
        """
        Test fields of the Video model.
        """
        self.assertEqual(self.video.description, "This is a test video.")
        self.assertEqual(self.video.category, "documentary")
        self.assertTrue(self.video.video_file)
        self.assertTrue(self.video.thumbnail)

    def test_video_progress_fields(self):
        """
        Test fields of the VideoProgress model.
        """
        self.assertEqual(self.video_progress.last_position, 0)
        self.assertFalse(self.video_progress.completed)


class VideoViewTests(TestCase):
    def setUp(self):
        """
        Prepare data for view tests.
        """
        self.client = Client()
        
        self.user = UserAccount.objects.create_user(
            email="testuser@mail.com",
            password="password123"
        )
        
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        
        self.video = Video.objects.create(
            title="Sample Video",
            description="This is a test video.",
            category="documentary",
            video_file="videos/sample.mp4",
            thumbnail="thumbnails/sample.jpg"
        )
        self.video_progress = VideoProgress.objects.create(
            user=self.user,
            video=self.video,
            last_position=0
        )
        
        self.video_list_url = reverse("video-list")
        self.video_progress_url = reverse("video-progress-in-progress")
        self.save_progress_url = reverse("video-progress-save-progress", args=[self.video.id])

    def test_authenticated_video_list(self):
        """
        Test the video list view for an authenticated user.
        """
        response = self.client.get(self.video_list_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_video_list(self):
        """
        Test the video list view for an unauthenticated user.
        """
        self.client.defaults.pop('HTTP_AUTHORIZATION', None)
        response = self.client.get(self.video_list_url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_video_progress(self):
        """
        Test the video progress retrieval for an authenticated user.
        """
        response = self.client.get(self.video_progress_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_video_progress(self):
        """
        Test the video progress retrieval for an unauthenticated user.
        """
        self.client.defaults.pop('HTTP_AUTHORIZATION', None)
        response = self.client.get(self.video_progress_url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_save_progress(self):
        """
        Test saving video progress for an authenticated user.
        """
        response = self.client.post(self.save_progress_url, {"last_position": 50})
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_save_progress(self):
        """
        Test saving video progress for an unauthenticated user.
        """
        self.client.defaults.pop('HTTP_AUTHORIZATION', None)
        response = self.client.post(self.save_progress_url, {"last_position": 50})
        self.assertEqual(response.status_code, 401)