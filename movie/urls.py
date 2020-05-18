from django.urls import include, path
from rest_framework.routers import DefaultRouter

from movie import views

router = DefaultRouter()


app_name = 'movie'

urlpatterns = [
    path('', include(router.urls)),
]
