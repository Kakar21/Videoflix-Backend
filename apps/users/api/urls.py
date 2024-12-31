from django.urls import path
from users.api.views import (UserLoginView, UserRegistrationView)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
