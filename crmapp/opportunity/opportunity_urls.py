from django.urls import include, path
from rest_framework import routers
from .opportunity_views import OpportunityViewSet

router = routers.DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunities')

urlpatterns = [
    path('api/', include(router.urls)),
]
