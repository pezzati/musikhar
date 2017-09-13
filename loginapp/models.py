import os
import binascii

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from musikhar.async_tasks import send_sms, send_email


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
    mobile = models.CharField(max_length=11, null=True, blank=True)
    bio = models.CharField(max_length=120, default='')
    referred_by = models.ForeignKey('self', null=True, blank=True, related_name='referrers')
    is_public = models.BooleanField(default=True)

    def get_premium_by_referrer_count(self):

        if self.referrers.count() == 3:
            return None

    def send_sms_recovery_password(self):
        send_sms(self, msg={'msg': 'some msg'})

    def send_email_recovery_password(self):
        send_email(self, msg={'msg': 'some msg'})

    def get_followers(self):
        return User.objects.filter(id__in=self.followers.values_list('follower'))

    def get_following(self):
        return User.objects.filter(id__in=self.following.values_list('followed'))

    def is_follower(self, user):
        try:
            Follow.objects.get(followed=self, follower=user)
            return True
        except Follow.DoesNotExist:
            return False

    @property
    def poems(self):
        from karaoke.models import Post, Poem, OwnerShip
        return Poem.objects.filter(subclass_type=Post.POEM_TYPE, user=self)

    @property
    def songs(self):
        from karaoke.models import Post, Song, OwnerShip
        return Song.objects.filter(subclass_type=Post.SONG_TYPE, user=self)

    def user_has_access(self, user):
        if self == user:
            return True
        elif self.is_public:
            return True
        elif self.is_follower(user):
            return True
        return False

    def save_base(self, raw=False, force_insert=False,
                  force_update=False, using=None, update_fields=None):
        if not self.id:
            super(User, self).save_base(raw=raw,
                                        force_insert=force_insert,
                                        force_update=force_update,
                                        using=using,
                                        update_fields=update_fields)
            Follow.objects.create(followed=User.system_user(),
                                  follower=self)
            return
        super(User, self).save_base(raw=raw,
                                    force_insert=force_insert,
                                    force_update=force_update,
                                    using=using,
                                    update_fields=update_fields)

    @classmethod
    def system_user(cls):
        try:
            return User.objects.get(username=settings.SYSTEM_USER['username'])
        except User.DoesNotExist:
            system_user = User.objects.create(username=settings.SYSTEM_USER['username'],
                                              email=settings.SYSTEM_USER['email'],
                                              first_name=settings.SYSTEM_USER['first_name'])
            system_user.set_password(raw_password=settings.SYSTEM_USER['password'])
            system_user.save()
            return


class Follow(models.Model):
    followed = models.ForeignKey(User, related_name="followers")
    follower = models.ForeignKey(User, related_name="following")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.follower.username, self.followed.username)


class Artist(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.FileField(upload_to='artist/avatars', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.get_name()

    def get_name(self):
        if self.user and (self.user.first_name or self.user.last_name):
            return '{} {}'.format(self.user.first_name, self.user.last_name)
        return self.name


class Token(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=128, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.user.username

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






