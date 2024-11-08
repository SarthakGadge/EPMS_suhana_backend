from django.urls import path
from .views import RegisterView, LoginView, VerifyOTPView, ForgotPasswordRequestView, ForgotPasswordVerifyView, ResendOTPView

urlpatterns = [
    # Authentication Urls
    path('register/', RegisterView.as_view(), name='register'),    
    path('login/', LoginView.as_view(), name='login'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('forgot_password/', ForgotPasswordRequestView.as_view(), name='forgot-password-request'),
    path('reset_password/', ForgotPasswordVerifyView.as_view(), name='forgot-password-verify'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend-otp'),
]
