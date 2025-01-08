from django.urls import include, path, re_path
from rest_framework import routers
from .campaign_views import CampaignViewSet
from django.views.generic import TemplateView

# Initialize the router
router = routers.DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaigns')  # Register the CampaignViewSet

urlpatterns = [
    # Documentation URL
    re_path(r'^docs/(?P<path>.*)$', TemplateView.as_view(template_name='docs.html')),

    # Include the router-generated URLs for the campaigns viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'
]
