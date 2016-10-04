from django.conf.urls import url
from . import views
app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /music/71/
    # 71 is album_id
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    
    # /music/album/add/
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),

    # /music/album/71/
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # /music/album/71/delete
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
    # /music/<album_id>/favorite/
    # url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

]
