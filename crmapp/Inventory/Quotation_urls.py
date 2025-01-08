from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Quotation_views import ProductQuotationViewSet

router = DefaultRouter()
router.register(r'quotations', ProductQuotationViewSet, basename='quotations')

urlpatterns = [
    path('api/', include(router.urls)),
]
