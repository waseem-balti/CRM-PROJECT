from rest_framework import serializers
from crmapp.models import Lead

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'campaign', 'branch', 'email', 'mobile_phone', 
            'company', 'industry', 'lead_status', 'assigned_to', 'description', 
            'is_customer', 'created_by', 'date_created'
        ]