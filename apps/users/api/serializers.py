# Serializers
from rest_framework import serializers
from apps.users.models import UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.exceptions import AuthenticationFailed

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering new users."""
    class Meta:
        model = UserAccount
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Ensure the email is not already registered."""
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        return UserAccount.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    """Serializer for logging in users."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise AuthenticationFailed("Invalid login credentials.")
        if not user.is_email_verified:
            raise AuthenticationFailed("Email verification is pending.")
        return {
            'email': user.email,
            'tokens': user.generate_tokens()
        }
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user_id = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = UserAccount.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
                raise AuthenticationFailed("Invalid or expired reset link.")
            user.set_password(attrs['password'])
            user.save()
        except Exception:
            raise AuthenticationFailed("Invalid or expired reset link.")
        return attrs
