from django.db import models
from django.utils import timezone

from karaoke.models import Post
from loginapp.models import User


class Like(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)


class Favorite(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)