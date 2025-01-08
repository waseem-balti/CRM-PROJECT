from rest_framework import serializers
from crmapp.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'  # You can also list specific fields here if needed
