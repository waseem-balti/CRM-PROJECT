from rest_framework import serializers
from crmapp.models import Product, Lead, Campaign, Department, Funnel, KPI, LeadSource, Invoice

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class FunnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funnel
        fields = '__all__'

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'

class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSource
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
