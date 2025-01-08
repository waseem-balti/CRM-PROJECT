from rest_framework import serializers
from crmapp.models import Price

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'id',
            'branch',
            'price_book_name',
            'active',
            'currency',
            'description',
        ]

    def validate_price_book_name(self, value):
        """
        Field-level validation for 'price_book_name'.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Price book name must be at least 3 characters long.")
        return value

    def validate(self, data):
        """
        Object-level validation for logical consistency.
        """
        if not data.get('active') and not data.get('description'):
            raise serializers.ValidationError("Description is required if the price book is not active.")
        return data
