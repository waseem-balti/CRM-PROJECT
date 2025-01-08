from rest_framework import serializers
from crmapp.models import LeadSummary

class LeadSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSummary
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value
