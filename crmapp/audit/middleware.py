from django.utils.deprecation import MiddlewareMixin
from crmapp.models import AuditLog
import json

class AuditLogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'DELETE']:
            resource_name = view_func.__module__.split('.')[-1]
            resource_id = view_kwargs.get('pk')
            ip_address = self.get_client_ip(request)
            AuditLog.objects.create(
                user=request.user,
                action=request.method,
                resource_name=resource_name,
                resource_id=resource_id,
                ip_address=ip_address,
                description=f"{request.method} action on {resource_name}",
                changes=json.loads(request.body.decode('utf-8')) if request.body else None,
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
