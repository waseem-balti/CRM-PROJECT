from rest_framework import serializers
from crmapp.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    class Meta:
        model = UserProfile
        fields = '__all__'  # Include all fields in the UserProfile model
        read_only_fields = ['user']  # Prevent modification of the user field
