from rest_framework import serializers
from crmapp.models import Upload_Project

class UploadProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload_Project
        fields = [
            'name', 'overview', 'avatar', 'privacy', 
            'start_date', 'due_date', 'priority', 
            'budget', 'team_members'
        ]

    # Customize the `start_date` and `due_date` fields
    start_date = serializers.DateField(
        input_formats=['%Y-%m-%d'],  # Accepted format: YYYY-MM-DD
        format='%Y-%m-%d',          # Returned format: YYYY-MM-DD
    )
    due_date = serializers.DateField(
        input_formats=['%Y-%m-%d'],
        format='%Y-%m-%d',
    )
