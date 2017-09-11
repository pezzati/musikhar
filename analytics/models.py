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

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)
