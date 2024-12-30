from django.test import TestCase
from django.contrib.auth import get_user_model


# Custom Test Case for User Models
class UserModelTestCase(TestCase):
    def setUp(self):
        """Prepare a user instance for testing."""
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_instance(self):
        """Verify the user model behaves correctly."""
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_email_verified)