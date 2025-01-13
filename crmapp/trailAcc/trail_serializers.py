from crmapp.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils import timezone 
from django.utils.timezone import timedelta
class RegisterCustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            trial_start_date=timezone.now(),
            trial_end_date=timezone.now() + timedelta(minutes=5)  # 7-day trial period
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user


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
