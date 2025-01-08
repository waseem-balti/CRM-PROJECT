from rest_framework import serializers
from crmapp.models import Campaign

class CampaignReportSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)  # Include branch name
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)  # Assigned user name
    product_name = serializers.CharField(source='product.name', read_only=True)  # Product name

    class Meta:
        model = Campaign
        fields = [
            'id',
            'name',
            'branch_name',
            'assigned_to_name',
            'status',
            'campaign_type',
            'product_name',
            'target_audience',
            'sponsor',
            'channels',
            'budget',
            'expected_leads',
            'start_date',
            'end_date',
            'goals_and_objectives',
            'description',
            'date_created',
        ]  # Add or remove fields based on reporting needs
