from django.urls import include, path, re_path
from django.views.generic import TemplateView  # Import TemplateView
from rest_framework import routers
from .company_views import CompanyViewSet

# Initialize the router
router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')  # Register the CompanyViewSet

urlpatterns = [
    # Documentation URL
    re_path(r'^docs/(?P<path>.*)$', TemplateView.as_view(template_name='docs.html')),

    # Include the router-generated URLs for the companies viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'

]

