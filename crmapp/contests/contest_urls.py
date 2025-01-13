from django.urls import include, path
from rest_framework import routers
from .contest_views import ContestViewSet

router = routers.DefaultRouter()
router.register(r'contests', ContestViewSet, basename='contests')

urlpatterns = [
    path('api/', include(router.urls)),
]