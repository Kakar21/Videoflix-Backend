from django.test import TestCase
from apps.users.models import UserAccount
from apps.videos.models import Video

class VideoModelTest(TestCase):
    def setUp(self):
        """
        Setup test data
        """
        self.user = UserAccount.objects.create_user(email='test@mail.com', password='password123')
        self.video = Video.objects.create(
            title='Test Video',
            description='This is a test video description.',
            category='documentary',
            video_file='test_video.mp4',
            thumbnail='test_thumbnail.jpg'
        )

    def test_video_model(self):
        """
        Test the Video model
        """
        self.assertEqual(str(self.video), 'Test Video')
        self.assertTrue(isinstance(self.video, Video))
        self.assertEqual(self.video.category, 'documentary')
