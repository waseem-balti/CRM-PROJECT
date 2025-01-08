from rest_framework import serializers
from crmapp.models import ContactActivity

class ContactActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactActivity
        fields = ['lead','contact_type']
        read_only_fields = ['created_at', 'date_created']

    def validate(self, data):
        if not data.get('contact_type'):
            raise serializers.ValidationError("Contact type must be specified.")
        return data
