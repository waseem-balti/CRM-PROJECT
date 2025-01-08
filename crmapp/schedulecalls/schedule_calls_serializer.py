from rest_framework import serializers
from crmapp.models import ScheduleCalls

class ScheduleCallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCalls
        fields = '__all__'

    def validate(self, data):
        if not data.get('schedule_for'):
            raise serializers.ValidationError("Schedule type must be specified.")
        return data
