from django.db import models
from django.utils import timezone

from karaoke.models import Karaoke
from loginapp.models import User


class Like(models.Model):
    KARAOKE_LIKE = 'karaoke'
    TYPE_CHOICES = (
        (KARAOKE_LIKE, 'Karaoke')
    )

    user = models.ForeignKey(User)
    karaoke = models.ForeignKey(Karaoke, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=KARAOKE_LIKE)

    def __str__(self):
        if self.type == Like.KARAOKE_LIKE:
            return '{}-{}:{}'.format(self.user.username, self.type, self.karaoke)
