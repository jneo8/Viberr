from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    # FK to Album，
    album = models.ForeignKey(Album, on_delete=models.CASCADE,)
    song_title = models.CharField(max_length=250, default=None)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

    def set_favorite(self):
        if (self.is_favorite is True):
            self.is_favorite = False
        else:
            self.is_favorite = True
        self.save()
        return None
