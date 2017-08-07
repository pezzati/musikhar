from django.db import models


class Karaoke(models.Model):
    name = models.CharField(max_length=100, default="SongsOriginalName")
    file = models.FileField(upload_to='KaraokeFiles')
    rate = models.IntegerField(default=0)
    rate_count = models.IntegerField(default=0)
    cover_photo = models.FileField(upload_to='example', null=True, blank=True)
    # poem = models.ForeignKey('Artist', on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    # composer = models.ForeignKey(Artist, null=True, on_delete=models.CASCADE)


class Line(models.Model):
    karaoke = models.ForeignKey(Karaoke)
    text = models.CharField(max_length=300, default='', help_text='write your text line here')
    start_time = models.IntegerField(default=0, help_text='in milliseconds')
    end_time = models.IntegerField(default=0, help_text='in milliseconds')


class Genre(models.Model):
    name = models.CharField(max_length=50, default='new-genre')

