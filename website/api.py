from django.conf.urls import url, include
from rest_framework import routers

from fju.views import StudentViewSet, UniversityViewSet
from company import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'University', UniversityViewSet)

urlpatterns = [
    url(r'^stocks/', views.Stocklist.as_view(), name='stock'),
    url(r'^docs/', schema_view),
]
urlpatterns += router.urls