from django.urls import include, path
from rest_framework import routers
from .product_report_views import ProductReportViewSet

router = routers.DefaultRouter()
router.register(r'product-reports', ProductReportViewSet, basename='product-reports')

urlpatterns = [
    path('api/', include(router.urls)),
]
