# Serializers
from rest_framework import serializers
from apps.users.models import UserAccount
from django.contrib.auth import authenticate
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