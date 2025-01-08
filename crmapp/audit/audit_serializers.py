from rest_framework import serializers
from crmapp.models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'action', 'resource_name', 'resource_id',
            'timestamp', 'ip_address', 'description', 'changes',
        ]
