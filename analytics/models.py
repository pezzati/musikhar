from django.db import models
from django.utils import timezone

from karaoke.models import Post
from loginapp.models import User


class Like(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        ordering = ['time']

    def __str__(self):
        Like.objects.get()
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)

    @classmethod
    def user_liked_post(cls, user, post):
        try:
            cls.objects.get(user=user, post=post)
            return True
        except cls.DoesNotExist:
            return False


class Favorite(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)

    @classmethod
    def user_favorite_post(cls, user, post):
        try:
            cls.objects.get(user=user, post=post)
            return True
        except cls.DoesNotExist:
            return False


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.replace(' ', '_')
        if self.name[0] != '#':
            self.name = '#{}'.format(self.name)
        super(Tag, self).save(force_insert=force_insert,
                              force_update=force_update,
                              using=using,
                              update_fields=update_fields)


class TagPost(models.Model):
    tag = models.ForeignKey(Tag)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.tag.name, self.post.name)


class UserFileHistory(models.Model):
    requested_user = models.ForeignKey(User, related_name='requested_files_history', null=True, blank=True)
    owner_user = models.ForeignKey(User, null=True, blank=True, related_name='is_requested_files_history')
    file_path = models.CharField(max_length=150, default='')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.requested_user.username, self.date, self.file.name)
