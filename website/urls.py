from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^music/', include('music.urls'), ),

]

# only work on developer mode
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
