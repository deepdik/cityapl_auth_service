import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from cityapl.apps.user_auth.serializers import (AuthTokenSerializer,
   SocialLoginSerializer, UserProfileSerializer, SignupSerializer)
from cityapl.apps.user_auth.utils import OTPAuth


class LoginView(APIView):
    """
    To get authorization token from user credentials.
    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        user = serializer.validated_data['user']
        serializer = UserProfileSerializer(
        	user, context={'request': request})
        response = serializer.data
        response.update({'token': token})
        return Response(response, status=status.HTTP_200_OK)


class SignupView(APIView):
    """
    To get authorization token from user credentials.
    """
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        user = serializer.validated_data['user']
        serializer = UserProfileSerializer(
            user, context={'request': request})
        response = serializer.data
        response.update({'token': token})
        return Response(response, status=status.HTTP_200_OK)


class SocialLoginView(APIView):
    """
    To get authorization token from user credentials.
    """
    serializer_class = SocialLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        user = serializer.validated_data['user']
        serializer = UserProfileSerializer(
            user, context={'request': request})
        response = serializer.data
        response.update({'token': token})
        return Response(response, status=status.HTTP_200_OK)


class Logout(APIView):
    """
    User must be authenticated to successfully logout, i.e., Authorization
    token must be passed in header
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', None)
        token = token.split()[1]
        token_obj = Token.objects.filter(key=token)
        token_obj.delete()
        return Response(status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    """
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        user = request.user
        if user.is_mobile_verified:
            return Response({
            'detail':"Mobile is already verified"},
            status=status.HTTP_400_BAD_REQUEST)
        response, msg = OTPAuth.validate_otp(user, otp)

        if response:
            user.is_mobile_verified = True
            user.save()
            return Response({
                    'detail': msg},
                    status=status.HTTP_200_OK)

        return Response({
            'detail': msg},
            status=status.HTTP_400_BAD_REQUEST)


class OTPGenerateView(APIView):
    """
    To generate new OTP
    (need to protect this API)
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_mobile_verified:
            return Response({
            'detail':"Mobile is already verified"},
            status=status.HTTP_400_BAD_REQUEST)
        OTPAuth.generate_otp(user)
        return Response({
            'detail':"OTP sent successfully"},
            status=status.HTTP_200_OK)

