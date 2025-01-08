from django.urls import include, path
from rest_framework import routers
from .invoice_view import InvoiceViewSet

router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoices')

urlpatterns = [
    path('api/', include(router.urls)),
]
