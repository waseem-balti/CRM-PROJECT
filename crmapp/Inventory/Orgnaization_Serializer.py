from rest_framework import serializers
from crmapp.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',  # Automatically generated by Django
            'organization_name',
            'branch',
            'website',
            'phone_no',
            'fax',
            'email',
            'ownership',
            'industry',
            'organization_type',
            'no_of_employees',
            'assigned_to',
            'notify_owner',
            # Billing Address
            'billing_address',
            'billing_po_box',
            'billing_city',
            'billing_state',
            'billing_postal_code',
            'billing_country',
            # Shipping Address
            'shipping_address',
            'shipping_po_box',
            'shipping_city',
            'shipping_state',
            'shipping_postal_code',
            'shipping_country',
            'description',
           
        ]
        


    def validate_phone_no(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def validate_email(self, value):
        if value and Organization.objects.filter(email=value).exists():
            raise serializers.ValidationError("An organization with this email already exists.")
        return value