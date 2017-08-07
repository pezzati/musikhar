from django.db import models


class karaoke(models.Model):
    name = models.TextField(default="SongsOriginalName" , null=False ,blank=False)
    file = models.FileField(upload_to='KaraokeFiles', null=False , blank=False)
    rate = models.IntegerField(null= True , blank= True  )
    RateCount = models.IntegerField(null= True , blank= True)
    CoverPhoto = models.FileField(upload_to='example', null=True)
    poem = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,

    )
    gener = models.ManyToManyField(
        Gener, null=True

    )
    composer = models.ForeignKey(
        Artist, null=True ,
        on_delete=models.CASCADE,
    )
    line = models.ManyToManyField (
        Line, null=True
        )



class Line(models.Model):
    text = models.TextField(null=True, blank=True)
    starttime = models.IntegerField(null=True, blank=True)
    endtime = models.IntegerField(null=True, blank=True)
    #times are mili secnonds



class Artist(models.Model):
    name = models.TextField(null=True, blank=True)
    


class Gener(models.Model):
    name =models.CharField(null=True, blank=True)

