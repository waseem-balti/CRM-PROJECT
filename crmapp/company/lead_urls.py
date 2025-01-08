from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from .lead_views import LeadViewSet

# Initialize the router
router = routers.DefaultRouter()
router.register(r'leads', LeadViewSet, basename='leads')  # Register the LeadViewSet

urlpatterns = [
    # Documentation URL
    re_path(r'^docs/(?P<path>.*)$', TemplateView.as_view(template_name='docs.html')),
    # Include the router-generated URLs for the leads viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'

]
