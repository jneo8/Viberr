from django.conf.urls import url
from . import views
app_name = 'superlist'

urlpatterns = [
    # /music/
    url(r'^$', views.home_page, name='home'),

    # add new list
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(.+)/$', views.view_list, name='view_list'),   
]
