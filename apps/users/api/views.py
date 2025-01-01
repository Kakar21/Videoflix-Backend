import os
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.api.serializers import UserRegistrationSerializer, UserLoginSerializer, SetNewPasswordSerializer
from apps.users.models import UserAccount
from rest_framework import generics, status
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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
    
class PasswordResetRequestView(generics.GenericAPIView):
    def post(self, request):
        """
        Generate and send password reset email.
        """
        email = request.data.get('email')
        if email and UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email=email)
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