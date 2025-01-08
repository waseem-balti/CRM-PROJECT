from django.urls import path
from .inventory_reports_views import InventoryReportAPI

urlpatterns = [
    path('inventory-report/', InventoryReportAPI.as_view(), name='inventory-report'),
]
