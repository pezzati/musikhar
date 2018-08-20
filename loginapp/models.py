import os
import uuid

import binascii

from datetime import timedelta, datetime

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from musikhar.async_tasks import send_sms, send_email
from musikhar.utils import send_sms_template, conn, app_logger, send_zoho_email


def get_avatar_path(instance, filename):
    filename = filename.lower()

    return 'avatars/{}/{}'.format(instance.username, filename)


class User(AbstractUser):
    male = 0
    female = 1
    GenderTypes = (
        (male, 'Male'),
        (female, 'Female')
    )
    gender = models.IntegerField(choices=GenderTypes, default=male)
    birth_date = models.DateTimeField(null=True, blank=True)
    image = models.FileField(upload_to=get_avatar_path, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    mobile = models.CharField(max_length=11, null=True, blank=True)
    mobile_confirmed = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    bio = models.CharField(max_length=120, blank=True, null=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, related_name='referrers')
    is_public = models.BooleanField(default=True)

    point = models.IntegerField(default=0)
    premium_time = models.DateField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)

    genres = models.ManyToManyField('karaoke.Genre', blank=True)

    @property
    def name(self):
        if self.first_name or self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.username

    def get_premium_by_referrer_count(self):

        if self.referrers.count() == 3:
            return None

    def send_sms_recovery_password(self):
        send_sms(self, msg={'msg': 'some msg'})

    def send_mobile_verification(self, code=None):
        # app_logger.info('SEND_SMS_PHONE: {}'.format(self.mobile))
        if conn().exists(name='sms#{}'.format(self.mobile)):
            return
        if not code:
            self.verification_set.filter(type=Verification.SMS_CODE).delete()
            code = Verification.objects.create(user=self)
        # app_logger.info('SEND_SMS: {}'.format(code.code))
        conn().set(name='sms#{}'.format(self.mobile), value=code.code, ex=60)
        send_sms_template.delay(receiver=self.mobile, tokens=[code.code])

    def send_email_recovery_password(self):
        send_email(self, msg={'msg': 'some msg'})

    def send_email_verification(self, code=None):
        # app_logger.info('SEND_EMAIL_PHONE: {}'.format(self.mobile))
        if conn().exists(name='email#{}'.format(self.email)):
            return
        if not code:
            self.verification_set.filter(type=Verification.EMAIL_CODE).delete()
            code = Verification.objects.create(user=self, type=Verification.EMAIL_CODE)
        conn().set(name='email#{}'.format(self.email), value=code.code, ex=60)
        send_zoho_email.delay(dst_addr=self.email, subject=u'ورود به کانتو',
                              content=u'کاربر گرامی کد شما برای ورود به کانتو {} می‌باشد. \n با تشکر گروه کانتو'.format(code.code))

    def get_followers(self):
        return User.objects.filter(id__in=self.followers.values_list('follower'))

    def get_following(self):
        return User.objects.filter(id__in=self.following.values_list('followed'))

    def is_follower(self, user):
        if user == self:
            return True
        try:
            Follow.objects.get(followed=self, follower=user)
            return True
        except:
            return False

    @property
    def poems(self):
        from karaoke.models import Post, Poem, PostOwnerShip
        return Poem.objects.filter(subclass_type=Post.POEM_TYPE, user=self)

    @property
    def songs(self):
        from karaoke.models import Post, Song, PostOwnerShip
        return Song.objects.filter(subclass_type=Post.SONG_TYPE, user=self)

    def user_has_access(self, user):
        if self == user:
            return True
        elif self.is_public:
            return True
        elif self.is_follower(user):
            return True
        return False

    # def save_base(self, raw=False, force_insert=False,
    #               force_update=False, using=None, update_fields=None):
    #     if not self.id and not self.is_superuser and self.username != settings.SYSTEM_USER['username']:
    #         super(User, self).save_base(raw=raw,
    #                                     force_insert=force_insert,
    #                                     force_update=force_update,
    #                                     using=using,
    #                                     update_fields=update_fields)
    #         Follow.objects.create(followed=User.system_user(),
    #                               follower=self)
    #         return
    #     super(User, self).save_base(raw=raw,
    #                                 force_insert=force_insert,
    #                                 force_update=force_update,
    #                                 using=using,
    #                                 update_fields=update_fields)

    @classmethod
    def get_user(cls, username='', email='', mobile=''):
        query = Q()
        if username:
            query = Q(username=username)
        if mobile:
            query = query | Q(mobile=mobile)
        if email:
            query = query | Q(email=email)

        if not query:
            return None

        try:
            return User.objects.get(query)
        except User.DoesNotExist:
            return None

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


class Verification(models.Model):
    SMS_CODE = 'sms'
    EMAIL_CODE = 'email'
    TYPE_CHOICES = (
        (SMS_CODE, 'sms code'),
        (EMAIL_CODE, 'email code')
    )
    code = models.CharField(max_length=6, db_index=True)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SMS_CODE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('code', 'user')

    def __str__(self):
        return '<{}, {}>'.format(self.user.username, self.code)

    def generate_token(self, length=4):
        return str(uuid.uuid4().int)[:length]
        # if self.type == Verification.SMS_CODE:
        #     return '1111'
        # else:
        #     return '111111'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.code = self.generate_token()
        super(Verification, self).save(force_insert=force_insert,
                                       force_update=force_update,
                                       using=using,
                                       update_fields=update_fields)


class Follow(models.Model):
    followed = models.ForeignKey(User, related_name="followers")
    follower = models.ForeignKey(User, related_name="following")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.follower.username, self.followed.username)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Follow, self).save(force_insert=force_insert,
                                 force_update=force_update,
                                 using=using,
                                 update_fields=update_fields)
        from analytics.models import Event
        Event.add_follow_event(followed=self.followed, follower=self.follower)


class Artist(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.FileField(upload_to='artist/avatars', null=True, blank=True)
    image_obj = models.ForeignKey('mediafiles.MediaFile', null=True, blank=True)

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
    key = models.CharField(max_length=128, primary_key=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_token_code()

        return super(Token, self).save(*args, **kwargs)

    def is_valid(self):
        if (self.created + timedelta(days=90)) > timezone.now():
            return True

        return False

    @staticmethod
    def generate_token_code():
        return binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def get_user_token(cls, user):
        token = user.token_set.last()
        if not token:
            token = Token.objects.create(user=user)
        return token

    @classmethod
    def generate_token(cls, user):
        cls.objects.filter(user=user).delete()
        return cls.objects.create(user=user)


class Device(models.Model):
    ios = 'ios'
    android = 'android'
    TypeChoices = (
        (ios, 'iOS'),
        (android, 'Android')
    )

    udid = models.CharField(max_length=200, default='not-set')
    user = models.ForeignKey(User, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TypeChoices, default=android)
    os_version = models.IntegerField(default=0)
    one_signal_id = models.CharField(max_length=50, null=True, blank=True)
    build_version = models.IntegerField(default=0)
    last_update_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.type)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.last_update_date = datetime.now()
        super(Device, self).save(force_insert=force_insert, force_update=force_update, update_fields=update_fields,
                                 using=using)
