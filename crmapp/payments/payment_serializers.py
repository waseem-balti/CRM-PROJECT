from rest_framework import serializers
from crmapp.models import Payment
from django.core.exceptions import ValidationError

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['transaction_id', 'user', 'amount', 'status', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Ensure the payment amount is greater than zero"""
        if value <= 0:
            raise ValidationError("Payment amount must be greater than zero.")
        return value
    
    def validate_status(self, value):
        """Ensure the status is valid"""
        if value not in dict(Payment.STATUS_CHOICES):
            raise ValidationError("Invalid status.")
        return value
