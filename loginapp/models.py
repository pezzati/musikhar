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
    gender = models.IntegerField(choices=GenderTypes, default=male)
    birth_date = models.DateTimeField(null=True, blank=True)
    image = models.FileField(upload_to='avatars', null=True, blank=True)
    is_signup = models.BooleanField(default=False)
    country = models.CharField(max_length=50, null=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, related_name='referrers')

    def get_premium_by_referrer_count(self):

        if self.referrers.count() == 3:
            return None

    def get_followers(self):

        return User.objects.filter(username=self.followers.username)

    def get_following(self):
        
        return User.objects.filter(username=self.following.username)


class Follow(models.Model):
    followed = models.ForeignKey(User, related_name="followers")
    follower = models.ForeignKey(User, related_name="following")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.follower.username, self.followed.username)


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

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def get_user_token(cls, user):
        token = user.token_set.last()
        if not token:
            token = Token.objects.create(user=user)
        return token


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






