from rest_framework import serializers
from crmapp.models import Contest

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = [
            'id', 'name', 'objective', 'description', 'attached_file', 'department', 'assigned_to',
            'launch_date', 'due_date', 'company', 'created_at', 'updated_at'
        ]
