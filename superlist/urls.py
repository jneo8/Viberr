from django.conf.urls import url
from . import views
app_name = 'superlist'

urlpatterns = [
    # /music/
    url(r'^$', views.home_page, name='home'),

]
