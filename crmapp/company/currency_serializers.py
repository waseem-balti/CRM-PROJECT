from rest_framework import serializers
from crmapp.models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'  # Include all fields in the API response
