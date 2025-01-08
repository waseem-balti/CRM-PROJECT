from rest_framework import serializers
from crmapp.models import ProductQuotation

class ProductQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuotation
        fields = [
            'id',               
            'branch',
            'quotation_number',
            'quotation_date',
            'expiration_date',
            'customer_name',
            'customer_email',
            'customer_phone',
            'product_name',
            'quantity',
            'unit_price',
            'total_price',
            'description',
        ]
        read_only_fields = [ 'total_price']