# -*- coding: utf-8 -*-

from django.db import models
from loginapp.models import Artist


class OwnerShip(models.Model):
    SYSTEM_OWNER = 'system'
    USER_OWNER = 'user'
    TYPE_CHOICES = (
        (SYSTEM_OWNER, 'System ownership'),
        (USER_OWNER, 'User ownership')
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SYSTEM_OWNER)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey('loginapp.User', null=True, blank=True, related_name='ownerships')

    def user_has_access(self, user):
        if self.type == OwnerShip.SYSTEM_OWNER:
            return self.is_public
        elif user == self.user:
            return True
        elif self.is_public:
            return True


class Genre(models.Model):
    name = models.CharField(max_length=50, default='new-genre', null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Post(OwnerShip):
    KARAOKE_TYPE = 'song'
    POEM_TYPE = 'poem'
    TYPE_CHOICES = (
        (KARAOKE_TYPE, 'karaoke object'),
        (POEM_TYPE, 'poem object')
    )

    name = models.CharField(max_length=60, default='', help_text='Write songs name')
    subclass_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=KARAOKE_TYPE)
    desc = models.CharField(max_length=100, default='')
    cover_photo = models.FileField(upload_to='posts/covers', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return '{}'.format(self.name)

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


class Karaoke(Post):
    file = models.FileField(upload_to='posts/songs', null=True, blank=True)
    poet = models.ForeignKey(Artist, null=True, blank=True)
    related_poem = models.ForeignKey(Poem, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    composer = models.ForeignKey(Artist, null=True, blank=True, related_name='composed')
    singer = models.ForeignKey(Artist, null=True, blank=True, related_name='singed')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.subclass_type = Post.KARAOKE_TYPE
        super(Karaoke, self).save(force_insert=force_insert,
                                  force_update=force_update,
                                  using=using,
                                  update_fields=update_fields)


# class Line(models.Model):
#     karaoke = models.ForeignKey(Karaoke, null=True, blank=True)
#     poem = models.ForeignKey(Poem, null=True, blank=True)
#     text = models.CharField(max_length=300, default='', help_text='write your text line here')
#     start_time = models.IntegerField(default=0, help_text='in milliseconds')
#     end_time = models.IntegerField(default=0, help_text='in milliseconds')
#
#     class Meta:
#         ordering = ['start_time']
#
#     def __str__(self):
#         return '{}--{}:{}'.format(self.karaoke.name, self.start_time, self.end_time)



