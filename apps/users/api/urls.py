from django.urls import path
from users.api.views import (UserLoginView, UserRegistrationView, EmailCheckView,
                         EmailVerificationView, PasswordResetRequestView,
                         PasswordResetView, PasswordResetValidationView)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/validate/<uidb64>/<token>/', PasswordResetValidationView.as_view(), name='password-reset-validate'),
    path('password-reset/confirm/', PasswordResetView.as_view(), name='password-reset-confirm'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
