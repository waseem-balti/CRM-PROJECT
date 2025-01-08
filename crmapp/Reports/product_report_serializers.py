from rest_framework import serializers
from crmapp.models import Product

class ProductReportSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)  # Include branch name
    handler_name = serializers.CharField(source='handler.username', read_only=True)  # Include handler's username

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'branch_name',
            'product_active',
            'part_number',
            'manufacturer',
            'product_category',
            'sales_start_date',
            'sales_end_date',
            'support_start_date',
            'support_expiry_date',
            'vendor_name',
            'price',
            'commission_rate',
            'sales_percentage',
            'service_percentage',
            'purchase_cost',
            'qty_per_unit',
            'qty_in_stock',
            'usage_unit',
            'handler_name',
            'serial_no',
            'website',
            'description',
            'terms_condition',
            'date_created',
        ]  # Add or remove fields based on reporting needs
