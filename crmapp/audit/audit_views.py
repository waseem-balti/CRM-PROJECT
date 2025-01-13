from rest_framework import generics, filters, permissions
from rest_framework.pagination import PageNumberPagination
from crmapp.models import AuditLog
from .audit_serializers import AuditLogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from crmapp.renderers import UserRenderer

# Pagination for large audit logs
class AuditLogPagination(PageNumberPagination):
    renderer_classes = [UserRenderer]
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Permission for restricting access to logs
class IsAdminOrReadOnly(permissions.BasePermission):
    renderer_classes = [UserRenderer]
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

class AuditLogListCreateView(generics.ListCreateAPIView):
    renderer_classes = [UserRenderer]
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    pagination_class = AuditLogPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'action', 'resource_name', 'description']
    ordering_fields = ['timestamp', 'user']
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

class AuditLogDetailView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
