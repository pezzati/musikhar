from django.db import models
from django.utils import timezone

from karaoke.models import Post
from loginapp.models import User


class Like(models.Model):

    user = models.ForeignKey(User, related_name='user_liked')
    post = models.ForeignKey(Post, null=True, blank=True, related_name='post_liked')
    time = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)


class Favorite(models.Model):

    user = models.ForeignKey(User, related_name='user_favored')
    post = models.ForeignKey(Post, null=True, blank=True, related_name='post_favored')
    time = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)
