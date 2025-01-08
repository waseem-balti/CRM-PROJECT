from rest_framework import serializers
from crmapp.models import KPI

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'
