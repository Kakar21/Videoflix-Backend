from django.test import TestCase, Client
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

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

# Custom Test Case for Views
class UserViewTestCase(TestCase):
    def setUp(self):
        """Initialize test client and test URLs."""
        self.client = Client()
        self.user_data = {
            'email': 'newuser@example.com',
            'password': 'testpassword123',
        }
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        get_user_model().objects.create_user(email='testlogin@example.com', password='passwordlogin')

    def test_register_user(self):
        """Test the user registration endpoint."""
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 201)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(self.login_url, data={'email': 'wrong@example.com', 'password': 'wrongpassword'})
        self.assertIn(response.status_code, [401, 403])

# Custom Test Case for Email Verification
class EmailVerificationTestCase(APITestCase):
    def setUp(self):
        """Set up data for email verification tests."""
        self.user_data = {
            'email': 'verifyuser@example.com',
            'password': 'verifysecure123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.verify_url = reverse('verify-email')
        self.token = RefreshToken.for_user(self.user).access_token
        self.confirmation_link = f"http://testserver{self.verify_url}?token={str(self.token)}"

    def test_valid_email_verification(self):
        """Test email verification with a valid token."""
        response = self.client.get(self.confirmation_link)
        self.assertEqual(response.status_code, 302)
        self.assertIn('http://localhost:4200/login', response.url)
        user = get_user_model().objects.get(email=self.user_data['email'])
        self.assertTrue(user.is_email_verified)

    def test_invalid_email_verification(self):
        """Test email verification with an invalid token."""
        response = self.client.get(f"{self.verify_url}?token=invalidtoken")
        self.assertEqual(response.status_code, 400)

    def test_expired_email_verification(self):
        """Test email verification with an expired token."""
        expired_token = jwt.encode({'user_id': self.user.id, 'exp': 0}, settings.SECRET_KEY, algorithm='HS256')
        response = self.client.get(f"{self.verify_url}?token={expired_token}")
        self.assertEqual(response.status_code, 400)