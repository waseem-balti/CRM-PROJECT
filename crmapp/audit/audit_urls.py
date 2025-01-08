from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .audit_views import AuditLogListCreateView, AuditLogDetailView


urlpatterns = [
    path('api/audit/', AuditLogListCreateView.as_view(), name='audit-log-list'),
    path('api/audit/<int:pk>/', AuditLogDetailView.as_view(), name='audit-log-detail'),
]