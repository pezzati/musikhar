from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, default='new-genre', null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name




class Karaoke(models.Model):
    name = models.CharField(max_length=100, default="SongsOriginalName")
    file = models.FileField(upload_to='KaraokeFiles',null=True,blank=True)
    rate = models.IntegerField(default=0)
    rate_count = models.IntegerField(default=0)
    cover_photo = models.FileField(upload_to='example', null=True, blank=True)
    created_date = models.DateTimeField(null=True)
    # poem = models.ForeignKey('Artist', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    # composer = models.ForeignKey(Artist, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def lyrics(self):
        return self.line_set.all()

    @classmethod
    def get_popular(cls):
        return cls.objects.all().order_by('-rate')[:10]

    @classmethod
    def get_new(cls):
        return cls.objects.all().order_by('created_date')[:10]


class Line(models.Model):
    karaoke = models.ForeignKey(Karaoke)
    text = models.CharField(max_length=300, default='', help_text='write your text line here')
    start_time = models.IntegerField(default=0, help_text='in milliseconds')
    end_time = models.IntegerField(default=0, help_text='in milliseconds')

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return '{}--{}:{}'.format(self.karaoke.name, self.start_time, self.end_time)


class Post(models.Model):
    name = models.CharField(max_length=60, default='', help_text='Write songs name')
    recorded_file = models.FileField(upload_to='KaraokeFiles')
    like_state = models.BooleanField(default=False)
    karaoke = models.ForeignKey(Karaoke)
    created_date = models.DateTimeField(null=True)
    #visual Effects

    def __str__(self):
        return self.name

