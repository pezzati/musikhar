from django.db import models
from django.utils import timezone

from loginapp.models import User


def get_path(instance, filename):
    filename = filename.lower()

    sub_dir = 'songs'
    if instance.type == 'video':
        sub_dir = 'videos'

    return 'posts/{}/{}/{}_{}'.format(instance.user.username, sub_dir, timezone.now(), filename)


class MediaFile(models.Model):
    VIDEO_TYPE = 'video'
    SONG_TYPE = 'song'
    POEM_TYPE = 'poem'
    COVER_PHOTO = 'cover'
    TYPE_CHOICES = (
        (SONG_TYPE, 'karaoke file'),
        (POEM_TYPE, 'poem file'),
        (VIDEO_TYPE, 'video file'),
        (COVER_PHOTO, 'cover photo file')
    )
    user = models.ForeignKey(User)
    file = models.FileField(null=True, blank=True, upload_to=get_path)
    created_date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SONG_TYPE)

    def __str__(self):
        return '{} - {} - {}'.format(self.user.username, self.type, self.file)

    @classmethod
    def type_is_valid(cls, type=''):
        if type:
            if type in [
                cls.VIDEO_TYPE,
                cls.SONG_TYPE,
                cls.POEM_TYPE,
                cls.COVER_PHOTO
            ]:
                return True
        return False

