from django.urls import include, path, re_path
from rest_framework import routers
from .currency_views import CurrencyViewSet
from django.views.generic import TemplateView

# Initialize the router
router = routers.DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename='currencies')  # Register the CurrencyViewSet

urlpatterns = [
    # Documentation URL
    re_path(r'^docs/(?P<path>.*)$', TemplateView.as_view(template_name='docs.html')),

    # Include the router-generated URLs for the currencies viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'
]
