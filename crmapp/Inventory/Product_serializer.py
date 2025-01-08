from rest_framework import serializers
from crmapp.models import Product, ProductService

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'branch', 'product_active', 'part_number', 
            'manufacturer', 'product_category', 'sales_start_date', 
            'sales_end_date', 'support_start_date', 'support_expiry_date', 
            'vendor_name', 'website', 'serial_no', 'price', 'commission_rate', 
            'sales_percentage', 'service_percentage', 'purchase_cost', 
            'usage_unit', 'qty_per_unit', 'qty_in_stock', 'handler', 
            'product_image', 'description', 'terms_condition', 'date_created'
        ]
        
class ProductServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductService
        fields = [
            'id', 'name', 'branch', 'usage_unit', 'active', 'num_units', 
            'website', 'category', 'owner', 'support_start_date', 
            'support_expiry_date', 'price', 'commission_rate', 
            'purchase_cost', 'description'
        ]
