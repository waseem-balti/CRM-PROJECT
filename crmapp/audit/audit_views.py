from rest_framework import generics, filters, permissions
from rest_framework.pagination import PageNumberPagination
from crmapp.models import AuditLog
from .audit_serializers import AuditLogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Pagination for large audit logs
class AuditLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Permission for restricting access to logs
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

class AuditLogListCreateView(generics.ListCreateAPIView):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    pagination_class = AuditLogPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'action', 'resource_name', 'description']
    ordering_fields = ['timestamp', 'user']
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

class AuditLogDetailView(generics.RetrieveAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
