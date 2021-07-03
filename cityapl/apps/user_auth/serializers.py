"""
"""
import datetime

from django.contrib.auth import authenticate, get_user_model, password_validation
from django.conf import settings

from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from cityapl.libs.accounts.models import UserDevicesDetail
from cityapl.apps.user_auth.utils import SocialOauth2, CustomValidators
 

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer to validate credential of login user and authenticate the user.
    """
    password = serializers.CharField(min_length=8, required=True)
    mobile_number = serializers.CharField(min_length=10, required=True)
    device_token = serializers.CharField(required=True)
    device_type = serializers.ChoiceField(
        required=True, choices=User.ACCOUNT_TYPE)

    def validate(self, attrs):
        """
        """
        qs = User.objects.filter(mobile_number=attrs.get('mobile_number'))
        if qs.exists():
            user = qs.first()
            if not user.check_password(attrs.get('password')):
                user = None
        else:
            user = None
        
        if user:
            if not user.is_active:
                msg = ('User account disabled.')
                raise serializers.ValidationError({"detail": msg})

        else:
            msg = ("Invalid Login Credentials.")
            raise serializers.ValidationError({"detail": [msg]})

        attrs =  AuthTokenSerializer.update_user_details(user, attrs)
        return attrs

    @staticmethod
    def update_user_details(user, attrs):
        """
        """
        UserDevicesDetail.objects.update_or_create(
            user=user,
            device_type = attrs.get('device_type'),
            defaults={
                'device_token':attrs.get('device_token')
                }
            )
        token, _ = Token.objects.get_or_create(user=user)
        attrs['user'] = user
        attrs['token'] = token.key
        return attrs


class SignupSerializer(serializers.Serializer):
    """
    """
    password = serializers.CharField(min_length=8, required=True)
    mobile_number = serializers.CharField(min_length=10, required=True)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    device_token = serializers.CharField(required=True)
    device_type = serializers.ChoiceField(
        required=True, choices=User.ACCOUNT_TYPE)

    def validate(self, attrs):
        """
        """
        if not CustomValidators.validate_mobile(attrs.get('mobile_number')):
            raise serializers.ValidationError({"detail": 'Invalid mobile Number'})

        qs = User.objects.filter(mobile_number=attrs.get('mobile_number'))
        if qs.exists():
            raise serializers.ValidationError(
                {"detail": 'User is already register with this mobile number'})
        
        if attrs.get('email'):
            qs = User.objects.filter(
                email=attrs.get('email')
            ).exclude(email='').exclude(email=None).distinct()
            if qs.exists():
                raise serializers.ValidationError({
                    'detail':'User with this email is already exists'
                    })

        user = User.objects.create(
                email=attrs.get('email'),
                mobile_number=attrs.get('mobile_number'),
                first_name=attrs.get('device_token'),
                last_name=attrs.get('device_token'),
                username=attrs.get('mobile_number')
            )
        # set user eync password
        user.set_password(attrs.get('password'))
        attrs =  AuthTokenSerializer.update_user_details(user, attrs)
        return attrs



class SocialLoginSerializer(serializers.Serializer):
    """
    Serializer to validate credential of login user and authenticate the user.
    """
    id_token = serializers.CharField(required=True)
    social_login_type = serializers.ChoiceField(
        required=True, choices=User.PROVIDER_TYPE)
    device_token = serializers.CharField(required=True)
    device_type = serializers.ChoiceField(
        required=True, choices=User.ACCOUNT_TYPE)

    def validate(self, attrs):
        """
        """
        user_info = SocialOauth2.google_token_verify(attrs.get('id_token'))
        if not user_info[0]:
            raise serializers.ValidationError({"detail": 'Invalid id token'})

        qs = User.objects.filter(
            social_id=user_info['sub'],
            social_login_type=attrs.get('social_login_type')
        )
        if qs.exists():
            user = qs.first()
            if not user.is_active:
                msg = ('User account disabled.')
                raise serializers.ValidationError({"detail": msg})
        else:
            name = user_info['name'].split(" ", 1)
            # create user with this id
            user = User.objects.create(
                email=user_info.get('email'),
                mobile_number=user_info.get('mobile_number'),
                social_id=user_info['sub'],
                social_login_type=attrs.get('social_login_type'),
                first_name=name[0],
                last_name=name[-1],
                username=user_info['sub']
            )

        attrs =  AuthTokenSerializer.update_user_details(user, attrs)
        return attrs


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for serializing info for user.
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name','mobile_number'
        )
        read_only_fields = (
            'id', 'email', 'first_name', 'last_name',  'user_type',
            'username'
        )


