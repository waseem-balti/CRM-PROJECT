from rest_framework import serializers
from crmapp.models import AssignProduct

class AssignProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignProduct
        fields = '__all__'

    def validate(self, data):
        if data.get('target') and data.get('target') <= 0:
            raise serializers.ValidationError("Target must be a positive value.")
        return data
