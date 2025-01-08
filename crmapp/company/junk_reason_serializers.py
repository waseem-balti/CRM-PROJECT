from rest_framework import serializers
from crmapp.models import JunkReason

class JunkReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = JunkReason
        fields = '__all__'  # Include all fields in the response
