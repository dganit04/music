from django.shortcuts import render, redirect, render_to_response
from django.http import Http404, HttpResponse
from models import Album, Song, Artist
from django.core.urlresolvers import reverse
from django import forms
from forms import AlbumForm, SongForm, artistForm
from django.core import serializers


def index(request):
    sorting = request.GET.get('id', 'title')  # get sorting passed by url param or 'title' as a default
    year = request.GET.get('year')  # get filter year passed by url param
    print 'home '
    albums = Album.objects.all().order_by(sorting)
    if request.GET:  # if form method is 'get' - for sorting by year select
        print 'submit ', year, type(year)
        if year:
            int_year = int(year)  # making sure unicode type is an integer
            print 'int_year ', int_year, type(int_year)
            albums = Album.objects.filter(release_date__year__range=(str(int_year), str(int_year + 9)))
    print 'albums ', albums
    return render(request, 'mymusic/index.html', {  # show this view when getting to this page
        'albums': albums
    })


def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        print 'submit album'

        if form.is_valid():  # coming from save button click
            q = Album()
            for each in form:
                if type(each.field) is forms.ModelChoiceField:  # get the value from 'select' (artist)
                    # value_needed = form.cleaned_data[each.name].pk ---> this is the option number
                    value_needed = form.cleaned_data[each.name]
                    a = Artist.objects.get(name=value_needed)  # a is Artist instance
                    setattr(q, each.name, a)
                else:  # get the value from title or date
                    value_needed = form.cleaned_data[each.name]
                    setattr(q, each.name, value_needed)
            q.save()
            return redirect('index')  # you won't see 'form' in url
    else:  # if a GET (or any other method, or when getting to this page at first - we'll create a blank form
        form = AlbumForm()
        print 'Initial album_create page '
    return render(request, 'mymusic/album_create.html', {
        'form': form  # render create album with empty form or with the form we already started to fill
    })


def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        unit_id = request.POST.get('album')
        print 'unit_id ', unit_id
        if form.is_valid():  # coming from save button click, after running clean_title()
            q = Song()
            ar = ''
            for each in form:
                if type(each.field) is forms.ModelChoiceField:  # get the value from 'select'
                    value_needed = form.cleaned_data[each.name]
                    if each.name == 'artist':
                        ar = Artist.objects.get(name=value_needed)  # Artist instance from select
                        setattr(q, each.name, ar)
                    else:
                        alb = ar.album_set.all()  # all albums for this artist
                        title = alb[int(unit_id) - 1]
                        al = Album.objects.get(title=title)  # album instance from select
                        setattr(q, each.name, al)
                else:
                    value_needed = form.cleaned_data[each.name]  # other fields - title field
                    setattr(q, each.name, value_needed)
            q.save()
            print 'valid '
            return redirect('songs')  # you won't see 'form' in url
    else:  # when getting to page at first - Stay, or with 'GET' method
        form = SongForm()  # empty form
        print 'Initial song_create page '
    return render(request, 'mymusic/song_create.html', {
        'form': form  # show empty form in initial state or filled form in case the user started to type and submitted
    })


def load_albums(request):
    # load albums based on Artist name, getting here via jquery ajax
    a_id = request.GET.get('id')  # get artist id via url
    ar = Artist.objects.get(name=a_id)  # retrieve artist based on id
    albums = ar.album_set.all()  # retrive all albums for this artist (relational fileds)
    json_data = serializers.serialize('json', albums)  # translating Django models into other formats (json)
    # don't go to another page, just return ajax call in jquery via ajax
    return HttpResponse(json_data, content_type='application/json')


def artist_create(request):
    if request.method == 'POST':
        form = artistForm(request.POST)
        if form.is_valid():  # coming from save button click
            for each in form:
                value_needed = form.cleaned_data[each.name]
                Artist.objects.create(name=value_needed)  # create() saves it too
            return redirect('artists')  # you won't see 'form' in url
    else:  # if a GET (or any other method) we'll create a blank form
        form = artistForm()
        print 'init'
    return render(request, 'mymusic/artist_create.html', {
        'form': form  # render create artist with empty form or with the form we already started to fill
    })


def prepare_for_album(song_id):
    try:
        song = Song.objects.get(id=song_id)
        album = Album.objects.get(title=song.album)
        songs = album.song_set.all()
    except Song.DoesNotExist:
        raise Http404('This song does not exist, stop trying!')
    return {
        'album': album,
        'songs': songs
    }


def album_detail(request, id):
    print 'details'
    a_type = request.GET.get('type')
    if a_type == 'Song':  # coming from songs page
        obj = prepare_for_album(id)  # this is song id, get album/songs from another function
        obj['album'].className = 'album-pic-' + str(obj['album'].id) + ' pic'
        print 'detail ', obj['album'].className
        album = obj['album']
        songs = obj['songs']
        album.className = 'album-pic-' + str(album.id) + ' pic'
    else:  # coming from album page (index)
        try:
            album = Album.objects.get(id=id)
            songs = album.song_set.all()
            album.className = 'album-pic-' + str(album.id) + ' pic'
            print 'detail ', album.className
        except Album.DoesNotExist:
            raise Http404('This album does not exist, stop trying!')
    return render(request, 'mymusic/album_detail.html', {
        'album': album,
        'songs': songs
    })


def prepare_for_artist(my_type, id):
    if my_type == 'Song':
        song = Song.objects.get(id=id)
        artist = Artist.objects.get(name=song.artist)
    elif my_type == 'Album':
        album = Album.objects.get(id=id)
        artist = Artist.objects.get(name=album.artist)
    else:
        artist = Artist.objects.get(id=id)
    artist.songCount = len(artist.song_set.all())
    print 'prep-f-ar ', artist, artist.songCount, artist.songCount
    return artist

def artist_detail(request, id):
    my_type = request.GET.get('type')
    try:
        artist = prepare_for_artist(my_type, id)
        albums = artist.album_set.all()  # get all albums for this artist - related fields
        for a in albums:
            a.songs = a.song_set.all()
            # if len(a.songs) == 0:
            #     a.songs = [Song(title='---', artist=artist, album=a)]
            print 'each album ', a, 'songs ', a.songs, len(a.songs)
    except Artist.DoesNotExist:
        raise Http404('This artist does not exist, stop trying!')
    return render(request, 'mymusic/artist_detail.html', {  # gets here at first
        'albums': albums,
        'artist': artist
    })


def songs(request):
    order_by = sorting = request.GET.get('order_by', 'title')  # getting passing arg order_by || default field ('title')
    if sorting == 'artist':
        order_by = 'artist__name'  # order_by related filed
    elif sorting == 'album':
        order_by = 'album__title'
    songs = Song.objects.all().order_by(order_by)
    print 'songs ', order_by
    return render_to_response('mymusic/songs.html', {
        'songs': songs
    })


def artists(request):
    # print 'artists '
    artists = Artist.objects.all().order_by('name')
    return render(request, 'mymusic/artists.html', {
        'artists': artists
    })


def item_delete(request, id):
    my_type = request.GET.get('type')
    url = str(request.GET.get('url'))
    # url = 'mymusic/' + str(request.GET.get('url') + '.html')
    try:
        if my_type == 'Album':
            obj = Album
        elif my_type == 'Song':
            obj = Song
        else:
            obj = Artist
        item = obj.objects.get(id=id)
        item.delete()
    except Album.DoesNotExist:
        raise Http404('This item does not exist, stop trying!')
    return redirect(reverse(url))  # going to 'songs' based on its name (in this case same 'songs')
    # return redirect(url)


def reset(request):  # load initial Music
    print 'Reset'
    # Creating Artists, this is Artist instances
    Artist.objects.all().delete()  # delete whatever we have currently in database
    artist1 = Artist.objects.get_or_create(name='taylor swift')[0]
    artist2 = Artist.objects.get_or_create(name='beyonce')[0]
    artist3 = Artist.objects.get_or_create(name='justin bieber')[0]
    artist4 = Artist.objects.get_or_create(name='rihanna')[0]
    artist5 = Artist.objects.get_or_create(name='lady gaga')[0]
    artist6 = Artist.objects.get_or_create(name='elvis presley')[0]
    artist7 = Artist.objects.get_or_create(name='adele')[0]
    artist8 = Artist.objects.get_or_create(name='elton john')[0]
    artist9 = Artist.objects.get_or_create(name='shakirah')[0]
    artist10 = Artist.objects.get_or_create(name='bob dylan')[0]

    # Creating Albums
    Album.objects.all().delete()  # delete whatever we have currently in database
    album_dict = [
        {'title': 'sicks & stones', 'artist': artist1, 'release_date': '1967-05-14'},
        {'title': 'havana', 'artist': artist2, 'release_date': '1960-04-15'},
        {'title': 'believe', 'artist': artist3, 'release_date': '1963-04-16'},
        {'title': 'gladiators', 'artist': artist4, 'release_date': '2018-04-16'},
        {'title': '60s top hits', 'artist': artist5, 'release_date': '1961-04-16'},
        {'title': '70s top hits', 'artist': artist6, 'release_date': '1972-04-16'},
        {'title': '80s top hits', 'artist': artist7, 'release_date': '1980-04-16'},
        {'title': 'best of elton john', 'artist': artist8, 'release_date': '1973-04-16'},
        {'title': 'american pie', 'artist': artist9, 'release_date': '1979-04-16'},
        {'title': 'i will survive', 'artist': artist10, 'release_date': '1982-04-16'},
    ]
    for k in album_dict:
        # query = Album(title=k.get('title'), artist=k.get('artist'), release_date=k.get('release_date'))
        query = Album(title=k['title'], artist=k['artist'], release_date=k['release_date'])
        query.save()

    # Creating Songs, using Artist instance, Album instance
    Song.objects.all().delete()  # delete whatever we have currently in database
    song_dict = [
        {'title': 'woman in love', 'artist': artist1, 'album': Album.objects.get_or_create(title='sicks & stones')[0]},
        {'title': 'thriller', 'artist': artist2, 'album': Album.objects.get_or_create(title='havana')[0]},
        {'title': 'like a prayer', 'artist': artist3, 'album': Album.objects.get_or_create(title='believe')[0]},
        {'title': 'hotel california', 'artist': artist4, 'album': Album.objects.get_or_create(title='gladiators')[0]},
        {'title': 'somebody to love', 'artist': artist5, 'album': Album.objects.get_or_create(title='60s top hits')[0]},
        {'title': 'the joker', 'artist': artist6, 'album': Album.objects.get_or_create(title='70s top hits')[0]},
        {'title': 'cant get enough', 'artist': artist7, 'album': Album.objects.get_or_create(title='80s top hits')[0]},
        {'title': 'slow ride', 'artist': artist8, 'album': Album.objects.get_or_create(title='best of elton john')[0]},
        {'title': 'fast boat', 'artist': artist8, 'album': Album.objects.get_or_create(title='best of elton john')[0]},
        {'title': 'you and i', 'artist': artist9, 'album': Album.objects.get_or_create(title='american pie')[0]},
        {'title': 'a lonely man', 'artist': artist10, 'album': Album.objects.get_or_create(title='i will survive')[0]},
        {'title': 'a great trip', 'artist': artist10, 'album': Album.objects.get_or_create(title='i will survive')[0]},
    ]
    for k in song_dict:
        query = Song(title=k['title'], artist=k['artist'], album=k['album'])
        query.save()
    return redirect('index')
