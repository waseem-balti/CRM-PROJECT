from rest_framework import serializers
from crmapp.models import Lead, Campaign, Branch, LeadSource, Funnel, CustomUser

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'campaign', 'branch', 'email', 'mobile_phone', 
            'fax', 'lead_source', 'company', 'industry', 'lead_status', 'assigned_to', 
            'address', 'city', 'country', 'postal_code', 'state', 'description', 
            'move_to_opportunity', 'accept', 'deal_close', 'created_by', 'date_created'
        ]
        
    # Optionally, you can add validation methods or additional custom fields if needed
    def validate_mobile_phone(self, value):
        # Custom validation logic for mobile phone, if required
        if not value.isdigit():
            raise serializers.ValidationError("Mobile phone must contain only digits.")
        return value