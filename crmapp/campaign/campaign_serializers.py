from rest_framework import serializers
from crmapp.models import Campaign, Branch, CustomUser, Product

class CampaignSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = Campaign
        fields = [
            'id',
            'branch', 
            'name', 
            'assigned_to', 
            'campaign_type', 
            'product', 
            'target_audience', 
            'sponsor', 
            'channels', 
            'budget', 
            'expected_leads', 
            'goals_and_objectives', 
            'start_date', 
            'end_date', 
            'description',
            'media',
        ]
        read_only_fields = ['date_created']  # Make sure 'date_created' exists in the model
