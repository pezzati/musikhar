import os
import binascii

from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    male = 0
    female = 1
    GenderTypes = (
        (male, 'Male'),
        (female, 'Female')
    )
    mobile = models.CharField(max_length=20, null=True, blank=True)
    gender = models.IntegerField(choices=GenderTypes, default=male)
    age = models.IntegerField(default=0)
    image = models.FileField(upload_to='avatars', null=True, blank=True)
    is_signup = models.BooleanField(default=False)
    country = models.CharField(max_length=50,null=True,blank=True)



class Token(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=128, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_token()

        return super(Token, self).save(*args, **kwargs)

    def is_valid(self):
        if (self.created + timedelta(days=90)) > timezone.now():
            return True

        return False

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()


class Device(models.Model):
    ios = 'ios'
    android = 'android'
    TypeChoices = (
        (ios, 'iOS'),
        (android, 'Android')
    )

    udid = models.CharField(max_length=200, default='not-set')
    user = models.ForeignKey(User)
    type = models.CharField(max_length=10, choices=TypeChoices, default=android)
    os_version = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.type)
