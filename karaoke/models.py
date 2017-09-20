# -*- coding: utf-8 -*-
import os

from django.utils import timezone
from django.db import models

from loginapp.models import Artist, User


class OwnerShip(models.Model):
    SYSTEM_OWNER = 'system'
    USER_OWNER = 'user'
    TYPE_CHOICES = (
        (SYSTEM_OWNER, 'System ownership'),
        (USER_OWNER, 'User ownership')
    )

    ownership_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SYSTEM_OWNER)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey('loginapp.User', null=True, blank=True, related_name='ownerships')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.ownership_type == OwnerShip.SYSTEM_OWNER:
            self.user = User.system_user()

        super(OwnerShip, self).save(force_insert=force_insert,
                                    force_update=force_update,
                                    using=using,
                                    update_fields=update_fields)

    def user_has_access(self, user):
        if self.ownership_type == OwnerShip.SYSTEM_OWNER:
            return self.is_public
        else:
            return self.user.user_has_access(user)


class Genre(models.Model):
    name = models.CharField(max_length=50, default='new-genre', null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Post(OwnerShip):
    SONG_TYPE = 'song'
    POEM_TYPE = 'poem'
    TYPE_CHOICES = (
        (SONG_TYPE, 'song object'),
        (POEM_TYPE, 'poem object')
    )

    name = models.CharField(max_length=60, default='', help_text='Write songs name')
    subclass_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SONG_TYPE)
    description = models.CharField(max_length=100, null=True, blank=True)
    cover_photo = models.OneToOneField('mediafiles.MediaFile', null=True, blank=True, related_name='as_cover')
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('analytics.Tag', through='analytics.TagPost')

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return '{}'.format(self.name)

    def add_tags(self, tags=[]):
        from analytics.models import TagPost
        for tag in tags:
            TagPost.objects.create(tag=tag, post=self)

    @classmethod
    def get_popular(cls):
        return cls.objects.all().order_by('-rate')

    @classmethod
    def get_new(cls):
        return cls.objects.all()


class Poem(Post):
    text = models.CharField(max_length=1500, default='')
    poet = models.ForeignKey(Artist, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.subclass_type = Post.POEM_TYPE
        super(Poem, self).save(force_insert=force_insert,
                               force_update=force_update,
                               using=using,
                               update_fields=update_fields)


def get_song_file_path(instance, filename):
    filename = filename.lower()
    return 'posts/{}/songs/{}_{}'.format(instance.user.username, timezone.now().date(), filename)


class Song(Post):
    file = models.OneToOneField('mediafiles.MediaFile', null=True, blank=True, related_name='as_song')
    poet = models.ForeignKey(Artist, null=True, blank=True, related_name='song_poems')
    related_poem = models.ForeignKey(Poem, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    composer = models.ForeignKey(Artist, null=True, blank=True, related_name='composed')
    singer = models.ForeignKey(Artist, null=True, blank=True, related_name='singed')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.subclass_type = Post.SONG_TYPE
        super(Song, self).save(force_insert=force_insert,
                               force_update=force_update,
                               using=using,
                               update_fields=update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.file:
            os.remove(self.file.path)
        super(Song, self).delete(using=using, keep_parents=keep_parents)
