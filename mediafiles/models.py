import mutagen

from django.conf import settings
from django.db import models
from django.utils import timezone

from loginapp.models import User
from musikhar.utils import CONTENT_TYPE_AUDIO, CONTENT_TYPE_IMAGE, err_logger


def get_path(instance, filename):
    filename = filename.lower()

    sub_dir = 'songs'
    if instance.type == 'video':
        sub_dir = 'videos'
    elif instance.type == 'cover':
        sub_dir = 'covers'

    time = timezone.now()
    return 'posts/{}/{}/{}_{}/{}_{}'.format(instance.user.username, sub_dir, time.year, time.month, time.date(), filename)


class MediaFile(models.Model):
    VIDEO_TYPE = 'video'
    SONG_TYPE = 'song'
    POEM_TYPE = 'poem'
    COVER_PHOTO = 'cover'
    TYPE_CHOICES = (
        (SONG_TYPE, 'song file'),
        (POEM_TYPE, 'poem file'),
        (VIDEO_TYPE, 'video file'),
        (COVER_PHOTO, 'cover photo file')
    )

    LOCAL_RESOURCE = 0
    BACKTORY_RESOURCE = 1
    RESOURCE_TYPES_CHOICES = (
        (LOCAL_RESOURCE, 'Local Resource'),
        (BACKTORY_RESOURCE, 'Backtory')
    )

    user = models.ForeignKey(User)
    file = models.FileField(null=True, blank=True, upload_to=get_path)
    path = models.CharField(max_length=150, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SONG_TYPE)
    resource_type = models.IntegerField(choices=RESOURCE_TYPES_CHOICES, default=LOCAL_RESOURCE)

    def __str__(self):
        if self.resource_type == MediaFile.LOCAL_RESOURCE:
            return '{}{}'.format(settings.MEDIA_URL, self.file.name)
        else:
            return self.path

    def get_download_path(self):
        """
        get how to download this file
        :return: two values, Redirect and url.
                 If the file is local Redirect will be False and url doesn't have domain.
                 If the file is not local Redirect will be True and url is complete.
        """
        if self.resource_type == MediaFile.LOCAL_RESOURCE:
            return False, '{}{}'.format('/my_protected_files/', self.file.name)
        else:
            return True, self.path

    def get_content_type(self):
        try:
            if self.type == MediaFile.SONG_TYPE:
                return CONTENT_TYPE_AUDIO
            elif self.type == MediaFile.COVER_PHOTO:
                file_format = self.file.name.split('/')[-1].split('.')[-1].lower()
                return CONTENT_TYPE_IMAGE.get(file_format)
        except Exception as e:
            err_logger.info('[MEDIA_CONTENT_TYPE] {} - {} - {}'.format(timezone.now(),
                                                                       self.id,
                                                                       str(e))
                            )
            return None

    def get_media_seconds(self):
        try:
            element = mutagen.File(self.file.path)
            return element.info.length
        except mutagen.MutagenError:
            return None
        except AttributeError:
            err_logger.info('[FORMAT_ERROR] media_file: {}'.format(self.id))
            return -1


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

