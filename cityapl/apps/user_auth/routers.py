"""
"""
from django.urls import path, include 
from rest_framework.routers import SimpleRouter

from cityapl.apps.user_auth.views import (
    LoginView,
    SocialLoginView,
    SignupView,
    Logout,
    OTPVerifyView,
    OTPGenerateView
)


router = SimpleRouter()

# router.register(r'token', TokenViewSet, basename='token')

urlpatterns = [
	# path('token/create/', TokenAPIView.as_view(), name='token-create'),
	path('user/login/', LoginView.as_view(), name='login'),
	path('user/social-login/', SocialLoginView.as_view(), name='social-login'),
	path('user/signup/', SignupView.as_view(), name='signup'),
	path('user/logout/', Logout.as_view(), name='logout'),
	path('user/otp/verify/', OTPVerifyView.as_view(), name='otp-verify'),
	path('user/otp/generate/', OTPGenerateView.as_view(), name='otp-generate'),
]

urlpatterns += router.urls
