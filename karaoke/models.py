from django.db import models
from loginapp.models import Artist


class Genre(models.Model):
    name = models.CharField(max_length=50, default='new-genre', null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Karaoke(models.Model):
    name = models.CharField(max_length=100, default="SongsOriginalName")
    file = models.FileField(upload_to='KaraokeFiles', null=True, blank=True)
    rate = models.IntegerField(default=0)
    rate_count = models.IntegerField(default=0)
    cover_photo = models.FileField(upload_to='example', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    poem = models.ForeignKey(Artist, null=True, blank=True, related_name='poetried')
    genre = models.ForeignKey(Genre, null=True, blank=True)
    composer = models.ForeignKey(Artist, null=True, blank=True, related_name='composed')
    singer = models.ForeignKey(Artist, null=True, blank=True, related_name='singed')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_date']

    @property
    def lyrics(self):
        return self.line_set.all()

    @classmethod
    def get_popular(cls):
        return cls.objects.all().order_by('-rate')

    @classmethod
    def get_new(cls):
        return cls.objects.all().order_by('created_date')


class Line(models.Model):
    karaoke = models.ForeignKey(Karaoke)
    text = models.CharField(max_length=300, default='', help_text='write your text line here')
    start_time = models.IntegerField(default=0, help_text='in milliseconds')
    end_time = models.IntegerField(default=0, help_text='in milliseconds')

    class Meta:
        ordering = ['start_time']

    def show_karaoke(self):
        return self.karaoke.name

    def __str__(self):
        return '{}--{}:{}'.format(self.karaoke.name, self.start_time, self.end_time)


class Post(models.Model):
    user = models.ForeignKey('loginapp.User', related_name='posts')
    name = models.CharField(max_length=60, default='', help_text='Write songs name')
    recorded_file = models.FileField(upload_to='KaraokeFiles')
    like_state = models.BooleanField(default=False)
    karaoke = models.ForeignKey(Karaoke)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.karaoke.name, self.user.username)

