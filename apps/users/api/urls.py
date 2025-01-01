from django.urls import path
from users.api.views import (UserLoginView, UserRegistrationView, PasswordResetRequestView,
                         PasswordResetView, PasswordResetValidationView)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/validate/<uidb64>/<token>/', PasswordResetValidationView.as_view(), name='password-reset-validate'),
    path('password-reset/confirm/', PasswordResetView.as_view(), name='password-reset-confirm'),
]
