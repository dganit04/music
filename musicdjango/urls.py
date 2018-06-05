from django.conf.urls import include, url
from django.contrib import admin
from musicapp.api import v1_api
from musicapp import views
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^songs', views.songs, name='songs'),
    url(r'^artists', views.artists, name='artists'),
    url(r'^album/(?P<id>\d+)/', views.album_detail, name='album_detail'),
    url(r'^artist/(?P<id>\d+)/', views.artist_detail, name='artist_detail'),
    url(r'^delete/(?P<id>\d+)/', views.item_delete, name='item_delete'),
    url(r'^reset/', views.reset, name='reset'),
    url(r'^album-create', views.album_create, name='album_create'),
    url(r'^ajax/load_albums', views.load_albums, name='ajax_load_albums'),
    url(r'^album-create', views.album_create, name='album_create'),
    url(r'^song-create', views.song_create, name='song_create'),
    url(r'^artist-create', views.artist_create, name='artist_create'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

