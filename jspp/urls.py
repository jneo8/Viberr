from django.conf.urls import url
from . import views
app_name = 'jspp'

urlpatterns = [

    # /jspp/
    url(r'^$', views.IndexView.as_view(), name='index'),

    
]
