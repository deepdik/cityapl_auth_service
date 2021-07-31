"""
"""
from django.urls import path, include 
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from cityapl.apps.user_auth.views import (
    LoginView,
    SocialLoginView,
    SignupView,
    Logout,
    OTPVerifyView,
    OTPGenerateView
)


router = SimpleRouter()


urlpatterns = [
	path('api-token-verify/', verify_jwt_token),
	path('api-token-refresh/', refresh_jwt_token),
	path('user/login/', LoginView.as_view(), name='login'),
	path('user/social-login/', SocialLoginView.as_view(), name='social-login'),
	path('user/signup/', SignupView.as_view(), name='signup'),
	path('user/logout/', Logout.as_view(), name='logout'),
	path('user/otp/verify/', OTPVerifyView.as_view(), name='otp-verify'),
	path('user/otp/generate/', OTPGenerateView.as_view(), name='otp-generate'),
]

urlpatterns += router.urls
