from django.urls import path ,include
from rest_framework import routers
from .Organization_views import  OrganizationViewSet

router = routers.DefaultRouter()
router.register(r'Organization', OrganizationViewSet, basename='organization')

urlpatterns = [
    path('api/', include(router.urls)),
]