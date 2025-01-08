from django.urls import include, path
from rest_framework import routers
from .lead_summary_view import LeadSummaryViewSet

router = routers.DefaultRouter()
router.register(r'lead-summaries', LeadSummaryViewSet, basename='lead-summaries')

urlpatterns = [
    path('api/', include(router.urls)),
]
