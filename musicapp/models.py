from django.db import models
from managers import AlbumManager, SongManager


class Artist(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Album(models.Model):
    title = models.CharField(max_length=80, unique=True)
    artist = models.ForeignKey(Artist)
    release_date = models.DateField()
    objects = AlbumManager()

    def __unicode__(self):
        return u'%s' % self.title  # that's what you'll see in shell commands, only titles.

    def year(self):
        return self.release_date.year


class Song(models.Model):
    title = models.CharField(max_length=80, unique=True)
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album, null=True, blank=True)  # many-to-one relationship, many songs in one album
    objects = SongManager()

    def __unicode__(self):
        return u'%s - %s - %s' % (self.artist, self.title, self.album)
        # self.artist is not unicode, it is an obj because the filed is ForeignKey,
        # it should be unicode, definitely after putting the next sentence, but it doesn't,
        # so I refer to it as self.artist.name in songs.html
        # return u'%s - %s - %s' % (self.artist.name, self.title, self.album.title)
