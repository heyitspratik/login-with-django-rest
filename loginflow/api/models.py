from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=50,null=True,unique=True)
    mobile_number = models.CharField(_('Mobile Number'), max_length=20, blank=True, null=True, unique=True)
    mobile_verified = models.BooleanField(default=False)


class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    otp = models.IntegerField(blank=False)


class MultipleEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True, default=None)
    is_primary = models.BooleanField(default=True)
