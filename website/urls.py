from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from company import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^music/', include('music.urls'),),
    url(r'^stocks/', views.Stocklist.as_view()),
    url(r'^jspp/', include('jspp.urls'),),

]

urlpatterns = format_suffix_patterns(urlpatterns)
# only work on developer mode
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
