from rest_framework import serializers
from crmapp.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

    def validate(self, data):
        """Custom validation for Invoice data."""
        if data.get('quantity') and data.get('quantity') <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if data.get('price') and data.get('price') < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return data
