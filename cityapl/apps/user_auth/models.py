"""
Provide model user and user-account related models.
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserOTP(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='user_otp')
    otp = models.PositiveIntegerField()
    # 10 minutes
    exp_time = models.DateTimeField()

    class Meta:
        db_table = 'user_otp'

