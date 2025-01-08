from rest_framework import serializers
from crmapp.models import Funnel

class FunnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funnel
        fields = '__all__'  # You can also list specific fields here if needed
