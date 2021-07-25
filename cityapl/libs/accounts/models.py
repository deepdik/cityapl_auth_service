"""
Provide model user and user-account related models.
"""
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cityapl.libs.accounts.validators import validate_password


class UserManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        # email = self.normalize_email(email)
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Store User account details.
    """
    # Use either of the username fields below:
    NORMAL, SOCIAL = '1', '2'
    ACCOUNT_TYPE = (
        (NORMAL, 'normal'),
        (SOCIAL, 'social'),
    )

    FACEBOOK, GOOGLE = '1', '2'
    PROVIDER_TYPE = (
        (FACEBOOK, 'facebook'),
        (GOOGLE, 'google'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(
        _('username'),
        max_length=255,
        unique=True,
        help_text=_('Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    password = models.CharField(
        _('password'),
        max_length=128,
        validators=[validate_password],
        null=True,
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Required. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid email. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    mobile_number = models.CharField(max_length=12, blank=True, null=True)
    name = models.CharField(_('first name'), max_length=128, blank=True, null=True)

    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPE)
    social_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    social_account_type = models.CharField(max_length=2, choices=PROVIDER_TYPE)
    is_mobile_verify = models.BooleanField(default=False)
    is_mail_verify = models.BooleanField(default=False)
    objects = UserManager()


    # Modify USERNAME_FIELD and REQUIRED_FIELDS as required.
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (

        )
        # ordering = ['username'] # Set it as required.

    # Use Either one of __str__ methods.
    def __str__(self):
        return '{email}'.format(email=self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

# post_save.connect(register_user_activity, sender=User)


class UserDevicesDetail(models.Model):
    """
    User other details
    """
    IOS, ANDROID, WEB  = '1', '2', '3'
    DEVICE_TYPE = (
        (IOS, 'ios'),
        (WEB, 'web'),
        (ANDROID, 'android'),
        )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='user_detail')
    device_type = models.CharField(max_length=2, choices=DEVICE_TYPE)
    device_token = models.CharField(max_length=255)
    last_login = models.DateTimeField(blank=True, null=True)
    user_ip = models.CharField(max_length=64, blank=True, null=True)
    user_lat = models.CharField(max_length=64, blank=True, null=True)
    user_lng = models.CharField(max_length=64, blank=True, null=True)
    user_browser = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'user_detail'
    
