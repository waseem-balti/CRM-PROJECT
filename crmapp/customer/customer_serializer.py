from rest_framework import serializers
from crmapp.models import CustomUser

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','phone_no','location','status']

        