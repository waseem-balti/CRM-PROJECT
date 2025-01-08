# crmapp/trailAcc/serializers.py
from rest_framework import serializers
from crmapp.models import CustomUser  # Import from project folder

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'trial', 'trial_start_date', 'trial_end_date']

class StartTrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

    def create(self, validated_data):
        user = CustomUser.objects.get(email=validated_data['email'])
        user.start_trial(trial_duration_days=30)  # Default trial period of 30 days
        return user

class TrialStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'is_active', 'trial', 'trial_end_date']
