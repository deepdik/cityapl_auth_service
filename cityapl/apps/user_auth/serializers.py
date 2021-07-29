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
            if user.password != attrs.get('password'):
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
    mobile_number = serializers.CharField(min_length=10, required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    device_token = serializers.CharField(required=True)
    device_type = serializers.ChoiceField(
        required=True, choices=User.ACCOUNT_TYPE)

    def validate(self, attrs):
        """
        """
        if attrs.get('mobile_number'):
            if not CustomValidators.validate_mobile(attrs.get('mobile_number')):
                raise serializers.ValidationError({"detail": 'Invalid mobile Number'})

            qs = User.objects.filter(mobile_number=attrs.get('mobile_number'))
            if qs.exists():
                raise serializers.ValidationError(
                    {"detail": 'User is already register with this mobile number'})
            
        elif attrs.get('email'):   
                qs = User.objects.filter(
                    email=attrs.get('email')
                ).exclude(email='').exclude(email=None).distinct()
                if qs.exists():
                    raise serializers.ValidationError({
                        'detail':'User with this email is already exists'
                        })
        else:
            raise serializers.ValidationError({
                'detail':'Email or Mobile is required'
                })
        username = attrs.get('mobile_number') if attrs.get('mobile_number') else attrs.get('email')
        user = User.objects.create(
                email=attrs.get('email'),
                mobile_number=attrs.get('mobile_number'),
                name=attrs.get('name'),
                username=username,
                account_type=User.NORMAL,
                password=attrs.get('password')

            )
        # set user eync password
        print(attrs.get('password'))
        # user.set_password(attrs.get('password'))
        attrs =  AuthTokenSerializer.update_user_details(user, attrs)
        attrs["auth_type"] = 1 if attrs.get('email') else 2
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

        print('-------------', user_info)
        qs = User.objects.filter(
            social_id=user_info[1]['sub'],
            social_account_type=attrs.get('social_login_type')
        )
        if qs.exists():
            user = qs.first()
            if not user.is_active:
                msg = ('User account disabled.')
                raise serializers.ValidationError({"detail": msg})
        else:
            # create user with this id
            user = User.objects.create(
                email=user_info[1].get('email'),
                mobile_number=user_info[1].get('mobile_number'),
                social_id=user_info[1]['sub'],
                name=user_info[1]['name'],
                username=user_info[1]['sub'],
                account_type=User.SOCIAL,
                social_account_type=attrs.get('social_login_type')
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
            'email', 'name', 'mobile_number','is_mobile_verify',
            'is_mail_verify', 'account_type', 'social_account_type'

        )
