# -*- coding: utf-8 -*-

import json
from django.utils import timezone
from django.db import models
from loginapp.models import Artist, User
# from django.contrib.postgres.fields import JSONField

from musikhar.middlewares import error_logger
from musikhar.utils import mid_lyric_to_json


class PostOwnerShip(models.Model):
    SYSTEM_OWNER = 'system'
    USER_OWNER = 'user'
    TYPE_CHOICES = (
        (SYSTEM_OWNER, 'System ownership'),
        (USER_OWNER, 'User ownership')
    )

    ownership_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SYSTEM_OWNER)
    user = models.ForeignKey('loginapp.User', null=True, blank=True, related_name='ownerships')
    is_premium = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.ownership_type == PostOwnerShip.SYSTEM_OWNER:
            self.user = User.system_user()

        super(PostOwnerShip, self).save(force_insert=force_insert,
                                        force_update=force_update,
                                        using=using,
                                        update_fields=update_fields)

    def user_has_access(self, user):
        if self.ownership_type == PostOwnerShip.SYSTEM_OWNER:
            if self.is_premium:
                return user.is_premium
            else:
                return True
        else:
            return self.user.user_has_access(user)


class Genre(models.Model):
    name = models.CharField(max_length=50, default='new-genre', null=True, blank=True)
    cover_photo = models.FileField(upload_to='genre_covers', null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='children')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


def get_song_file_path(instance, filename):
    filename = filename.lower()
    return 'posts/{}/songs/{}_{}'.format(instance.user.username, timezone.now().date(), filename)


class Post(PostOwnerShip):
    SONG_TYPE = 'song'
    POEM_TYPE = 'poem'
    KARAOKE_TYPE = 'karaoke'
    TYPE_CHOICES = (
        (SONG_TYPE, 'song object'),
        (POEM_TYPE, 'poem object'),
        (KARAOKE_TYPE, 'Karaoke object')
    )

    name = models.CharField(max_length=60, default='', help_text='Write songs name')
    subclass_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SONG_TYPE)
    description = models.CharField(max_length=100, null=True, blank=True)
    cover_photo = models.ForeignKey('mediafiles.MediaFile', null=True, blank=True, related_name='as_cover')
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('analytics.Tag', through='analytics.TagPost')
    genre = models.ForeignKey(Genre, null=True, blank=True)
    likes = models.ManyToManyField(to=User, through='analytics.Like', related_name='liked_posts')
    rate = models.IntegerField(default=0)
    favorites = models.ManyToManyField(to=User, through='analytics.Favorite', related_name='favorite_posts')
    popularity = models.IntegerField(default=0)
    popularity_rate = models.FloatField(default=0)

    last_time_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return '{}'.format(self.name)

    def add_tags(self, tags=[]):
        if not tags:
            return
        from analytics.models import TagPost
        for tag in tags:
            TagPost.objects.create(tag=tag, post=self)

    def get_file(self, target=''):
        if self.subclass_type == Post.SONG_TYPE:
            return self.song.file
        elif self.subclass_type == Post.KARAOKE_TYPE:
            if target == 'full':
                return self.karaoke.full_file
            else:
                return self.karaoke.file

    def get_cover(self):
        if self.cover_photo:
            return self.cover_photo
        if self.subclass_type == Post.KARAOKE_TYPE:
            return self.karaoke.artist.image_obj if self.karaoke.artist.image_obj else None
        return None

    @classmethod
    def get_popular(cls, count=0, type=''):
        if type:
            if count:
                return cls.objects.filter(subclass_type=type).order_by('-popularity_rate')[:count]
            else:
                return cls.objects.filter(subclass_type=type).order_by('-popularity_rate')
        else:
            if count:
                return cls.objects.all().order_by('-popularity_rate')[:count]
            else:
                return cls.objects.all().order_by('-popularity_rate')

    @classmethod
    def get_new(cls, count=0, type=''):
        if type:
            if count:
                return cls.objects.filter(subclass_type=type).order_by('-created_date')[:count]
            else:
                return cls.objects.filter(subclass_type=type).order_by('-created_date')
        else:
            if count:
                return cls.objects.all().order_by('-created_date')[:count]
            else:
                return cls.objects.all().order_by('-created_date')

    @classmethod
    def get_free(cls, count=0, type=''):
        if type:
            if count:
                return cls.objects.filter(subclass_type=type, is_premium=False)[:count]
            else:
                return cls.objects.filter(subclass_type=type, is_premium=False)
        else:
            if count:
                return cls.objects.filter(is_premium=False)[:count]
            else:
                return cls.objects.filter(is_premium=False)


class Poem(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000, default='')
    poet = models.ForeignKey(Artist, null=True, blank=True)

    def __str__(self):
        return self.post.name


def get_mid_file_path(instance, filename):
    filename = filename.lower().encode('utf-8')

    time = timezone.now()

    return 'posts/mids/{}_{}/{}_{}'.format(time.year, time.month, instance.id, filename)


class Karaoke(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    file = models.ForeignKey('mediafiles.MediaFile', null=True, blank=True, related_name='as_karaoke')
    full_file = models.ForeignKey('mediafiles.MediaFile', null=True, blank=True, related_name='as_full_karaoke')
    duration = models.FloatField(null=True, blank=True)
    artist = models.ForeignKey(Artist, null=True, blank=True)
    lyric = models.ForeignKey(Poem, null=True, blank=True)
    mid = models.CharField(null=True, blank=True, max_length=100000)
    mid_file = models.FileField(upload_to=get_mid_file_path, null=True, blank=True)

    def __str__(self):
        return self.post.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # print('karaoke save!!!!!!')
        if not self.duration and self.file:
            self.duration = self.file.get_media_seconds()
        super(Karaoke, self).save(force_insert=force_insert,
                                  force_update=force_update,
                                  using=using,
                                  update_fields=update_fields)
        if self.mid_file and not self.mid:
            try:
                res = mid_lyric_to_json(self.mid_file.path)
                self.mid = json.dumps(res)
                try:
                    self.duration = res[-1]['time'] + res[-1]['duration']
                except Exception as e:
                    error_logger.info('[MID_FILE_ERROR] time: {}, error: {}'.format(timezone.now(), str(e)))
            except Exception as e:
                self.mid = {'error': str(e)}

            self.save()
        # print('SAVEDD')


class Song(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    karaoke = models.ForeignKey(Karaoke)
    file = models.OneToOneField('mediafiles.MediaFile', related_name='as_song')
    duration = models.FloatField(null=True, blank=True)
    # poet = models.ForeignKey(Artist, null=True, blank=True, related_name='song_poems')
    # related_poem = models.ForeignKey(Poem, null=True, blank=True)
    # composer = models.ForeignKey(Artist, null=True, blank=True, related_name='composed')
    # singer = models.ForeignKey(Artist, null=True, blank=True, related_name='singed')

    def __str__(self):
        return self.post.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.duration and self.file:
            self.duration = self.file.get_media_seconds()
        super(Song, self).save(force_insert=force_insert,
                               force_update=force_update,
                               using=using,
                               update_fields=update_fields)

    # def delete(self, using=None, keep_parents=False):
    #     if self.file:
    #         os.remove(self.file.path)
    #     super(Song, self).delete(using=using, keep_parents=keep_parents)
