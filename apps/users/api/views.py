from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.api.serializers import UserRegistrationSerializer, UserLoginSerializer
from apps.users.models import UserAccount
from rest_framework import generics, status

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