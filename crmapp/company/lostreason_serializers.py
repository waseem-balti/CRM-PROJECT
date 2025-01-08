from rest_framework import serializers
from crmapp.models import LostReason

class LostReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostReason
        fields = '__all__'
