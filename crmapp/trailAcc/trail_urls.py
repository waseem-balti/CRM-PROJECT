from django.urls import path,include
from rest_framework import routers
from .trail_views import RegisterCustomUserViewSet

router = routers.DefaultRouter()
router.register(r'trail-users', RegisterCustomUserViewSet, basename='users')

urlpatterns = [
    path('api',include(router.urls))
]
