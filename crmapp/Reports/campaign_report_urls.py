# campaign_urls.py
from django.urls import include, path
from rest_framework import routers
from .campaign_report_views import CampaignReportViewSet

router = routers.DefaultRouter()
router.register(r'campaign-reports', CampaignReportViewSet, basename='campaign-reports')

urlpatterns = [
    path('api/', include(router.urls)),
]
