from django.urls import include, path
from rest_framework import routers
from .junk_reason_views import JunkReasonViewSet

# Initialize the router
router = routers.DefaultRouter()
router.register(r'junk-reasons', JunkReasonViewSet, basename='junk-reasons')  # Register the JunkReasonViewSet

urlpatterns = [
    # Include the router-generated URLs for the junk reasons viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'
]
