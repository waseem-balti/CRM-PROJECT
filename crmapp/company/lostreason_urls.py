from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .lostreason_views import LostReasonViewSet

router = DefaultRouter()
router.register(r'lost-reasons', LostReasonViewSet, basename='lostreason') # Register the LostReasonViewSet

urlpatterns = [
    path('api/', include(router.urls)),
]
