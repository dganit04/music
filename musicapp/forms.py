from django import forms
import datetime
from models import Album, Song, Artist
from django.core.exceptions import ValidationError

artists = Artist.objects.all()
albums = Album.objects.all()


class AlbumForm(forms.Form):
    title = forms.CharField(max_length=200, error_messages={'required': 'Please enter Album name'})
    artist = forms.ModelChoiceField(queryset=artists, empty_label=None)
    release_date = forms.DateField(initial=datetime.date.today)
    title.widget.attrs['class'] = 'col-sm-6'
    artist.widget.attrs['class'] = 'col-sm-6'
    release_date.widget.attrs['class'] = 'col-sm-6'

    def clean_title(self):  # avoid duplicate name
        new_title = self.cleaned_data['title'].lower()
        try:
            album = Album.objects.get(title=new_title)
            if album:
                print 'already exist ', new_title
                raise forms.ValidationError(u'%s Album already exists' % new_title)
        except Album.DoesNotExist:
            print 'Good, this is a new album title.'
        return new_title


class SongForm(forms.Form):
    title = forms.CharField(max_length=200, error_messages={'required': 'Please enter Song name'})
    artist = forms.ModelChoiceField(queryset=artists, empty_label=None)
    album = forms.ModelChoiceField(queryset=albums, empty_label=None)
    title.widget.attrs['class'] = 'col-sm-6'
    artist.widget.attrs['class'] = 'col-sm-6'
    album.widget.attrs['class'] = 'col-sm-6'

    def clean_title(self):  # avoid duplicate name
        newTitle = self.cleaned_data['title'].lower()
        print 'clean_title ', newTitle
        try:
            song = Song.objects.get(title=newTitle)
            if song:
                raise forms.ValidationError(u'%s Song already exists' % newTitle)
        except Song.DoesNotExist:
            print 'Song Does not exist'
        return newTitle


class artistForm(forms.Form):
    name = forms.CharField(max_length=200, error_messages={'required': 'Please enter Artist name'})
    name.widget.attrs['class'] = 'col-sm-6'

    def clean_name(self):  # avoid duplicate name
        newName = self.cleaned_data['name'].lower()
        try:
            artist = Artist.objects.get(name=newName)
            if artist:
                raise forms.ValidationError(u'%s Artist already exists' % newName)
        except Artist.DoesNotExist:
            print 'Artist Does not exist'
        print 'YAY! ', newName
        return newName
