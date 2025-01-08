from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .kpi_views import KPIViewSet

router = DefaultRouter()
router.register(r'kpis', KPIViewSet, basename='kpis')  # Register the KPIViewSet

urlpatterns = [
    path('api/', include(router.urls)),
]
