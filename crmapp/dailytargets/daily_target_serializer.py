from rest_framework import serializers
from crmapp.models import DailyTarget

class DailyTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTarget
        fields = '__all__'

    def validate(self, data):
        if data.get('achieved') and data.get('achieved') > data.get('target'):
            raise serializers.ValidationError("Achieved value cannot exceed the target.")
        if data.get('revenue_enrated') and data.get('revenue_enrated') < 0:
            raise serializers.ValidationError("Revenue cannot be negative.")
        return data
