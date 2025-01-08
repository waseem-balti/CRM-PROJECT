from rest_framework import serializers
from crmapp.models import Lead

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'campaign', 'branch', 'email', 'mobile_phone', 
            'company', 'industry', 'lead_status', 'assigned_to', 'description', 
            'move_to_opportunity', 'deal_close', 'is_customer', 'created_by', 'date_created'
        ]
        
    def validate(self, data):
        if data.get('is_customer', False) and not data.get('move_to_opportunity', False):
            raise serializers.ValidationError("Only opportunities can be converted to customers.")
        return data

    def update(self, instance, validated_data):
        # If is_customer is set to True, mark the opportunity as converted
        if validated_data.get('is_customer', False):
            instance.is_customer = True
            instance.move_to_opportunity = False  # No longer an opportunity
        return super().update(instance, validated_data)
