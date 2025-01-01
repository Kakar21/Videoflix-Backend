import os
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.api.serializers import UserRegistrationSerializer, UserLoginSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserAccount
from apps.users.utils import EmailUtility
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect
from dotenv import load_dotenv
load_dotenv()

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handle user registration and send verification email.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user = UserAccount.objects.get(email=user.email)
        token = RefreshToken.for_user(user).access_token
        domain = get_current_site(request).domain
        activation_link = f"http://{domain}{reverse('verify-email')}?token={str(token)}"
        EmailUtility.send_verification_email(user, activation_link)
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        """
        Authenticate the user and provide JWT tokens.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'email': serializer.validated_data['email'],
            'refresh_token': serializer.validated_data['refresh'],
            'access_token': serializer.validated_data['access'],
        }, status=status.HTTP_200_OK)
    
class EmailVerificationView(generics.GenericAPIView):
    def get(self, request):
        """
        Confirm email verification through token.
        """
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = UserAccount.objects.get(id=payload['user_id'])
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
            return redirect('http://localhost:4200/login')
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(generics.GenericAPIView):
    def post(self, request):
        """
        Generate and send password reset email.
        """
        email = request.data.get('email')
        if email and UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"http://localhost:4200{reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})}"
            EmailUtility.send_password_reset_email(user, reset_link)
        return Response({'message': 'Password reset email sent if the email exists.'}, status=status.HTTP_200_OK)

class PasswordResetValidationView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        """
        Validate the reset token and user ID.
        """
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = UserAccount.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'Token and user validated successfully.'}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordResetView(generics.GenericAPIView):
    def patch(self, request):
        """
        Update user password with the new one.
        """
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    
class EmailCheckView(generics.GenericAPIView):
    def post(self, request):
        """
        Check if an email is already registered.
        """
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        is_registered = UserAccount.objects.filter(email=email).exists()
        return Response({'is_registered': is_registered})