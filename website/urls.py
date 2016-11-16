from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^music/', include('music.urls'),),
    url(r'^jspp/', include('jspp.urls'),),
    url(r'^superlist/', include('superlist.urls'),),
    url(r'^api/', include('website.api'),),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
# only work on developer mode
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
